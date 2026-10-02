# GitHub Actions実装例: Untrusted PR boundary

PR作成者が変更できるコードを、書き込み権限やシークレットを持たない`pull_request`ワークフローで検証し、権限が必要な処理を
レビュー・merge後の`push`から別のrunとして始める例です。通常のPRでは`make test`、mainへのpushでは
そのpushのrevisionのcheckoutと一致確認を行います。公開・deploy処理は採用先で接続します。
二つのrunの間でartifact、cache、output、workspaceを受け渡さず、両workflowに`cache-mode: none`を指定します。
`main`へのpushだけではレビュー済みと証明できません。権限処理を追加する前に、対象branchのPR必須条件と
直接push・bypassの実効設定を確認します。

`contents: read`のジョブにも`GITHUB_TOKEN`は存在します。この例はトークンを一切なくすものではなく、
PRコードへ書き込み権限、配送されたシークレット、OIDC、永続資産、内部到達性を与えない構成です。

[設計パターン](../../README.md) / [対応するコントロール](../../../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) / [教材](../../../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/learning.md)

## 対象と参照版

- 対象: GitHub.comのGitHub Actions。
- 製品ガイダンスの基準版: `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24）。
- 追加確認日: `2026-09-30`。現行のcache・workflow構文・イベント・runner仕様に加え、branch保護とrulesetのPR必須条件・bypassを確認。固定基準版は置き換えない。
- `actions/checkout`は`de0fac2e4500dabe0009e67214ff5f5447ce83dd`へ固定。同revisionのREADME・action.ymlはNode.js 24、最低Runner版`2.327.1`を示す。採用時にhosted runnerの実行可否を確認する。
- GitHub Enterprise Serverの対応や、実GitHub設定・run・拒否は今回確認していない。

## ファイル

| ファイル | 用途 | 取り扱い |
|---|---|---|
| [`secure/pr-validation.yml`](secure/pr-validation.yml) | PR由来のコードを読取り専用tokenで検証する | 導入先の`.github/workflows/`へ移し、test commandとrunner境界をレビューする |
| [`secure/fresh-main-run.yml`](secure/fresh-main-run.yml) | `main`へのpush revisionから新しいrunを始める | Checkoutの一致確認に加え、reviewとbypassの実効条件を確かめてから権限処理へ接続する |
| [`insecure/privileged-untrusted-pr.yml`](insecure/privileged-untrusted-pr.yml) | 境界を壊す構成をレビューで見分ける | **導入・有効化・コピー禁止** |

## 手元のリポジトリへ入れる

対象のrootを`target`、この例のdirectoryを`source_dir`へ絶対pathで指定します。既存ファイルがあれば上書きせず差分を統合します。

```bash
source_dir="/absolute/path/to/product-security-guidance/engineering/cicd-security/untrusted-pr-boundary/implementations/github-actions"
target="/absolute/path/to/target-repository"

(
  set -eu
  test "$(git -C "$target" rev-parse --show-toplevel)" = "$target"
  test -f "$source_dir/secure/pr-validation.yml"
  test -f "$source_dir/secure/fresh-main-run.yml"
  test ! -e "$target/.github/workflows/pr-validation.yml"
  test ! -e "$target/.github/workflows/fresh-main-run.yml"
  mkdir -p "$target/.github/workflows"
  cp "$source_dir/secure/pr-validation.yml" "$target/.github/workflows/pr-validation.yml"
  cp "$source_dir/secure/fresh-main-run.yml" "$target/.github/workflows/fresh-main-run.yml"
)
```

途中で失敗すれば後続のcopyを止めます。GitHubへ反映する前に、PR側の`make test`を採用先の無害な検証コマンドへ合わせます。
Default branchが`main`でない場合は、push対象と`if`の両方を変えます。必要なsetupを追加する場合も、secret・権限・自動cacheを持ち込まないか確認します。

## 有効にする前に接続を確認する

### 1. 先に既存経路を調べる

全ワークフローについて、`pull_request`、`pull_request_target`、`workflow_run`、`issue_comment`、
reusable workflow、手動checkout、artifact、cache、outputを調べます。安全なファイルを追加しても、
既存の権限付きPR経路が残れば境界は成立しません。

### 2. PR検証を読取り専用にする

PR作成者が検証コマンドや呼び出すファイルを変更できる前提で扱います。

- top-levelを`permissions: {}`とし、jobには`contents: read`だけを付与する。
- checkout後に認証情報を残さない。
- secret、OIDC、保護されたEnvironmentを参照しない。
- `cache-mode: none`をjob側や呼出先で書込みmodeへ変えない。
- 既定例のGitHub-hosted runnerを、永続するself-hosted runnerへ安易に置き換えない。

### 3. 新しい信頼境界から権限処理を始める

`secure/fresh-main-run.yml`は、`main`への`push`のSHAをcheckoutし、実際のHEADと一致するか確認します。
Markerの`echo`は公開・deployを行いません。実際の処理へ置き換える際に、必要なpermission、Environment、OIDC条件をそのjobへだけ付与します。
SHAの一致は取得した内容とpush eventの一致だけを示します。レビュー済みかどうかはbranch保護・rulesetの条件で別に確認します。
PR runのartifact、cache、output、workspaceを復元してはいけません。

### 4. 提供元の設定を合わせる

repository／organizationのActions token、fork approval、runner group、Environment、ruleset、required checkを確認します。
workflowファイルだけでは、これらの実効状態や実際のrunへ配送された権限を証明できません。
Pushされたことだけでレビュー済みとは判断せず、対象branchへの直接push・bypass・workflow変更の承認条件も確認します。
レビューを必須とする場合は、有効なbranch保護・rulesetの対象が`main`を含むこと、想定外の主体が直接pushや
bypassを使えないことを確認します。意図的な例外は主体・用途・権限処理の扱いを別に決めます。
この例の`validate`を必須検査にする場合は、対象branchの有効なルールへ接続し、失敗・取消・欠落とhead更新後の拒否を観測します。

## 使い捨てリポジトリでのsmoke test

本番credentialを使わない対象で、無害なfork PRと、レビュー・merge後のrunを使い、次を別々に記録します。
最初はmarkerを出して正常終了する検証コマンドだけでよく、その後に採用先の検証へ接続します。

1. PR runが`pull_request`で起動し、意図したrevisionをcheckoutしている。
2. PR runにwrite permission、secret、OIDC、保護されたEnvironment、永続runner、内部networkがない。
3. PR runの状態を消費する権限付きworkflow、cache、artifact、outputがない。
4. 権限処理を追加する前に、保護条件の対象branchとbypass主体を確認する。レビュー経路を前提とするなら、使い捨て対象で非bypass主体の直接pushが拒否されることを確認する。
5. merge後のrunがpushのSHAをcheckoutし、HEADとの一致確認とmarker表示に成功する。PR runの生成ファイルを戻していない。
6. provider設定、workflow inventory、runの一部を確認できない場合、結果を`NOT_CHECKED`または`ERROR`にしている。

静的解析はレビューを補助できますが、提供元設定と実runを置き換えません。実際のsecretを置いた流出試験や、
本番Environmentへの攻撃的な試験は行いません。

無害な検証を非ゼロ終了へ変え、必要なcheckを成功へ変換しないことを確認します。
検査の取消・欠落、承認後のhead更新でも、古い結果を使ってmergeできないか確認します。
Cache操作が権限により省略されてもjobの失敗になるとは限らないため、成功表示だけでcache拒否を観測したとは扱いません。
確認方法の製品非依存な正本は[controlの診断項目](../../../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md#failure-checks)です。

2026-09-27に、ローカルのcopy・既存二fileの上書き防止・入力不足時の停止・YAMLとshell構文を確認しました。
Revision照合は一致で成功し、不一致・期待値の空欄や欠落・Git repository不在では拒否されました。
GitHubの設定変更、fork PR、token配送、cache拒否、直接push・bypass・merge拒否は未実施です。

## 解除する

既存workflowへ統合した差分は、レビューした以前の設定へ戻します。新規配置した場合は、この例の二つのworkflowだけを削除します。
必須検査に接続した場合は、先に置き換える判定を接続して必須条件を見直します。Workflowだけを消して検査欠落でmergeが止まる状態にしません。

## この例を変更する場合

- metadata-onlyの`pull_request_target`を追加するなら、PR code、dependency、artifact、cacheを読み込まず、
  PR由来の文字列をshellや式へ直接展開しない専用workflowにする。
- run間でデータを渡すなら、schema、サイズ、完全性、producer、consumerでの解釈を固定する。
- private dependencyが必要なら、本番credentialを渡さず、読み取り専用mirrorまたは一時環境を検討する。
- third-party Actionを追加するならfull commit SHAへ固定し、そのActionが扱う入力とtokenをレビューする。

## 制限

この例は、branch／rulesetの強制、組織のfork policy、runnerの一回限りのライフサイクル、OIDCのcloud側trust、
cacheのprovenance、build sandbox、release integrityを実装しません。`pull_request_target`や`workflow_run`を
全面的に禁止する仕様でもなく、最初の導入で境界を見誤りにくくするための保守的な構成です。
外部cache・runner世代の選び方は[CI state and runner lifecycle](../../../ci-state-and-runner-lifecycle/README.md)、
権限処理の用途と付与は[Workflow authority minimization](../../../purpose-bound-job-authority/README.md)へ進めます。

## 参照資料

- [GitHub Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [GitHub Compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [REF-CICD-010 Preventing pwn requests](../../../../../sources/README.md#ref-cicd-010)
- [REF-CICD-005 GitHub Actions Best Practice 2025](../../../../../sources/README.md#ref-cicd-005)
- [GitHubセキュリティガイダンスの基準版](../../../../../sources/README.md#spec-github-security-guidance)
- [Cache仕様と採否](../../../../../sources/README.md#spec-ci-cache-boundary)
