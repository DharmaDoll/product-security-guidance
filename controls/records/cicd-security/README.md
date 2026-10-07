# CI/CD Security

変更内容を検証する処理と、リポジトリ、クラウド、リリース環境へ影響を与えられる処理を、同じ信頼境界へ置かないようにします。

| コントロール | 問うこと | できてはいけないこと | 教材 |
|---|---|---|---|
| [PSB-CICD-001 Workflow dependency identity](psb-cicd-001-workflow-dependency-identity/README.md) | 外部コードをレビューした版へ結び、更新と追加取得を判断できるか | 参照名の変更に利用側が追随し、差分なしで別のコードが実行される | [タグが動くと実行コードが変わる](psb-cicd-001-workflow-dependency-identity/learning.md) |
| [PSB-CICD-002 Workflow input handling](psb-cicd-002-workflow-input-handling/README.md) | 外部から届く値を命令へ変えず、許可した操作へ渡せるか | 題名・本文・入力値が追加コマンドや未許可の操作指定になる | [題名がコマンドになる](psb-cicd-002-workflow-input-handling/learning.md) |
| [PSB-CICD-004 Workflow authority minimization](psb-cicd-004-workflow-authority-minimization/README.md) | 各jobに必要な権限だけを渡し、残す権限の開始条件を保護できるか | テスト等の用途に不要なソース・公開・cloud操作が可能になる | [read-onlyでも公開物を書き換えられる](psb-cicd-004-workflow-authority-minimization/learning.md) |
| [PSB-CICD-005 Untrusted PR boundary](psb-cicd-005-untrusted-pr-boundary/README.md) | 外部PRが変えられるコードや成果物から、権限や秘密情報に届かないか | PRの実行結果を後続の権限付き処理が実行する | [PR由来の状態が権限付き処理へ届く](psb-cicd-005-untrusted-pr-boundary/learning.md) |
| [PSB-CICD-006 Workload federation boundary](psb-cicd-006-workload-federation-boundary/README.md) | 承認したworkloadだけへ必要なcloud権限を必要期間だけ渡せるか | 正規tokenであれば別の実行条件や過大な操作権限まで許可される | [短命tokenでも残る交換先の権限](psb-cicd-006-workload-federation-boundary/learning.md) |
| [PSB-CICD-007 Runner lifecycle isolation](psb-cicd-007-runner-lifecycle-isolation/README.md) | jobの状態や権限を次のjobへ残さず、実行資産を破棄できるか | 登録だけ消したhostや共有storageが後続jobへ再利用される | [新しいjobが前のjobを引き継ぐ](psb-cicd-007-runner-lifecycle-isolation/learning.md) |
| [PSB-CICD-009 Cache trust boundary](psb-cicd-009-cache-trust-boundary/README.md) | 信頼できない保存者のデータを権限付き処理へ渡していないか | key一致だけで復元内容を承認済みと判断する | [新しいrunnerへ古い攻撃が届く](psb-cicd-009-cache-trust-boundary/learning.md) |

教材は対応するcontrolのフォルダにあります。具体的な設計へ進むときは次のpatternを使います。

| 判断する対象 | 設計pattern |
|---|---|
| Workflowが呼ぶ外部コードと入力 | [Reviewed workflow dependency binding](../../../engineering/cicd-security/reviewed-workflow-dependency-binding/README.md)・[Workflow data and command boundary](../../../engineering/cicd-security/workflow-data-and-command-boundary/README.md) |
| Jobの権限と未信頼PR | [Purpose-bound job authority](../../../engineering/cicd-security/purpose-bound-job-authority/README.md)・[Untrusted PR boundary](../../../engineering/cicd-security/untrusted-pr-boundary/README.md) |
| Cloud権限、runner、cache | [Workload federation boundary](../../../engineering/cicd-security/workload-federation-boundary/README.md)・[CI state and runner lifecycle](../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md) |

## 読み進め方

Workflowの静的検査は[DETECT-001](../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)が共通要件を扱います。[その教材](../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md#workflowの検査が成功したのに変更を止められない)で「job成功でもmergeを止められない」例を読み、[Workflow analysis gate and reporting](../../../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)で検査・結果表示・受入条件を選べます。旧CICD-003のためだけのcontrolは作っていません。

[入力の教材](psb-cicd-002-workflow-input-handling/learning.md)では、題名をスクリプトへ埋め込む方式とデータとして渡す方式を比較し、[Workflow data and command boundary](../../../engineering/cicd-security/workflow-data-and-command-boundary/README.md)で呼出先までの扱いを選べます。

[Runner教材](psb-cicd-007-runner-lifecycle-isolation/learning.md)、[Cache教材](psb-cicd-009-cache-trust-boundary/learning.md)と
[CI state and runner lifecycle pattern](../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)で、再利用するcacheと破棄するhostを分けて設計します。

Cloudへ接続する場合は[Workload federation boundary](psb-cicd-006-workload-federation-boundary/README.md)と
[学習ノート](psb-cicd-006-workload-federation-boundary/learning.md)で、未信頼PR分離後も残る交換条件・操作権限を確認します。

ソース側でレビューされた変更をCIへ渡す場合も、[PR境界の教材](psb-cicd-005-untrusted-pr-boundary/learning.md)と
[設計pattern](../../../engineering/cicd-security/untrusted-pr-boundary/README.md)で、誰が変更した内容をどの権限で実行するかを追います。
`main`へのpushをレビュー済みとみなす前に、branch保護・rulesetの直接pushとbypassを確認します。
GitHub Actionsを使う場合の限定例は[こちら](../../../engineering/cicd-security/untrusted-pr-boundary/implementations/github-actions/README.md)です。

ソースからリリースまでの前後の責任は[横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で確認できます。
