# ENG-RUNTIME-001: Runtime detection to triage

## 利用場面と構造

本番の異常を通知するだけで終わらせず、正確な対象・観測範囲・担当者の判断へつなげる設計です。

```text
Reviewed sensor・rule → 最小event → 対象identityの照合 → 認証した通知先 → ownerのtriage
         ↓                                ↓                      ↓
独立したhealth・drop・coverage → 観測障害の通知       稼働製品の照合・証跡保全
                                                                ↓
                                                   独立承認 → 対応・復旧の確認
```

Admission時の情報だけでは実行時container ID等が確定しない場合があります。
Deployment・runtime inventoryを使って許可したdigestと実際のcontainerを関連付け、名前だけで対応しません。
Identity欠落は調査を止める理由ではなく、対象未確定として記録し、破壊的操作を止める条件です。

## 責任と確認方法

| 境界・担当 | 採用先で行う確認 | 失敗したとき |
|---|---|---|
| Platform: sensor・driver | 固定版・integrity、kernel対応、最小権限、node coverage、更新canary | 未対応範囲を明示し、health障害として通知 |
| Security: rule | 検証用workloadで無害なprocess・file・通信の試験。期待するruleと対象で照合 | Rule欠落と不検知の理由を調査。広いignoreへ切り替えない |
| Operations: 観測・配送 | 同じ区間のdrop・queue・connection・鮮度と試験通知の到達を確認 | 既存検知を保ち、観測障害も別に記録 |
| Product owner: triage | Deployment ID・image digest・製品ownerを照合し、追加証跡で正当な行動か判断 | Unknown owner・inventory不完全を該当なしにしない |
| Incident owner: 対応 | 証跡保全、対象限定、独立承認、復旧条件、事後確認を演習 | Fixtureやseverityだけでkill・delete・隔離・失効しない |

検証用環境を使い、本番sensorを無断で停止せず、実credential・保護ファイルの内容を試験へ使いません。
通知成功のHTTP応答だけではownerが処理できる証拠にならないため、receiver記録・割当・acknowledgementまで確認します。

## 選択肢と運用費

Host sensorはkernel対応と実行権限の管理が必要です。Managedな転送・分析を使う場合も、license・coverage・retention・配送・障害の責任を確認します。
最初はauditとbaselineでruleを調整し、workload単位の誤検知・drop・配送遅延・未処理時間を見ます。
失われたeventを完全に復元できるとは限りません。観測不完全な区間と、追加調査・risk判断を記録します。

## 製品適用とPSIRTへの受け渡し

Runtimeの対象は、一つのcontainer・deploymentです。Packageに侵害疑いがある場合は、
[旧PSB-GOV-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/supply-chain-incident-readiness/README.md)のSBOM→build→artifact→deploymentの逆引きへ渡します。
Package一致は侵害確定ではなく調査対象の抽出です。Inventory、pagination、鮮度が不完全なら、全製品の該当なしとは判断しません。
FIRSTのPSIRT能力評価は、受付・分析・修復・開示・連絡等の組織証拠が必要であり、このpatternだけでは満たしません。

## 未実装・参照資料

今回はlive installer、vendor API、normalizerの移植、通知system、自動対応を追加していません。
旧fixtureはschemaの学習・試験材料として保留し、製品の現在のevent・health contractを再レビューしてから独立実装へ移します。
Sysdigの`13.0.0-fixture`は合成値であり推奨versionではありません。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)、[教材](../../../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/learning.md)
- [Falco参照](../../../sources/README.md#ref-container-003)、[Sysdig参照](../../../sources/README.md#ref-container-004)、[初動・PSIRT資料](../../../sources/README.md#ref-runtime-response-handoff-001)
- [Build boundary](../../build-security/build-execution-boundary/README.md): 短命CIの観測と本番の継続監視は運用条件が異なる
