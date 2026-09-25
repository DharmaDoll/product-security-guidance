# A compromised frontend should not inherit the whole network

[コントロール記録](README.md) ·
[設計パターン](../../../../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md) ·
[Kubernetes実装](../../../../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)

## シナリオ：Frontendでcode executionを奪われる

Internetからrequestを受けるfrontendが、backend APIの`8080/TCP`だけを呼ぶ構成を考えます。Frontendの入力処理に欠陥があり、攻撃者がcontainer内でcommandを実行できるようになりました。

Cluster内が既定で相互通信可能なら、攻撃者はbackend以外のPod、管理用service、metadata endpoint、Internet上のcommand-and-controlへ接続を試せます。Frontendのprocessをnon-rootにしても、network reachabilityは小さくなりません。

Frontendのegressをbackend APIのidentityとportに限定し、backendのingressもfrontend identityだけに限定すれば、片方のlabelやpolicyを誤っても反対側が通信を止められます。ただしselectorに使うlabelを攻撃者自身が付け替えられるなら、そのlabelは信頼できるidentityではありません。

## Default denyは入口にすぎない

Kubernetesでは、policyに選択されていないPodはその方向についてnon-isolatedです。全Podを選ぶdefault denyを最初に置き、必要なflowだけを別policyで加えます。

Allow policyは加算されます。狭いpolicyを追加しても、別の`allow all`を打ち消せません。また、sourceのegressとdestinationのingressは独立しており、Pod間通信には両側の許可が必要です。

## DNSを許可しても宛先を許可したことにはならない

Egressを既定拒否にするとDNSも止まります。名前解決が必要ならclusterのDNS経路を個別に許可します。ただしDNSへの53番portを許可することは、解決されたIPへの接続を許可することでも、許可したdomainだけへ接続を限定することでもありません。

Core NetworkPolicyはPod・namespace selector、IP block、L4 portを扱います。Service名、TLS identity、FQDN、強制egress gateway、拒否log等が必要なら、対応するCNI、gateway、proxy、service mesh等へ役割を渡します。

## YAMLの存在と通信の遮断を分ける

API serverは、network pluginがNetworkPolicyを実装していなくてもobjectを受理できます。YAMLのlintや`kubectl get networkpolicy`だけで「遮断できた」と判断してはいけません。

許可経路が接続できることを先に確認し、そのallowだけを外すと同じsource・destination間が遮断されることを試します。Plugin障害、Pod停止、DNS失敗を拒否成功として数えないため、sourceのexec経路とdestinationの生存も合わせて確認します。

## 振り返りで問うこと

- Frontendが実際に必要とする通信を、相手・方向・protocol・portで説明できるか。
- 現在観測できる通信を、必要性を判断せず全てallowへ変えていないか。
- 新しいnamespaceやselector外のPodが既定許可にならないか。
- Selectorに使うlabelを誰が変更できるか。
- DNS、control plane、telemetryの例外が全egressへ広がっていないか。
- NetworkPolicyの存在を、CNIによる実効的な遮断の証拠にしていないか。
- HostNetwork、node traffic、NAT、IPv6、FQDN等、core policyが扱わない経路を把握しているか。

この教材は[NIST SP 800-190とKubernetes資料の採否](../../../../sources/README.md#ref-workload-network-segmentation-001)を使ったリポジトリでの解釈です。個別clusterへの導入済み状態は示しません。
