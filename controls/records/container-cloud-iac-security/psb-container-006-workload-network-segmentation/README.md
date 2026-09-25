# PSB-CONTAINER-006: Workload network segmentation

学ぶ：[A compromised frontend should not inherit the whole network](learning.md) ·
設計する：[Workload network allow boundary](../../../../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md) ·
試す：[Kubernetes NetworkPolicy](../../../../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)

## 問い

Workloadが侵害されても、業務上必要な相手・方向・protocol・port以外へ接続できず、その制限が実際の通信で効いていることを確認できるか。

## できてはいけないこと

Policyがない、selectorが外れている、片方向しか制限していない、CNIがpolicyを実装していない等の理由で、workload間通信や外部宛て通信が既定許可になってはいけません。
DNS、監視、control plane等に必要な通信を理由に、全namespace、全workload、全宛先、全portを許可してはいけません。

## 適用範囲と非適用

Workload間とworkloadから外部へのL3／L4通信、通信主体を表すidentity、ingress／egressの既定拒否、必要なallow、network pluginの実効性、policyの反映・例外・観測が対象です。

Applicationの認証・object認可、TLS identity、L7のrequest認可、[node／host network](../psb-container-003-container-host-daemon-boundary/README.md)、cloud VPC全体、通信量によるresource exhaustion、dataの機密性は別の主題です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `NET-SEG-1` | 必要な通信を、source workload identity、destination identityまたは管理境界、方向、protocol、port、用途として列挙し、所有者と変更理由を追跡する |
| `NET-SEG-2` | 管理対象の全workloadをingress・egressの両方向で既定拒否にし、policy未配置・selector漏れ・新規namespaceを通常の全許可へ変えない |
| `NET-SEG-3` | 一つの通信にはsource側egressとdestination側ingressの両方で必要最小限のallowを要求する。Identityに使うnamespace・label等を未信頼の主体が偽装できないようにする |
| `NET-SEG-4` | DNS、control plane、identity、telemetry、health等の基盤通信を個別に列挙し、広い宛先・port・protocolのfallbackへ変えない |
| `NET-SEG-5` | 異なるsensitivity zoneや外部宛てのegressを明示的な境界で制限する。IP変換、Service、FQDN等をcore policyで正確に表せない場合は、egress gateway、proxy、または対応するnetwork implementationへ渡す |
| `NET-SEG-6` | 使用するnetwork implementationが対象protocol、IPv4／IPv6、workload class、ingress／egressを実際に強制することを確認し、hostNetwork、node traffic、NAT等の非対応経路を別の境界で扱う |
| `NET-SEG-7` | 許可する通信と拒否する通信をsource・destinationの両側からlive probeし、policy反映待ち、収集不能、plugin障害を「遮断済み」へ変えない。例外は対象・owner・期限を限定する |

## 実装判断の羅針盤

最初にapplicationの通信実績ではなく、必要な通信契約を決めます。現在観測できる全通信をそのままallowへ変えると、侵害済み通信や不要なlegacy経路まで固定するためです。

Default denyは起点であり完成ではありません。送信元のegressと受信先のingressが同じ通信契約を許し、別identityや別portでは拒否されることを確認します。Kubernetes NetworkPolicyはallow ruleが加算されるため、一つでも`{}`等の広いallowがあれば、別policyでその通信をdenyへ戻せません。

API上にNetworkPolicy objectがあるだけでは強制を証明しません。NetworkPolicyを実装するCNIまたはnetwork pluginと、許可・拒否を区別するlive connectivity testが必要です。Policy反映には時間差があり得るため、作成順序と移行中の状態も設計します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。実施済みの診断結果ではありません。

- NetworkPolicyがないnamespace、新しく作られたnamespace、selectorから外れたPodが全通信を許可されないか。
- Ingressだけ、またはegressだけをdefault denyにし、反対方向を制限済みと誤認していないか。
- Source egressが許可してもdestination ingressが拒否すること、その反対も独立して確認できるか。
- `ingress: [{}]`、`egress: [{}]`、空の`namespaceSelector`、全port等を持つ別policyがallowを広げていないか。
- 許可identityに使うPod labelやnamespace labelを、通信元自身や別tenantが付け替えられないか。
- DNSを許可するruleが全namespaceの任意PodやDNS以外の宛先を許可していないか。名前解決の許可を、解決後の宛先許可と取り違えていないか。
- Service／load balancer／egress NATの前後で、`ipBlock`が意図したsource・destinationを評価しているか。
- NetworkPolicy objectを受理するが強制しないplugin、未対応protocol、IPv6、hostNetwork、nodeからの通信で迂回できないか。
- Policyをworkloadより後に作成した瞬間や、変更の反映途中に意図しない通信が成立しないか。
- 拒否logがないこと、probe timeout、collector停止を「通信は遮断された」という証拠にしていないか。
- 期限切れまたはowner不明の例外が、全egressやzone間通信を許可し続けていないか。

## 境界と受け渡し

- Workloadのprocess・kernel・host権限は[PSB-CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)が扱います。
- NetworkPolicy selectorへ使うlabelやnamespaceの変更権限は、[IaC change boundary](../psb-iac-001-infrastructure-change-authorization-and-drift/README.md)とcluster管理面の別のcontrolが必要です。
- TLS、service identity、applicationのrequest認可はこのcontrolのL3／L4 allowとは別に確認します。
- 実行後の予期しないflow、port scan、観測障害は[PSB-CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。
- CPU、memory、PID、local storage等は[PSB-CONTAINER-007 Workload resource consumption bounds](../psb-container-007-workload-resource-consumption-bounds/README.md)が扱います。

## 参照資料とマッピング

- [REF-WORKLOAD-NETWORK-SEGMENTATION-001](../../../../sources/README.md#ref-workload-network-segmentation-001)
- [NIST SP 800-190](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
