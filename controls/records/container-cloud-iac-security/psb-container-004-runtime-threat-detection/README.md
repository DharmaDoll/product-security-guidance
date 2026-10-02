# PSB-CONTAINER-004: Runtime threat detection

## 問い

許可済みworkloadが実行中に示す異常を、正確な対象と観測範囲へ結び、観測障害と区別して担当者の判断へ渡せるか。

## できてはいけないこと

侵害されたアプリケーションのshell起動や保護ファイル変更を見逃したり、別workloadのイベントを誤って対応対象にしたりしてはいけません。
Sensor停止、event drop、通知不達を「イベントなし」と扱ってはいけません。
Severityだけで本番のkill・delete・隔離・失効を自動実行したり、生のcommandやpayloadを公開証跡へ残したりしてはいけません。

## 適用範囲と非適用

Containerの実行後の行動、sensor・rule・adapter、workloadとimageの同一性、観測・通知・対応への受け渡しが対象です。
Sensorの導入・[host／daemon防御](../psb-container-003-container-host-daemon-boundary/README.md)、admission、脆弱性scan、全製品の影響調査、PSIRT全体の能力は別の保証です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `RUNTIME-1` | Sensor・adapter・config・rulesetのレビュー済み版とidentityを確認する |
| `RUNTIME-2` | Eventを実行中のcontainer・workloadと稼働inventoryへ照合し、確認できたimage digestと許可判断へ結び付ける。IDが欠ける・一致しない対象は未確定として残す |
| `RUNTIME-3` | 想定外のprocess・shell起動を検知する |
| `RUNTIME-4` | 保護対象の実行ファイル・設定・認証情報のpathへの書込を検知する |
| `RUNTIME-5` | 想定外のprivilege・capability・namespace変更を検知する |
| `RUNTIME-6` | Runtime socket・host境界への不審なアクセスを検知する |
| `RUNTIME-7` | 未承認listener・宛先への通信を検知する |
| `RUNTIME-8` | Process数・CPU・memory等の異常消費を検知する |
| `RUNTIME-9` | 対象nodeとruleのcoverage、sensor・forwarderのhealth、鮮度、取得できるdrop・配送状態を同じ観測区間で評価し、欠測を「検知なし」にしない |
| `RUNTIME-10` | 安全な試験イベントについて、通知先への配送とownerへの割当・受領を別に確認する |
| `RUNTIME-11` | 証跡を保全し、破壊的対応は独立した認可へ渡す。検知結果だけでは実行しない |
| `RUNTIME-12` | 調査に必要な最小metadataを残し、raw command・payload・認証情報を既定の証跡から除く |

## 実装判断の羅針盤

先に守るworkloadと検知したい行動を決め、ruleが観測できるevent・条件・限界へ落とします。
製品名やsensor導入数をcoverageと同一視しません。通知までの経路を試験し、security findingと観測障害に別の対応先を用意します。
Dropがある区間は観測不完全です。Dropがゼロでも、未対応のnode・未定義rule・回避された行動まで観測できた証拠にはなりません。
Sensorが稼働するnode自体の侵害が疑われる場合、そのnodeからの「異常なし」を独立した証拠にせず、[host／daemon境界](../psb-container-003-container-host-daemon-boundary/README.md)の実効状態と外部の観測を照合します。

対象を特定できたら、稼働deploymentとimage digestを内部inventoryへ照合します。
同じpackageを使う全製品への波及調査は、runtime eventだけで確定せずSBOM・build・deployment情報へ引き継ぎます。
Artifactの問題が確認された場合は[GOV-005の置換と非稼働確認](../../governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)へ渡します。Node自体の侵害ではnodeの隔離・credential失効を別に判断し、artifactの置換だけで解決したことにしません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は採用先で確認する項目であり、本PJがlive sensorや通知先で試した結果ではありません。

- 無害な試験行動について、選んだruleが対象workloadのeventを出し、別workloadのIDや可変tagへ誤って結び付けないか。
- Container IDやimage digestが欠ける・合わないeventを捨てず、対象未確定として調査へ渡せるか。未確定のまま別対象を停止しないか。
- 対象nodeやruleの欠落、sensor停止、event drop、forwarder停止、通知不達を「検知なし」と表示しないか。Dropがゼロでも未観測範囲を隠さないか。
- 試験イベントの送信成功だけで終えず、通知先での受信、担当者への割当、受領まで区別できるか。
- 誤検知の調整や一時的な除外が他workload・他ruleへ広がらず、変更後のcoverageと期限を確認できるか。
- Severityだけでkill・delete・隔離・失効を実行できないか。必要な証跡を保全し、対象と承認を別に確認できるか。
- 既定の通知・証跡に生のcommand引数、payload、認証情報を含めず、詳しい情報へのアクセスを限定できるか。

## 保証しない範囲

未知挙動、rule回避、host侵害、暗号化payload、アプリケーションの意味的な認可違反は残ります。
Falco／Sysdigは実装候補であり必須製品ではありません。今回はsensor・通知先・対応systemの実装を追加していません。
旧synthetic fixtureの成功も本番導入や対応能力の証拠ではありません。

- [教材](learning.md)
- [Runtime detection to triage pattern](../../../../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)
- [Falco資料](../../../../sources/README.md#ref-container-003)、[Sysdig資料](../../../../sources/README.md#ref-container-004)
- [NIST SP 800-190の採否](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、[Framework mapping](../../../../mappings/frameworks.yaml)
