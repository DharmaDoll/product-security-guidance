# Container / Cloud / IaC Security

インフラの変更、成果物の公開と使用、稼働中の権限と監視を分けて確認します。

| Control | 問うこと |
|---|---|
| [PSB-IAC-001 Infrastructure change authorization and drift](psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | レビューした変更案どおりに適用され、その後の意図しない変更を見つけられるか |
| [PSB-CONTAINER-001 Deployment artifact admission](psb-container-001-deployment-artifact-admission/README.md) | 起動するすべての成果物を使用直前に確かめ、受入条件に合わなければ止められるか |
| [PSB-CONTAINER-002 Container registry publication boundary](psb-container-002-container-registry-publication-boundary/README.md) | 許可した成果物だけを公開し、公開後の差替えや使用停止を管理できるか |
| [PSB-CONTAINER-003 Container host and daemon boundary](psb-container-003-container-host-daemon-boundary/README.md) | 一つのworkloadやnodeの侵害から、hostやcluster全体の管理権限へ進ませないか |
| [PSB-CONTAINER-004 Runtime threat detection](psb-container-004-runtime-threat-detection/README.md) | 稼働中の異常を対象のworkloadへ結び付け、監視できなかった状態と分けて担当者へ渡せるか |
| [PSB-CONTAINER-005 Workload privilege confinement](psb-container-005-workload-privilege-confinement/README.md) | Workloadが侵害されても、不要なhost・kernel・管理面の権限を使えないか |
| [PSB-CONTAINER-006 Workload network segmentation](psb-container-006-workload-network-segmentation/README.md) | Workloadが侵害されても、許可していない相手へ通信できないか |
| [PSB-CONTAINER-007 Workload resource consumption bounds](psb-container-007-workload-resource-consumption-bounds/README.md) | 一つのworkloadが故障・侵害されても、共有資源を使い尽くさないか |

具体的な判断は各controlから教材と設計パターンへ進めます。IaCとhost管理面は対象環境を決めていないため、実装例はありません。Workloadの権限、通信、資源制限にはKubernetesの実装例がありますが、実際のclusterで効くかは未確認です。

## 公開から稼働までを辿る

[Release Integrity](../release-integrity/README.md)は、完成した成果物のdigestと必要な署名・来歴・SBOMを結び、利用者の期待値で受け入れる境界です。Container imageでは、[CONTAINER-002の教材](psb-container-002-container-registry-publication-boundary/learning.md)で「registryに公開・保持した」と「使用してよい」を分け、[CONTAINER-001の教材](psb-container-001-deployment-artifact-admission/learning.md)で実行直前の全artifactを確認します。設計する際は[registryのpattern](../../../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)と[admissionのpattern](../../../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)へ進めます。

公開済みでも使用許可とは限らず、admissionが許可しても実際に稼働したdigestはまだ分かりません。稼働中の対象を観測し、旧digestが残らないかを確認する復旧判断は[GOV-005](../governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)へ渡します。OCI image indexと実行先が選んだmanifestは別のdigestを持つため、採用先でその対応を保ちます。

実行後のnode管理面と検知の違いは[CONTAINER-003の教材](psb-container-003-container-host-daemon-boundary/learning.md)と[CONTAINER-004の教材](psb-container-004-runtime-threat-detection/learning.md)から辿れます。
