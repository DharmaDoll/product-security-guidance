# Incident impact and response planning

`ENG-GOV-001` / `governance-operations`

## 解く設計問題

依存の通知を、根拠のある製品影響調査と承認付き初動へ変換する。調査を実対応の権限から分離する。
対象読者はPSIRT、product security、build platform、運用担当者です。

## 推奨構造

```text
Exact component / advisory
  → scope-aware inventory query
  → SBOM ↔ build evidence ↔ artifact digest ↔ observed deployment
  → impact candidates + bounded no-match + unresolved scope
  → owned dry-run plan
  → independently approved response (outside this pattern's verifier)
```

Incident担当は検索条件と対象範囲、build担当は成果物との対応、運用担当は稼働観測、承認者は対応の権限と影響を所有します。
Collectorや分析基盤から来る識別情報を無条件に信頼せず、対応元の記録と照合します。

## 方式の選択

| 方式 | 向く状況 | 代償・確認事項 |
|---|---|---|
| Local inventory検索 | 管理範囲が限定され、snapshotを保全できる | 更新漏れ、探索対象漏れ、複数ecosystemの識別を管理する |
| 外部分析基盤 + local証跡 | 製品横断でcomponent・advisory検索が必要 | ACL、pagination、処理完了、鮮度、API契約を確認する。分析基盤だけを正本にしない |
| Deployment collectorとの結合 | 稼働service・環境を特定する | Cluster・namespace・短命workloadの観測範囲、取得時点とcollector停止を明示する |

Dependency-Trackは二番目の方式の候補であり必須製品ではありません。旧4.14.3 fixture契約を現行APIの保証として使いません。
検索用read-only権限をSBOM uploadや対応用権限から分け、秘密情報・生payloadを共有レポートへ持ち込みません。

## 対応計画の境界

保全、配布停止、credential失効、artifact/cache隔離、承認したversionでのclean rebuild、関係者への連絡について、
対象、owner、承認、実行条件、可用性影響、確認方法を定めます。危険な操作を検索結果から自動実行しません。
緊急封じ込めと保全を並行する条件も事前に決めます。復旧後の監視と再侵入確認は別の手順です。

## 失敗経路と確認方法

ACLで製品が欠ける、次pageを読まない、別SBOMを結ぶ、tagをdigestとして扱う、collector停止を空結果にする、承認なしで削除する、を負のシナリオとして確認します。
組織での演習では既知の対象を含む非本番調査を行い、inventoryの独立した一覧と照合し、権限不足・収集停止が未解決として担当者へ届くことを確認します。
Fixtureの成功だけで本番網羅性や対応能力を判定しません。実対応の演習は別の承認・範囲で行います。

## 関連資料と未移植範囲

[Control](../../../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)、
[教材](../../../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/learning.md)、[仕様・採否](../../../sources/README.md#ref-supply-chain-impact-001)を参照してください。
旧normalized JSON検査・runbook生成器は保留しています。Live adapter、deployment collector、実対応は未実装・未検証です。
