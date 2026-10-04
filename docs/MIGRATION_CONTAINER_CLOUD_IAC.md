# Container / Cloud / IaC Security — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [Container host and daemon boundary移行記録](#container-host-daemon-migration)
- [Container registry publication boundary移行記録](#container-registry-migration)
- [Deployment artifact admission移行記録](#deployment-artifact-admission-migration)
- [PSB-IAC-001 Infrastructure change boundary 移行記録](#iac-change-boundary-migration)
- [Workload network segmentation移行記録](#network-segmentation-migration)
- [Workload resource consumption bounds移行記録](#resource-consumption-migration)
- [Workload privilege confinement移行記録](#workload-confinement-migration)

<a id="container-host-daemon-migration"></a>

<a id="container-host-daemon-migration--container-host-and-daemon-boundary移行記録"></a>
## Container host and daemon boundary移行記録

旧[PSB-CONTAINER-003](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-host-daemon-hardening)を、
[control](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)と
[pattern](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

<a id="container-host-daemon-migration--境界の見直し"></a>
### 境界の見直し

旧controlはhost OS、kernel、runtime socket、operator、audit、hardware trustを一つの主題にしていました。この主題は維持します。直接の失敗は、個々のhardening項目の不足ではなく「workload、local process、operator、node credentialがruntime・kubelet・host TCBを制御し、workload policyを迂回して一nodeの侵害をclusterへ広げること」です。

Workload manifestのnon-root、capability、hostPath、seccomp等は[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)へ既に分離しています。CONTAINER-003はhost側が提供・強制するruntime、kernel、node agent、management surface、node identityとlifecycleを扱います。Runtime sensorのevent評価は[PSB-CONTAINER-004](../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)へ残し、sensorを動かすnode権限・互換性・保護をこの主題から渡します。

<a id="container-host-daemon-migration--旧項目の扱い"></a>
### 旧項目の扱い

| 旧項目 | 新しい配置 | 判断 |
|---|---|---|
| `HST-001` dedicated minimal host | `HOST-1` | 「desktopやdatabase禁止」の固定listではなく、pool purpose、sensitivity、component・service inventoryへ変更 |
| `HST-002` supported／patched stack | `HOST-1,2,8` | OS／kernel／runtimeだけでなくshim、node agent、root権限plugin、更新失敗、node replacementを含める |
| `HST-003` daemon endpoint／socket | `HOST-3,7` | Docker daemonだけでなくruntime、NRI、kubelet、debug、metricsとworkload mount、操作権限を扱う |
| `HST-004` rootless／user namespace／lockdown | `HOST-6,8` | 全platformへの一律必須をやめ、threatとplatform supportに応じた隔離とsilent fallback拒否へ変更 |
| `HST-005` protected paths | `HOST-4,8` | 固定path・mode・digestから、image／変更経路、plugin、static workload、credential、symlink・mountを含む契約へ変更 |
| `HST-006` seccomp／LSM／module | `HOST-6,8` | Workload profileの内容はCONTAINER-005、hostが提供する実効状態とfallbackはCONTAINER-003に分離 |
| `HST-007` operator／network／audit | `HOST-3,7,8` | Exact identity、action、source、duration、approval、break-glass、runtime socketによるaudit迂回へ拡張 |
| `HST-008` boot／TPM／attestation | `HOST-5,8` | 全nodeの必須checkから、riskとprovider capabilityに応じてnode参加条件へ使う選択肢へ変更 |
| `HST-009` evidence health | `HOST-8` | `PASS`等の共通verifier状態ではなく、node coverage、freshness、権限、欠測を各判断へ結ぶ |

<a id="container-host-daemon-migration--具体化判断"></a>
### 具体化判断

この主題ではprovider-neutralなcontrolとpatternを必要な成果物に選び、具体実装は追加しません。

Secret scanはGit objectとscannerの接続が対象repository上で閉じ、代表実装の入力・拒否・確認を再現できます。Kubernetes workload admission、NetworkPolicy、ResourceQuotaも使い捨てclusterに限定したYAMLとlive probeを示せます。一方、host／daemonはOS distribution、runtime、Kubernetes distribution、managed／self-managed、node image build、identity、network、attestationによって変更箇所と観測方法が変わります。

旧`secure/host-evidence.json`、`policy.json`、`exceptions.json`、Python verifierは移植しません。これらは固定した自己申告値を比較し、live host、socket、listener、runtime process、node credential、patch service、audit、TPMを観測していませんでした。Synthetic fixtureの9件`PASS`を実効的なhost implementationに見せる問題があるためです。

実装を検討する条件は、対象OS image、kernel、runtime、node agent、plugin、provider責任分界、変更する設定、使い捨てnode pool、更新・隔離・rollback、取得可能なlive evidenceを一組で選び、導入・確認への実効性を説明できることです。選ぶ場合は、containerd self-managed、Docker rootless、managed Kubernetes node pool等の限定名で`implementations/`へ置きます。設定ガイドと診断項目で十分な場合は追加しません。

<a id="container-host-daemon-migration--参照資料の再評価"></a>
### 参照資料の再評価

- NIST SP 800-190 `4.3.1`、`4.3.5`、`4.5.1`〜`4.5.5`、`4.6`を2026-09-25に公式PDFで再照合しました。旧`mitigates / high`はlive enforcementを示していないため、`supports / medium / design-reviewed`へ縮小します。
- Kubernetes 1.37のkubelet authentication／authorization、API server bypass risks、Node authorization／NodeRestriction、security checklistをnode管理面の具体的な設計入力にしました。Kubernetesをcontrol要件にはしません。
- `containerd/containerd@82f33ce76db81e47393be1cbdb6eba3343687fc5`のOperator Security Guidelinesを、socket、protected path、plugin、debug／metrics、patch範囲の実装候補に使います。特定file modeを他runtimeへ普遍化しません。
- Docker公式のdaemon socket保護とrootless modeは方式比較に使います。Remote daemonやrootlessを全nodeへ必須化しません。
- 旧CIS Docker Benchmark候補は、認可された固定版とrecommendation inventoryのreviewがないため引き続きmappingしません。

<a id="container-host-daemon-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 新判断 |
|---|---|
| NIST `4.3.1` | `HOST-3,7 / supports / medium`。Runtime・node管理surfaceの権限を限定するが、orchestrator全体のadmin accessは扱わない |
| NIST `4.3.5` | `HOST-5,8 / supports / medium`。Node identity、enrollment、isolation、removalを扱うが、cluster全体のresilienceや相互通信は実装していない |
| NIST `4.5.1` | `HOST-1,2 / supports / medium`。Purposeを絞ったnodeとcomponent lifecycleを設計するが、live service inventoryは未確認 |
| NIST `4.5.2` | `HOST-1,6 / supports / medium`。Sensitivityによるpoolとshared-kernel isolationを設計するが、配置・sandboxは未実装 |
| NIST `4.5.3` | `HOST-2,8 / supports / medium`。Support・更新・再作成と実効version evidenceを扱うが、vendor feedとlive nodeは未接続 |
| NIST `4.5.4` | `HOST-7,8 / supports / medium`。Host管理identity、privileged operation、auditを扱うが、実login・sudo・sessionは未確認 |
| NIST `4.5.5` | `HOST-4,8 / supports / medium`。Protected stateとdriftを扱うが、live filesystem・mountは未確認 |
| NIST `4.6` | `HOST-5,8 / supports / medium`。Boot／attestationを選択可能なnode trust入力にするが、TPMやcloud attestationは未実装 |

<a id="container-host-daemon-migration--完了条件と残る範囲"></a>
### 完了条件と残る範囲

- Controlの問い、直接の失敗、8特性、診断で確認する項目、workload・runtime detectionとの境界を読める。
- 教材からruntime socket、kubelet、static Pod、node identityによるAPI迂回を理解し、controlとpatternへたどれる。
- Patternからnode trust contract、方式、導入順序、失敗経路、実装開始条件を判断できる。
- 旧9 checks、synthetic verifier、8 framework関係、参照資料の採否を追跡できる。
- Live host、node pool、runtime、kubelet、credential、audit、attestationは未検証であり、実装・導入済みとは扱わない。

<a id="container-registry-migration"></a>

<a id="container-registry-migration--container-registry-publication-boundary移行記録"></a>
## Container registry publication boundary移行記録

旧`PSB-CONTAINER-002`の7 checkを、[control](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)の`REGISTRY-1..7`と
[pattern](../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

Transport、repository／action authority、short-lived publisher、release immutability、audit、lifecycle、evidence healthはregistryがartifactを保管・配布する境界として保持しました。
Build、signing、provenance、scanning、consumer verification、admission、runtimeは隣接成果物へ分離しています。

旧policy・identity・operation・audit・inventory JSON、Python verifier、testsは非移植です。Synthetic recordの整合はlive registryの実効権限、mutation拒否、collector完全性、replica・cacheを証明しません。問題のある操作や異常は確認項目として保持しました。

<a id="container-registry-migration--具体化判断"></a>
### 具体化判断

Exact endpoint、repository／action scope、digest immutability、audit、lifecycleという技術構造はpatternへ具体化しました。
Provider、edition、API、identity、event schema、retentionが未選定なので実装例は作りません。2026-09-28の読み合わせで、公開・保持・使用可能性を分け、`deprecated`の一律拒否を外しました。[教材](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/learning.md)でこの違いを説明しています。採用先が定まり、導入・確認に実効性がある場合に限り、live APIと無害な拒否試験を行える限定実装を検討します。設定ガイドと診断項目で足りる場合は実装しません。

<a id="container-registry-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.2.1` | `REG-001 / mitigates / high` | `REGISTRY-1 / supports / medium / design-reviewed`。Exact endpointと保護通信の設計関係。Live transportは未確認 |
| NIST SP 800-190 `4.2.2` | `REG-006 / mitigates / high` | `REGISTRY-6,7 / supports / medium / design-reviewed`。Stale state、deadline、deployability、evidence healthとの部分関係 |
| NIST SP 800-190 `4.2.3` | `REG-002..005 / mitigates / high` | `REGISTRY-2..5,7 / supports / medium / design-reviewed`。Authn／authz、publisher identity、mutation protection、auditとの設計関係 |

NIST本文は特定providerの短命federation、state名、期限、tag protection APIを規定しません。これらは旧controlと攻撃経路を再評価したrepository interpretationです。NIST SP 800-190全体の対応や組織導入を主張しません。

<a id="deployment-artifact-admission-migration"></a>

<a id="deployment-artifact-admission-migration--deployment-artifact-admission移行記録"></a>
## Deployment artifact admission移行記録

旧`PSB-CONTAINER-001`を、artifact acceptanceから実行許可へのhandoffに絞った
[control](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と
[pattern](../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

<a id="deployment-artifact-admission-migration--分割判断"></a>
### 分割判断

旧controlは次の三つを一つのverifierへ入れていました。

1. Exact OCI artifactとauthenticated provenanceのconsumer verification
2. Non-root、capability、host、filesystem、seccomp、resource、networkによるworkloadの権限・到達範囲・availability制限
3. Create／update時のfail-closed admission enforcement

1と3は「現在受け入れているexact artifactだけを使用境界で実行する」という一つの失敗へ接続できます。
2は、artifactが正規でもapplicationが侵害された後の権限・到達範囲・resource impactを制限する別の成果です。
脅威、platform evidence、runtimeでの確認方法が異なるため、今回のcontrolから分離しました。

| 旧check | 新しい配置 | 判断 |
|---|---|---|
| `CNT-001` exact trusted OCI digest | `ARTIFACT-ADMIT-1`、`3` | 全artifactのexact identityとfinal state bindingへ拡張。Registry lifecycleは別主題 |
| `CNT-002` provenance binding | `ARTIFACT-ADMIT-2`、`3`、`5` | REL-001の直接実行または認証済みdecision receiptをexact digest・targetへ結合 |
| `CNT-009` fail-closed admission | `ARTIFACT-ADMIT-3..6` | 全経路、障害状態、policy identity、auditへ分解 |
| `CNT-003..006` privilege・host・filesystem・seccomp | [PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md) | Workload privilege confinementへ分割移行。詳細は[専用の移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#workload-confinement-migration) |
| `CNT-007` CPU・memory・PID | [PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md) | Workload budget、namespace quota、node capacity・pressure、runtime evidenceを含む別主題として分割移行 |
| `CNT-008` default-deny network | [PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) | Network segmentation、両端のallow、実効CNI evidenceを含む別主題として分割移行 |

<a id="deployment-artifact-admission-migration--具体化判断"></a>
### 具体化判断

製品非依存でも、artifact set、consumer decision、target、policy identity、decision状態、final-state enforcementからなるcontractは具体化できます。
Patternにはdirect verification、認証済みreceipt、declarative policy、external service、runtime enforcementの選択肢とKubernetes adapterの確認項目を示しました。

実行可能な実装は今回の必須成果物にしません。Deployment platform、cluster version、consumer verifier、registry、evidence transport、identity profileが未選定で、同じサンプルでは実際の強制を示せないためです。
2026-09-28の読み合わせで、OCI image indexと実行先で選ばれるmanifestの対応、registryの使用停止判断をadmissionへ渡す条件を補い、[教材](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/learning.md)を追加しました。採用先が決まり、導入・確認に実効性がある場合に限り、製品version、全API経路、final mutation state、失敗時の拒否、runtime identityの照合を確認できる限定実装を検討します。文書と診断項目で足りる場合は追加しません。

旧Python verifier、synthetic AdmissionReview、OCI manifest、provenance、signature、policy、platform evidence、testsは非移植です。
Offline object同士の整合は、live admission configuration、external dependency、runtimeの実効digestを証明しません。
問題のある操作や異常は、実行済み結果ではなく確認項目として移しました。

<a id="deployment-artifact-admission-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| SLSA `1.2 / build-l2#consumer-validates-authenticity` | `CNT-002 / verifies / high` | `ARTIFACT-ADMIT-2,3,5 / supports / medium / design-reviewed`。REL-001のcurrent decisionを使用境界へ結ぶ設計関係 |
| SLSA `1.2 / build-provenance` | `CNT-002 / verifies / high` | `ARTIFACT-ADMIT-1,2,3 / supports / medium / design-reviewed`。Subjectとexact admitted digestの結合に限定 |
| NIST SP 800-190 `4.1.5` | `CNT-001,002,009 / supports / high` | `ARTIFACT-ADMIT-1..5 / supports / medium / design-reviewed`。Trusted image identity・signature validation・execution enforcementとの部分関係 |
| NIST SP 800-190 `4.4.5` | `CNT-001,002,009 / mitigates / high` | `ARTIFACT-ADMIT-4,5,6 / supports / medium / design-reviewed`。Baseline before run、identity、auditのうちartifact admission部分 |
| NIST SP 800-190 `4.4.3` | `CNT-003..007 / mitigates / high` | CONTAINER-005の`WORKLOAD-CONFINE-1..5,7`とCONTAINER-007の`RESOURCE-1..3,5,7`へ、それぞれ`supports / medium / design-reviewed`として再評価 |
| NIST SP 800-190 `4.3.3`、`4.4.2` | `CNT-008 / mitigates / high` | PSB-CONTAINER-006で`supports / medium / design-reviewed`として再評価。実効CNIや外部egressの導入証拠にはしない |

NIST 4.4.5はdevelopment／test／productionの分離、RBAC、user identity、audit、vulnerability・compliance baselineも扱います。
今回のcontrolはその全体を満たしません。SLSAのproducer／platform要件、Build level達成、NIST SP 800-190全体の対応も主張しません。

<a id="iac-change-boundary-migration"></a>

<a id="iac-change-boundary-migration--psb-iac-001-infrastructure-change-boundary-移行記録"></a>
## PSB-IAC-001 Infrastructure change boundary 移行記録

<a id="iac-change-boundary-migration--結論"></a>
### 結論

旧`PSB-IAC-001 Secure IaC Golden Path`は、標準moduleやCI templateを配る考え方と、plan・apply・provider状態を強制する境界を一つにしていました。移行後は`PSB-IAC-001 Infrastructure change authorization and drift boundary`として、reviewしたsource・依存、resolved plan、policy判断、apply authority、provider上の現在状態を同じ変更として結ぶ8特性へ再編集しました。

Golden Pathは捨てず、[設計pattern](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)の「安全な変更を作りやすくする入口」として位置付けます。標準moduleの利用を、resource固有要件への合格や実環境の安全性と同一視しません。

<a id="iac-change-boundary-migration--移行元"></a>
### 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/control.yaml)
- [ユーザー提供原文](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/docs/user-supplied-golden-path-guideline-ja.md)

<a id="iac-change-boundary-migration--旧12項目の扱い"></a>
### 旧12項目の扱い

| 旧項目 | 移行先 | 判断 |
|---|---|---|
| `IAC-001` module version／integrity | `IAC-CHANGE-1` | 採用。ただしTerraform provider lockとremote module versionを分け、存在しない共通`sha256` contractを要求しない |
| `IAC-002` multi-cloud compute defaults | `IAC-CHANGE-2`とpattern | 変更して採用。暗号化、network、image等はresource・provider固有controlの入力。AWS／GCP／Azureを一つのfixtureで通すことを要件にしない |
| `IAC-003` private administration／IAM | `IAC-CHANGE-2`と隣接control | 変更して採用。Infrastructure変更経路と、作成するresourceの管理面要件を分ける |
| `IAC-004` resolved plan gate | `IAC-CHANGE-2` | 採用。Source textやmodule名ではなくcreate／update／delete／replaceと値を評価する |
| `IAC-005` fail closed | `IAC-CHANGE-3` | 採用。Unknown、unsupported、error、対象漏れ、人の判断を別状態にする |
| `IAC-006` reusable CI composition | 非継承 | Secret、SCA、SBOM、署名、container scan等をIaC controlの必須一覧に複製していた。各controlとCI patternの責任へ戻す |
| `IAC-007` deploy identity | `IAC-CHANGE-5`とPSB-CICD-006 | 境界だけ採用。OIDC claim、token発行・交換はCICD-006、targetとapply操作の限定はIAC-001が扱う。固定15分を普遍値にしない |
| `IAC-008` provider enforcement | `IAC-CHANGE-6` | 採用。特定hookのcreate／update対応を`all-provisioning-paths`と自己申告する方式は廃止 |
| `IAC-009` runtime drift | `IAC-CHANGE-7` | 採用。固定24時間を外し、provider inventory、実resource、collection health、未管理resourceまで判断する |
| `IAC-010` automatic remediation | `IAC-CHANGE-8` | 採用。安全なaction名の自己申告ではなく、新しいplan、impact、rollback、証拠保全を求める |
| `IAC-011` exceptions | `IAC-CHANGE-8` | 採用。Resource・rule・owner・理由・期限・影響を結ぶ |
| `IAC-012` plan artifact | `IAC-CHANGE-4` | 採用。Hashとretentionだけでなく、review・targetとの結合、read／write、機微値、差替え、廃棄を扱う |

<a id="iac-change-boundary-migration--旧実装を移さない理由"></a>
### 旧実装を移さない理由

旧`verify.py`はTerraform、OPA、cloud providerを実行せず、用意した`golden-path-policy.json`と`tfplan.json`のfieldを比較していました。例えば次の内容は、実システムを観測した結果ではなくfixture内の自己申告でした。

- `providers`がAWS／GCP／Azureの三つである。
- `coverage`が`all-provisioning-paths`である。
- Driftを24時間以内に検査した。
- OIDC、provider policy、例外、remediation、plan artifactが期待文字列を持つ。
- Reusable workflowが他controlを`implemented`として列挙する。

これはpolicy metadataのschema testにはできますが、module解決、provider lock、実planのunknown、plan差替え、apply authority、provider側の拒否、actual state、driftを証明しません。`secure` fixtureが12項目を通ることを「実装」と読める構成だったため、script、secure／insecure JSON、固定値、旧Make targetを移植しません。

TerraformとOPAを使うだけのdemoも今回は作りません。Providerとresourceを選ばないplanでは、security invariantとapply後の実効値を確認できず、旧fixtureの表現を変えるだけになるためです。[Patternの開始条件](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md#実装を作る開始条件)を満たす限定実装を今後作ります。

<a id="iac-change-boundary-migration--参照資料の扱い"></a>
### 参照資料の扱い

2026-07-28のユーザー提供guidanceは正式な組織policyや外部標準ではありません。新しい主題別の参照記録`REF-IAC-CHANGE-BOUNDARY-001`で、Golden Path、resolved plan policy、provider hook、driftという論点の出発点として保持します。

外部資料へのリンクやmulti-cloudの例は、提供文書に記載された事実として扱い、個々の製品挙動を確認済みとはしません。今回、HashiCorp Terraformのplan、dependency lock、refresh-onlyとOPAのTerraform plan limitationを公式文書で2026-09-25に再確認しました。

<a id="iac-change-boundary-migration--旧framework-mapping"></a>
### 旧framework mapping

旧5関係は移行後の特性へ継承しません。

| 旧関係 | 判断 |
|---|---|
| OpenSSF OSPS `OSPS-QA-03.01` | Primary branchのautomated status checkをpassまたはmanual bypassする要件。Planとapplyの同一性、provider状態は規定しない |
| OpenSSF OSPS `OSPS-QA-04.02` | 複数source repositoryからなるreleaseで同等以上のsecurity requirementを求める要件。IaC resource変更の境界ではない |
| OpenSSF OSPS `OSPS-AC-04.01` | 旧registry titleはCI/CD least privilegeだが、2026.02.19版の詳細関係はCI control側で扱う。Apply targetとplan bindingへの直接要件として重複追加しない |
| NIST SSDF `PW.6.1` | 実行形式の安全性を改善するbuild toolの利用を扱う。Infrastructure plan・apply・driftへの直接要件ではない |
| GitHub Secure use reference `GHSC-SECURE-BUILDS` | Product guidanceとしてCI設計の入力にはなるが、IaC controlのframework requirementではない |

OpenSSF、SSDF、GitHub資料を否定する判断ではありません。意味が一致する別controlで管理し、旧件数を維持するための間接mappingを作らない判断です。

<a id="iac-change-boundary-migration--完了範囲と残る作業"></a>
### 完了範囲と残る作業

完了したものは、8特性のcontrol、具体的な失敗から始まる教材、sourceからactual stateまでのpattern、診断観点、参照資料記録、成果物mapping、横断分析です。

2026-09-29の読み合わせでは、Terraformの保存plan指定が追加の対話承認なしに実行されることと、途中失敗を自動rollbackしないことを[公式apply仕様](https://developer.hashicorp.com/terraform/cli/commands/apply)で確認しました。承認記録をplan・targetへ結ぶ責任と、失敗後に一部変更を確認する責任をcontrol・教材・patternへ戻しました。新しい実装例・テストコードは追加しません。

未実施なのは、実IaC tool、provider、resource、policy engine、cloud sandbox、identity、plan store、provider guardrail、drift collector、remediationの選定と実行です。実装例を追加する時は、正常系だけでなくplan差替え、unknown／error、別経路の変更、drift、収集失敗、cleanupを実cloud状態で確認します。

<a id="network-segmentation-migration"></a>

<a id="network-segmentation-migration--workload-network-segmentation移行記録"></a>
## Workload network segmentation移行記録

旧`PSB-CONTAINER-001 / CNT-008`を、
[control](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)と
[pattern](../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)へ分割移行しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

<a id="network-segmentation-migration--分割判断"></a>
### 分割判断

Network reachabilityは、containerのUID、capability、filesystem等とは別の実効境界です。Process権限を小さくしても、侵害後のworkloadがneighbor、管理service、外部宛てへ接続できれば、lateral movement、command and control、exfiltrationは成立します。そのため[Workload privilege confinement](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)へ戻さず、一つのnetwork主題にしました。

旧`CNT-008`は「workloadを選択するdefault-deny ingress／egress」とCNI enforcement evidenceを要求していました。この成果は残しますが、default denyだけでは実際のapplication通信を設計できません。新controlではsource・destination identity、両側のallow、DNS等の基盤flow、異なるsensitivity zone・external egress、plugin coverage、live probeまでへ分解しました。

| 旧要素 | 新しい配置 | 判断 |
|---|---|---|
| Workloadを選ぶdefault deny | `NET-SEG-2` | 全管理workload・新namespace・両方向のdefaultへ拡張 |
| Ingress／egress allow | `NET-SEG-1,3` | Sourceとdestination双方のflow contractとして具体化 |
| CNI enforcement evidence | `NET-SEG-6,7` | Boolean fixtureを廃止し、許可追加・削除を伴うlive probeへ変更 |
| Network border／external egress | `NET-SEG-5` | Core policyで表せないFQDN・NAT等をgateway／proxy／対応CNIへ渡す |
| DNS・platform flow | `NET-SEG-4` | 広いfallbackにせず、採用環境で個別に列挙する |

<a id="network-segmentation-migration--具体化判断"></a>
### 具体化判断

2026-09-29の読み合わせでは、代表実装の拒否probeにdestinationのlocal listener確認を追加しました。Sourceのexecが正常でもdestinationが停止していれば接続失敗を遮断成功と数えません。Live clusterでのCNI強制と全通信経路は引き続き未確認です。

Kubernetes core NetworkPolicyは技術経路が明確で、policy objectだけでは実効性を証明できないという重要な失敗があります。そのため[Kubernetes 1.37代表実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)を必要な成果物に選びました。

実装は三namespaceをingress・egressともdefault denyにし、`client -> api:8080/TCP`だけを両側から許可します。Source egressとdestination ingressについて、片側の一時allowを追加すると接続でき、削除すると拒否され、再追加で接続が戻ることをlive Pod間で確認します。これによりPod停止やCNI非対応を単純な「拒否成功」にしません。

DNS、external destination、dual stack、hostNetwork、node trafficはclusterごとの差が大きく、portableな安全値を一つのmanifestへ埋め込めません。代表実装の範囲外として明記し、patternで実装選択と確認方法を示します。

旧`secure/network-policy.json`、`insecure/network-policy.json`、`platform-evidence.json`、Python verifierは非移植です。旧verifierはselectorと空rule、`enforcement_available: true`という自己申告の整合を確認しても、CNI data planeの通信拒否を確認しないためです。

<a id="network-segmentation-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.3.3` | `CNT-008 / mitigates / high` | `NET-SEG-1..3 / supports / medium / design-reviewed`。Sensitivity levelとwell-defined interfaceによるinter-container separationとの設計関係 |
| NIST SP 800-190 `4.4.2` | `CNT-008 / mitigates / high` | `NET-SEG-1,2,4..7 / supports / medium / design-reviewed`。Egress border、app-aware filtering、flow・anomaly observationとの部分関係 |

旧`mitigates / high`はsynthetic fixtureとboolean platform evidenceを含むため継承しません。NISTはKubernetes selector、default deny object、CNI、FQDN、DNS ruleを規定しません。現在のmappingはNIST本文と新特性の設計関係であり、実導入やNIST準拠を示しません。

<a id="network-segmentation-migration--完了条件と残る範囲"></a>
### 完了条件と残る範囲

- Controlの問い、直接の失敗、7特性、診断で確認する項目、隣接境界を読める。
- 教材からcontrol、pattern、Kubernetes代表実装へたどれる。
- Kubernetes 1.37とagnhost 2.66.1の対象、policy、live probe、cleanup、制限を読める。
- NISTとKubernetes資料の版・確認日・採否、旧check・mapping・実装の扱いを追跡できる。
- YAML、shell、repository構造は検査する。Live clusterでのCNI enforcementは未実行として残す。
- DNS、external egress、IPv6、host／node、cloud network、L7 identityは採用環境で別の具体実装を必要とする。

<a id="resource-consumption-migration"></a>

<a id="resource-consumption-migration--workload-resource-consumption-bounds移行記録"></a>
## Workload resource consumption bounds移行記録

旧`PSB-CONTAINER-001 / CNT-007`を、
[control](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)と
[pattern](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)へ分割移行しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

<a id="resource-consumption-migration--分割判断"></a>
### 分割判断

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

<a id="resource-consumption-migration--具体化判断"></a>
### 具体化判断

2026-09-29の読み合わせでは、Kubernetes 1.37で利用できるPod-level CPU／memory予算と、この例が要求するcontainer単位の明示値を区別しました。Pod-levelのみを指定するPodは代表実装で拒否されますが、control全体でその方式を禁じません。PID、node pressure、runtimeの実効cgroupは引き続き未確認です。

KubernetesではResourceQuotaとValidating Admission Policyによる受入境界が明確です。そのため[Kubernetes 1.37代表実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)を必要な成果物に選びました。

実装はCPU、memory、ephemeral-storageの明示request／limitをregular・init containerへ要求し、ephemeral containerを拒否します。Namespaceのrequest／limit合計とPod・Job数をResourceQuotaで制限し、正常Podの作成、quota使用量、QoS、必須値不足、aggregate quota超過をlive APIで確認します。

PID limit、node reservation、pressure／eviction、cgroupの実効値はcluster providerとnode構成に依存します。架空のKubeletConfigurationや自己申告fixtureを`PASS`にせず、代表実装の非対応範囲として残しました。旧`1000m`、`512Mi`、PID `256`は普遍的な安全値ではないため非継承です。

旧`secure/policy.json`、`platform-evidence.json`、AdmissionReview fixture、Python verifierは非移植です。旧verifierは限られたquantity形式と固定上限を検査し、`pids_limit_enforced: true`という自己申告を実効runtime証拠としていたためです。

<a id="resource-consumption-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.4.3` | `CNT-003..007 / mitigates / high` | `RESOURCE-1..3,5,7 / supports / medium / design-reviewed`。Resource allocation、runtime configurationの継続的強制との部分関係。Namespace quota、Kubernetes resize、node pressureの規定とは扱わない |

旧`mitigates / high`はsynthetic fixture、固定値、PID自己申告を含むため継承しません。NIST本文のresource allocationとruntime configurationを設計根拠にし、Kubernetes固有のResourceQuota、CEL、request／limit semantics、evictionをNIST要件へ変換しません。

<a id="resource-consumption-migration--完了条件と残る範囲"></a>
### 完了条件と残る範囲

- Controlの問い、直接の失敗、7特性、診断で確認する項目、隣接境界を読める。
- 教材からcontrol、pattern、Kubernetes代表実装へたどれる。
- Kubernetes 1.37の対象、namespace budget、admission、live API確認、cleanup、制限を読める。
- NISTとKubernetes資料の版・確認日・採否、旧check・mapping・実装の扱いを追跡できる。
- YAML、shell、repository構造は検査する。Live clusterでのadmission・quota・runtimeは未実行として残す。
- PID、node reservation、pressure／eviction、cgroup、capacity、provider固有実装は採用環境で別の具体化を必要とする。

<a id="workload-confinement-migration"></a>

<a id="workload-confinement-migration--workload-privilege-confinement移行記録"></a>
## Workload privilege confinement移行記録

旧`PSB-CONTAINER-001`から保留していたworkload confinementを、
[control](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)と
[pattern](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

<a id="workload-confinement-migration--分割判断"></a>
### 分割判断

Application processの侵害後に、root、kernel機能、hostのnamespace・path・runtime API、書込み可能なroot filesystem、control-plane credentialへ進む経路は、一つの実効runtime profileとして判断する必要があります。Main containerだけでなくinit、sidecar、ephemeral、debugを同じ強制点で扱うため、旧`CNT-003..006`を一つの主題へまとめました。

Resourceとnetworkは同じPod設定に現れても、守る成果と実効性の証拠が異なります。CPU・memory・PID・storageのavailabilityにはrequest／limit、quota、scheduling、eviction、node capacity、runtime enforcementが関係します。Network segmentationにはCNI、workload identity、ingress／egress、DNS、service mesh、外部境界が関係します。この二つをconfinement profileへ詰め込まず、それぞれ独立した後続主題にします。

| 旧check | 新しい配置 | 判断 |
|---|---|---|
| `CNT-003` non-root・privileged・escalation | `WORKLOAD-CONFINE-1,2,7` | 全container経路の実効identityとfinal admissionへ拡張 |
| `CNT-004` capability | `WORKLOAD-CONFINE-3,7` | 既定で全dropし、対象OSで必要な追加だけを許可 |
| `CNT-005` host namespace・hostPath | `WORKLOAD-CONFINE-4,7` | Host process、device、port、runtime／node管理socketまで同じhost境界として扱う |
| `CNT-006` read-only root・seccomp | `WORKLOAD-CONFINE-3,5,7` | Syscall／MACとfilesystemを別の特性に分け、同じprofileで強制 |
| `CNT-007` CPU・memory・PID | `split-migrated` | [PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)へ分割し、quota、scheduling、eviction、runtime実効値を含めて再編集。詳細は[専用の移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#resource-consumption-migration) |
| `CNT-008` default-deny network | `split-migrated` | [PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)へ分割し、CNI coverageと実効到達性を含めて再編集。詳細は[専用の移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#network-segmentation-migration) |
| `CNT-009` fail-closed admission | `PSB-CONTAINER-001`と`WORKLOAD-CONFINE-7` | Artifact identityとruntime authorityは別に判定するが、どちらも最終使用境界でfail closedにする |

`WORKLOAD-CONFINE-6`のcontrol-plane credentialは旧checkの直接移植ではありません。Kubernetesが既定でservice account credentialをPodへ渡し得るため、process侵害時のauthorityを制限する同じ問いへ追加したリポジトリでの解釈です。

<a id="workload-confinement-migration--具体化判断"></a>
### 具体化判断

2026-09-29の読み合わせでは、代表実装のsmoke testに同名namespace・policy・bindingの存在確認を加え、既存対象を上書き・削除しないようにしました。Server-side dry runは新規Podの受入・拒否を確認するもので、既存Podの実効状態やruntime適用を証明しません。

この主題は、Kubernetesで使う主要な強制点と不足分が明確です。そのため文書だけで終えず、Kubernetes 1.37の[Pod Security Admission + CEL代表実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)を必要な成果物に選びました。

組込み`restricted` profileを`enforce` mode・`v1.37`固定で使い、そこに含まれないread-only root filesystemとservice account tokenの自動mount禁止だけをValidating Admission Policyで補います。IaC／CI検査は早いfeedbackであり、controller生成後のPod、直接作成、ephemeral containerを扱う最終強制点にはしません。

旧offline Python verifier、synthetic manifest、platform evidence、testsは非移植です。宣言同士の整合だけではlive API serverのpolicy、対象scope、failure semantics、runtime適用を証明しないためです。新実装には使い捨てcluster向けのserver-side dry-run手順と正常・拒否fixtureを置きましたが、このrepositoryからlive clusterへは接続しておらず拒否結果は未実行です。

<a id="workload-confinement-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.4.3` | `CNT-003..007 / mitigates / high` | この移行では`WORKLOAD-CONFINE-1..5,7 / supports / medium / design-reviewed`へ限定。その後resource allocationは`RESOURCE-1..3,5,7 / supports / medium / design-reviewed`として[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)で再評価。Credential特性へは割り当てない |
| NIST SP 800-190 `4.3.3` | `CNT-008 / mitigates / high` | この移行では非継承。その後`NET-SEG-1..3 / supports / medium / design-reviewed`として[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)で再評価 |
| NIST SP 800-190 `4.4.2` | `CNT-008 / mitigates / high` | この移行では非継承。その後`NET-SEG-1,2,4..7 / supports / medium / design-reviewed`としてPSB-CONTAINER-006で再評価 |

旧mappingの`high` confidenceと`mitigates`は、synthetic fixtureの成功や広いcheck割当を含んでいたため継承しません。現在のmappingは公式NIST本文と新特性を照合した設計関係であり、NIST準拠や組織への導入を示しません。

<a id="workload-confinement-migration--完了条件と残る範囲"></a>
### 完了条件と残る範囲

- Controlの問い、直接の失敗、7特性、診断で確認する項目、隣接境界を読める。
- 教材からcontrol、pattern、Kubernetes代表実装へたどれる。
- Kubernetes 1.37の対象、変更箇所、使い捨てclusterでの確認、解除、制限を読める。
- NIST、Kubernetes資料の版・確認日・採否と、旧check・mappingの扱いを追跡できる。
- YAML、shell、repository構造は検査する。Live clusterの拒否とruntime stateは未確認として残す。
- Node／daemon hardeningは[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)、resource consumptionはPSB-CONTAINER-007、network segmentationはPSB-CONTAINER-006へ移行済み。IaC golden pathは別の移行候補として残す。
