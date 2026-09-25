# Workload privilege confinement移行記録

旧`PSB-CONTAINER-001`から保留していたworkload confinementを、
[control](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)と
[pattern](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

## 分割判断

Application processの侵害後に、root、kernel機能、hostのnamespace・path・runtime API、書込み可能なroot filesystem、control-plane credentialへ進む経路は、一つの実効runtime profileとして判断する必要があります。Main containerだけでなくinit、sidecar、ephemeral、debugを同じ強制点で扱うため、旧`CNT-003..006`を一つの主題へまとめました。

Resourceとnetworkは同じPod設定に現れても、守る成果と実効性の証拠が異なります。CPU・memory・PID・storageのavailabilityにはrequest／limit、quota、scheduling、eviction、node capacity、runtime enforcementが関係します。Network segmentationにはCNI、workload identity、ingress／egress、DNS、service mesh、外部境界が関係します。この二つをconfinement profileへ詰め込まず、それぞれ独立した後続主題にします。

| 旧check | 新しい配置 | 判断 |
|---|---|---|
| `CNT-003` non-root・privileged・escalation | `WORKLOAD-CONFINE-1,2,7` | 全container経路の実効identityとfinal admissionへ拡張 |
| `CNT-004` capability | `WORKLOAD-CONFINE-3,7` | 既定で全dropし、対象OSで必要な追加だけを許可 |
| `CNT-005` host namespace・hostPath | `WORKLOAD-CONFINE-4,7` | Host process、device、port、runtime／node管理socketまで同じhost境界として扱う |
| `CNT-006` read-only root・seccomp | `WORKLOAD-CONFINE-3,5,7` | Syscall／MACとfilesystemを別の特性に分け、同じprofileで強制 |
| `CNT-007` CPU・memory・PID | `split-migrated` | [PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)へ分割し、quota、scheduling、eviction、runtime実効値を含めて再編集。詳細は[専用の移行記録](RESOURCE_CONSUMPTION_MIGRATION.md) |
| `CNT-008` default-deny network | `split-migrated` | [PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)へ分割し、CNI coverageと実効到達性を含めて再編集。詳細は[専用の移行記録](NETWORK_SEGMENTATION_MIGRATION.md) |
| `CNT-009` fail-closed admission | `PSB-CONTAINER-001`と`WORKLOAD-CONFINE-7` | Artifact identityとruntime authorityは別に判定するが、どちらも最終使用境界でfail closedにする |

`WORKLOAD-CONFINE-6`のcontrol-plane credentialは旧checkの直接移植ではありません。Kubernetesが既定でservice account credentialをPodへ渡し得るため、process侵害時のauthorityを制限する同じ問いへ追加したリポジトリでの解釈です。

## 具体化判断

この主題は、Kubernetesで使う主要な強制点と不足分が明確です。そのため文書だけで終えず、Kubernetes 1.37の[Pod Security Admission + CEL代表実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)を必要な成果物に選びました。

組込み`restricted` profileを`enforce` mode・`v1.37`固定で使い、そこに含まれないread-only root filesystemとservice account tokenの自動mount禁止だけをValidating Admission Policyで補います。IaC／CI検査は早いfeedbackであり、controller生成後のPod、直接作成、ephemeral containerを扱う最終強制点にはしません。

旧offline Python verifier、synthetic manifest、platform evidence、testsは非移植です。宣言同士の整合だけではlive API serverのpolicy、対象scope、failure semantics、runtime適用を証明しないためです。新実装には使い捨てcluster向けのserver-side dry-run手順と正常・拒否fixtureを置きましたが、このrepositoryからlive clusterへは接続しておらず拒否結果は未実行です。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.4.3` | `CNT-003..007 / mitigates / high` | この移行では`WORKLOAD-CONFINE-1..5,7 / supports / medium / design-reviewed`へ限定。その後resource allocationは`RESOURCE-1..3,5,7 / supports / medium / design-reviewed`として[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)で再評価。Credential特性へは割り当てない |
| NIST SP 800-190 `4.3.3` | `CNT-008 / mitigates / high` | この移行では非継承。その後`NET-SEG-1..3 / supports / medium / design-reviewed`として[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)で再評価 |
| NIST SP 800-190 `4.4.2` | `CNT-008 / mitigates / high` | この移行では非継承。その後`NET-SEG-1,2,4..7 / supports / medium / design-reviewed`としてPSB-CONTAINER-006で再評価 |

旧mappingの`high` confidenceと`mitigates`は、synthetic fixtureの成功や広いcheck割当を含んでいたため継承しません。現在のmappingは公式NIST本文と新特性を照合した設計関係であり、NIST準拠や組織への導入を示しません。

## 完了条件と残る範囲

- Controlの問い、直接の失敗、7特性、診断で確認する項目、隣接境界を読める。
- 教材からcontrol、pattern、Kubernetes代表実装へたどれる。
- Kubernetes 1.37の対象、変更箇所、使い捨てclusterでの確認、解除、制限を読める。
- NIST、Kubernetes資料の版・確認日・採否と、旧check・mappingの扱いを追跡できる。
- YAML、shell、repository構造は検査する。Live clusterの拒否とruntime stateは未確認として残す。
- Node／daemon hardeningは[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)、resource consumptionはPSB-CONTAINER-007、network segmentationはPSB-CONTAINER-006へ移行済み。IaC golden pathは別の移行候補として残す。
