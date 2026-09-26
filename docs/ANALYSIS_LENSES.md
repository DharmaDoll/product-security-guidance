# 横断分析の軸

[Security scope](SECURITY_SCOPE.md)を分析範囲の正本とします。七つのレイヤーには一般的なApplication Securityを含めますが、製品自体のAI securityはai-security-foundryの担当です。
RAG、モデル・データセット、AI application gateway、AI製品のTEVVは本PJの未移行gapとして数えません。段階3はAIを使う開発環境を扱います。

追加移行（2026-09-17）: [PSB-GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)はPSIRTの製品影響調査・初動計画と攻撃段階12を直接扱います。下の初期pilotの集約に対する更新です。受付・開示・修復完了・復旧全体や実環境への採用を意味しません。Stage 9のSBOM・artifact、stage 11の稼働観測を入力として受け取ります。

追加移行（2026-09-20）: [PSB-GOV-002](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)は全段階から利用され得るgovernance境界です。個別controlの失敗を限定的に扱うdecisionであり、元の失敗や分析上の空白を対応済みに変えません。

追加移行（2026-09-20）: [PSB-DETECT-001](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)は、段階9のartifact・SBOM検査と段階12の検知結果を直接扱います。CI・runnerで実行されても、その権限や隔離は隣接controlの責任です。Scannerのclean resultを未検査対象や未知脆弱性へ一般化しません。

追加移行（2026-09-26）: [PSB-DETECT-003](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)は段階11の外部公開候補と所有台帳の照合を直接扱い、段階12へ未登録・期待外・再出現を渡します。収集障害は公開なしの証拠にならず、実際の収集元・台帳・通知は未導入です。

追加移行（2026-09-24）: [PSB-GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)は段階12でcredential固有の封じ込め、consumer移行、旧authority拒否、closure条件を直接扱います。段階2・6から漏えい対象、段階9・10へ影響identityを受け渡します。Provider操作とincident全体の復旧は未検証です。

追加移行（2026-09-24）: [PSB-GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)は段階12でaffected artifactのresponse decision、distinct-digest replacement、old digest非稼働、closureを直接扱います。段階8〜11の生成・配布・稼働観測を接続しますが、それらをGOV-005自身が実装したとは扱いません。

追加移行（2026-09-24）: [PSB-GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)は段階12でfinding・適用性・severity・known exploitationをowner・priority・組織期限へ結びます。段階11のactive exposureを入力とし、GOV-005へresponse decisionを渡します。Live feed・policy・PSIRT運用は未検証です。

追加移行（2026-09-24）: [PSB-BUILD-003](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)は段階8でcontrol-plane generation、artifact subject、field source、provenance authenticationを直接扱います。段階7のuser-defined buildから権限を分け、段階9のconsumerへevidence contractを渡します。承認builder、製品実装、配布、artifact signing、SBOM、admissionは別の責任です。

追加移行（2026-09-26）: [PSB-BUILD-002](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)は段階8でproducerが承認するbuilderと正規releaseのbuild手順を扱います。段階2のsource・定義、段階7の実行経路を受け、BUILD-003のplatform証拠と段階9のreleaseへ渡します。実platformの能力・実行・publish gateは未確認です。

追加移行（2026-09-25）: [PSB-REL-003](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)は段階9でsource・build・operations observation、exact artifactとSBOMのbinding、coverage、公開、analysis processingを直接扱います。CycloneDX限定実装はartifact bindingだけを実値で確認し、live storage・Dependency-Track・deployment catalogは未検証です。

追加移行（2026-09-25）: [PSB-REL-004](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)は段階9で供給者SBOMの出所と対象成果物を利用者側の期待値へ照合し、隔離から通常台帳へ渡す境界を扱います。段階4の調達判断と段階12の影響調査へ接続します。実供給者・署名方式・取込先は未選定です。

追加移行（2026-09-26）: [PSB-REL-005](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)は段階9で承認したexact artifactへ限定した権限で署名し、検証材料を取得可能にしてからreleaseを完了する境界を扱います。段階6のworkload identity、段階8のfinal artifactから入力を受け、REL-001と段階10の使用判断へ渡します。実signer・公開先・release gateは未検証です。

追加移行（2026-09-24）: [PSB-CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)は段階10で、REL-001のconsumer acceptanceをexact artifactのfinal use gateへ結びます。旧controlのworkload privilege・host・resource・networkは別主題へ分離し、registry publicationとlive admissionも未実装です。

追加移行（2026-09-24）: [PSB-CONTAINER-002](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)は段階10でregistry endpoint、publish authority、OCI digest、immutability、audit、withdrawalを直接扱います。Provider実装、artifact内容の安全性、admission、rolloutは別の責任です。

追加移行（2026-09-25）: [PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)は段階10でfinal workloadのprocess・kernel・host・filesystem・control-plane authorityを制限し、段階11へ意図したprofileを渡します。Kubernetes代表実装はありますがlive clusterでは未確認です。Resource consumptionは後続のCONTAINER-007へ分けています。

追加移行（2026-09-25）: [PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)は段階10で通信契約、default deny、source egressとdestination ingressのallowを準備し、段階11で実効到達性を扱います。Kubernetes代表実装はlive clusterで未実行であり、CNI coverage、DNS、external egress、host／node経路は採用環境で確認が必要です。

追加移行（2026-09-25）: [PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)は段階10でworkload・namespaceのresource budgetを強制し、段階11でruntime ceiling、node capacity、pressureを扱います。Kubernetes代表実装はnamespace admissionとquotaに限定し、PID、node reservation、pressure／eviction、cgroupは未確認です。

追加移行（2026-09-25）: [PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)は段階10でnode image・identity・参加条件を準備し、段階11でruntime socket、kubelet、host管理面、更新・隔離・再登録を扱います。対象OS／runtime／provider未選定のため実装は作らず、live node evidenceは未確認です。

追加移行（2026-09-25）: [PSB-IAC-001](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)は段階10でreviewしたsource・依存、resolved plan、policy判断、apply authorityを結び、段階11でprovider上の実resourceとdriftを扱います。段階6のworkload identityを入力とし、段階12へ観測障害、例外、修正判断を渡します。対象provider／resource未選定のため実装は作らず、live cloudは未確認です。

追加移行（2026-09-25）: [PSB-REL-002](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)は段階9でexact artifactから一つ以上のprovenanceを発見・取得する配布境界を扱います。段階8のBUILD-003から生成結果を受け、REL-001と段階10の使用gateへconsumer-retrievableなprovenanceを渡します。対象ecosystem未選定のためlive distributionは未確認です。

## Workload privilege confinement

[CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)と
[設計パターン](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)は、正規artifact内のapplicationが侵害された後も不要なhost authorityへ進ませない境界を扱います。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 9→10：Artifactからworkloadへ | Artifact authenticityとは別に、最終workloadへ渡すidentity、capability、profile、mount、credentialを決める |
| 10：IaC・deployment admission | Main、init、sidecar、ephemeral、debugを含むfinal objectをfail closedで評価する。IaC検査は早いfeedbackに限定する |
| 11：Runtime | Admission時の意図を実効UID、capability、seccomp／MAC、mount、credentialの観測へ渡す。Admission成功をruntime適用の証拠にしない |

七レイヤーではplatformとinfrastructureを直接扱い、operationsへ実効状態の観測を渡します。Resource consumptionとnetwork segmentationは独立した後続成果が扱い、node／daemonは[CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)へ渡します。

## Workload network segmentation

[CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)と
[設計パターン](../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)は、侵害されたworkloadからneighbor、異なるsensitivity zone、管理service、外部宛てへ広がるnetwork経路を扱います。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 10：IaC・deployment admission | 必要なflow、selector identity、default deny、両端のallowをworkload露出前に準備する。Manifest受理を強制済みの証拠にしない |
| 11：Runtime・外部露出 | Source egressとdestination ingressの両方で実通信を制限し、CNI coverage、zone間通信、external egressの実効性を確認する |
| 12：検知・対応 | 予期しないflow、policy反映失敗、plugin health、probe失敗をruntime検知・調査へ渡す |

七レイヤーではplatformとinfrastructureを直接扱い、operationsへ実効状態と観測障害を渡します。Resource consumptionは独立した成果が扱い、node／daemon hardeningは[CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)、application identityとlive CNI導入は別途必要です。

## Workload resource consumption bounds

[CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)と
[設計パターン](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)は、loop、fork、log、replica増加等による一workloadのresource消費を共有nodeや別tenantへ広げない境界を扱います。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 10：IaC・deployment admission | CPU、memory、PID、local storage、object数のworkload budgetとtenant aggregate quotaをcreate、update、scale、resize、debug経路で強制する |
| 11：Runtime・外部露出 | Requestとruntime ceiling、node allocatable・reservation、throttle、OOM、eviction、unschedulable、memory／disk／PID pressureを区別する |
| 12：検知・対応 | Resource exhaustionと観測障害をruntime検知・capacity・application ownerへ渡す |

七レイヤーではplatformとinfrastructureを直接扱い、operationsへ実効状態とpressureを渡します。Application availability、autoscaling、冗長化、SLO、live node／runtime evidenceは別途必要です。

## Container host and daemon boundary

[CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)と
[設計パターン](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)は、workload、local process、operator、node credentialからruntime・kubelet・host TCBを制御し、一nodeの侵害をclusterへ広げる経路を扱います。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 10：IaC・deployment admission | Node image、component set、pool sensitivity、node identity、secure enrollmentを決め、reviewしていないnodeの参加を拒否する |
| 11：Runtime・外部露出 | Runtime／NRI socket、kubelet、debug／metrics、protected path、host isolation、管理操作、patch・replacementを実効状態へ結ぶ |
| 12：検知・対応 | Compromised nodeのnetwork隔離、scheduling停止、credential失効、削除、local state処理、再登録拒否と証跡をoperationsへ渡す |

七レイヤーではplatformとinfrastructureを直接扱い、operationsへnode evidenceと侵害時の切離しを渡します。Provider-neutralなpatternまでを作り、対象platformを選ばない合成実装やlive node導入は主張しません。

## Infrastructure change authorization and drift boundary

[IAC-001](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)と
[設計パターン](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)は、reviewしたinfrastructure sourceと、実際にapplyされprovider上に残る状態が別物になる経路を扱います。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 6：CI/CD identity・control plane | CICD-006から保護されたjob identityを受け取り、apply対象と操作へ限定する。Token発行条件自体はCICD-006が扱う |
| 10：IaC・deployment admission | Source・module・provider・variable・policy・targetをresolved planへ結び、unknown・errorを分け、reviewした保存planだけをapplyする。別変更経路はprovider側拒否または観測へ渡す |
| 11：Runtime・外部露出 | Provider inventoryと実resourceをdesired stateへ照合し、out-of-band変更、未管理resource、stale state、収集失敗を区別する |
| 12：検知・対応 | Drift、例外、観測障害、自動修正のimpactをownerへ渡し、危険な修正は新しいplanとreviewへ戻す |

七レイヤーではplatformとinfrastructureを直接扱い、operationsへcurrent stateと修正判断を渡します。Golden Pathは安全な変更を作りやすくする入口ですが、利用したことを合格や導入証拠にしません。Provider-neutralなpatternまでを作り、synthetic JSON checkerやlive cloud implementationは採用していません。

## Deployed artifact recovery

[GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)と
[設計パターン](../engineering/governance-operations/deployed-artifact-recovery/README.md)は、GOV-001のimpact scopeを
危険なbytesが稼働しない状態まで追跡します。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 8：Build・provenance生成 | [BUILD-003](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)がplatform生成とartifact bindingを扱う。Cause-aware clean buildと採用platformの実装は別途必要 |
| 9：Release・signature・SBOM | REL-001のconsumer acceptanceへnew digestと期待値を渡す。生成・公開は別の責任 |
| 10：Registry・admission・deployment | [CONTAINER-002](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)がpublication、[CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)がexact artifact admissionを扱う。Live providerとtarget rolloutは別途必要 |
| 11：稼働観測 | Original scopeをfreshに再観測し、new digestとold digest非稼働を別に確認する |
| 12：対応・復旧 | Current risk decision、owner・期限、open・overdue・remediated・error状態を直接扱う |

七レイヤーではoperationsとPSIRTに直接対応し、external and supply chainからbuild・artifact evidenceを受け取ります。
Live platformのrebuild、publication、admission、rolloutは未検証です。

## Credential exposure containment

[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)と
[設計パターン](../engineering/governance-operations/credential-exposure-containment/README.md)は、通常のcredential lifecycleとは別に、
漏えい疑い後のauthority graph、封じ込め、consumer移行、拒否確認、影響調査へのhandoffを扱います。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 2・6：Source / CI/CD authority | 漏えいしたcredential、派生session、発行条件、既知consumerをincident scopeへ渡す |
| 9・10：Release / registry / deployment | Exposure windowのsigning・publication・deployment identityをGOV-001の影響調査と後続のartifact responseへ渡す |
| 12：対応・復旧 | Class別封じ込め、bounded replacement、consumer disposition、旧authority拒否とclosure blockerを直接扱う |

七レイヤーではoperationsとPSIRTに直接対応し、governanceへ承認責任を接続します。
実API、providerの伝播、live denial、組織のincident response能力は確認していません。

## Secret publication boundary

[SOURCE-002](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)と[設計パターン](../engineering/source-protection/secret-checks-before-publication/README.md)は、
端末での早期検査と共有先の受入判断を分けます。Git hooksを省略できること、最新ファイルから消えた値が履歴に残ることを前提にします。

| 攻撃段階 | 直接扱う境界・受け渡し |
|---|---|
| 1：開発端末 | hookと検査方針の管理、コミット・送信対象の検査。端末が侵害されてもローカル検査が必ず動くとは扱わない |
| 2：ソース管理 | 受信側の独立した判断、書込経路・対象履歴・除外の管理。受信処理への到達と共有refへの受入を区別 |
| 5：CI | 隣接。送信後の検査とmerge拒否を補完し、未信頼コードに権限を渡さない |
| 12：対応 | 露出範囲をSOURCE-004の認証情報所有者へ渡す。履歴整理だけで失効・回収済みにしない |

七レイヤーではplatformに直接対応し、operationsへ対応を渡します。[資料と採否](../sources/README.md#ref-secret-publication-001)を保持し、確認項目の記載を実検証へ変換しません。

## Developer endpoint management

[Developer endpoint trust](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)と[Managed developer endpoint](../engineering/source-protection/managed-developer-endpoint/README.md)は、SOURCE-001の端末管理範囲を扱います。
七レイヤーではplatformを直接扱い、operationsへ観測・初動、governanceへ基準と例外の責任を接続します。

| 攻撃段階 | 主な脅威 | 対応control・設計・参照 |
|---|---|---|
| 1：開発者端末 | 未更新・不要なアプリ・過大権限・物理的な接触から、ソースやセッションへ到達 | 上記controlとpattern。診断で確認する項目を記載し、製品実装・実環境は未確認。[入力と採否](../sources/README.md#ref-developer-endpoint-baseline-001) |
| 2：ソース管理 | 侵害・紛失後も認証情報や既存セッションが有効 | [SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)へ対象と失効を引き継ぐ。変更レビューや公開防止は別の境界 |
| 3・7：開発agent・実行環境 | 端末が管理下でも外部コードに広い権限を渡す | [AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と[BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)の実行境界。全開発端末への適用確認ではない |
| 12：調査・対応 | 監視停止を異常なしとし、未到達の隔離・消去を完了扱いにする | 端末管理者と認証情報の所有者が初動を分担。[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)へ変更・成果物への影響調査を渡す |

登録と観測とアクセス判断の切れ目を[教材](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/learning.md)で扱います。実際の端末・通知・復旧は未検証です。

## 追加移行：CI state and runner lifecycle

| 攻撃段階 | 主な脅威 | 対応control・参照 |
|---|---|---|
| 5: Workflow / cache | 低信頼のwriterが後続jobの復元内容を変更する | [Cache trust boundary](../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md)、[cache仕様](../sources/README.md#spec-ci-cache-boundary) |
| 7: Runner / build execution | 前jobのstateやhost権限が別jobへ届く | [Runner lifecycle isolation](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、[runnerガイダンス](../sources/README.md#ref-cicd-014) |
| 9→12: Release / incident response | 侵害jobの成果物が公開され、破棄時に調査ログも失われる | [設計pattern](../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)で外部ログ保存とconsumerの再判断へ引き継ぐ。Release Integrity・runtime detectionの導入は未確認 |

[REF-PORTFOLIO-001](../sources/README.md#ref-portfolio-001)ではplatformを直接扱い、operationsへログ・対応を引き継ぎます。
Sensorの候補[REF-BUILD-001](../sources/README.md#ref-build-001)はruntime detectionの評価入力であり、隔離や破棄の代替ではありません。

この文書は、コントロールを領域別に並べるだけでは見落としやすい空白と、攻撃連鎖の途中で切れる
受け渡しを確認するための入口です。コントロール要件、フレームワーク要件、組織への導入証拠を
追加するものではありません。

人が読む正本はこの文書、機械可読な対応関係は
[`mappings/analysis-lenses.yaml`](../mappings/analysis-lenses.yaml)です。

## 根拠と役割

未移行領域の棚卸しと次の構造検証は[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)へまとめました。
その候補は以下の試作版の直接対応とは区別し、移行完了まで機械可読mappingへ追加しません。

読者が分野から探す基本分類は[11 domain](../controls/README.md#domain一覧)です。
この文書の七つのレイヤーと攻撃段階は、その分類を横断して偏り・脅威・受け渡しを確認するために使います。
レイヤー名や攻撃段階から新しいdomainを自動的に作りません。

| 分析軸 | 根拠 | この試作版での役割 | この分析軸からは導かないもの |
|---|---|---|---|
| プロダクトセキュリティの7レイヤー | [`REF-PORTFOLIO-001`](../sources/README.md#ref-portfolio-001) | ポートフォリオの偏り、欠落、読者の入口を確認する | フレームワーク識別子、準拠要件、既定のKPI |
| サプライチェーン攻撃の12段階 | [`LOCAL-SUPPLY-CHAIN-ATTACK-STAGES`](../sources/README.md#local-supply-chain-attack-stages) | 攻撃経路、前後のコントロール、責任の受け渡しを確認する | 各コントロールの合格条件、導入済み判定、完全な脅威網羅 |

`REF-PORTFOLIO-001`は、個別要件の出典ではなく、リポジトリ全体を七つの観点から見直すための資料です。
サプライチェーン攻撃一覧は、このリポジトリで作られた横断索引です。外部の規範資料ではないため、
ここでは原文の要件を移植せず、攻撃段階と受け渡しだけを利用します。

## 対応関係の読み方

- `直接`: 試作対象のコントロールが、そのレイヤーまたは攻撃段階で成立すべき状態を定義する。
- `隣接`: 境界の一部を支援するが、そのレイヤーまたは段階の主要な結果は別のコントロールが担う。
- `受け渡し`: この試作対象の出力を次の段階が引き継ぐ。次の段階を実装済みという意味ではない。
- `空白`: この試作版には直接対応する成果物がない。現行リポジトリ全体の未実装を意味しない。

この関係は、コントロールへの合格、組織への導入、フレームワークへの準拠を表しません。

## プロダクトセキュリティの7レイヤー

| レイヤー | 試作版との関係 | 読み取れること | この試作版に残る空白 |
|---|---|---|---|
| アプリケーション | 直接 | Object accessのControl・教材・設計・SQLite限定実装がある | HTTP認証、全endpoint、並行処理、他のアプリケーション欠陥、SAST／DAST |
| プラットフォームとインフラストラクチャ | 直接 | ソース権限、依存取得、PR・cache・runner、workload認証、build隔離、承認builderと一貫した手順、provenance生成、IaC change、registry publication、artifact admission、workload privilege confinement、workload network segmentation、workload resource consumption bounds、container host／daemon boundary、scannerの判断境界を扱う | 管理面全体、実builderの能力評価。移行した設計も実環境の強制は別途確認が必要 |
| 運用 | 直接 | Runtime検知・health・配送・triage、credential封じ込め、artifact recoveryの判断境界を定義する | Live sensor、provider・deployment操作、通知・対応の実測、実環境の導入証拠 |
| PSIRTと脆弱性管理 | 直接（一部） | GOV-001の影響調査、GOV-003のpriority、GOV-004のcredential封じ込め、GOV-005のartifact復旧closure。実対応と能力評価は未確認 | 受付、開示、組織全体の修復完了追跡 |
| 外部依存とサプライチェーン | 直接 | 依存の採用・同一性・実行許可、拡張の審査、build隔離、承認builder、platform provenance生成、artifact署名、provenance配布、release SBOM identity・analysis intake、supplier SBOMの受入境界、consumerの署名・来歴照合、registry publication、artifact admissionを扱う | Live builder・署名・supplier intake・SBOM publication・analysis・target rollout。各境界をつなぐ実環境の証拠は未確認 |
| ガバナンス | 直接（一部） | GOV-002の例外管理とAI-002の拡張採用・独立審査・失効を扱う | 組織全体の責任分担、KPI、導入状況の評価 |
| 教育と文化 | 隣接 | 学習ノートを具体的なシナリオから読み、関連control・patternへ辿れる | 役割別の教材coverageと演習。受講者の理解度・出席・行動変容は本PJで記録しない |

七つのレイヤーすべてにファイルを作ることが目的ではありません。空白を見えるようにし、次に移すべき
コントロールや、組織側で用意すべき証拠を判断できることが目的です。

## サプライチェーン攻撃の12段階

| 段階 | 主な境界 | 試作版との関係 | 試作対象または受け渡し先 |
|---|---|---|---|
| 1 | 開発端末と端末内の信頼境界 | 直接 | `PSB-SOURCE-001`が端末保護と状態に応じたアクセス判断、`PSB-SOURCE-004`が認証情報の権限と期間を扱う |
| 2 | ソース、リポジトリ、バージョン管理システムの管理面 | 直接（一部） | SOURCE-002が秘密情報の公開・受入境界を扱う。コードレビューと管理面全体は別の責任 |
| 3 | AI支援開発のサプライチェーン | 直接（一部） | [AI-001](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)がrepository指示の変更と効果、AI-002が拡張採用、AI-003が読んだ資料から依頼・操作への昇格防止、AI-004が実効権限を扱う。作業単位の予算・停止は[次の候補](AI_DEVELOPMENT_SCOPE_REVIEW.md)で、実agentの評価・拒否も未確認 |
| 4 | 依存関係の選定、解決、取得 | 直接 | `PSB-DEPS-001〜004`が待機期間、準備用コードの実行許可、取得物の同一性、更新レビューを別の判断として扱う |
| 5 | CIワークフロー、プルリクエスト、外部アクション、キャッシュ | 直接 | [PSB-CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)が未信頼の実行と派生状態を権限付きconsumerから分離する。外部Actionの完全性は別に確認する |
| 6 | CI/CDのIDと管理面 | 直接 | `PSB-SOURCE-004`が認証情報の責任を分離し、`PSB-CICD-006`がworkloadの認証条件と交換後の権限を限定する。管理面全体の変更保証までは扱わない |
| 7 | ランナーとビルド実行 | 直接 | `PSB-CICD-007`がrunnerのライフサイクル、`PSB-BUILD-001`が実行中の権限・通信・観測を定義する。実環境の強制と導入は未確認 |
| 8 | ビルド基盤と来歴生成 | 直接（一部） | [PSB-BUILD-002](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)が承認builderと一貫したrelease経路、[PSB-BUILD-003](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)がplatformによるprovenance生成・artifact binding・field source・認証を扱う。実platform評価とlive release gateは別途必要 |
| 9 | 成果物、リリース、署名、SBOM | 直接 | PSB-REL-005が署名生成、PSB-REL-002がartifactごとのprovenance配布、PSB-REL-003がrelease SBOMのidentity・coverage・analysis処理、PSB-REL-004がsupplier SBOMの受入れ、PSB-REL-001がconsumerの署名・来歴・期待値照合を定義する。Live signing・supplier intake・distribution・analysis・consumer cryptoは未確認 |
| 10 | レジストリ、IaC、デプロイ許可 | 直接（一部） | [PSB-IAC-001](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)がIaC change、[PSB-CONTAINER-002](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)がregistry publication、[PSB-CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)がexact artifactの使用許可、[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)がnode image・identity・参加条件、[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)がruntime authority、[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)がnetwork policy、[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)がresource budgetの準備を扱う。Rolloutとlive platformは別途必要 |
| 11 | 本番実行時と外部露出 | 直接 | PSB-CONTAINER-003がnode runtime・host管理面、PSB-CONTAINER-005が意図したworkload profile、PSB-CONTAINER-006がnetwork allow境界、PSB-CONTAINER-007がresource ceilingとpressureを扱い、PSB-CONTAINER-004がruntime検知、PSB-SOURCE-003がpublic source exposure、PSB-DETECT-003が外部公開サービスと台帳の照合を定義する。Live node・runtime、実効profile、CNI・cgroup・pressure、sensor、外部collectorは未確認 |
| 12 | 検知、インシデント対応、復旧 | 直接（一部） | GOV-001で影響調査、GOV-003でvulnerability priority、GOV-004でcredential封じ込め、GOV-005でartifact recoveryを扱う。実対応と復旧全体は未確認 |

## 代表的な攻撃経路

### Repository指示の変更から開発agentへ

段階2で指示ファイルの変更を保護されたbranchへ受け入れると、段階3の後続の開発作業へ影響します。[AI-001](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)は、変更の独立レビューと実際に読む版、開発作業での効果を分けます。指示が権限を広げられない実行側の制限はAI-004へ渡します。旧合成benchmarkは実agentの成果ではなく、GitHub変更レビュー例も未導入です。製品AIの設計・TEVVをこの経路に含めません。

### 開発資料からagentの権限へ

Issueや未信頼branchの文書がagentへ入る段階2→3では、出所と正規の依頼を[AI-003](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)で分けます。Agentが提案した操作が開発者のファイル、認証情報、通信へ進む段階3→1・2では[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)が外側で制限します。拒否だけで元の作業が完了したとは推定しません。異常の監査・通知は段階12へ渡します。製品別の実行時強制と作業結果の検証は未確認です。

### Agent extension admission

操作の認可については[Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)、端末の到達範囲については[Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md)を先行追加しました。承認と実行を結び付ける設計であり、AI-004のcontrol記録も再編集しましたが、実行時強制は未検証です。

| 攻撃段階 | 主な脅威 | 対応control・参照 |
|---|---|---|
| 3: 拡張の取得・採用 | 承認後の差替え、有害な指示・tool、過剰な権限、古い審査結果 | [PSB-AI-002](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)、[版と採否](../sources/README.md#ref-agent-extension-admission-001) |
| 3→1・2: 読み込み・操作 | 同名の別拡張を起動、remote serverの誤認、未承認の書込み・秘密情報へのアクセス | [Agent extension admission](../engineering/ai-development-security/agent-extension-admission/README.md)から実行環境へ照合情報を渡す。認証情報は[PSB-SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)、実行時の保証目標は移行済みAI-004、実際の強制は未確認 |
| 3→12: 失効・対応 | 収集停止を有効と誤認、失効後もsessionや認証情報が残る | AI-002は承認の利用停止条件を定義。実際の停止・認証情報失効・復旧は別途確認 |

七つのレイヤーでは外部依存とgovernanceを直接扱い、platformへ実行時の強制を引き渡します。
Benchmarkと組織全体のAI governanceは未移行です。AI-003の間接prompt injection対策はガイダンス移行であり、実agentの有効性は未確認です。

### Operations pilot：Runtime detection to triage

| 攻撃段階 | 主な脅威 | 対応control・参照 |
|---|---|---|
| 11: 本番実行 | 侵害後のshell・file変更・privilege・通信・resource濫用、対象誤認 | [PSB-CONTAINER-004](../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)、[Falco資料](../sources/README.md#ref-container-003)、[Sysdig資料](../sources/README.md#ref-container-004) |
| 12: 初動・復旧 | 観測障害・通知不達をcleanと誤認、影響製品の誤特定、無承認の破壊操作 | [Runtime detection to triage](../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)から、移行済みの[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)へ対象と調査範囲を渡す。[対応資料](../sources/README.md#ref-runtime-response-handoff-001)は保持。実環境の配送・対応・復旧は未確認 |

七レイヤーではoperationsを直接扱い、PSIRT・governanceへ引き継ぎます。検知と障害を同時に保持し、全製品の無影響や組織成熟度を推定しません。

### Application pilot：Object access boundary

[Object access authorization](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)と
[Object access boundary](../engineering/secure-design/object-access-boundary/README.md)は、正規利用者が他者の対象IDを指定するアプリケーション内の悪用経路を扱います。
Application層に直接対応しますが、供給経路の12段階には割り当てません。[参照資料](../sources/README.md#ref-application-authorization-001)から認証と認可の違いを設計へ反映しました。
Python / SQLiteの限定した読み書きは検証済みでも、全APIの認可・組織採用の確認ではありません。

### Application pilot：Unicode source review

[PSB-CODE-005](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)は、投稿されたsourceの見た目と処理系が読む文字・識別子の食い違いを、段階2の変更受入で見つける主題です。Application層を主とし、受入側のCI（段階5）とbuild（段階8）へレビュー済みrevisionを引き渡します。[Python 3.10限定実装](../engineering/secure-coding/unicode-source-review/implementations/python/README.md)は実ファイルを検査しますが、protected CI、review UI、他言語の検査を実装したものではありません。認可等のアプリケーション欠陥は[Object access](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)など別の境界で扱います。

### 追加移行：Consumer artifact acceptance

| 攻撃段階 | 主な脅威 | 対応control・参照 |
|---|---|---|
| 9: Release | Bytes差替え、未承認署名者、正規署名だが想定外の生成条件 | [PSB-REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)、[仕様と採否](../sources/README.md#spec-consumer-artifact-verification) |
| 10: 使用許可 | 検証後に可変tagを再解決、別bytesや無検証fallbackを使用 | [Consumer artifact acceptance](../engineering/release-integrity/consumer-artifact-acceptance/README.md)から同じdigestのbytesを使用gateへ渡す。実admissionは未確認 |
| 12: 調査 | Crypto・parser・取得障害を受入成功に変換 | 同patternで使用を停止し、違反と評価不能を別に調査する |

七レイヤーでは外部依存を直接扱い、governanceへ期待値管理を渡します。[教材](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/learning.md)は同一性・認証・受入の違いを扱います。

### 追加移行：Provenance distribution and availability

| 攻撃段階 | 主な脅威 | 対応control・参照 |
|---|---|---|
| 8→9: 生成からreleaseへ | 生成済みprovenanceがartifactとは別の曖昧・mutableな参照へ置かれる | [PSB-REL-002](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)がBUILD-003のexact subject identityをartifact-level relationへ渡す |
| 9: Release・配布 | 複数artifactの対応誤り、部分公開、consumer access不能、上書き、早期削除、silent downgrade | [Provenance distribution and availability](../engineering/release-integrity/provenance-distribution-and-availability/README.md)でpublication completion、consumer probe、immutability、retention、no downgradeを設計する |
| 9→10: 検証・使用許可 | 配布側のavailable表示を検証済みと誤認する | Exact artifactから取得したprovenance bytesをREL-001へ渡し、その後同じartifact digestを使用gateへ渡す |
| 12: 調査・復旧 | 取得不能・削除・replica不整合・観測失敗を欠落許容へ変える | Release Operationsへ状態を分けて渡し、artifact利用停止、復旧、consumer通知を判断する |

七レイヤーではexternal and supply chainを直接扱い、operationsへ配布障害とlifecycleを渡します。Live registry／release service、consumer retrieval、retention、withdrawalは未検証です。

### 追加移行：Release SBOM identity and analysis

| 攻撃段階 | 主な脅威 | 対応control・受け渡し |
|---|---|---|
| 4→8: Dependencyからfinal artifactへ | Source manifestだけのSBOMをfinal artifact inventoryとして使い、buildで加わったcomponentを見落とす | [PSB-REL-003](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)がobservation phaseとauthorityを分け、build／post-build SBOMをartifact digestへ結ぶ |
| 9: Release・SBOM | 別artifact binding、dangling relationship、根拠のないcomplete claim、SBOMだけの公開失敗 | [Release SBOM identity and analysis intake](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)でidentity、coverage、publication completionを設計し、[CycloneDX限定実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)で一部を実値確認する |
| 9→12: Analysis | Upload受付をanalysis完了とし、validation・processing failureやstale dataを0 findingsへ変える | Exact project・SBOM identity、least privilege、`ACCEPTED`から`PROCESSED`までの状態と`ERROR`を分ける。Live adapterは未実装 |
| 11→12: 稼働影響 | Source・build・operations inventoryを上書きし、componentからdeploymentへ辿れない | Artifact digestから別identityのdeployment observationへ関係を保ち、collection gapを稼働なしへ変えずGOV-001へ渡す |

七レイヤーではexternal and supply chainを直接扱い、PSIRTとoperationsへinventoryと評価healthを渡します。限定実装の成功はgenerator coverage、publication、analysis、deployment inventoryの導入証拠ではありません。

### 追加移行：Supplier SBOM intake trust

| 攻撃段階 | 主な脅威 | 対応control・受け渡し |
|---|---|---|
| 4→9: 供給者からの受領 | 調達した製品と別のSBOMや未承認の署名者を、取得した成果物へ付け替える | [PSB-REL-004](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)が利用者側の期待値、出所、成果物digestを取込前に照合する |
| 9: 通常台帳への境界 | 署名成功だけで不明な内容を受け入れ、隔離や検証障害を迂回する | [Supplier SBOM intake boundary](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)で`INTAKE_CANDIDATE`、`QUARANTINE`、`ERROR`を分ける |
| 9→12: 影響調査 | 訂正・撤回されたSBOMを正本としたまま、部品の非該当を判断する | 供給者・製品・成果物・SBOMの関係と判断時点をGOV-001へ渡す。台帳での処理完了も受入判断とは別に確認する |

七レイヤーではexternal and supply chainを直接扱い、operationsとPSIRTへ状態を渡します。実供給者の署名・配送方式、失効source、台帳での隔離は未確認です。

### 追加移行：Build containment

| 攻撃段階 | 主な脅威 | 対応control・参照 |
|---|---|---|
| 7: Build実行 | 承認した依存のコードが秘密情報、host、通信、deploy権限を悪用 | [PSB-BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)、[仕様と採否](../sources/README.md#spec-build-containment) |
| 8→9: 来歴・release | Jobの自己申告や固定した出力が無条件に信頼される | [設計pattern](../engineering/build-security/build-execution-boundary/README.md)からplatform側の来歴生成と[consumerの期待値照合](../engineering/release-integrity/consumer-artifact-acceptance/README.md)へ引き継ぐ。Live生成・照合は未確認 |
| 12: 調査・対応 | センサー停止や配送障害をイベントなしと解釈する | 同patternでhealthを別に確認。[Sensor候補](../sources/README.md#ref-build-001)は未導入 |

七レイヤーではplatformを直接扱い、operationsへ観測を渡します。[教材](../controls/records/build-security/psb-build-001-build-containment/learning.md)は、依存の同一性と実行権限を別の判断にするためのものです。

### 追加移行：Workload federation boundary

[PSB-CICD-006](../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)は
段階6で、意図しないworkloadからcloud権限への交換と、過大な交換後権限を制限します。
段階5のPR・workflow・cacheは交換jobへ昇格させず、段階7のrunner隔離と検知は別途必要です。
段階9・10のartifact公開・deployへ渡すのは承認済みの限定権限であり、artifactの安全性・admissionは保証しません。
七レイヤーではプラットフォームに直接対応し、運用・ガバナンスへつながります。
詳細は[pattern](../engineering/cicd-security/workload-federation-boundary/README.md)、
根拠の採否は[参照資料](../sources/README.md#spec-workload-federation)を参照してください。

### 追加移行：Reviewed dependency intake

| 攻撃段階 | 主な脅威 | 対応control・受け渡し |
|---|---|---|
| 4：依存選定・解決・取得 | 未レビューの推移依存、manifest drift、同じversionのartifact差し替え | [Dependency change review](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)が採用判断、[Dependency artifact identity](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)が通常buildのgraph・bytesを結び付ける |
| 5：PR・CI・merge | Findingや評価失敗、取消、検査欠落を許可として扱う | Dependency change reviewが現在の判断を必須merge gateへ接続する |
| 7：runner・build実行 | 承認した入力にある悪意や、後続実行での権限悪用 | 両controlから固定した入力を渡す。実行許可・隔離・runner破棄は別の責任 |
| 9・12：release・脆弱性対応 | 成果物との対応切れ、merge後の新しいadvisory | 署名・来歴・SBOMと、継続SCA・PSIRTへ引き継ぐ。今回の移行では実装していない |

七つのレイヤーでは外部依存・プラットフォームからPSIRT・ガバナンスへ判断を接続します。
各controlの教材と共通する方式は[Reviewed dependency intake](../engineering/dependency-security/reviewed-dependency-intake/README.md)、
資料の採否は[参照資料記録](../sources/README.md#spec-dependency-lock-identity)で確認できます。
この関係は探索用であり、組織の導入済み状態を証明しません。

### 追加移行：Install execution policy

[PSB-DEPS-002](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)は、
段階4の取得・準備から段階7の実行へ進む間に、未承認のhookやbuild backendを起動する経路を切ります。
Cooldownを通過した依存でも実行許可は別です。許可したbuild、import・testの隔離、runner破棄、
リリース・本番の安全性は後続へ残ります。七つのレイヤーでは外部依存に直接対応し、
プラットフォーム権限とガバナンスへ接続します。上の三件のpilotの表に加えた関係は
[`analysis-lenses.yaml`](../mappings/analysis-lenses.yaml)にも記録しています。

### Source credential compromise path

```text
侵害された端末／拡張機能／AIツール
  -> source credentialが漏えい
  -> ソース管理基盤上の権限を悪用
  -> ソース、ワークフロー、依存関係を変更
  -> 正常に見えるビルドと署名済みリリースへ進む
```

`PSB-SOURCE-004`は二つ目の矢印で得られる権限と有効期間を狭めます。最初の侵害、変更内容のレビュー、
後続のビルドや署名の妥当性は保証しません。AIツールを利用する場合は、モデル出力を信頼済みの判断として
扱わず、ツール認可をモデルの外側で強制するという`REF-PORTFOLIO-001`の境界も維持します。

### Malicious dependency to production path

```text
悪意あるバージョンを公開
  -> 依存関係の解決処理が採用
  -> CIランナー／ビルド環境で実行
  -> 成果物、来歴、署名、SBOMを生成
  -> レジストリから本番環境へ配布
  -> 実行時検知と影響調査
```

`PSB-DEPS-001`は、公開直後の候補が最初に採用される箇所だけを扱います。待機期間を通過した後の
隔離、成果物の完全性、来歴、署名、デプロイ許可、実行時検知は、後続段階への明示的な受け渡しです。

### Untrusted PR to privileged CI path

```text
PRのcode／dependencyを変更
  -> 権限イベントまたは後続consumerが実行
  -> token／secret／OIDC／runner権限を利用
  -> repository、build、releaseを汚染
```

`PSB-CICD-005`は、未信頼の状態が権限を持つconsumerへ届く矢印を変えます。イベントやrunを分けるだけでなく、
cache、artifact、output、workspaceによる昇格も追跡します。信頼済みrevisionから始めた後のOIDC条件、
runnerの完全性、成果物の来歴、署名は、引き続き別の境界です。

## 新しい成果物へ適用する手順

1. [`sources/`](../sources/README.md)で、利用する資料の版、役割、採否、限界を確認する。
2. 七つのレイヤーから主な一つを選び、必要なら隣接レイヤーを記録する。
3. 十二の攻撃段階から、直接扱う段階と、前後の受け渡しを分ける。
4. 攻撃経路のどの矢印を変えるのか、強制点とともに説明する。
5. 対応しない段階を削除せず、空白または残余リスクとして残す。
6. 関係を[`analysis-lenses.yaml`](../mappings/analysis-lenses.yaml)へ記録する。

分析軸の表を埋めるためだけに、空のコントロール、学習資料、実装例を作ってはいけません。
