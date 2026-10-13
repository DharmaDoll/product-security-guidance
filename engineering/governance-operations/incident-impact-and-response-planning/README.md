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

## 検索0件を判定する前に

「一致なし」は検索APIの返答です。製品についての「該当なし」に進める前に、次の範囲を同じ調査時点で確認します。

| 確認する範囲 | 欠けている場合 |
|---|---|
| 対象製品・版とSBOMの取得地点、収集対象、除外条件 | ソースSBOMにない部品を、完成物にもないとは言えない |
| 成果物digestとSBOMの対応、分析基盤での取込と必要な分析の完了 | 別成果物や処理途中の結果を使う恐れがある |
| 対象projectへの閲覧権限、全ページ、検索条件と結果時刻 | 見えていない製品・結果が残る |
| 稼働環境の観測範囲、時刻、成果物digestとの対応 | リリース済みと稼働中、未観測と非稼働を区別できない |

各条件が満たされても「該当なし」は示した製品・環境・時点・収集範囲に限ります。一部だけ確認できた場合は、その部分の非該当と残る調査不能を併記します。SBOMの生成と分析状態の確認方法は[REL-003の設計](../../release-integrity/release-sbom-identity-and-analysis/README.md)、供給者SBOMの訂正・撤回は[REL-004](../../release-integrity/supplier-sbom-intake-boundary/README.md)を参照します。

GOV-003へは、影響候補、範囲付き非該当、調査不能のどれかに加え、対象・観測時刻・根拠・不足情報・再確認担当を渡します。GOV-003が露出、深刻度、悪用情報、組織方針を合わせて優先度を決めます。調査不能は担当者を置いて再調査または暫定対応を選ぶ材料であり、自動的な低優先度や最高優先度ではありません。

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
旧normalized JSON検査・runbook生成器は移植しません。文書と診断項目でこの主題の範囲は完了です。Live adapter、deployment collector、実対応は未検証であり、採用先で導入・確認に役立つ場合だけ具体化します。

<a id="intrusion-containment"></a>

## 公開サービスへの侵入から、横展開の封じ込めへ

ここからは依存部品の検索とは異なり、侵入後の操作を観測した場合の対応設計です。[GOV-012](../../../controls/records/governance-operations/psb-gov-012-detection-and-response-readiness/README.md)から対象・根拠・未確認範囲を受け取り、SOC、アプリ、基盤、認証基盤の担当者で処置を決めます。既存のSBOM検索で全被害を把握できるとは扱いません。

| 判断 | 処置の選択と代償 | 効果の確認 |
|---|---|---|
| 侵入先が内部へアクセスしている | 対象の通信制限・隔離・停止を選ぶ。停止は通常業務や揮発する証拠に影響する。証拠保全と緊急封じ込めを並行し、全調査を待たない | 設定の受理だけでなく、問題の経路が止まったか、迂回先・既存接続が残らないかを見る |
| 認証情報が悪用された疑いがある | GOV-004へ権限・利用先・時刻を渡す。ネットワーク隔離だけでは別環境から使える権限を止められない | 古い権限と派生セッションの利用拒否、新しい権限で必要な処理が動くかを確認する |
| VMや管理APIへ広がった | 移動先のログ、追加された鍵・アカウント・ロール・定期処理等を調査する。VMなら信頼できる状態からの再構築も選ぶ。管理APIでは実行元の隔離と権限の失効を別々に判断する | 元の侵入先だけでなく移動先と残存アクセス経路の処置結果を確認する |
| 公開物や配備先が変えられた | 公開・配備を制限し、GOV-005へ影響する成果物を渡す | 正しい置換先の稼働、旧版の非稼働、再配布・切り戻し経路を確認する |

処置ごとに対象、判断者、実行者、許可範囲、通常業務への影響、確認方法、解除条件を決めます。既に承認された緊急対応の条件内なら、毎回新たな承認を待つ運用にはしません。逆に対象を特定できない通知だけで、広範囲を自動停止しません。操作権限や連絡先が使えない場合の引き継ぎも決めます。

再開前には、入口の修正、移動先の調査、追加された権限・不正な処理の除去、必要なサービスの正常動作を確認します。データの持ち出し・改変が疑われれば、データ所有者と組織のインシデント対応へ渡します。復旧は漏えいの取消しではありません。未観測の対象は担当者と次の行動を残し、全体を復旧済みにしません。[成果物の復旧設計](../deployed-artifact-recovery/README.md#incident-recovery-boundary)が扱う範囲も区別します。

机上演習では、隔離権限なし、移動先ログの欠落、token失効失敗、一部環境だけ復旧、隔離による監視断を取り上げ、誰が判断を引き継ぐか確認します。実操作を試す場合は許可された非本番対象に限定し、処置の効果と解除を別に確かめます。

根拠は[NISTの封じ込め・除去・復旧のガイダンス](../../../sources/README.md#ref-security-operations-lifecycle-001)です。上の具体的な分担は本PJの設計判断で、実操作は未確認です。この追記は既存GOV-001を全インシデント対応のControlへ拡張するものではありません。VM・管理APIを含む独立した封じ込めControlは今回追加せず、設計ガイダンスと診断観点で扱います。
