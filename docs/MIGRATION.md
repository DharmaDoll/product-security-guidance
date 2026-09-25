# 移行台帳

## 目的

旧リポジトリをそのままコピーせず、セキュリティ特性、学習価値、実装価値を選別して再構成します。
旧パスを新しいツリーへ残すためだけの転送用ディレクトリは作りません。この台帳とGit履歴で追跡します。

移行元のコミット: `91fdb7661b38723ce6fb38da93cf3c68b701e521`

## 移行時の扱い

- `migrated`: 同じセキュリティ特性を保って新しい成果物へ移した。
- `split`: 一つの旧パッケージを複数の成果物へ分けた。
- `deferred`: 有用だがパイロットでは移していない。
- `retired`: 形骸化または重複のため移さない。
- `review-required`: 参照資料や境界の再確認が必要。
- `out-of-scope`: 別PJの担当など、本PJの移行対象から除外する。移行待ちや移植済みとは扱わない。
- `scope-review-required`: 開発環境と製品のAI機能が混在するため、対象内の部分を選別してから移行可否を決める。

## パイロットの移行記録

各日付の件数・「次」の記述は、その時点の履歴です。現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を参照してください。

### 2026-09-25：REL-002 Provenance distribution and availability boundaryを移行

旧`PSB-REL-002`を、artifact familyとchannelのscope、exact artifact digestから一つ以上のattestationへのrelation、publication completion、intended-consumer retrieval、immutability、retention、no downgradeを扱う
[7特性のcontrol](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)と
[設計pattern](../engineering/release-integrity/provenance-distribution-and-availability/README.md)へ再編集しました。SLSA v1.2に合わせ、旧「一artifact・一provenance」固定を一対多へ直し、public HTTPS、5分、365日を普遍要件から外しました。

旧Python verifierとJSON fixtureはrelease API、registry、storage、consumer clientへ接続せず、`immutable: true`、`available: true`、public access、synthetic timestamp等を比較していたため非移植です。対象ecosystem、artifact、attestation client、identity、retentionを選べない状態で同じstructureを作り直さず、[実装開始条件](../engineering/release-integrity/provenance-distribution-and-availability/README.md#実装を作る開始条件)を定めました。

SLSA `producer-distributes-provenance`とNIST SSDF `PS.2.1`は公式本文で再照合し、旧`verifies／supports / high`をいずれも`supports / medium / design-reviewed`へ縮小しました。現在33 control・32 pattern・109 framework mappingです。次は旧`PSB-REL-003`のSBOM binding／publicationを、観測時点、artifact identity、complete性、公開、analysis取込、処理状態の境界から選別します。詳細は[移行記録](PROVENANCE_DISTRIBUTION_MIGRATION.md)を参照してください。

### 2026-09-25：IAC-001 Infrastructure change authorization and drift boundaryを移行

旧`PSB-IAC-001 Secure IaC Golden Path`を、reviewしたsource・module／provider・入力・policy・target、resolved plan、保存plan、apply authority、provider側の変更経路、実resource、drift・修正判断を結ぶ
[8特性のcontrol](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)へ再編集しました。Golden Pathは合格条件ではなく、安全な変更を作りやすくする入口として残しました。

旧Python verifierとmulti-cloud JSON fixtureはTerraform、OPA、cloud providerを実行せず、module integrity、全変更経路の強制、OIDC、drift、例外、remediation等を自己申告fieldで比較していたため非移植です。対象provider、resource、security invariant、sandboxを選べない状態で同じ構造を作り直さず、[実装開始条件](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md#実装を作る開始条件)を定めました。

Terraformの保存plan、機微情報、provider dependency lockとremote moduleの違い、refresh-only、OPA plan limitationを公式文書で再確認しました。旧OpenSSF 3件、SSDF 1件、GitHub 1件のmappingはIaC plan・apply・provider状態への直接要件ではないため非継承とし、framework mappingは107件のままです。詳細は[移行記録](IAC_CHANGE_BOUNDARY_MIGRATION.md)を参照してください。
旧参照ID`REF-USER-003`は、資料の役割が分からない汎用名だったため新しい索引へ継承せず、主題を示す`REF-IAC-CHANGE-BOUNDARY-001`へ置き換えました。
現在32 control・31 pattern・107 framework mappingです。次は旧`PSB-REL-002`のProvenance publication／distributionを、subject digestとの結合、発見・取得、保持、downgrade、取得不能の境界から選別します。

### 2026-09-25：CONTAINER-003 Container host and daemon boundaryを移行

旧`PSB-CONTAINER-003`を、runtime socket、kubelet・補助endpoint、host上のprotected state、node identity、host側isolation、管理操作、更新・隔離・再登録を扱う
[8特性のcontrol](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)へ再編集しました。Workload specの権限制約はCONTAINER-005へ残し、host側のtrusted computing baseとAPI迂回経路へ範囲を絞りました。

対象OS distribution、runtime、Kubernetes distribution、managed／self-managed providerが未選定のため、具体実装は追加していません。旧`policy.json`、`host-evidence.json`、exception fixture、Python verifierはlive host、socket、listener、process、credential、patch、audit、attestationを観測しないため非移植です。実装開始条件をpatternと[移行記録](CONTAINER_HOST_DAEMON_MIGRATION.md)へ明記しました。

NIST SP 800-190 `4.3.1`、`4.3.5`、`4.5.1`〜`4.5.5`、`4.6`は公式PDFで再照合し、旧`mitigates / high`を`supports / medium / design-reviewed`へ縮小しました。Kubernetes 1.37、固定commitのcontainerd Operator Security Guidelines、Docker公式資料を設計入力に追加しました。
現在31 control・30 pattern・107 framework mappingです。次は旧`PSB-IAC-001`のSecure IaC Golden Pathを、source review、resolved plan、apply権限、provider側の現在状態、drift・修正の境界から選別します。

### 2026-09-25：CONTAINER-007 Workload resource consumption boundsを分割移行

旧`PSB-CONTAINER-001`から保留していた`CNT-007`を、一workloadのresource消費が共有nodeや別tenantへ広がる範囲を制限する
[7特性のcontrol](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)へ再編集しました。CPU・memoryだけでなく、PID、local storage、object数、namespace quota、node allocatable・reservation・pressure、resize・debug経路、実効状態の観測を分けて判断します。

Kubernetes 1.37の[ResourceQuota + CEL代表実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)も追加しました。Live APIでCPU／memory／ephemeral-storageの必須値不足とnamespace aggregate quota超過を拒否し、正常PodのQoSとquota usageを確認する構成です。Repositoryでは静的検査だけを行い、live clusterでは未実行です。PID、node pressure、cgroup、capacityはこの実装の完了範囲に含めません。

旧`1000m`、`512Mi`、PID `256`、synthetic AdmissionReview、`pids_limit_enforced: true`のplatform evidence、Python verifierは非移植です。NIST SP 800-190 `4.4.3`はresource関連特性へ`supports / medium / design-reviewed`で部分的に再配置しました。詳細は[移行記録](RESOURCE_CONSUMPTION_MIGRATION.md)を参照してください。
現在30 control・29 pattern・99 framework mappingです。次は旧`PSB-CONTAINER-003`のcontainer host／daemon hardeningを選別します。

### 2026-09-25：CONTAINER-006 Workload network segmentationを分割移行

旧`PSB-CONTAINER-001`から保留していた`CNT-008`を、侵害されたworkloadの通信を必要な相手・方向・protocol・portへ限定する
[7特性のcontrol](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)へ再編集しました。Default denyだけでなく、source egressとdestination ingress、identity属性の変更権限、DNS等の基盤flow、zone・external境界、CNI coverage、live probeを分けて判断します。

技術経路が明確で、policy objectの存在を実効性と取り違えやすい主題なので、Kubernetes 1.37の
[NetworkPolicy代表実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)も追加しました。片側のallowを一時追加・削除し、Pod間通信が成功・拒否・再成功へ変わることを確認する構成です。Repositoryでは静的検査だけを行い、live clusterとCNI data planeでは未実行です。

旧synthetic network fixture、`enforcement_available: true`のplatform evidence、Python verifierは非移植です。NIST SP 800-190 `4.3.3`と`4.4.2`は`supports / medium / design-reviewed`へ縮小しました。詳細は[移行記録](NETWORK_SEGMENTATION_MIGRATION.md)を参照してください。
現在29 control・28 pattern・98 framework mappingです。次は旧`CNT-007`のresource availabilityを、workload resourceとnamespace／cluster capacityの境界から再評価します。

### 2026-09-25：CONTAINER-005 Workload privilege confinementを分割移行

旧`PSB-CONTAINER-001`から保留していた`CNT-003..006`を、侵害されたworkloadが不要なprocess・kernel・host・filesystem・control-plane authorityへ進まないための
[7特性のcontrol](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)へ再編集しました。

技術経路が明確な主題なので、Kubernetes 1.37のPod Security Admission `restricted`とValidating Admission Policyを組み合わせた
[代表実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)も追加しました。
Read-only root filesystemとservice account tokenの自動mount禁止をCELで補い、正常Podと三つの拒否fixtureをserver-side dry runする構成です。Live clusterでは未実行です。

旧`CNT-007`のresource availabilityと`CNT-008`のnetwork segmentationは、実効性の証拠と失敗経路が異なるため別主題へ保留しました。旧synthetic verifierは非移植です。NIST SP 800-190 `4.4.3`は`supports / medium / design-reviewed`へ縮小し、networkの2関係は非継承のままです。詳細は[移行記録](WORKLOAD_CONFINEMENT_MIGRATION.md)を参照してください。
現在28 control・27 pattern・96 framework mappingです。次は旧`CNT-008`のnetwork segmentationを選別し、resource availabilityとは分けて扱います。

### 2026-09-25：教材を各controlの隣へ移動

独立した教材索引を廃止し、既存教材を対応するcontrolディレクトリの`learning.md`へ移しました。
Controlからシナリオ、誤解、判断基準へ自然に進み、そこからpatternとimplementationをたどれる構成です。
Runnerとcache、dependency artifact identityとchange reviewで共有していた教材は、本文を複製せず、
各controlが答える問いへ分割して相互リンクしました。`docs/learning/`は削除しました。

既存のObject access教材には対応controlがなかったため、教材、pattern、7件の限定実装テストから境界を確認し、
[PSB-DESIGN-001 Object access authorization](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)を追加しました。
これは旧controlや未提供の組織チェックリストを復元したものではなく、repository pilotとしての保証目標です。
HTTP認証、全endpoint、並行処理、exact ASVS mapping、組織への導入は未確認です。

移行後の再学習で生じた問いや誤解は、まず対応する`learning.md`へ戻します。複数教材で再利用価値が確認できた見方は
insightを、具体的な技術経路を試す価値が確認できた部分はimplementationを検討します。先に成果物の数を増やしません。
現在27 control・26 pattern・95 framework mappingです。

### 2026-09-25：異常時テストの読者向け表現を変更

専門用語だけでは目的が伝わりにくいため、読者向けの名称を「診断で確認する項目（異常時テスト）」へ変更しました。
`Negative test`は検索用語として説明に残します。現在この見出しを持つ9件のcontrolでは、何を確認する一覧なのか、
本PJが実際に試した結果なのかを冒頭で区別しました。参照先は安定した`failure-checks` anchorへ統一しています。

チェックリストだけでも成果物として成立し、テストコードや実行結果を必須にしない方針は変えていません。
今後は専門用語より先に、読者が何を判断・確認するのかを平易な日本語で書きます。

### 2026-09-25：SOURCE-002の自作Python scannerを追加

旧`scan-sensitive.py`を、[Python pattern scanner](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)として再編集しました。
Python標準ライブラリだけで、代表的なsecret pattern、機密file名、staged内容、commit message、pushで追加する履歴を検査します。
Gitleaksを使わずに正規表現とGit hookの接続を読み、軽い組織固有ruleを試すためのimplementationです。

ローカルhookは省略可能であり、受信側の独立した拒否やGitleaks相当の検出を保証しません。旧installerとDocker wrapperは
引き続き非移植です。12 ruleの無効canary、near miss、値の非表示、indexと作業ツリーの違い、削除後も履歴に残る値を
7 testで確認しました。任意の手元のrepositoryへcopyして有効化する手順、使い捨てrepositoryで実際のGit hookを通す
smoke test、解除手順も示しました。本PJ自身のhookは有効化していません。詳細な採否は[Git hooks移行記録](GIT_HOOKS_MIGRATION.md)に保持します。

### 2026-09-25：独立したinsight成果物を撤去

`docs/insights/`の3文書と索引を削除しました。いずれもcontrol、学習資料、patternにある考え方の言い換えが中心で、
独立成果物として読者へ別の判断を提供できていませんでした。本文を別の場所へ複製して保存せず、既存の教材にある
シナリオ、誤解、実務で確認する問いを正本として残します。

今後、講義で生じた問いや別領域でも使えそうな見方は、まず関連する教材の文脈で育てます。複数の講義で繰り返し使われ、
教材から切り離す理由が明確になるまで、独立したinsightファイルを先に作りません。成果物モデル、執筆ルール、索引、
関連リンクもこの判断へ合わせました。

### 2026-09-24：CONTAINER-002 Container registry publication boundaryを再編集

旧7 checkを[7特性のcontrol](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)へ再編集しました。
Registry endpoint、repository／action authority、short-lived publisher、release immutability、audit、lifecycle、evidence healthを一つのregistry境界に保持し、artifact生成・scanning・consumer verification・admissionは統合していません。

旧synthetic policy・operation・audit・inventory、Python verifier、testsは非移植です。NIST SP 800-190 `4.2.1`〜`4.2.3`は実装検証から`supports / medium / design-reviewed`へ縮小しました。
詳細は[移行記録](CONTAINER_REGISTRY_MIGRATION.md)を参照してください。
現在26 control・26 pattern・95 framework mappingです。次はCONTAINER-001から分けたworkload confinementの境界を選別します。

### 2026-09-24：CONTAINER-001をDeployment artifact admissionへ分割移行

旧`PSB-CONTAINER-001`からexact artifact、consumer acceptance、final-state enforcement、全経路coverage、failure semantics、decision identityを、
[6特性のcontrol](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と
[設計pattern](../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)へ再編集しました。
旧`CNT-003..008`のprivilege・host・filesystem・resource・networkはworkload confinementへ保留し、registry lifecycleも統合していません。

旧offline Python verifier、synthetic AdmissionReview・manifest・provenance・platform evidence・testsはlive強制を証明しないため非移植です。
SLSA 2件とNIST SP 800-190 2件を`supports / medium / design-reviewed`へ縮小し、NISTのworkload／network 3件は非継承としました。
詳細は[移行記録](DEPLOYMENT_ARTIFACT_ADMISSION_MIGRATION.md)を参照してください。
現在25 control・25 pattern・92 framework mappingです。次は旧CONTAINER-002 Registry securityを選別します。

### 2026-09-24：BUILD-003 Platform provenance generationを再編集

旧`PSB-BUILD-003`のplatform-side generation、artifact subject、field source、authenticity、failure semanticsを、
[6特性のcontrol](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)と
[設計pattern](../engineering/build-security/platform-owned-provenance-generation/README.md)へ再編集しました。
旧synthetic statement、local key、OpenSSL verifier、JSON policy、testsはcontrol-plane生成とidentity保護を証明しないため非移植です。

SLSA v1.2公式本文へ照合し、`invocationId`一律必須を非継承、L2のtenant由来field例外を明示しました。
旧SLSA mapping 2件は`supports / medium / design-reviewed`へ縮小しました。詳細は[移行記録](PLATFORM_PROVENANCE_MIGRATION.md)を参照してください。
現在24 control・24 pattern・88 framework mappingです。次はstage 10の旧CONTAINER-001 Deployment admissionを、registry publicationと分けて選別します。

### 2026-09-24：SOURCE-003の公開source exposureを再編集

[PSB-SOURCE-003 Public source exposure triage](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)を
6特性へ再編集し、[ENG-SOURCE-004](../engineering/source-protection/public-exposure-observation-and-triage/README.md)で
public observation、coverage、値の最小化、occurrence state、triage、response handoffを設計できる形にしました。
旧6 checkの配置、4件のframework mapping、実装の採否は[移行記録](PUBLIC_EXPOSURE_MIGRATION.md)に保持しています。

旧GitHub Actions workflow、Python scanner、domain・state JSON、testsは移植していません。Providerと運用を選ぶ前に
一つの実装を正本化しない判断です。診断で確認する項目をcontrolに記載し、実行済み証拠とは扱いません。
旧mapping 4件も固定原文へ照合し、ATT&CK `T1593.003`だけを`detects / medium / design-reviewed`として部分割当、
`T1552.001`、SSDF `RV.1.1`、OSPS `OSPS-BR-07.01`は非継承としました。
この時点で20 control・20 pattern・80 framework mappingです。次は旧GOV-004 Credential exposure containmentを選別します。

### 2026-09-24：GOV-004 Credential exposure containmentを再編集

[PSB-GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)を7特性へ再編集し、
[ENG-GOV-003](../engineering/governance-operations/credential-exposure-containment/README.md)でclass別封じ込め、bounded replacement、
consumer disposition、old-authority denial、exposure-window impact、closureを設計できる形にしました。
旧10 check、実装、mappingの採否は[照合記録](CREDENTIAL_EXPOSURE_MIGRATION.md)に保持しています。

旧JSON policy・response bundle・Python verifier・fixture testsは、live providerの失効・session・trust・auditを証明しないため
非移植です。診断で確認する項目を移し、具体実装はprovider、credential class、非本番検証範囲を選定してから追加します。
旧mappingはATT&CK `T1078`だけを部分継承し、意味が異なるSSDF `RV.2.1`とOSPS `AC-04.01`を非継承としました。
現在21 control・21 pattern・81 framework mappingです。次はGOV-004の影響調査から引き継ぐ
旧GOV-005 Deployed artifact refreshを選別します。

### 2026-09-24：GOV-005 Deployed artifact recoveryを再編集

[PSB-GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)を7特性へ再編集し、
[ENG-GOV-004](../engineering/governance-operations/deployed-artifact-recovery/README.md)でcurrent risk、response decision、
clean rebuild、exact digest rollout、old digest非稼働、closureを設計できる形にしました。旧check・実装・mappingの採否は
[移行記録](DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md)に保持しています。

旧offline JSON fixture・Python verifier・testsはlive builder、registry、admission、deploymentを証明しないため非移植です。
SSDF `RV.1.1`・`RV.2.1`は各一特性へ縮小し、ATT&CK `T1195.002`は部分継承、OSPS `DO-04.01`は非継承としました。
現在22 control・22 pattern・84 framework mappingです。次はGOV-005のrisk decisionへ入力を渡す旧GOV-003
Exploited vulnerability prioritizationを選別します。

### 2026-09-24：GOV-003 Product vulnerability priority decisionを再編集

[PSB-GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)と
[ENG-GOV-005](../engineering/governance-operations/vulnerability-priority-decision/README.md)へ、旧8 checkを移行しました。
旧composite verifier、synthetic KEV・CVSS・case fixturesは非移植とし、将来の実装をdata source、calculator、applicability、
policy、case deliveryのadapterへ分割しました。SSDF `RV.1.1`・`RV.2.1`は範囲を縮小して部分継承しています。
詳細は[移行記録](VULNERABILITY_PRIORITY_MIGRATION.md)を参照してください。

現在23 control・23 pattern・86 framework mappingです。次はGovernance / Operationsの連続移行を一度止め、
stage 8・10に残る直接gapと旧候補の優先度を再評価します。

### 2026-09-24：SOURCE-004の残るframework mappingを照合

[SOURCE-004照合記録](SOURCE_CREDENTIAL_MAPPING.md)で、GitHub guidance 4件、Enterprise ATT&CK v19.1の2件、
OSPS Baseline 2026.02.19の1件を固定版の公式本文へ照合し、`design-reviewed`へ更新しました。
GitHub account securityは`SRC-AUTH-2,4,5`、credential typesは`SRC-AUTH-1,3,5`、SAMLとSCIMは
`SRC-AUTH-5`へ絞りました。Credential typesとOSPSの旧`high` confidenceは、部分対応を表す`medium`へ変更しました。

OWASP Agentic 2026は公式landing pageとmedia metadataまで確認しましたが、PDF本文の自動取得がHTTP 403で拒否されたため、
`ASI03`の旧関係をレビュー済みへ変更していません。旧8件の版・関係・confidence・対象check・review日・根拠は照合記録と
固定commitに保持しています。Framework mappingは79件のままです。次はSOURCE-002の公開前境界から事後対応へつなぐ
SOURCE-003 Public source exposureを選別します。

### 2026-09-23：SOURCE-002の秘密情報の公開境界を追加

利用者が指定したGit hooksの主題を先に整理し、[Secret publication boundary](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)と
[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)を追加しました。
7特性と診断で確認する項目で、コミット予定の内容・メタデータ・導入履歴、hooksの迂回、独立した受入、検査障害、値の非表示、限定した除外を扱います。
[旧13項目・4件の対応表](GIT_HOOKS_MIGRATION.md)に元の版・ID・対象check・confidence・理由・レビュー日を保持しました。
OSPS-BR-07.01のみを部分的な設計関係として割り当て、SSDF PS.3.1は非継承、ATT&CKとCISAの新特性への割当は保留です。

旧SOURCE-001のDEH-004・005はSOURCE-002への隣接関係へ更新し、29項目の配置をcontrol移行11・隣接15・保留3にしました。
現在19 control・19 pattern・79 framework mappingです。旧installer・スキャナーは移植せず、Git設定変更・hooks有効化・実診断は実施していません。
SOURCE-004のSSDF PS.3.1対応の照合は次作業に残します。

### 2026-09-23：SOURCE-004のSSDF mappingを照合

[SOURCE-004照合記録](SOURCE_CREDENTIAL_MAPPING.md)で、旧`PS.3.1 / supports / medium`と17件の旧check割当を履歴として保持しました。
公式本文では`PS.3.1`がrelease files・integrity information・provenanceのarchiveを扱うため、認証情報ライフサイクルとの関係を非継承としました。
`PS.1.1`の最小権限によるcode accessを別に評価し、SRC-AUTH-1〜6への部分的な`supports / medium / design-reviewed`を追加しました。
Framework mapping総数は79件のままです。PS.3.1を満たすrelease preservation controlは現行ポートフォリオに存在せず、PSB-REL-001へ機械的に移していません。

### 2026-09-22：SOURCE-001の端末管理コントロールを追加

[Developer endpoint trust](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)を追加し、先行した設計の11項目を8特性へ整理しました。
[29項目の対応表](ENDPOINT_MIGRATION.md)は、control移行11・隣接13・保留5を追跡します。
診断で確認する項目を記載し、コード実行や端末への導入を証拠として追加していません。

旧framework関係4件は版・ID・confidence・対象check・レビュー日・根拠を対応表に保持しました。
認証情報保管と依存取得の3件は隣接領域、SSDF PS.3.1はrelease保存との意味の不一致として新controlへ継承しません。
公式本文を確認したPO.5.2との部分的な設計関係を別途追加しました。合計18 control・18 pattern・78 framework mappingです。
参照資料の採否、索引、設計との対応、横断分析、次作業を更新しました。製品設定・収集器・実環境診断は保留です。

### 2026-09-22：独立化後の作業案内と異常時テストの方針を整理

独立化前の計画を、本PJを正本とする継続的な移行・執筆の手順へ更新しました。
現在地と次作業を移行計画へ集約し、候補一覧・構造レビュー・READMEからの案内を統一しました。
初回の順序とレビュー結果は履歴として保持します。次の主題はSOURCE-001の端末管理範囲のcontrol記録と旧framework関係の照合です。

利用者の指定により、診断で確認する項目はチェックリストだけでも完成する方針を明記しました。
詳細は[文書品質](CONTENT_QUALITY.md#failure-checks)を正本とし、実施済み・検証済みの証拠とは区別します。
新しいcontrol・pattern・製品実装は追加していません。保留している実装や実環境検証を完了扱いにはしません。

### 2026-09-21：独立化の準備

旧ツリーへのローカルMarkdown参照114箇所を、コミット`f429877`の完全SHAを含む外部リンクへ置き換えました。
参照先がそのGitオブジェクトに存在することを確認し、資料の版・採否・保留判断は維持しています。
単独で動く`make check`、検査器のテスト、既存実装テストの入口を追加しました。[切り出し手順](REPOSITORY_CUTOVER.md)に公開前の判断を残しています。
この記録は準備の完了であり、新しいリモートリポジトリの作成・push完了を意味しません。

### 2026-09-21：SOURCE-001の端末管理設計を先行移行

[ENG-SOURCE-002](../engineering/source-protection/managed-developer-endpoint/README.md)と[教材](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/learning.md)を追加しました。
旧29項目を[対応表](ENDPOINT_MIGRATION.md)で11項目の設計移行、13項目の隣接領域への受け渡し、5項目の保留へ分類しています。
提供原文、10項目baseline、リポジトリ独自の拡張を区別し、出典不明・利用条件未確認を[参照資料記録](../sources/README.md#ref-developer-endpoint-baseline-001)へ残しました。
Control記録と旧4件のframework関係、実装・収集器は未移行です。現在17 control・18 pattern・77 framework mappingです。実端末の検査や設定変更は行っていません。

### 2026-09-21：AI-002／AI-004の失効時の受け渡しを補修

拡張の採用承認と一回の操作承認を分け、失効対象の識別、情報の鮮度、新規呼出しの拒否、既存処理・認証情報の停止、送信済み操作の結果確認を[既存pattern](../engineering/ai-development-security/agent-extension-admission/README.md#失効を実行環境へ渡す)へ整理しました。
旧AI-002 metadataの「AI-004未移行」を修正。新規control・pattern・framework関係は増やしていません。17 control・17 pattern・77 mappingを維持します。実端末・token・外部操作には触れていません。

### 2026-09-20：AI-004のcontrol記録をガイダンス移行

[PSB-AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)を10特性へ再編集し、旧26項目を全てmetadataへ追跡可能にしました。以下の「未移行」は各時点の履歴です。
旧15件のframework関係は版・ID・関係・confidence・元の根拠を保持し、現在の設計との対応理由を分離しました。AISVS固定版の該当5要件を確認し、暗号学的結合は方式依存として保留しました。ATLAS・Agentic Top 10は旧レビューを継承し、上流taxonomyは再確認していません。
現在17 control・17 pattern、framework関係は77件です。製品adapter、実行テスト、実環境の隔離・認可・監査は未移行です。

### 2026-09-20：AI-004の残項目を既存設計へ再配置

AAR-012〜021、025〜026を既存ENG-AI-001〜003へ追補しました。Tool同一性と実行時一覧、承認の真正性と並行消費、接続先照合、監査と配送・通知の責任を分けています。
全26項目の追跡先とcontrol記録へまとめる方針は[AI runtime migration reconciliation](AI_RUNTIME_MIGRATION.md)に集約しました。旧資料の設定値・方式を一般要件へ変えず、変更した解釈と製品未検証の範囲をSourcesに記録しています。
前回まで保留した設計の棚卸しを進めたもので、control全体・framework mapping・実装の移行は引き続き未完了です。件数は16 control・17 patternを維持します。

### 2026-09-20：横断補修とAI-004の設計部分の先行移行

- DETECT-001のmappingは旧実装の根拠を`legacy_rationale`へ保存し、移行先のガイダンスが定義する判断と分離しました。版・ID・関係・confidenceは変更していません。
- 横断分析・候補一覧の移行状態を更新し、GOV-002の設計上の接続先をDETECT-001を含む3件へ揃えました。Scanner設計本文の日英混在も補修しました。
- 旧[AI-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)のAAR-008〜011、AAR-022〜024を、[ENG-AI-002](../engineering/ai-development-security/development-action-authorization/README.md)と[教材](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/learning.md)へ`split`。移行元は`3bfbeb21246bb2f58c55fa5212068805bca1719b`です。
- 上記は設計判断の再編集です。AAR-001〜007、012〜021、025〜026、全26項目のcontrol記録、旧実装・テスト・framework mappingの移植は`deferred`です。旧版の参照仕様は削除しません。
- 受入条件は、開発環境限定、迂回経路の前提、承認と実行の一致、評価失敗と結果不明の区別、旧項目の追跡可能性です。コードや製品設定がないため、形式的な実行テストは追加しません。
- Control記録は16件のまま、設計パターンは16件です。AI-004全体を移行済みとは数えません。製品固有の有効性、実運用、独立した読者評価は未確認です。

### 2026-09-20：AI-004の隔離設計を追加

旧AAR-001〜007を[ENG-AI-003](../engineering/ai-development-security/development-runtime-isolation/README.md)へ設計として先行移行しました。AAR-005の公開承認はENG-AI-002へ引き継ぎます。移行元は同じく`3bfbeb21246bb2f58c55fa5212068805bca1719b`です。
前項で保留したうち、この7項目の設計再編集を今回進めました。現在残る設計の棚卸し対象はAAR-012〜021、025〜026です。全26項目のcontrol記録、旧実装・テスト・framework mappingの移植は引き続き保留します。
受入条件は、操作認可との違い、ファイル・認証情報・通信・管理面の到達経路、Source Protection・Build・runnerとの責任分界、無害な導入確認方法と残余リスクの明示です。
製品設定と実行コードは追加していないため、架空の拒否試験は作りません。Controlは16件、patternは17件です。資料の版・採否は[参照資料](../sources/README.md#ref-development-runtime-isolation-001)に保持します。

### 初期pilotの対応表

| 旧成果物 | 扱い | 新しい成果物 | 補足 |
|---|---|---|---|
| `controls/source-protection/source-access-credential-lifecycle/README.md` | `split` | コントロール、学習資料、設計パターン、GitHub実装例 | 認証情報のライフサイクルに関する特性を保持し、導入手順をコントロールから分離。初期pilotで作成した独立insightは2026-09-25に撤去 |
| 同パッケージの`control.yaml` | `split` | 簡潔な`control.yaml`、フレームワーク対応関係 | 17件の確認項目をセキュリティ特性へ再編。参照していたフレームワークのバージョンとIDは保持し、新しい特性への割り当てをレビュー対象にした |
| 同パッケージの`secure/`、`insecure/`、検証器、期待結果 | `deferred` | なし | JSONメタデータの検査が実環境の権限制御を強化するか再評価するまで移さない |
| 同パッケージのGitHub導入手順 | `split` | GitHub実装例 | 製品固有の導入判断だけを再編集 |
| `REF-AI-004`、`REF-USER-001`、GitHubのフレームワーク登録情報 | `migrated` | 参照資料と仕様、フレームワーク対応関係 | 固定コミット、バージョン、採用範囲、制約を保持 |
| `controls/dependency-security/release-cooldown/README.md` | `split` | コントロール、学習資料、設計パターン、npm実装例 | 待機期間が保証することと、npm／プロキシ固有の手順を分離。初期pilotで作成した独立insightは2026-09-25に撤去 |
| 同パッケージの`control.yaml` | `split` | 簡潔な`control.yaml`、フレームワーク対応関係 | 待機期間、プロキシ、完全性の境界を再編。MITRE／SSDFのバージョンとIDは保持 |
| 同パッケージのポリシー用データ、プロキシクライアント、汎用検証器 | `deferred` | なし | 価値のある実装例を選ぶまで一括では移さない |
| npmプロジェクト設定 | `migrated` | npm実装例 | 小さな具体例として分離。実際に有効な挙動は採用環境で確認する |
| `REF-DEPS-001`、`REF-DEPS-004`、パッケージマネージャー仕様、インシデント資料 | `migrated` | 参照資料と仕様 | コミュニティの一覧と公式製品仕様を区別し、変更され得る資料を再レビュー対象にした |
| `docs/SECURITY_GUIDANCE_SOURCES.md`の`REF-AI-003` | `split` | `REF-PORTFOLIO-001`、横断分析の軸、機械可読な分析マッピング | AI固有資料ではなく、七つのレイヤーでポートフォリオ全体を確認する資料として改称。旧IDはこの移行記録にだけ残す。製品候補、KPI、フレームワーク名は要件へ自動変換しない |
| `docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md` | `split` | 参照資料記録、横断分析の軸、機械可読な分析マッピング | 十二の攻撃段階と代表経路を採用。試作対象外のコントロールを移行済みとは扱わない |
| パイロット対象外の`REF-*`記録 | `deferred` | 旧参照資料一覧 | 削除せず、対応するコントロールまたはパターンの移行時に記録単位で移す |
| `controls/cicd-security/untrusted-pr-boundary/README.md` | `split` | コントロール、学習ノート、設計パターン、GitHub Actions実装例 | 未信頼状態のproducer／consumerと権限境界を本質として再編集 |
| 同パッケージの`control.yaml` | `split` | 簡潔な`control.yaml`、フレームワーク対応関係 | 6件の確認項目を6特性へ再配置。GitHub guidanceとOSPSの版、ID、関係を保持し、割り当てをレビュー対象にした |
| 同パッケージのworkflow例 | `split` | GitHub Actions実装例の`secure/`と`insecure/` | 無権限PR検証とmerge後のfresh runを保持。危険な比較例は直接的な境界越えに絞り、自動有効化しない位置へ隔離 |
| `REF-CICD-005`、`REF-CICD-010`、対応するGitHub／OSPS仕様 | `migrated` | 参照資料と仕様、フレームワーク対応関係 | 固定版、旧レビュー日、採否、制限を保持。現在の製品挙動や導入済み状態は別途確認する |

## 今後の移行

### 追加移行：Workload federation boundary

基準は`3bfbeb21246bb2f58c55fa5212068805bca1719b`。旧パッケージに未コミット変更がないことを確認した。

| 旧成果物 | 扱い | 新しい成果物・境界 |
|---|---|---|
| `controls/cicd-security/audience-bound-oidc-federation/README.md`、`control.yaml` | `split` | PSB-CICD-006、学習ノート、ENG-CICD-002。8旧checkを6特性へ再配置、4framework関係を保持、割当はレビュー中 |
| AWS trust policy | `migrated` | GitHub Actions / AWS実装例の小さなJSON。Exact subject・audienceを保持し、Environmentだけではbranch・workflowが限定されないと明記 |
| Workflow・role permissions・Terraform手順 | `split` | 設定値・権限判断・公式仕様を製品別ガイダンスと参照記録へ分離。全面的なコード移植は保留 |
| REF-CICD-009、GitHub・AWS・OIDC仕様 | `migrated` | 参照版、旧レビュー、採否・制約を保持。旧一覧のoffline replay契約と現行manual referenceの差を明記 |

旧keyの削除をprovider側の無効化と混同しないよう明確化した。派生session・窃取時の復旧は隣接責任であり、
この試作版でlive交換・拒否・失効を確認したとは扱わない。

### 追加移行：Reviewed dependency intake

基準コミットは`3bfbeb21246bb2f58c55fa5212068805bca1719b`。旧二パッケージに未コミット変更がないことを確認して再編集した。

| 旧成果物 | 扱い | 新しい成果物・判断 |
|---|---|---|
| `controls/dependency-security/lockfile-integrity/README.md`、`control.yaml` | `split` | PSB-DEPS-003、そのcontrolの教材、ENG-DEPS-003。5旧checkを5特性へ再配置し、3件のframework関係を保持 |
| 同パッケージのnative wrapper、runtime metadata、tamper test、期待結果 | `deferred` | 製品仕様と旧対応状態を保持。小さな独立実装として再レビューするまで一括では移さない |
| `controls/dependency-security/dependency-change-review/README.md`、`control.yaml` | `split` | PSB-DEPS-004、そのcontrolの教材、ENG-DEPS-003。3旧checkを3特性へ再配置し、5件のframework関係を保持 |
| GitHub workflow | `migrated` | 製品別実装へfull SHA・最小権限・基本policyを保持。Live graphとmerge拒否は外部確認手順で扱う |
| `REF-DEPS-002`、native lock仕様、SLSA／SCVS／CISA等の隣接資料 | `migrated` | 版・ID・採否・除外理由と参照リンクを保持。参照一覧の拡張提案と基本workflowの範囲差を明記 |

当初は一つの共有教材にしたが、2026-09-25にartifact identityとchange reviewの問いへ分割し、各controlの隣へ移した。
Hash検証と脆弱性判定の合格を互いの代替にせず、mappingの特性割当はレビュー中とする。

### 初回の追加移行：Install execution policy

| 旧成果物 | 扱い | 新しい成果物・境界 |
|---|---|---|
| `controls/dependency-security/install-script-execution/README.md`、`control.yaml` | `split` | `PSB-DEPS-002`、学習ノート、`ENG-DEPS-002`。5件の旧checkを4特性へ再配置し、framework版・ID・関係を保持。割当はレビュー中 |
| pip設定・実装ガイド | `split` | pip実装例、wheel限定・hash確認の設定snippet、ローカルの候補選択・backend起動抑止テスト。実環境導入は別途確認 |
| npm、pnpm、Bun設定、汎用設定検証器 | `deferred` | 製品仕様へのリンクと採否は保持。現行挙動を再確認するまで設定・検証器は移さない |
| OWASP、CISA、OSPSの関連資料 | `migrated` | 参照資料記録として保持。OSPSは旧来の候補のまま、direct mappingを追加しない |

追加移行の基準コミットは`3bfbeb21246bb2f58c55fa5212068805bca1719b`です。
作業時の旧パッケージに未コミット変更がないことを確認し、三件のpilotの基準とは分けて記録します。

以後の作業順序、参照資料の名称改革、完了判定は[移行計画](MIGRATION_PLAN.md)を参照してください。

### 追加移行：CI state and runner lifecycle

基準コミットは`3bfbeb21246bb2f58c55fa5212068805bca1719b`。旧パッケージは変更せず、判断材料を再編集した。

| 旧成果物 | 扱い | 新しい成果物・境界 |
|---|---|---|
| `controls/cicd-security/runner-hardening/README.md`、`control.yaml` | `split` | PSB-CICD-007、そのcontrolの教材、ENG-CICD-003。9旧checkを9特性へ配置、6framework関係を保持 |
| `controls/cicd-security/cache-provenance-isolation/README.md`、`control.yaml` | `split` | PSB-CICD-009、そのcontrolの教材、同pattern。7旧checkを7特性へ配置、3framework関係を保持 |
| workflow、provisioner、marker test、期待結果 | `deferred` | 旧参照版を保持。Providerの実効cache設定、compute・storageの破棄、実際の否定ケースを再確認してから独立実装へ移す |
| `REF-CICD-014`、`REF-BUILD-001`、cache製品仕様、SITF | `migrated` | 参照版・リンク・採否・限界をsourcesへ保持。runtime sensorは候補のまま |

当初の共有教材は2026-09-25にrunner lifecycleとcache trustの問いへ分割し、各controlの隣へ移した。
GitHubの現在のcache仕様は確認したが、組織のcache、runner割当・破棄、ネットワーク制限を実測したとは扱わない。
16チェックと9mapping関係の保持は移行の完全性の確認であり、導入の証拠ではない。特性割当はレビュー中。


### 追加移行：Build containment

| 旧成果物 | 扱い | 新しい成果物・境界 |
|---|---|---|
| `controls/build-security/build-containment/README.md`、`control.yaml` | `split` | PSB-BUILD-001、教材、ENG-BUILD-001。6旧checkを6特性へ配置し、3件のframework版・ID・関係を保持。割当はレビュー中 |
| JSON計画、検証器、tests、期待結果 | `deferred` | 宣言の検査と実行時強制を区別。実sandbox・通信・telemetryを確認するadapterとしては移植しない |
| GitHub・SLSA参照、SSDF／OSPS mapping、REF-BUILD-001 | `migrated` | Sourcesに参照版・採否・限界を保持。SLSA Build trackのみ。Sensorは候補のまま |

基準コミットは`3bfbeb21246bb2f58c55fa5212068805bca1719b`。旧パッケージは未変更。
2026-09-17にSLSA v1.2の参照箇所を確認したが、実環境の隔離・通信拒否・収集・配送は未確認。
ローカルの構造・リンク・旧対応の保持確認は、組織導入の証拠ではない。


### 追加移行：Consumer artifact acceptance

| 旧成果物 | 扱い | 新しい成果物・境界 |
|---|---|---|
| `controls/release-integrity/signature-provenance-verification/README.md`、`control.yaml` | `split` | PSB-REL-001、教材、ENG-REL-001。5旧checkを5特性へ配置、4framework関係を保持。ACCEPT-5は旧来通りdirect mappingなし |
| Ed25519 fixture、crypto verifier、tests、期待結果 | `deferred` | 現行ツリーの公開鍵欠落とOpenSSL非ゼロ終了の一括分類を確認。実装を修正・移植せず再レビューへ保留 |
| SLSA、npm仕様、SSDF／OSPS | `migrated` | 版・リンク・採否・隣接境界をsourcesに保持。SLSA level、keyless、実使用gateは未確認 |

基準コミットは`3bfbeb21246bb2f58c55fa5212068805bca1719b`。旧パッケージは未変更。
2026-09-17の確認は仕様と構造・リンク・旧関係の保持に限り、実署名照合・拒否・組織採用を確認したとは扱わない。


### 新規構造検証：Application authorization

移行元controlはなし。`ENG-DESIGN-001`、教材、Python / SQLite限定実装を新規追加した。
既存の計画済み`PSB-CODE-*` IDは使わず、REF-USER-004の原本未提供は変更しない。
OWASPの設計入力とリポジトリ独自のシナリオを分け、ASVSのexact mappingは意味的レビューまで追加しない。
Python 3.10.4で7テスト成功。実DB queryの許可・拒否・拒否後の不変性をローカルで確認した。HTTP認証や組織採用の証拠ではない。

### 追加移行：Runtime detection to triage

| 旧成果物 | 扱い | 新しい成果物・境界 |
|---|---|---|
| `controls/container-cloud-iac-security/runtime-threat-detection/README.md`、`control.yaml` | `split` | PSB-CONTAINER-004、教材、ENG-RUNTIME-001。12旧checkを12特性へ配置、1framework関係を保持。割当はレビュー中 |
| Falco／Sysdig normalizer、verifier、synthetic fixture、tests | `deferred` | Liveのevent・health契約を再レビューしてから独立実装へ。Fixtureを本番導入・通知・対応の証拠にしない |
| REF-CONTAINER-003／004、NIST SP 800-190 | `migrated` | 旧参照版・URL・採否・限界を保持。現在の製品contractは本文取得不足のため再レビューが必要 |
| GOV-001、FIRST・NIST incident・SBOM資料 | `deferred` | ENG-RUNTIME-001の製品適用・組織対応への入力として旧正本を参照。Controlや能力評価は未移植 |

基準コミットは`3bfbeb21246bb2f58c55fa5212068805bca1719b`。旧controlは変更せず、live sensor・通知・triage・対応操作は未確認。



### GOV-001追加移行（2026-09-17）

[Control](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)、教材、ENG-GOV-001へ分離。7件のINC checkをIMPACT-1〜7へ継承し、旧mappingの版・ID・関係・対象を保持した。
旧REF-REL-001・REF-REL-002・REF-USER-005の関連入力はREF-SUPPLY-CHAIN-IMPACT-001へ集約し、仕様・採否・旧確認日を残した。旧adapter、live API、collector、実対応、組織能力評価は保留。上のdeferred記録はruntime移行時点の履歴であり、この追加移行でcontrol部分のみ更新した。

### GOV-002追加移行（2026-09-20）

[Control](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)、[教材](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/learning.md)、[ENG-GOV-002](../engineering/governance-operations/security-exception-decision-boundary/README.md)へ分離しました。旧GEX-001〜008をEXCEPTION-1〜8へ一対一で継承し、旧framework mappingの版・ID・関係・confidence・対象を保持しています。
旧verifier、fixture、`psb-security-exception/v1`、30日上限は実装候補として保留しました。Live approval、信頼時刻、取消、policy engine、実gateの採用は未確認です。

### GOV-002 consumer接続（2026-09-20）

PSB-DEPS-001 `DEP-AGE-6`とPSB-DEPS-002 `DEP-EXEC-2`を、[exception consumer mapping](../mappings/exception-consumers.yaml)でGOV-002へ接続しました。
元の不合格property、exact target identity、control側に残すrisk判断、例外でも許可しない範囲を明示しています。Live enforcementは未確認で、他controlは意味的レビュー前にconsumerへ追加していません。

### DETECT-001追加移行（2026-09-20）

[Control](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)、[教材](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md)、[ENG-DETECT-001](../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)へ分離しました。
旧DVS-001〜008をSCAN-1〜8へ一対一で継承し、5件のframework mappingの版・ID・関係・confidence・対象を保持しています。旧`REF-DETECT-001..003`は役割名`REF-SCANNER-EVIDENCE-001`へ統合し、旧版、digest、採否、限界を残しました。
Trivy、DockSec、Checkovの旧adapter・fixtureは保留し、現行配布物、live DB、coverage、CI gateを検証済みとは扱いません。SCAN-6だけをGOV-002のconsumerへ接続しました。

### AI-002追加移行（2026-09-20）

[Control](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)、[教材](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/learning.md)、[ENG-AI-001](../engineering/ai-development-security/agent-extension-admission/README.md)へ再編集しました。
旧AID-001〜007をEXT-1〜7へ一対一で対応付け、脅威・対象・必要な理由を保持しています。旧metadata verifierの入力形式は保証目標にせず、内容審査の記録と審査の質、benchmarkの記録と実際の評価、承認と実行時の強制を区別しました。
旧REF-AI-001・REF-AI-002の今回関連する判断をREF-AGENT-EXTENSION-ADMISSION-001へ集約。既存REF-AI-004は正本への参照を維持し、資料全体の移行完了とは扱いません。
ATLAS `2026.05 (format 6.0.0)`の2件、Agentic Top 10 `2026 / ASI04`の1件、AISVS `1.0 / v1.0-C10.1.1..2`の2件は、旧関係・confidence・根拠・対象・レビュー日を保持した`migration-review-required`です。AISVSの`verifies`は旧関係を表し、今回の文書移行で検証した意味ではありません。
合成artifact、verifier、benchmark、revocation collectorは保留。旧AI-001・AI-003・AI-004は未移行の隣接境界として残し、製品固有設定・tool・外部サービスを導入していません。

### AI securityの担当範囲を限定（2026-09-20）

利用者の指示に基づき、[Security scope](SECURITY_SCOPE.md)を新設しました。AI Development Securityは開発端末・IDE・CLI・repository・CIでAIを使う開発環境に限定します。
製品自体のAI securityは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)の担当です。旧AI-010・AI-011・DEPS-005・DETECT-002は`out-of-scope`、旧AI-005〜009は開発環境に必要な部分の`scope-review-required`へ変更しました。
移行済みAI-002と16件の記録は維持します。前回報告の旧52件・差分36件は全件移行の残作業数として使いません。一般的なApplication Securityと本番監視は引き続き対象です。
旧成果物・参照仕様の削除や別PJへの移植は行っていません。別PJの個別coverageは今回検証していません。

### 主題ごとの具体化判断とSOURCE-002実装計画（2026-09-23）

利用者の指摘を受け、[成果物モデル](ARTIFACT_MODEL.md#主題ごとの具体化判断)に必要な具体実装を選ぶ基準を追加しました。
全controlへの実装義務と、全実装の一律保留を避け、文書の完成と選んだ成果物の残作業を区別します。
SOURCE-002は文書・確認項目の作成済みから、具体実装を残作業に持つ主題へ更新しました。
旧scanner・wrapper・installerの採否は再レビューで決めます。[計画](MIGRATION_PLAN.md#source-002の具体実装計画)を追加した段階で、実装移植・hooks有効化・実診断は未実施です。

### SOURCE-002代表実装（2026-09-23）

[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しました。
Gitleaks 8.30.1へ検出を集約し、独自PythonはGit objectの列挙、上限・未対応形式の拒否、scanner結果の整合確認へ限定しています。
旧独自検出ルール、Docker wrapper、installer、fixtureを移植しておらず、旧実装との検出同等性は主張しません。
一時worktreeとbare repositoryで23件が成功しました。本PJ自身のhooks、本番repository、SaaS設定は変更しておらず、組織への導入証拠ではありません。

## 未決定の設計事項

1. コントロールIDを長期的に`PSB-*`のまま維持するか。
2. `Source credential lifecycle`という主題を、対話型ID、自動化用ID、失効へ分割するか。
3. 依存関係の待機期間と、管理プロキシを通すことを別コントロールにするか。
4. 個別の導入確認項目を、コントロールのメタデータではなく評価へ移すか。
5. セキュリティ特性へ暫定的に再配置したフレームワーク対応関係を、どの単位で再レビューするか。
6. 七つのレイヤーと十二の攻撃段階を、将来の生成索引へ含めるか。

## 参照資料の移行ルール

コントロールを短くすることと、参照仕様を減らすことは別です。仕様、分類体系、製品ガイダンス、
利用者提供資料、インシデント調査は[`参照資料と仕様`](../sources/README.md)へ移し、コントロール、実装例、
マッピングから参照資料IDで参照します。資料を採用しない場合も、重要な除外判断は削除せず理由を残します。
