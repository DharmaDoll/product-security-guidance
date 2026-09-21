# No events is not no incident

## 通知が途切れた本番workload

許可済みimageのアプリケーションが侵害され、想定外のshellが起動しました。
Sensorはイベントを生成しましたが、forwarderが切断され、通知先には届きませんでした。
担当者の画面ではイベントがゼロです。「攻撃がなかった」と「観測・通知できなかった」は同じ表示になり得ます。

この架空シナリオでは、rule、sensor、queue、配送、受取先のhealthをイベント件数と別に確認すれば、観測障害として対応できます。
無害な試験イベントを発生させて、対象identityと通知先で照合することも必要です。
逆にイベントが届いても、image名やworkload名だけで対象を判断すると、再作成・再配置後の別containerへ対応するおそれがあります。

## 三つの状態を潰さない

| 状態 | 読み取れること | 読み取れないこと |
|---|---|---|
| 対象と結び付いた検知 | 定義した行動が観測された | 侵害の確定、他製品の影響、対応操作の許可 |
| 正常な観測区間で検知なし | 設定した範囲・ruleで該当eventがない | 未観測node、未知行動、全製品の安全性 |
| 観測・通知の障害 | 必要な判断材料が欠けている | 該当eventが存在しなかったこと |

検知と障害は同時にも起こります。一つの障害で既に得た検知を消さず、部分的な検知で障害を隠さない記録にします。
False positiveの調整は、workload・rule・期間を限定してレビューします。Global ignoreで通知量だけを減らさないようにします。

## 初動へ渡すもの

対象のimmutable identity、観測時刻・区間、ruleとsensorの版、health、配送結果、最小限の検知理由を渡します。
担当者は追加情報で正当な運用か侵害疑いか判断し、影響するdeployment・製品を調べます。
隔離や認証情報失効は可用性や調査証跡へ影響するため、独立した承認と復旧条件が必要です。

[REF-PORTFOLIO-001](../../sources/README.md#ref-portfolio-001)のoperationsからPSIRT・governanceへつなぐ教材です。
供給経路の段階11→12を扱いますが、侵入経路や全製品への波及をeventだけで確定しません。

- [Control](../../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)
- [設計patternと確認方法](../../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)
