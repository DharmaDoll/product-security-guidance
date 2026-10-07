# PSB-CONTAINER-004 Runtime threat detection

**稼働中の異常を正しいworkloadへ結び付け、観測できなかった状態と区別して担当者へ渡せるか。**

例えば、侵害されたcontainerがshellを起動しても、sensorが停止していればeventは出ません。「eventなし」を「異常なし」と扱うと見逃します。別workloadのeventへ誤って結び付ければ、対応対象も間違えます。

## 満たすべきこと

1. **何をどこで観測するか決める。** 対象workloadと行動に合うsensor・ruleの版を確認する（RUNTIME-1）。想定外のprocess、保護fileの変更、権限変更、runtime socket、通信、資源消費など、選んだruleが観測できる行動と限界を示す（RUNTIME-3〜8）。
2. **eventの対象を確かめる。** Eventを実行中のcontainer、workload、image digest、稼働inventoryへ照合し、IDが欠ける・一致しない場合は対象未確定として残す（RUNTIME-2）。
3. **観測と通知の状態を分ける。** 対象node・ruleのcoverage、sensor、転送、event dropを同じ期間で確認し、欠測を「検知なし」にしない（RUNTIME-9）。無害な試験eventが通知先へ届き、担当者に割り当てられ、受領されるところまで別々に確認する（RUNTIME-10）。
4. **対応を別に判断する。** 証跡を保ち、kill・delete・隔離・失効などの破壊的対応は独立した承認へ渡す（RUNTIME-11）。通常の通知や証跡には生のcommand、payload、認証情報を載せない（RUNTIME-12）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 無害な試験行動を、選んだruleが正しいworkloadのeventとして示すか。別workloadや可変tagへ誤って結び付けないか。
- Container IDやimage digestが欠けるeventを、対象未確定のまま扱えるか。
- Sensor停止、event drop、ruleや対象nodeの欠落、通知不達を「検知なし」に変えていないか。
- 試験eventが送信されたという表示だけで終わらず、受信・担当への割当・受領を確認できるか。
- Severityだけで破壊的対応を実行できないか。通知・証跡へ機微なcommandやpayloadが入らないか。

これらは診断・設計レビューの確認項目であり、live sensorや通知先で試した結果ではありません。

## このコントロールの範囲

対象は実行後の行動、観測範囲、eventの対象、通知と対応への受け渡しです。Hostとsensorの置き場は[CONTAINER-003](../psb-container-003-container-host-daemon-boundary/README.md)、実行前の許可は[CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)へ渡します。Artifactの問題が見つかった後の置換と非稼働確認は[GOV-005](../../governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)が扱います。Ruleがない行動やhost自体の侵害まで、eventなしから安全とは判断できません。

Rule、sensor、通知先の選び方は[engineering](../../../../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)を参照してください。FalcoやSysdigは候補であり必須製品ではありません。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[Falco資料](../../../../sources/README.md#ref-container-003)、[Sysdig資料](../../../../sources/README.md#ref-container-004)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
