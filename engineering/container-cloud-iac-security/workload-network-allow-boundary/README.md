# ENG-CONTAINER-004: Workload network allow boundary

## 利用場面と推奨構造

Application processが侵害されても、必要な通信経路から別workload、管理面、異なるsensitivity zone、外部宛てへ横展開させない設計です。

```text
reviewed flow contract
  source identity -> destination identity / boundary -> protocol + port
          |                         |
          v                         v
   source egress allow       destination ingress allow
          \                         /
           +--- default deny ------+
                       |
                       v
              CNI / network data plane
                       |
             allowed + denied live probes
                       |
                       v
              flow and health observation
```

Default denyを先に置き、必要なflowを両側から加えます。Manifestの存在ではなく、採用したnetwork data planeで許可・拒否が実際に成立するところまでを一つの導入単位にします。

## Flow contract

| 要素 | 決めること | 証拠 |
|---|---|---|
| Source | Workload／namespace／zone identity、その属性の変更権限 | Inventory、label／identity owner、admission decision |
| Destination | Workload identity、管理境界、external destination | Selector、gateway／proxy route、destination owner |
| Direction | Ingress、egress、両方の責任 | Source policy、destination policy |
| Transport | Protocol、portまたはport range | Policy rule、listener inventory |
| Purpose | 何のために必要で、いつ廃止するか | Review、change、owner、期限 |
| Enforcement | CNI、host、gateway、proxy、meshのどこで止めるか | 対象version、coverage、live probe |
| Observation | Allow／deny／errorとdata plane health | Flow evidence、drop、collector health、probe result |

Flow観測から契約候補を作ることはできますが、観測されたという理由だけで必要な通信にはしません。Maintenance、起動時、障害時だけのflowも所有者と条件を確認します。

## Kubernetes NetworkPolicyでの配置

Core NetworkPolicyはPodに接続するL3／L4 flowを、Pod selector、namespace selector、IP block、protocol、portで表します。Policyに選択されていないPodはその方向についてnon-isolatedなので、各管理namespaceへ全Podを選択するingress・egress default denyを先に置きます。

Allow ruleは加算されます。狭いpolicy同士はdenyを上書きする優先順位を持たず、どれか一つのpolicyが許可すれば通信は許可されます。送信元と受信先の両方がisolatedの場合、source egressとdestination ingressの両方が同じconnectionを許可する必要があります。

Namespace名を指定する場合、control planeが付ける変更不能な`kubernetes.io/metadata.name` labelを使えます。Custom namespace labelやPod labelをidentityとして使う場合は、その値を変更できる主体を確認します。Selectorの一致は暗号学的なworkload identityではありません。

NetworkPolicy objectの作成とdata planeへの反映には時間差があり得ます。Default denyと基礎allowをworkloadより先に準備し、policy変更中の一時的な全許可を避けます。APIから反映完了時刻を直接知る方法はないため、live probeで確認します。

代表実装は[Kubernetes NetworkPolicy](implementations/kubernetes-networkpolicy/README.md)にあります。

## DNS・control plane・external egress

Default-deny egressはDNSも止めます。採用clusterのDNS実装、Pod label、NodeLocal DNS、IPv4／IPv6を確認し、必要なsourceから必要なresolverのTCP／UDP 53だけを許可します。DNSを許可しても、解決後の宛先やdomain identityは制限されません。

Kubernetes API、workload identity、telemetry、time、package repository等も、用途ごとに別flowとして扱います。管理面へ直接接続させる代わりに、専用proxyやbrokerを選ぶ方がauthorityと監査を狭められる場合があります。

Core NetworkPolicyはService名やFQDNを宛先identityにできず、NATの前後で`ipBlock`が見るaddressもnetwork implementationにより異なり得ます。External egressのdomain、TLS identity、固定出口、inspectionが必要なら、対応CNI、egress gateway、proxy等を選びます。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Kubernetes NetworkPolicy | Pod／namespaceとL3／L4 portで表せるflow。Portableな起点だが、明示deny、FQDN、Service名、拒否log、host trafficを一括して扱えない |
| CNI固有policy | Cluster-wide default、FQDN、identity、flow log等が必要な場合。CRD・version・data planeへの依存とmigration costが増える |
| Egress gateway／proxy | External destinationを固定出口、domain、TLS等で制御したい場合。Bypass防止、proxy availability、credential、非HTTP protocolを所有する |
| Service mesh | Service identity、mTLS、L7 routeが必要な場合。Pod networkの全経路を自動的に閉じるとは限らず、sidecar／ambientのcoverageを確認する |
| Cloud firewall／security group | Node、subnet、cloud resource境界を補う場合。Pod identityとの対応、NAT、cluster内flowの見え方がplatform依存になる |

一つの方式へ全責任を集約しません。Core policyでworkload間を閉じ、external egressはgateway、node経路はhost／cloud boundaryという組合せもあります。

## 導入順序

1. Workload、namespace、zone、外部destinationとidentityの変更権限をinventory化する。
2. 必要なflow contractをownerとreviewし、DNS等の基盤flowを分ける。
3. 使い捨て環境でdefault denyを先に置き、workloadを作成する。
4. Source egressとdestination ingressを別policyとして追加する。
5. 許可flowの成功後、片側のallowだけを外して拒否を確認し、source実行・destination生存を別に確認する。
6. Policy反映、plugin health、IPv4／IPv6、hostNetwork、node、NAT、external経路の限界を記録する。
7. 本番では観測から不要flowを削り、例外の期限と新namespaceのdefaultを継続確認する。

## 失敗経路

- Namespaceを作成してからdefault denyを追加し、反映までの間に全通信を許可する。
- Ingressだけを閉じ、侵害後のscan・C2・exfiltrationに使うegressを残す。
- `namespaceSelector`と`podSelector`を別配列要素にし、意図したANDではなくORとして広く許可する。
- 狭いpolicyと同時に`allow all`があり、狭い方が優先されると誤認する。
- Workload自身が変更できるlabelをnetwork identityとして信頼する。
- DNS許可をdomain allowlistと誤認する。
- NetworkPolicy objectの一覧をCNI enforcement evidenceにする。
- Timeout、Pod停止、route障害、collector停止をpolicyによる拒否として数える。

## このpatternの範囲

このpatternはL3／L4 reachabilityを扱います。TLS・service identity、application認証・認可、data encryption、[node／host network](../node-runtime-management-boundary/README.md)、帯域・connection exhaustion、network intrusion responseは別の責任です。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)
- [教材](../../../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/learning.md)
- [Workload privilege and host boundary](../workload-privilege-and-host-boundary/README.md)
- [Runtime detection to triage](../runtime-detection-to-triage/README.md)
- [参照資料と採否](../../../sources/README.md#ref-workload-network-segmentation-001)
