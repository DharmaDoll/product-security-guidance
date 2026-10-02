# ENG-CICD-004: Reviewed workflow dependency binding

外部コードの変更を、利用側が気付かず取り込まないようにします。CIを設計する人が、**参照を固定する場所、更新をレビューする場所、追加取得を確認する範囲**を選ぶpatternです。対応する要件は[PSB-CICD-001](../../../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)です。

## 配置と受け渡し

```text
正規の配布元・意図した版・変更内容を確認
  → commit / image digestへ固定したworkflow変更
  → 直接参照の検査 ＋ 固定コード内の追加取得review
  → 保護された受入経路
  → 用途に必要な権限だけで実行
```

検査は参照の形式、reviewは選ぶ内容と追加取得、受入ルールは検査・reviewを飛ばさないことを担当します。外部Actionの内側や同じrepositoryのActionを調べた記録と、呼出元の参照検査結果を分けます。更新PRには配布元、旧版と新版、commit permalink、用途、読んだ範囲、残る取得経路と対応を残します。

## 方式を選ぶ

| 方式 | 向く条件 | 代償と確認点 |
|---|---|---|
| 小さな自社scriptへ置き換える | 必要処理が短く、外部Actionの機能を多く使っていない | 自社で保守する。scriptのdownloadやpackage取得を新しい抜け道にしない |
| 外部Actionを固定し、更新PRを作る | 配布元の機能・保守を使いたい | SHA変更だけで承認しない。追加取得、出所、権限に応じたreviewが残る |
| レビューしたforkを維持する | 必要機能があり、上流の可変取得をそのまま許容できない | 更新追従と修正責任を持つ。forkという名前だけで信頼しない |
| Provider policyとrepository検査を組み合わせる | 複数repositoryへ同じ条件を適用したい | 対象・迂回・上書きを確認する。Provider policyの対象外を検査で補う |

[GitHub / Python実装](implementations/python-workflow-refs/README.md)は直接参照の小さな検査とpinactによる修正手順を示します。検査の対象は明示したworkflowです。Composite Action、jobのcontainer・service、remote workflow内部、scriptの取得経路は別の確認へ残すため、全依存を固定するscannerとして選ばないでください。

## 強制点と失敗経路

手元の検査は早く気付くために使い、merge条件の検査は独立した受入経路へ接続します。同じPRでscript、依存lock、workflow、担当者設定まで無効化できるなら、緑表示は受入条件になりません。必要なreviewをbranch保護・ruleset等で要求し、対象branch、管理者の迂回、check名の衝突も確認します。PRコードを検査するjobの権限は[CICD-005](../untrusted-pr-boundary/README.md)へ従います。

検査障害や読めないworkflowは固定済みにせず止めます。正当なworkflowに外部参照がない場合は、その対象を読めたことと参照数ゼロを明示できます。入力が空の状態とは区別します。対応しない構文はエラーにし、別の検査方式か、レビューした構文変更を選びます。

直接参照が固定されていても、内部で可変取得が見つかった時はjobの用途・権限を確認します。高権限の処理へ渡す前に取得内容を固定・検証する、処理を分離する、方式を変更する、[期限付き例外](../../governance-operations/security-exception-decision-boundary/README.md)を選ぶ、という判断を残します。内部を取得できなかった場合も、その欠落をreview結果へ残します。

## 隣接する設計

[Reviewed dependency intake](../../dependency-security/reviewed-dependency-intake/README.md)へ渡すのは採用する版と変更判断、[Dependency release cooldown](../../dependency-security/dependency-release-cooldown/README.md)へ渡すのは観測期間の判断です。[Organization baseline and drift review](../../source-protection/organization-baseline-and-drift-review/README.md)は必要repositoryへの適用、[CI state and runner lifecycle](../ci-state-and-runner-lifecycle/README.md)は実行後に残る状態を扱います。

直接扱う攻撃段階はworkflow・Actionの取得と実行準備です。固定した参照と残る追加取得の情報をrunner・buildへ渡し、問題のある版の失効・更新は運用へ渡します。七つのレイヤーと攻撃段階は[横断分析](../../../docs/ANALYSIS_LENSES.md)の参照軸で、追加の要件や導入証拠ではありません。直接の根拠と本PJの判断は[Sources](../../../sources/README.md#spec-workflow-dependency-references)、旧実装との比較は[移行判断](../../../docs/WORKFLOW_DEPENDENCY_MIGRATION.md)にあります。
