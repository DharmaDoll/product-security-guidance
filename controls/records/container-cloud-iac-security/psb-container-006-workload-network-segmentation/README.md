# PSB-CONTAINER-006 Workload network segmentation

**Workloadが侵害されても、必要な相手以外へ通信できないか。**

例えば、frontendが侵害されたとき、ネットワーク制限が効いていなければ内部の別workloadや外部の任意の宛先へ接続できます。Policyファイルがあるだけでは、実際の通信が止まるとは言えません。

## 満たすべきこと

1. **必要な通信を決める。** 送信元、宛先、方向、protocol、port、用途とownerを列挙する（NET-SEG-1）。DNSや監視など基盤通信も個別に決め、広い許可へまとめない（NET-SEG-4）。
2. **両方向を既定で拒否する。** 管理対象の全workloadでingress・egressを制限し、新しいnamespaceやselector漏れを全許可にしない（NET-SEG-2）。必要な通信だけを送信元のegressと受信先のingressで許し、identityに使うlabel等を勝手に変更させない（NET-SEG-3）。異なるzoneや外部宛ても、宛先を表せる境界で制限する（NET-SEG-5）。
3. **実際の通信で確かめる。** 選んだnetwork pluginが対象protocol、IPv4／IPv6、workload、例外経路を強制できるか確認する（NET-SEG-6）。許可・拒否の通信を両側から試し、反映待ちや観測失敗を「遮断済み」にしない（NET-SEG-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Policyのないnamespaceやselectorから外れたworkloadが全通信を許されないか。
- Ingressだけ、またはegressだけの制限を、両方向の制限済みと誤認していないか。
- 別policyの広いallowや、未信頼者が変更できるlabelで許可範囲を広げられないか。
- DNS用の許可が任意の宛先まで通していないか。名前解決を許すことと通信先の許可を混同していないか。
- NetworkPolicyを受理しても強制しないplugin、IPv6、hostNetwork、NAT等から迂回できないか。
- Policy反映待ち、probe失敗、期限切れ例外を「遮断できた」結果に変えていないか。

これらは診断・設計レビューの確認項目であり、live通信を試した結果ではありません。

## このコントロールの範囲

対象はworkload間と外部宛てのL3／L4通信です。Host側の通信は[CONTAINER-003](../psb-container-003-container-host-daemon-boundary/README.md)、workloadのprocess権限は[CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)、実行後の予期しない通信は[CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。Applicationの認証、TLS identity、request単位の認可は別に確認します。

通信契約、実装が表せない宛先、移行時の反映順は[engineering](../../../../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)で選びます。[Kubernetes実装例](../../../../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)は限定した構成です。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-workload-network-segmentation-001)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
