# PSB-CICD-002 Workflow input handling

**PRの題名など外部から届く値を、CIの命令に変えずに使えているか。**

## なぜ必要か

例えば、題名を確認するだけのWorkflowでも、その値をscriptの中に埋め込むと、題名の一部が追加コマンドとして実行されることがあります。誰が値を変えられ、どこで命令として解釈されるかが判断の起点です。

## 満たすべきこと

1. **入力の流れを追う。** 題名、本文、branch名、入力値などについて、変更できる人、届くeventとjob、最後に解釈される箇所を確認する（CI-INPUT-1）。Stepの出力や生成ファイルを経由しても、出所だけで信頼済みにしない（CI-INPUT-5）。
2. **命令と値を分ける。** 外部の値をscriptのソースへ埋め込まず、固定した命令へデータとして渡す（CI-INPUT-2）。対象のshellや言語で引数の数と内容を保ち、後段で再び命令として評価しない（CI-INPUT-3）。
3. **操作の意味も限定する。** 一つの引数として渡せても、値が操作、対象、オプションを選ぶなら、許可した指定だけを実行する（CI-INPUT-4）。実行へ届く箇所を検査し、表示用の式と区別する。対象不足や解析失敗を「問題なし」にしない（CI-INPUT-6）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 題名や本文に引用符、改行、コマンド区切りを含めても、固定した処理以外の命令が増えないか。
- 空白、ワイルドカード、空文字を渡しても、意図しない引数や対象に変わらないか。
- 環境変数、step出力、Action入力、生成ファイルへ移した値が、後段で命令として再解釈されないか。
- 未知の操作、オプションに見える値、対象外のパスを渡しても、許可外の処理を実行しないか。
- 検査対象の欠落、未対応構文、検査失敗を、確認済みの結果に変えていないか。

これらは診断・設計レビューの確認項目であり、実際のCIで試した結果ではありません。

## フレームワークとの関係

Workflowが外部入力を命令として解釈しないための個別関係は、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に登録していません。参照したshell・CIの仕様は設計の根拠であり、規格の特定要件へ自動的に割り当てません。

## このコントロールの範囲

対象は外部入力をWorkflowのscript、Action、呼出先プログラムへ渡す経路です。式があるだけで欠陥とは判断せず、値が実行内容へ届くかを見ます。未信頼コード自体の実行と権限付き処理の分離は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、jobの権限は[CICD-004](../psb-cicd-004-workflow-authority-minimization/README.md)、runnerの状態は[CICD-007](../psb-cicd-007-runner-lifecycle-isolation/README.md)へ渡します。

入力の渡し方と操作の選び方は[engineering](../../../../engineering/cicd-security/workflow-data-and-command-boundary/README.md)を参照してください。この主題はガイダンスと診断項目で完了とし、独自scannerを必須にしません。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、[GitHub仕様](../../../../sources/README.md#spec-github-workflow-input)、[Bash仕様](../../../../sources/README.md#spec-bash-shell-expansion-5-2)、[OWASP資料](../../../../sources/README.md#ref-command-input-defense)、[本PJの解釈](../../../../sources/README.md#ref-workflow-input-001)、旧項目との[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-input-migration)へも辿れます。
