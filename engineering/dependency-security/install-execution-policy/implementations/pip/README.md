# pip実装例: Wheel-only dependency intake

Pythonの依存を、ソースからのbuildを許可せず、レビュー済みhashと照合して取得する例です。
通常のinstallでは、対応するwheelがあれば進み、ソース配布物しかない候補やhashの不一致では止まります。
独自のscannerは使わず、pipの二つのoptionを使います。

## 対象と前提

承認済みindexから名前とexact versionで依存を取得し、source buildを必要としないPython環境向けです。
確認した公式文書はpip `26.2.1`表示版、確認日は`2026-09-16`、追加確認日は`2026-09-27`です。
ローカルの挙動検査で使用した版はテスト出力に記録します。導入先はサポートされるPython・pipを
固定して再確認してください。この試作版はpip自体のインストールを行いません。

入力は直接・推移依存すべてのexact versionとレビュー済みSHA-256を含むrequirementsです。
この取得経路にlocal project、editable、VCS、直接指定のsource archiveを混ぜません。
requirements内の追加option・includeによるpolicyの上書きもレビュー対象です。

## 手元のリポジトリへ入れる

[`secure/requirements-policy.txt`](secure/requirements-policy.txt)はoptionだけの見本であり、依存を固定した入力ではありません。
採用先では、直接・推移依存のexact versionと対象wheelのレビュー済みhashを含む`requirements.lock`を用意します。
既存manifestからその入力を作る手順・差分レビューと、承認したindexの設定は採用先で決めます。

次はPOSIX環境の例です。`target`を対象リポジトリの絶対pathへ置き換えます。
使うPythonとpipの版を採用先で固定し、作成する専用環境のpathを対象の`.gitignore`へ追加してください。

```bash
target="/absolute/path/to/target-repository"
intake_venv="$target/.venv-dependency-intake"

(
  set -eu
  test -f "$target/requirements.lock"
  test ! -e "$intake_venv"
  python3 -m venv "$intake_venv"
  "$intake_venv/bin/python" -m pip --version
  "$intake_venv/bin/python" -m pip install --only-binary=:all: --require-hashes --no-cache-dir -r "$target/requirements.lock"
)
```

途中で失敗すれば後続のコマンドを止めます。作成済みの環境があれば作り直さず、新しいpathを選びます。
`requirements.lock`はこの試作版に付属しません。最後のコマンドは外部indexへ通信します。
通常CIも同じoptionと承認済み入力を使い、installが失敗したら後続の処理を開始しないように接続します。

`--only-binary=:all:`は候補のsource distributionを除外し、`--require-hashes`は取得内容を入力のhashへ
結び付けます。両者は別の性質です。`--prefer-binary`はsource buildの拒否の代わりになりません。
[pip install reference](https://pip.pypa.io/en/stable/cli/pip_install/)

既に入っているパッケージを要求が満たされているとして再利用すると、pipはそのhashを確認しない経路があります。
上の手順では新しい専用環境を使い、システムのsite-packagesや既存の依存環境を取り込みません。
専用環境はOSのsandboxではなく、後続のimport・testに渡す権限は別に制限します。

## 安全なsmoke test

このディレクトリで次を実行します。

```bash
python3 -m unittest discover -s tests -v
```

無害なwheelとsource distributionを一時領域で作り、ネットワークなしでpipの実際の候補選択と
metadata準備を確認します。成功するwheel、拒否されるsdist、hash不一致を検査し、
比較用の制限なし実行では無害なbackendがmarkerを残して停止することを確認します。
比較用packageはテスト中だけ生成し、workflowや通常のinstallへ配置しません。

テストはpip `--dry-run`の取得・準備段階を対象にします。採用先での通常install、全入力の制限、
CI配線、host隔離を証明しません。pip不在・失敗・予期しない結果はテスト失敗です。

2026-09-27はPython 3.10.4 / pip 23.3.1で4件を確認しました。これは観測した版であり、推奨版の指定ではありません。
テストでは`--no-deps`で一つの検出対象だけを調べます。通常installでの全推移依存やmanifestとの対応は確認していません。

同日は上の導入手順も、ネットワークを使わず無害なwheelだけで試しました。
新しい環境での通常install、誤ったhashの拒否、既存環境がある場合の開始拒否をpip 22.0.4で観測しました。
採用先のPython・pip・依存入力での確認は別に行います。

## 導入先で確認する

保護されたCIで実際に使うPython・pipの版、入力、command、設定の優先順位を確認します。
対応wheelを持つ依存が通常installできること、wheelがない候補が拒否され、source buildへ戻らないことを
無害な対象で確認します。未取得・未確認は`NOT_CHECKED`、収集・実行失敗は`ERROR`として残します。

## 解除する

この例を呼ぶCIや手元のinstallコマンドを、レビューした以前の手順へ戻します。
見本のoptionをrequirementsへ入れた場合は、その差分も戻します。作成した専用環境を使う処理を止め、
削除対象が上の`intake_venv`だけであることを確認してから環境を削除します。既存の共有環境は解除対象ではありません。

## 限界

Wheel内のコードは後続のimport・testで実行できます。hashが一致しても内容の安全性を示しません。
Pythonのbuild isolationはbuild用依存を分ける仕組みで、OS権限のsandboxではありません。
source buildが必要なら、この経路の拒否を解除するのではなく、別の隔離buildとして設計します。
[Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/)

Manifestと固定入力の対応、全推移依存、別platform向けの配布物、追加の取得コマンドと設定上書きは採用先で確認します。
この例だけで[DEPS-003](../../../../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)全体を満たすとは扱いません。

仕様の採否と他製品の候補は[参照資料記録](../../../../../sources/README.md#spec-install-execution-policy)、
方式は[pattern](../../README.md)を参照してください。
[DEPS-002の教材](../../../../../controls/records/dependency-security/psb-deps-002-install-execution-policy/learning.md)から、取得の許可と実行の許可の違いを読めます。
