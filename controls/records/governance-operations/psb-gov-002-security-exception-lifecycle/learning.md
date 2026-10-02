# 学習：例外は検査の合格ではない

[コントロール記録](README.md) · [設計パターン](../../../../engineering/governance-operations/security-exception-decision-boundary/README.md)

## シナリオ

Release直前にdependency checkが失敗した。担当者は「このversionだけを一週間許可」と考えたが、gateには`package=*`の除外が設定され、その後の別versionにも残った。
元のfindingを消したため、後から誰が何を受け入れたかも分からない。

## 二つのdecisionを分ける

Security checkの結果は「要求を満たしていない」。例外は「特定条件で、そのriskを期限まで受け入れる」です。
後者があっても前者は`PASS`になりません。この分離により、例外件数、残るrisk、是正の進捗を隠さず管理できます。

Scopeは人向けの説明だけでなく、gateが使うexact identifierで表します。Control property、package version、artifact digest、repository、environmentなど、対象ごとに必要なidentityは異なります。
共通schemaがその意味を推測してはいけません。

## 期限と評価不能

期限切れは、誰かが台帳を掃除するまで有効なのではありません。使用時の信頼できる時刻で失効します。
台帳を取得できない、承認を確認できない、対象を対応付けられない場合は「例外なし」と同じ許可結果を返すのではなく、評価不能として元の拒否を維持します。

この判断は脆弱性の対応期限を上書きしたり、残る旧成果物を復旧済みにしたりしません。前者は[GOV-003](../psb-gov-003-vulnerability-priority-decision/learning.md)、後者は[GOV-005](../psb-gov-005-deployed-artifact-recovery/learning.md)で具体的な場面から確認できます。

設計は[Security exception decision boundary](../../../../engineering/governance-operations/security-exception-decision-boundary/README.md)、保証目標は[コントロール記録](README.md)、資料の採否は[Sources](../../../../sources/README.md#ref-security-exception-lifecycle-001)を参照してください。
