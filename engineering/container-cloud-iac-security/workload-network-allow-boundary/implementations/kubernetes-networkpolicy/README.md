# Kubernetes NetworkPolicy implementation

Kubernetes 1.37のcore `networking.k8s.io/v1` NetworkPolicyで、三つの使い捨てnamespaceをingress・egressとも既定拒否にし、`client -> api:8080/TCP`だけを両側から許可する実装です。

`verify.sh`はYAMLの形を見るだけではありません。許可を一時的に追加・削除し、同じPod間の接続が成功から拒否へ変わることを確認します。これによりsource egressとdestination ingressを別々に試し、NetworkPolicyを受理するだけで強制しないnetwork pluginを失敗として扱います。

これは[PSB-CONTAINER-006](../../../../../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)の限定した代表実装です。DNS、外部egress、hostNetwork、node traffic、L7 identityは扱いません。

## 対象と前提

- Kubernetes `1.37.x`
- `kubectl` `1.37.x`またはversion skew policy内のclient
- `networking.k8s.io/v1` NetworkPolicyを実際に強制するCNI／network plugin
- Linux PodとIPv4 Pod address
- `registry.k8s.io/e2e-test-images/agnhost:2.66.1`を取得できるtest cluster、またはreview済みmirrorへの置換
- 三つの使い捨てnamespaceを作成・削除できる権限

`agnhost:2.66.1`はKubernetes `v1.37.0` source treeがE2E testに指定する版です。この例ではtest用image tagとして固定しています。長期利用やair-gapped環境では、取得したmulti-architecture manifest digestを確認して組織のregistryへmirrorし、`workloads.yaml`をそのexact digestへ置き換えます。

## 通信契約

| Source | Destination | Port | Base state |
|---|---|---:|---|
| `psb-net-client/client` | `psb-net-server/api` | TCP 8080 | Source egressとdestination ingressの両方で許可 |
| `psb-net-client/client` | `psb-net-server/other` | TCP 8080 | Destination ingressだけ許可し、source egressで拒否 |
| `psb-net-untrusted/untrusted` | `psb-net-server/api` | TCP 8080 | Source egressだけ許可し、destination ingressで拒否 |

Probeでは拒否側のallowを一時追加して接続成功を確認し、そのpolicyだけを削除して遮断を確認します。Pod停止や`kubectl exec`障害を拒否成功として数えないため、source containerへのexec healthも確認します。

## ファイル

| ファイル | 役割 |
|---|---|
| `namespaces.yaml` | 固定名の使い捨てnamespaceとPod Security `restricted:v1.37` |
| `default-deny.yaml` | 各namespaceの全Podをingress・egressとも既定拒否 |
| `workloads.yaml` | 一つのclient、一つのuntrusted client、二つのHTTP server |
| `allow.yaml` | Base stateのsource egressとdestination ingress |
| `probe-allow-client-other-egress.yaml` | Source egressの成功・削除後拒否を試す一時policy |
| `probe-allow-untrusted-api-ingress.yaml` | Destination ingressの成功・削除後拒否を試す一時policy |
| `verify.sh` | Policy適用、live probe、再許可、cleanup |

## 使い捨てclusterで試す

現在のcontextが破棄可能なtest clusterであり、NetworkPolicyを強制するpluginが入っていることを確認します。固定namespaceが既に存在する場合、scriptは削除せず停止します。

```bash
kubectl config current-context
PSB_TEST_CONTEXT=YOUR-DISPOSABLE-CONTEXT ./verify.sh
```

成功時の主な出力は次のとおりです。

```text
PASS authorized client to api flow allowed
PASS client egress removal denied client to other
PASS api ingress removal denied untrusted to api
PASS authorized client to api flow remained allowed
```

ProbeはPod IPへ直接接続するためDNS allowを必要としません。終了時には三つのnamespaceを削除します。Server-side dry runではなく実Pod間通信を行うため、image pullとcluster networkを使用します。

## 採用先へ持ち込む

1. Namespace、workload、sensitivity zone、DNS／control plane／telemetry／external destinationの必要flowを先にreviewする。
2. 採用したCNIとversionが、NetworkPolicy、対象protocol、IPv4／IPv6、hostNetwork等をどう扱うか確認する。
3. `default-deny.yaml`相当を新しい管理namespaceの作成時に先行適用する仕組みを用意する。
4. `allow.yaml`のようにsource egressとdestination ingressを別々に記述し、namespaceは変更不能な`kubernetes.io/metadata.name`、Podは変更権限を管理したlabelで選ぶ。
5. DNS等の基盤flowを採用clusterの実装に合わせて追加する。広い`namespaceSelector: {}`や全egressで代用しない。
6. 許可flowの成功、各片側allowの削除後拒否、別identity・別port・外部宛てをlive probeする。
7. Policy反映時間、CNI health、flow log、例外、selector変更を継続して確認する。

このsampleのnamespace名やlabelを置き換えるだけでは、実際の通信契約やlabel変更権限を確認できません。

## 解除

使い捨て確認は`verify.sh`が自動でnamespaceごと削除します。採用先では、default denyを先に外すと全通信が既定許可へ戻り得ます。Workload停止または承認済みの代替境界を用意し、allow policy、workload、最後にnamespace baselineの順で影響を確認します。

## 制限

- このrepositoryにはlive Kubernetes clusterと`kubectl`がなく、Pod間probeは未実行です。
- Core NetworkPolicyはallow ruleの加算modelで、明示deny、優先順位、FQDN、Service名、TLS identity、強制gateway、拒否logを提供しません。
- NodeからPodへのtraffic、Pod自身、hostNetwork Pod、localhost、NetworkPolicy外protocolの扱いには制限またはplugin差があります。
- Service、load balancer、NAT、`ipBlock`の評価順はnetwork implementationにより異なり得ます。
- TestはIPv4 Pod IPとTCP 8080だけを確認します。UDP、SCTP、ICMP、IPv6、dual stackは別途必要です。
- DNS allowを含めていません。CoreDNS、NodeLocal DNS、custom resolverのidentityとaddressを採用clusterで確認します。
- Network reachabilityの制限は、通信相手の認証、request認可、暗号化、applicationの安全性を保証しません。
