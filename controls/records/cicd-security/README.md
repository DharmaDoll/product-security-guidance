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

教材は対応するControlのフォルダにあります。個別の方式は各Controlへ統合しました。工程を続けて読む場合は、[PRの検証からリリース用ビルド・公開への引き渡しまで](../../../engineering/pull-request-to-release-build.md)へ進んでください。

## 設計の選択へ進む

| 読者の問い | 設計・教材 |
|---|---|
| 検査した結果をマージ条件と表示へどうつなぐか | [検査・受入・結果公開の設計](../../../engineering/workflow-analysis-gate-and-reporting.md)。共通要件は[GOV-009](../governance-operations/psb-gov-009-scanner-evidence-trust-boundary/README.md)、[教材](../governance-operations/psb-gov-009-scanner-evidence-trust-boundary/learning.md#workflowの検査が成功したのに変更を止められない)でjob成功だけでは変更を止められない場面を読む |
| 何を再利用し、何を破棄するか | [cacheとrunnerの設計](../../../engineering/ci-state-and-runner-lifecycle.md)。[Runner教材](psb-cicd-007-runner-lifecycle-isolation/learning.md)と[Cache教材](psb-cicd-009-cache-trust-boundary/learning.md)で、hostの残存状態と外部cacheを分ける |
| PR検証と後続runをGitHubでどう分けるか | [限定した実装例](../../../engineering/implementations/github-untrusted-pr/README.md)。mainへのpushだけでレビュー済みとせず、branch保護・直接push・bypassを確認する |
| CIからクラウド権限をどう取得するか | [CICD-006の方式](psb-cicd-006-workload-federation-boundary/README.md)と[教材](psb-cicd-006-workload-federation-boundary/learning.md)。token発行、交換条件、交換後の操作を分ける |

入力の渡し方は[CICD-002の方式](psb-cicd-002-workflow-input-handling/README.md)と[教材](psb-cicd-002-workflow-input-handling/learning.md)から呼出先まで追います。ソースからリリースまでの前後の責任は[横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で確認できます。旧CICD-003のためだけのControlは作らず、検査の共通条件はGOV-009で扱います。
