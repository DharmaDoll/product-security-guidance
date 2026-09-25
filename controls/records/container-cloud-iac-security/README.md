# Container / Cloud / IaC Security

実行前の設定と許可、hostの境界、実行後の観測を分けて判断します。

| Control | 問うこと |
|---|---|
| [PSB-IAC-001 Infrastructure change authorization and drift](psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | Reviewしたsource・依存、resolved plan、許可されたapply、provider上の現在状態を同じ変更として追跡できるか |
| [PSB-CONTAINER-001 Deployment artifact admission](psb-container-001-deployment-artifact-admission/README.md) | 実行する全artifactを現在のconsumer acceptanceへ結び、全経路でfail closedにできるか |
| [PSB-CONTAINER-002 Container registry publication boundary](psb-container-002-container-registry-publication-boundary/README.md) | 公開権限、digest identity、変更防止、audit、withdrawalをregistryで維持できるか |
| [PSB-CONTAINER-003 Container host and daemon boundary](psb-container-003-container-host-daemon-boundary/README.md) | Workload・operator・node identityからruntime・kubelet・host管理面への権限を制限し、侵害nodeを信頼から外せるか |
| [PSB-CONTAINER-004 Runtime threat detection](psb-container-004-runtime-threat-detection/README.md) | どのworkloadの行動を観測し、観測障害と検知を区別して担当者へ渡せるか |
| [PSB-CONTAINER-005 Workload privilege confinement](psb-container-005-workload-privilege-confinement/README.md) | Workloadが侵害されても不要なkernel・host・filesystem・control-plane authorityへ進めないか |
| [PSB-CONTAINER-006 Workload network segmentation](psb-container-006-workload-network-segmentation/README.md) | Workloadが侵害されても明示した相手・方向・protocol・port以外へ通信できず、その強制を実通信で確認できるか |
| [PSB-CONTAINER-007 Workload resource consumption bounds](psb-container-007-workload-resource-consumption-bounds/README.md) | 故障・侵害されたworkloadの資源消費をreview済みbudget内へ制限し、共有capacityの枯渇を防げるか |

IaCはsourceからplan、apply、provider上の現在状態までの境界をcontrol・教材・patternへ移行しました。対象providerとresourceを選ばない合成実装は作っていません。Host／daemonも対象platform未選定のため実装はありません。Workload confinement、network segmentation、resource consumptionにはKubernetesの代表実装がありますが、live clusterでは未確認です。
