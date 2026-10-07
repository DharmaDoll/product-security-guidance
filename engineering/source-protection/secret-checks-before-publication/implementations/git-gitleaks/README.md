# Git hooks and Gitleaks

Gitへcommitまたはpushしようとしている内容をGitleaksで検査し、秘密情報が見つかった場合や
検査を完了できなかった場合に操作を止める実装例です。

検出ルールはGitleaksが担います。[gate.py](gate.py)はGitから検査対象を取り出し、Gitleaksを実行し、
結果をGitの許可または拒否へ接続します。

GitHub.comへ直接pushする場合は、端末上の`pre-commit`・`commit-msg`・`pre-push`を使います。端末のhookは省略できるため、GitHub側の拒否は[push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)の設定と対象範囲を別に確認してください。自前のGit受信先向け`pre-receive`コードは末尾で紹介する参考例です。通常の導入手順には含めません。

## 何をするものか

```text
commitまたはpush
        |
        v
Git hookがgate.pyを呼ぶ
        |
        v
gate.pyがcommit対象・履歴を取り出す
        |
        v
Gitleaksで検査
        |
        +-- 検出なし ----------> Git操作を続ける
        +-- 秘密情報を検出 ----> Git操作を止める
        +-- 検査不能・故障 ----> Git操作を止める
```

ローカルhookは、開発者が問題へ早く気付くための検査です。hookの有効化だけで、GitHub側に同じ検査が追加されるわけではありません。

## この実装を導入した環境でのcommitとpush

| 操作 | 起きること |
|---|---|
| `git commit` | `pre-commit`が`git add`済みのファイルとパスを検査し、`commit-msg`がコミットメッセージを検査する |
| `git push` | `pre-push`が送信するbranch・tagから到達できるcommit、tree、blobを検査する |

検出がなければ`CHECKED no findings within the configured scope`と表示して処理を続けます。
秘密情報を検出した場合は`REJECTED`、検査器の故障や未対応入力は`ERROR`または`INCOMPLETE`として停止します。

この例は、小規模なUTF-8テキスト中心のGitリポジトリを対象にしています。大規模な履歴、binary、archive、
Git LFSを含むrepositoryでは、そのまま導入せず[制限と拒否条件](#制限と拒否条件)を確認してください。

[Secret checks before publication](../../README.md)の送信前検査を具体化する一例であり、
旧Pythonのsecret正規表現群やDocker wrapperを移植したものではありません。

## 対象と信頼境界

2026-09-23にLinux x86_64、Git 2.47.2、Python 3.13.5（hook実行）・3.10.4（テスト実行）、Gitleaks 8.30.1で確認しました。
他OS・版は未検証です。`/usr/bin/git`、`/usr/bin/python3`、POSIX shellを使います。
製品仕様と取得物の根拠は[REF-GITLEAKS-HOOKS-001](../../../../../sources/README.md#ref-gitleaks-hooks-001)です。

端末に置くhookと検査ルールは、レビューした版を使います。開発者が送るtreeから未レビューのhookやrulesを実行しません。
端末侵害やscanner自身の脆弱性への隔離は実装していません。

## どこまで検査するか

| Hook | 実際に検査する内容 |
|---|---|
| [pre-commit](hooks/pre-commit) | indexの全通常ファイルのblobとパス。作業ツリーを読み直さない |
| [commit-msg](hooks/commit-msg) | Gitから渡されるメッセージファイル |
| [pre-push](hooks/pre-push) | stdinの更新対象OIDから到達する全commit・tree・blob・annotated tag、送信先ref名 |

履歴の差分最適化は行いません。送信対象から到達できる既存履歴も再検査するため、新規ブランチ、履歴書換え、mergeだけで導入された内容、
タグ、複数refを同じ方式で扱えます。remote-tracking refを検査済みの証拠にせず、欠落したobjectは拒否します。
commitの生データから親とtreeを追うため、replace refsやgraftsによる履歴の置換を検査の根拠にしません。
削除対象には新しい到達内容がないため、そのref名だけを検査し、同時に更新する他refは検査します。
到達不能な余分なpack object、reflog、既存の別refは今回の検査対象ではありません。

## 判定・設定・出力

[gitleaks.toml](gitleaks.toml)で固定版の組込みルールを使用します。検査対象の`.gitleaks.toml`・`.gitleaksignore`、
環境の`GITLEAKS_*`、`gitleaks:allow`コメントで検査を弱めません。組込みのallowlistは検出方針の一部として残ります。
誤検知に対する利用者の例外機構は実装しません。必要なら対象・期限・承認の管理を別途設計し、無期限のbaselineや全体除外を追加しないでください。

| 終了値 | 意味 | Git操作 |
|---|---|---|
| 0 | 必要な処理を終了し、この範囲で検出なし | 続行可能 |
| 1 | 検出あり | 拒否 |
| 2 | ERRORまたはINCOMPLETE。失敗、未対応、上限超過、欠落 | 拒否 |

Gitleaksの検出終了値を10に指定し、終了値とJSON reportの一致を確認します。未知の状態、壊れたreport、異常終了を検出なしにしません。
子プロセスのstdout・stderrはそのまま表示せず、固定した理由と、必要ならGit object IDだけを表示します。
パス・ref・メッセージ自体にも秘密値があり得るため、それらを診断出力に再掲しません。Reportはメモリ上で処理し、ファイルへ保存しません。
この抑制はadapterの出力に対するもので、呼出し元のGit、shellのtrace、OS監視等の出力・メモリ保護は別途確認が必要です。

## レビュー済みのローカル用bundleを準備する

以下は導入先で明示的に行う手順です。本PJ自身のhooksは変更していません。
まずこのディレクトリのコードと設定をレビューし、対象repositoryの外へ版を区別したbundleを作ります。
`bundle`は新規ディレクトリとし、既存の内容へ上書きしません。

```sh
bundle=/path/to/reviewed/source002-gitleaks-8.30.1
mkdir "$bundle"
mkdir "$bundle/bin"
cp gate.py gitleaks.toml "$bundle/"
cp -R hooks "$bundle/"
chmod 755 "$bundle/hooks/"*
```

GitleaksのLinux x64公式配布物を取得し、固定したSHA-256を照合してからbinaryのみを展開します。
親ディレクトリは事前に管理者が準備してください。ダウンロードや実行をhook自身では行いません。

```sh
curl -fL https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz -o "$bundle/gitleaks.tar.gz"
printf '%s  %s\n' '551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb' "$bundle/gitleaks.tar.gz" | sha256sum -c - &&
  tar -xzf "$bundle/gitleaks.tar.gz" -C "$bundle/bin" gitleaks
printf '%s  %s\n' '88f91962aa2f93ac6ab281d553b9e125f5197bbbce38f9f2437f7299c32e5509' "$bundle/bin/gitleaks" | sha256sum -c -
"$bundle/bin/gitleaks" version
```

照合が失敗した場合は有効化しません。SHA-256はGitHubのrelease asset情報と取得物を照合した値であり、
独立した署名による発行者検証ではありません。導入時に組織の取得元・署名検証方針も適用します。
実行のたびにadapterがbinaryのSHA-256を確認します。bundleの親ディレクトリを含む変更権限は別の強制点です。

## 手元のリポジトリで有効化する

対象ごとに`core.hooksPath`の実効値と設定元、既存hooksの有無を確認し、元の設定を記録します。
既存hookがある場合はここで止め、管理者が呼出し順と終了値の伝播をレビューして統合します。自動上書きするinstallerはありません。

```sh
# 出力なし（終了1）は設定なし。その他のエラーは先に解消する。
git -C /path/to/worktree config --show-origin --get-all core.hooksPath
git -C /path/to/worktree rev-parse --git-path hooks
# 既存設定・hooksの確認後に実行する。
git -C /path/to/worktree config --local core.hooksPath "$bundle/hooks"
```

GitHub.com側の設定はこの手順に含みません。push protectionが使えるか、どの値を拒否し、誰が迂回できるかはGitHub側で別に確認します。

有効化後は下記テストと同等の確認を検証用repositoryで行います。hooksが存在するだけでは導入済みと判断しません。
更新は別の版のbundleを準備・レビュー・検証してから対象の設定を切り替えます。
解除・切り戻しでは、実効値が今回設定した値のままかを確認して、記録した以前の値・設定元へ戻します。
以前のlocal値がなければ今回追加したlocalの`core.hooksPath`だけを解除します。他のhooksや設定は削除しません。

## 制限と拒否条件

この実装は、検査できない入力を「問題なし」として通しません。対象repositoryが次の制限に合わない場合は、
上限だけを緩めるのではなく、binaryや大規模履歴を扱える別の検査方式を選んでください。

- 1 objectまたはメッセージは2 MiBまで、検査に渡す内容とパス等の合計は32 MiBまで、1回に1,000 objectまで、hook入力は64 KiBまでです。これらはこの実装例の上限であり、製品非依存の要件ではありません。
- 各子プロセスは15秒、Gitleaksは10秒、hook全体は120秒で打ち切ります。大規模repository向けの最適化やOSレベルのメモリ制限は含みません。
- UTF-8以外、NUL等の制御文字、既知のarchive拡張子、LFS pointer、symlink、submodule、未解決index、shallow clone、partial clone、`refs/heads/`・`refs/tags/`以外のrefは拒否します。
- Archiveの展開、符号化された値の復号、Git LFS等の外部格納物の取得は行いません。Archive拡張子のないUTF-8データは文字列として検査しますが、拡張子だけで安全とは判断しません。
- 大きな既存履歴や、既存履歴に検出対象があるrepositoryでは継続的に拒否され得ます。検査範囲を黙って縮めず、別方式へ移行してください。

各入力には固定した非機密のテキスト見出しを付け、Gitleaksのstdinへ元のbytesを続けて渡します。
これはUTF-8として受け付けた内容が、先頭のMIME識別で無言で読み飛ばされることを避けるためです。
Gitleaksの組込みルール・allowlist・分割処理の限界は残ります。パス条件を必要とするルールはstdinでは元のパス条件を評価できず、
名前の検査だけでその不足は解消しません。全秘密情報の不在や旧scannerの検出範囲の包含は保証しません。

## 検証する

リポジトリのルートで実行します。Binaryは上記の照合済み配布物を指定します。未指定・不一致は失敗となり、検証成功へ変換しません。

```sh
SOURCE002_GITLEAKS=/path/to/verified/gitleaks make test-secret-hooks
```

[test_gate.py](test_gate.py)は、一時ディレクトリにworktree・bare repository・bundleを作り、実Git操作とGitleaksで確認します。
秘密鍵として無効な未発行の検出用文字列を実行時に組み立て、外部サーバーへ送信しません。
検査障害の一部はadapter単体への故障注入で確認し、実Gitleaksで再現した挙動とは区別します。

- 正常コミットと受信、staged内容と作業ツリーの不一致、メッセージ、履歴に残る値。
- ローカルhooksを省略したpushの受信拒否と、共有refが作られないこと。
- 複数ref、force push、mergeで導入された内容、annotated tagのメッセージ、blobへの直接tag。
- 候補内の設定・除外・allowコメント、pathに含まれる値、UTF-8のMIME識別文字列による省略。
- 未対応形式・上限、浅い履歴、欠落object、検査器不在・変更、不正設定、出力の非表示。
- 故障注入：タイムアウト、未知の終了値、壊れたJSON、終了値とreportの不一致。

この確認は対象版・隔離環境の挙動です。本番サービスの権限、全書込経路、負荷、端末への配布、組織の導入状態は未検証です。bare repositoryへのpushは受信側hookの動きを比べるためのテストであり、GitHub.comのpush protectionを試したものではありません。
[コントロールの診断で確認する項目](../../../../../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md#failure-checks)全体を自動化したものでもありません。

## 対応する特性と残る責任

端末側のSECRET-1〜4・6の限定実装を示します。端末のhookを省略した場合にGitHub.comが何を拒否するかは示しません。
SECRET-7は利用者による除外を提供しない範囲だけを担い、期限付き例外の承認・取消は未実装です。
判定に使ったobject IDと検査範囲はそのhook呼出しに限ります。ローカルの並行変更や利用者によるhook省略は防げません。既に共有先へ到達した値の失効・調査はSOURCE-004へ引き継ぎます。

## 参考：自前のGit受信先

自分でGitの受信先を運用する環境に限り、[pre-receive](hooks/pre-receive)が[gate.py](gate.py)を呼んで受信した履歴を調べる例も含めています。使い捨てのbare repositoryで拒否を確認しましたが、実サーバーへの導入手順や運用構成の提案ではありません。GitHub.comへこのhookを配置できず、[GitHub Enterprise Serverのhook機能](https://docs.github.com/en/enterprise-server@3.21/admin/enforcing-policies/enforcing-policy-with-pre-receive-hooks/about-pre-receive-hooks)での動作も確認していません。受信側で拒否しても内容は一度受信先へ届きます。
