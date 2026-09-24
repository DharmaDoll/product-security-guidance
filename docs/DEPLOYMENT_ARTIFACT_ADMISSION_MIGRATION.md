# Deployment artifact admission移行記録

旧`PSB-CONTAINER-001`を、artifact acceptanceから実行許可へのhandoffに絞った
[control](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と
[pattern](../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

## 分割判断

旧controlは次の三つを一つのverifierへ入れていました。

1. Exact OCI artifactとauthenticated provenanceのconsumer verification
2. Non-root、capability、host、filesystem、seccomp、resource、networkのworkload confinement
3. Create／update時のfail-closed admission enforcement

1と3は「現在受け入れているexact artifactだけを使用境界で実行する」という一つの失敗へ接続できます。
2は、artifactが正規でもapplicationが侵害された後の権限・到達範囲・resource impactを制限する別の成果です。
脅威、platform evidence、runtimeでの確認方法が異なるため、今回のcontrolから分離しました。

| 旧check | 新しい配置 | 判断 |
|---|---|---|
| `CNT-001` exact trusted OCI digest | `ARTIFACT-ADMIT-1`、`3` | 全artifactのexact identityとfinal state bindingへ拡張。Registry lifecycleは別主題 |
| `CNT-002` provenance binding | `ARTIFACT-ADMIT-2`、`3`、`5` | REL-001の直接実行または認証済みdecision receiptをexact digest・targetへ結合 |
| `CNT-009` fail-closed admission | `ARTIFACT-ADMIT-3..6` | 全経路、障害状態、policy identity、auditへ分解 |
| `CNT-003..006` privilege・host・filesystem・seccomp | 保留 | 将来のworkload confinement control／pattern候補 |
| `CNT-007` CPU・memory・PID | 保留 | Scheduling、quota、runtime enforcement、availability設計として再評価 |
| `CNT-008` default-deny network | 保留 | Network segmentationと実効CNI evidenceを含む別主題として再評価 |

## 具体化判断

製品非依存でも、artifact set、consumer decision、target、policy identity、decision状態、final-state enforcementからなるcontractは具体化できます。
Patternにはdirect verification、認証済みreceipt、declarative policy、external service、runtime enforcementの選択肢とKubernetes adapterの確認項目を示しました。

実行可能な実装は今回の必須成果物にしません。Deployment platform、cluster version、consumer verifier、registry、evidence transport、identity profileが未選定で、同じサンプルでは実際の強制を示せないためです。
採用先が決まった時点で、製品version、全API経路、final mutation state、fail-closed behavior、runtime digest observationまで確認できるadapterを追加します。

旧Python verifier、synthetic AdmissionReview、OCI manifest、provenance、signature、policy、platform evidence、testsは非移植です。
Offline object同士の整合は、live admission configuration、external dependency、runtimeの実効digestを証明しません。
Negative scenariosは実行済み結果ではなく診断観点として移しました。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| SLSA `1.2 / build-l2#consumer-validates-authenticity` | `CNT-002 / verifies / high` | `ARTIFACT-ADMIT-2,3,5 / supports / medium / design-reviewed`。REL-001のcurrent decisionを使用境界へ結ぶ設計関係 |
| SLSA `1.2 / build-provenance` | `CNT-002 / verifies / high` | `ARTIFACT-ADMIT-1,2,3 / supports / medium / design-reviewed`。Subjectとexact admitted digestの結合に限定 |
| NIST SP 800-190 `4.1.5` | `CNT-001,002,009 / supports / high` | `ARTIFACT-ADMIT-1..5 / supports / medium / design-reviewed`。Trusted image identity・signature validation・execution enforcementとの部分関係 |
| NIST SP 800-190 `4.4.5` | `CNT-001,002,009 / mitigates / high` | `ARTIFACT-ADMIT-4,5,6 / supports / medium / design-reviewed`。Baseline before run、identity、auditのうちartifact admission部分 |
| NIST SP 800-190 `4.4.3` | `CNT-003..007 / mitigates / high` | 非継承。Workload confinement主題へ保留 |
| NIST SP 800-190 `4.3.3`、`4.4.2` | `CNT-008 / mitigates / high` | 非継承。Network segmentation主題へ保留 |

NIST 4.4.5はdevelopment／test／productionの分離、RBAC、user identity、audit、vulnerability・compliance baselineも扱います。
今回のcontrolはその全体を満たしません。SLSAのproducer／platform要件、Build level達成、NIST SP 800-190全体の対応も主張しません。
