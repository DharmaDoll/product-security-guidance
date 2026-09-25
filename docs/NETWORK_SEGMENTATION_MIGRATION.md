# Workload network segmentation移行記録

旧`PSB-CONTAINER-001 / CNT-008`を、
[control](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)と
[pattern](../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)へ分割移行しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

## 分割判断

Network reachabilityは、containerのUID、capability、filesystem等とは別の実効境界です。Process権限を小さくしても、侵害後のworkloadがneighbor、管理service、外部宛てへ接続できれば、lateral movement、command and control、exfiltrationは成立します。そのため[Workload privilege confinement](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)へ戻さず、一つのnetwork主題にしました。

旧`CNT-008`は「workloadを選択するdefault-deny ingress／egress」とCNI enforcement evidenceを要求していました。この成果は残しますが、default denyだけでは実際のapplication通信を設計できません。新controlではsource・destination identity、両側のallow、DNS等の基盤flow、異なるsensitivity zone・external egress、plugin coverage、live probeまでへ分解しました。

| 旧要素 | 新しい配置 | 判断 |
|---|---|---|
| Workloadを選ぶdefault deny | `NET-SEG-2` | 全管理workload・新namespace・両方向のdefaultへ拡張 |
| Ingress／egress allow | `NET-SEG-1,3` | Sourceとdestination双方のflow contractとして具体化 |
| CNI enforcement evidence | `NET-SEG-6,7` | Boolean fixtureを廃止し、許可追加・削除を伴うlive probeへ変更 |
| Network border／external egress | `NET-SEG-5` | Core policyで表せないFQDN・NAT等をgateway／proxy／対応CNIへ渡す |
| DNS・platform flow | `NET-SEG-4` | 広いfallbackにせず、採用環境で個別に列挙する |

## 具体化判断

Kubernetes core NetworkPolicyは技術経路が明確で、policy objectだけでは実効性を証明できないという重要な失敗があります。そのため[Kubernetes 1.37代表実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)を必要な成果物に選びました。

実装は三namespaceをingress・egressともdefault denyにし、`client -> api:8080/TCP`だけを両側から許可します。Source egressとdestination ingressについて、片側の一時allowを追加すると接続でき、削除すると拒否され、再追加で接続が戻ることをlive Pod間で確認します。これによりPod停止やCNI非対応を単純な「拒否成功」にしません。

DNS、external destination、dual stack、hostNetwork、node trafficはclusterごとの差が大きく、portableな安全値を一つのmanifestへ埋め込めません。代表実装の範囲外として明記し、patternで実装選択と確認方法を示します。

旧`secure/network-policy.json`、`insecure/network-policy.json`、`platform-evidence.json`、Python verifierは非移植です。旧verifierはselectorと空rule、`enforcement_available: true`という自己申告の整合を確認しても、CNI data planeの通信拒否を確認しないためです。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.3.3` | `CNT-008 / mitigates / high` | `NET-SEG-1..3 / supports / medium / design-reviewed`。Sensitivity levelとwell-defined interfaceによるinter-container separationとの設計関係 |
| NIST SP 800-190 `4.4.2` | `CNT-008 / mitigates / high` | `NET-SEG-1,2,4..7 / supports / medium / design-reviewed`。Egress border、app-aware filtering、flow・anomaly observationとの部分関係 |

旧`mitigates / high`はsynthetic fixtureとboolean platform evidenceを含むため継承しません。NISTはKubernetes selector、default deny object、CNI、FQDN、DNS ruleを規定しません。現在のmappingはNIST本文と新特性の設計関係であり、実導入やNIST準拠を示しません。

## 完了条件と残る範囲

- Controlの問い、直接の失敗、7特性、診断で確認する項目、隣接境界を読める。
- 教材からcontrol、pattern、Kubernetes代表実装へたどれる。
- Kubernetes 1.37とagnhost 2.66.1の対象、policy、live probe、cleanup、制限を読める。
- NISTとKubernetes資料の版・確認日・採否、旧check・mapping・実装の扱いを追跡できる。
- YAML、shell、repository構造は検査する。Live clusterでのCNI enforcementは未実行として残す。
- DNS、external egress、IPv6、host／node、cloud network、L7 identityは採用環境で別の具体実装を必要とする。
