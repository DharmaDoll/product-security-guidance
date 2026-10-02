# GitHub workflowの直接参照を確認する

[check_refs.py](check_refs.py)は、workflowが直接呼ぶActionとreusable workflowの参照を読み、外部Git参照の完全なcommit SHAとcontainer Actionのdigestを確認します。ネットワークへ接続せず、workflowやActionを実行せず、ファイルも変更しません。手元で確認し、同じ検査をCIのmerge条件へ接続するための例です。参照を直す時は既存のpinactも使えます。

対象はGitHub.comのworkflow、Python 3.10以上と**PyYAML 6.0.3**です。同梱[requirements.txt](requirements.txt)はCPython 3.10〜3.14、Linux glibcのx86_64／arm64、macOSのIntel／Apple Siliconのwheel hashを固定します。今回実行した環境はLinux x86_64、Python **3.10.4**、PyYAML **6.0.3**です。他の環境では動作確認が必要です。参照仕様・配布物の確認日は[Sources](../../../../../sources/README.md#spec-workflow-dependency-references)にあります。

## 手元のrepositoryへ入れる

このPJの実装ディレクトリの絶対パスを`WORKFLOW_REFS_SOURCE`へ入れ、導入先repositoryのrootで実行します。既存の同名ファイルは上書きせず内容を確認してください。Pythonのvenv機能とpip、package取得の通信が必要です。検査そのものには通信やcredentialは要りません。

```bash
WORKFLOW_REFS_SOURCE='/absolute/path/to/product-security-guidance/engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs'
mkdir -p scripts/security/workflow-refs
cp -n "$WORKFLOW_REFS_SOURCE/check_refs.py" "$WORKFLOW_REFS_SOURCE/requirements.txt" scripts/security/workflow-refs/
WORKFLOW_REFS_VENV="$(mktemp -d)"
python3 -m venv "$WORKFLOW_REFS_VENV"
"$WORKFLOW_REFS_VENV/bin/python" -m pip install --require-hashes --only-binary=:all: --no-deps -r scripts/security/workflow-refs/requirements.txt
"$WORKFLOW_REFS_VENV/bin/python" scripts/security/workflow-refs/check_refs.py .github/workflows
```

成功は終了値`0`と`CHECKED files=... pinned=... local=... rejected=0`です。`LOCAL`は同じrepositoryの参照で、固定済み外部参照の数へ含めません。外部参照のない通常の`run`だけのworkflowも、読めた対象と参照数ゼロを表示します。空ディレクトリや読めない入力はエラーになります。

## 簡単なsmoke test

次はPJ側の二つの**実行しないYAML例**を検査します。導入先の`.github/workflows`へコピーしないでください。SHAとimage digestは構文確認用の架空値で、取得・実行する対象ではありません。

```bash
"$WORKFLOW_REFS_VENV/bin/python" scripts/security/workflow-refs/check_refs.py "$WORKFLOW_REFS_SOURCE/pinned.yml"
echo "$?"
"$WORKFLOW_REFS_VENV/bin/python" scripts/security/workflow-refs/check_refs.py "$WORKFLOW_REFS_SOURCE/mutable.yml"
echo "$?"
"$WORKFLOW_REFS_VENV/bin/python" scripts/security/workflow-refs/check_refs.py "$WORKFLOW_REFS_SOURCE/not-present.yml"
echo "$?"
```

順に`0`、`1`、`2`を期待します。`0`は対象内の参照形式を確認、`1`は参照条件を満たさない、`2`は入力・構造・依存などの問題で検査不能です。後ろ二つはCIを止めます。`|| true`や`continue-on-error`で成功へ変換しないでください。

同梱[test_refs.py](test_refs.py)はCLIを通じた12件のテストです。固定参照、tag・branch・Docker tag、短いSHA・計算式、flow形式・引用key・折畳みscalar・alias、`run`内の文字列、ローカルworkflow、入力不足・symlink、壊れたYAML・重複key・非workflow構造、merge key・custom tag・循環alias、全対象の検査と非変更、parser不足を確認します。

```bash
"$WORKFLOW_REFS_VENV/bin/python" -m unittest discover -s "$WORKFLOW_REFS_SOURCE" -p 'test_*.py' -v
```

## 参照を直す

外部Git参照を`owner/repo[/path]@<40桁SHA>`、外部reusable workflowを`owner/repo/.github/workflows/file.yml@<40桁SHA>`へ変更します。正規の配布元で意図した版とcommitを確認し、コメントへrelease名を残せます。Docker Actionは`docker://registry/image@sha256:<64桁hex>`へ変更します。Digestの形式だけでimageの無害性や配布元を確認したことにはなりません。

自動修正の補助に[pinact v4.1.1](https://github.com/suzuki-shunsuke/pinact/releases/tag/v4.1.1)を使えます。この版とsource commit `b1a554a82ef4f55533237e49c19a24ddf0045100`を参照した例で、最新版の推奨ではありません。[公式の導入手順](https://github.com/suzuki-shunsuke/pinact/blob/b1a554a82ef4f55533237e49c19a24ddf0045100/INSTALL.md)と[固定checksum](pinact-v4.1.1-checksums.txt)でarchiveを検証してください。Linux x86_64の最短例は次です。

```bash
set -e
WORKFLOW_PINACT_DIR="$(mktemp -d)"
curl --fail --location --silent --show-error --output "$WORKFLOW_PINACT_DIR/pinact_linux_amd64.tar.gz" https://github.com/suzuki-shunsuke/pinact/releases/download/v4.1.1/pinact_linux_amd64.tar.gz
printf 'd1cffebe5704b74e2e5f8a864efb9f7e54768972dc686188c008033fb1797841  %s\n' "$WORKFLOW_PINACT_DIR/pinact_linux_amd64.tar.gz" | sha256sum -c -
tar -xzf "$WORKFLOW_PINACT_DIR/pinact_linux_amd64.tar.gz" -C "$WORKFLOW_PINACT_DIR" pinact
"$WORKFLOW_PINACT_DIR/pinact" --version
```

この取得ブロックはBashで実行し、`set -e`で取得・checksum確認の失敗時に止めます。成功後、次の修正は**GitHub APIへ通信し、指定workflowを書き換えます**。読み取りだけの検査とは異なるため、更新branchで明示的に行い、差分をレビューしてください。v4.1.1のpinactではDockerを処理対象から外し、digestへ手動修正して最後の検査へ含めます。Branchから意図した版を選ぶ判断も人へ残します。

```bash
"$WORKFLOW_PINACT_DIR/pinact" run -e '^docker://' .github/workflows/your-workflow.yml
git diff -- .github/workflows
"$WORKFLOW_REFS_VENV/bin/python" scripts/security/workflow-refs/check_refs.py .github/workflows
```

固定したcommit内部の追加取得の確認は[教材](../../../../../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/learning.md)へ戻ります。pinactの自動commit、全更新、cooldownやcomment検証を、この最小例へ追加しません。

## CIへ接続する

コピーするのは[workflow.yml](workflow.yml)のgateだけです。名前とpush対象branchを導入先へ合わせます。

```bash
cp -n "$WORKFLOW_REFS_SOURCE/workflow.yml" .github/workflows/workflow-reference-check.yml
```

`contents: read`、永続credentialなし、secret・OIDC・write権限なしの一時runnerで、全workflowを検査します。必要なcheckとworkflow・script・requirementsのreviewを、対象branchの保護ルールへ接続してください。実装例の存在だけでmergeは保護されません。同じPRで検査を削除・改変できる経路や管理者の迂回は別に確認します。

GitHubのfull-length SHA policyも利用できますが、**reusable workflowのタグ参照までは拘束しません**。[SOURCE-006のGitHub手順](../../../../source-protection/organization-baseline-and-drift-review/implementations/github/README.md)で対象と実適用を確認します。Merge queueを使う場合は`merge_group`等の必要イベントも導入先で設計・確認します。

実CIのsmoke testは、許可された使い捨てrepositoryで、このgateと同じコピー先のscriptを動かしてから行います。可変参照の例は`.github/workflows`へ追加せず、非workflowディレクトリのYAMLを一時的に検査へ渡し、check失敗・merge拒否を確認します。壊れた入力のエラーも確認した後、gateを全実workflowの検査へ戻します。ここで示す手順は未実行で、GitHubのrequired check・policy・迂回拒否を本PJで確認したとは扱いません。

## 解除する

まず代わりの検査を決め、管理者がこのcheckだけを必須条件から外します。導入PRで追加したworkflowと`scripts/security/workflow-refs`のファイルを削除します。参照をSHA・digestへ固定した変更はそのまま維持できます。共有ファイルを消さないよう導入差分を確認してください。

手元の一時venvとpinactは、作成したパスを確認してからそのディレクトリだけを削除します。GitHub policyを有効にした場合は、代替の受入条件を確認したうえで変更前の設定へ戻します。

## 検査の範囲と限界

検査するのは、明示したworkflowの`jobs.*.uses`と`jobs.*.steps[*].uses`です。Directory指定は直下の`.yml`・`.yaml`だけを読みます。同じrepositoryのworkflowは`./.github/workflows/...`とGitHub.comの`$/.github/workflows/...`を識別し、ローカルActionは`./...`を識別します。外部参照の存在・release対応・出所、ローカルcheckoutの信頼、全GitHub構文の正しさは検証しません。

Composite Action、remote workflowの内部、`jobs.*.container`・service、Dockerfile、script・package・binaryの取得を自動でたどりません。YAML merge key、custom tag、循環alias、重複key、symlink入力は検査エラーです。普通のaliasとflow形式は読めます。未対応構文を無視して成功させず、対応した検査方式かreviewした書換えを選びます。

実測したのはローカルCLIとLinuxのhash付き依存導入です。pinactのLinux archive hash・実行版・helpは確認しましたが、実GitHub APIによる更新、macOS、実Action実行、組織の採用やmerge保護は未確認です。[Patternの選択条件](../../README.md)と[controlの境界](../../../../../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)に、この限界を戻しています。
