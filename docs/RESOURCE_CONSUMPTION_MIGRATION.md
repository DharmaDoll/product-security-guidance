# Workload resource consumption bounds移行記録

旧`PSB-CONTAINER-001 / CNT-007`を、
[control](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)と
[pattern](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)へ分割移行しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

## 分割判断

CPU／memory／PIDの枯渇はprocess privilegeやnetwork reachabilityとは異なる実効境界です。非rootかつnetwork分離されたworkloadでも、loop、fork、log、replica増加によって共有nodeや別tenantを停止できます。そのためCONTAINER-005やCONTAINER-006へ戻さず、resource consumptionを一つの主題にしました。

Workloadのrequest／limit、namespaceのaggregate quota、node allocatable・reservation・pressureは強制点が異なりますが、直接の失敗は「一workloadの消費が共有capacityへ広がること」です。個別controlへ分割すると受け渡しが読みにくくなるため、一つのcontrolの別特性として保持し、実装例のcoverageを限定します。

| 旧要素 | 新しい配置 | 判断 |
|---|---|---|
| CPU／memory request | `RESOURCE-1..4` | Scheduling、tenant合計、owner、peak時の意味へ拡張 |
| CPU／memory limit | `RESOURCE-1..3,7` | Throttle、OOM、runtime enforcement、resizeを区別 |
| PID maximum | `RESOURCE-2,5..7` | 固定値を非継承。Pod hard limit、node reservation、PID pressureを一組で扱う |
| Admission check | `RESOURCE-2,7` | Main containerだけでなくinit、controller生成、scale、resize、debug経路へ拡張 |
| Platform evidence | `RESOURCE-5..7` | Boolean自己申告を廃止し、node config、runtime state、pressure・event・collector healthへ変更 |
| Storage・object amplification | `RESOURCE-2,4..7` | 旧checkに不足していたlog、writable layer、`emptyDir`、inode、Pod／Job／PVC数を追加 |

## 具体化判断

KubernetesではResourceQuotaとValidating Admission Policyによる受入境界が明確です。そのため[Kubernetes 1.37代表実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)を必要な成果物に選びました。

実装はCPU、memory、ephemeral-storageの明示request／limitをregular・init containerへ要求し、ephemeral containerを拒否します。Namespaceのrequest／limit合計とPod・Job数をResourceQuotaで制限し、正常Podの作成、quota使用量、QoS、必須値不足、aggregate quota超過をlive APIで確認します。

PID limit、node reservation、pressure／eviction、cgroupの実効値はcluster providerとnode構成に依存します。架空のKubeletConfigurationや自己申告fixtureを`PASS`にせず、代表実装の非対応範囲として残しました。旧`1000m`、`512Mi`、PID `256`は普遍的な安全値ではないため非継承です。

旧`secure/policy.json`、`platform-evidence.json`、AdmissionReview fixture、Python verifierは非移植です。旧verifierは限られたquantity形式と固定上限を検査し、`pids_limit_enforced: true`という自己申告を実効runtime証拠としていたためです。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.4.3` | `CNT-003..007 / mitigates / high` | `RESOURCE-1..3,5,7 / supports / medium / design-reviewed`。Resource allocation、runtime configurationの継続的強制との部分関係。Namespace quota、Kubernetes resize、node pressureの規定とは扱わない |

旧`mitigates / high`はsynthetic fixture、固定値、PID自己申告を含むため継承しません。NIST本文のresource allocationとruntime configurationを設計根拠にし、Kubernetes固有のResourceQuota、CEL、request／limit semantics、evictionをNIST要件へ変換しません。

## 完了条件と残る範囲

- Controlの問い、直接の失敗、7特性、診断で確認する項目、隣接境界を読める。
- 教材からcontrol、pattern、Kubernetes代表実装へたどれる。
- Kubernetes 1.37の対象、namespace budget、admission、live API確認、cleanup、制限を読める。
- NISTとKubernetes資料の版・確認日・採否、旧check・mapping・実装の扱いを追跡できる。
- YAML、shell、repository構造は検査する。Live clusterでのadmission・quota・runtimeは未実行として残す。
- PID、node reservation、pressure／eviction、cgroup、capacity、provider固有実装は採用環境で別の具体化を必要とする。
