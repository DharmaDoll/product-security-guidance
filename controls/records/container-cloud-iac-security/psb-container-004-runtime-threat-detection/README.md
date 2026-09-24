# PSB-CONTAINER-004: Runtime threat detection

## 問い

許可済みworkloadが実行中に示す異常を、正確な対象と観測範囲へ結び、観測障害と区別して担当者の判断へ渡せるか。

## できてはいけないこと

侵害されたアプリケーションのshell起動や保護ファイル変更を見逃したり、別workloadのイベントを誤って対応対象にしたりしてはいけません。
Sensor停止、event drop、通知不達を「イベントなし」と扱ってはいけません。
Severityだけで本番のkill・delete・隔離・失効を自動実行したり、生のcommandやpayloadを公開証跡へ残したりしてはいけません。

## 適用範囲と非適用

Containerの実行後の行動、sensor・rule・adapter、workloadとimageの同一性、観測・通知・対応への受け渡しが対象です。
Sensorの導入・host防御、admission、脆弱性scan、全製品の影響調査、PSIRT全体の能力は別の保証です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `RUNTIME-1` | Sensor・adapter・config・rulesetのレビュー済み版とidentityを確認する |
| `RUNTIME-2` | Eventをcluster・namespace・workload・Pod UID・container ID・image digestと許可policyへ結び付ける |
| `RUNTIME-3` | 想定外のprocess・shell起動を検知する |
| `RUNTIME-4` | 保護対象の実行ファイル・設定・認証情報のpathへの書込を検知する |
| `RUNTIME-5` | 想定外のprivilege・capability・namespace変更を検知する |
| `RUNTIME-6` | Runtime socket・host境界への不審なアクセスを検知する |
| `RUNTIME-7` | 未承認listener・宛先への通信を検知する |
| `RUNTIME-8` | Process数・CPU・memory等の異常消費を検知する |
| `RUNTIME-9` | Rule coverage、sensor・forwarderのhealth、鮮度、sequence・dropを同じ観測区間で評価する |
| `RUNTIME-10` | 認証した通知先へ試験イベントが届き、ownerが受け取れることを確認する |
| `RUNTIME-11` | 証跡を保全し、破壊的対応は独立した認可へ渡す。検知結果だけでは実行しない |
| `RUNTIME-12` | 調査に必要な最小metadataを残し、raw command・payload・認証情報を既定の証跡から除く |

## 実装判断の羅針盤

先に守るworkloadと検知したい行動を決め、ruleが観測できるevent・条件・限界へ落とします。
製品名やsensor導入数をcoverageと同一視しません。通知までの経路を試験し、security findingと観測障害に別の対応先を用意します。
Dropがある区間は観測不完全です。Dropがゼロでも、未対応のnode・未定義rule・回避された行動まで観測できた証拠にはなりません。

対象を特定できたら、稼働deploymentとimage digestを内部inventoryへ照合します。
同じpackageを使う全製品への波及調査は、runtime eventだけで確定せずSBOM・build・deployment情報へ引き継ぎます。

## 保証しない範囲

未知挙動、rule回避、host侵害、暗号化payload、アプリケーションの意味的な認可違反は残ります。
Falco／Sysdigは実装候補であり必須製品ではありません。今回はsensor・通知先・対応systemの実装を追加していません。
旧synthetic fixtureの成功も本番導入や対応能力の証拠ではありません。

- [教材](learning.md)
- [Runtime detection to triage pattern](../../../../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)
- [Falco資料](../../../../sources/README.md#ref-container-003)、[Sysdig資料](../../../../sources/README.md#ref-container-004)
- [Mapping](../../../../mappings/frameworks.yaml): 旧関係を保持。特性割当はレビュー中
