# PSB-GOV-001 Supply-chain impact assessment

## このcontrolを一枚で理解する

| 項目 | 内容 |
|---|---|
| セキュリティ上の問題 | 問題のある依存が判明しても、使用したbuild、成果物、稼働環境を結び付けられず、影響製品を見落とす。 |
| 誰から、または何から守るか | 侵害された依存の配布者、古い・欠けたinventory、範囲を誤認する調査、未承認の破壊的対応から守る。 |
| 何が対象か | 対象packageの正確な識別情報、SBOM、build証跡、成果物digest、稼働deployment、対応計画。 |
| 何をするか | 識別情報を照合し、収集範囲と鮮度を確認して、影響候補・範囲内の該当なし・調査不能を分け、担当者と承認条件を持つ初動計画へ渡す。 |
| 成功状態 | 対象と時点が明示された影響候補一覧を説明でき、欠落は未解決として残り、実対応は別の承認で管理される。 |
| 対象外・残余リスク | 依存の使用だけで侵害や悪用を証明しない。全processの観測、実対応、復旧、PSIRT成熟度は別途確認する。 |

## 問いと適用範囲

「この依存の問題は、どの製品のどの稼働環境に関係するか。何が未確認で、誰が対応を決めるか」に答えられるか。
既知の侵害versionや脆弱性の通知を受け、製品横断の調査を始める場面に適用します。
Package名だけの検索、可変image tagだけのdeployment一覧、SBOM提出済みという自己申告では成立しません。

## 必要なセキュリティ特性

| ID | 満たすべき状態 | 防ぐ失敗 |
|---|---|---|
| IMPACT-1 | Package ecosystem・名前・exact version等を照合してrepository、build、artifactを逆引きする | 同名の別packageを含めたり、影響するbuildを漏らしたりする |
| IMPACT-2 | SBOMの識別子、build記録、証跡digestが同じ成果物へ結び付く | 別buildのSBOMを根拠に対応する |
| IMPACT-3 | 証拠の保全対象、対応owner、独立した承認、dry-run計画を定める | 無承認の削除・失効で証拠や可用性を失う |
| IMPACT-4 | 影響候補、限定した範囲の該当なし、調査不能を別の状態とする | 取得失敗を該当なしとして閉じる |
| IMPACT-5 | Inventoryの欠落とrunbookの安全条件を検査し、不備を未解決として残す | 不完全な調査結果で全体を安全と宣言する |
| IMPACT-6 | 外部分析基盤ではexact CVE・component、全page、対象project権限、鮮度・処理healthを確認し、project UUID・version・SBOM serial・PURLをlocal証跡と相互照合する | 部分検索や古い結果を製品全体の真実とする |
| IMPACT-7 | Active deployment ID、environment、観測時刻、実際のartifact digestをbuildと照合する | Releaseの存在を稼働の証明と取り違える |

IMPACT-6は外部分析基盤を使う場合の条件です。使わない場合も、検索対象の完全性と証跡の対応を確認する責任は残ります。

## 実装判断の羅針盤

まず製品・環境の調査範囲と担当者を定義し、その範囲をinventoryが観測できるか確認します。
SBOMのcomponent一致は影響候補の入口であり、悪用可能性・露出・既存の緩和策は別の判断です。
Buildに含まれない開発専用依存なら、runtimeの攻撃経路がないこともあります。一方、install時に実行された依存は、成果物に残らなくてもbuild環境へ影響し得ます。

証拠保全は対応判断の入力ですが、切迫した被害を止めるための隔離を無期限に待たせる規則ではありません。
緊急時は承認済みの手順で、最小限の保全と封じ込めを並行させ、失う証拠と判断理由を記録します。
旧サンプルの固定順序はdry-runの契約であり、あらゆるincidentの絶対順序ではありません。

## 学習・設計・根拠

- [教材: Impact is an evidence chain](learning.md)
- [設計: Incident impact and response planning](../../../../engineering/governance-operations/incident-impact-and-response-planning/README.md)
- [参照仕様と採否](../../../../sources/README.md#ref-supply-chain-impact-001)、[framework関係](../../../../mappings/frameworks.yaml)
- [Runtimeの検知と初動](../../../../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)

この記録はガイダンス移行です。外部API、稼働inventory、通知、実対応は検証していません。
