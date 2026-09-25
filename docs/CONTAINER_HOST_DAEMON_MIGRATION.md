# Container host and daemon boundary移行記録

旧[PSB-CONTAINER-003](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-host-daemon-hardening)を、
[control](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)と
[pattern](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

## 境界の見直し

旧controlはhost OS、kernel、runtime socket、operator、audit、hardware trustを一つの主題にしていました。この主題は維持します。直接の失敗は、個々のhardening項目の不足ではなく「workload、local process、operator、node credentialがruntime・kubelet・host TCBを制御し、workload policyを迂回して一nodeの侵害をclusterへ広げること」です。

Workload manifestのnon-root、capability、hostPath、seccomp等は[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)へ既に分離しています。CONTAINER-003はhost側が提供・強制するruntime、kernel、node agent、management surface、node identityとlifecycleを扱います。Runtime sensorのevent評価は[PSB-CONTAINER-004](../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)へ残し、sensorを動かすnode権限・互換性・保護をこの主題から渡します。

## 旧項目の扱い

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

## 具体化判断

この主題ではprovider-neutralなcontrolとpatternを必要な成果物に選び、具体実装は追加しません。

Secret scanはGit objectとscannerの接続が対象repository上で閉じ、代表実装の入力・拒否・確認を再現できます。Kubernetes workload admission、NetworkPolicy、ResourceQuotaも使い捨てclusterに限定したYAMLとlive probeを示せます。一方、host／daemonはOS distribution、runtime、Kubernetes distribution、managed／self-managed、node image build、identity、network、attestationによって変更箇所と観測方法が変わります。

旧`secure/host-evidence.json`、`policy.json`、`exceptions.json`、Python verifierは移植しません。これらは固定した自己申告値を比較し、live host、socket、listener、runtime process、node credential、patch service、audit、TPMを観測していませんでした。Synthetic fixtureの9件`PASS`を実効的なhost implementationに見せる問題があるためです。

実装を開始する条件は、対象OS image、kernel、runtime、node agent、plugin、provider責任分界、変更する設定、使い捨てnode pool、更新・隔離・rollback、取得可能なlive evidenceを一組で選ぶことです。対象が決まれば、containerd self-managed、Docker rootless、managed Kubernetes node pool等の限定名で`implementations/`へ置きます。

## 参照資料の再評価

- NIST SP 800-190 `4.3.1`、`4.3.5`、`4.5.1`〜`4.5.5`、`4.6`を2026-09-25に公式PDFで再照合しました。旧`mitigates / high`はlive enforcementを示していないため、`supports / medium / design-reviewed`へ縮小します。
- Kubernetes 1.37のkubelet authentication／authorization、API server bypass risks、Node authorization／NodeRestriction、security checklistをnode管理面の具体的な設計入力にしました。Kubernetesをcontrol要件にはしません。
- `containerd/containerd@82f33ce76db81e47393be1cbdb6eba3343687fc5`のOperator Security Guidelinesを、socket、protected path、plugin、debug／metrics、patch範囲の実装候補に使います。特定file modeを他runtimeへ普遍化しません。
- Docker公式のdaemon socket保護とrootless modeは方式比較に使います。Remote daemonやrootlessを全nodeへ必須化しません。
- 旧CIS Docker Benchmark候補は、認可された固定版とrecommendation inventoryのreviewがないため引き続きmappingしません。

## 旧framework mapping

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

## 完了条件と残る範囲

- Controlの問い、直接の失敗、8特性、診断で確認する項目、workload・runtime detectionとの境界を読める。
- 教材からruntime socket、kubelet、static Pod、node identityによるAPI迂回を理解し、controlとpatternへたどれる。
- Patternからnode trust contract、方式、導入順序、失敗経路、実装開始条件を判断できる。
- 旧9 checks、synthetic verifier、8 framework関係、参照資料の採否を追跡できる。
- Live host、node pool、runtime、kubelet、credential、audit、attestationは未検証であり、実装・導入済みとは扱わない。
