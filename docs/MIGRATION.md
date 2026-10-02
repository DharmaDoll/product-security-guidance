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

### 2026-10-03：GOV-001のframework関係を再照合

[Supply-chain impact assessment](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)の旧三関係を、[NIST SSDF 1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の`RV.1.1・RV.2.1`と[MITRE ATT&CK T1195.001](https://attack.mitre.org/techniques/T1195/001/)に照合しました。現行mappingにはSSDFの二関係を`supports / medium`の部分的な設計関係として残します。`RV.1.1`はcredible reportを受けた後の対象版と成果物・稼働先の調査に限定し、情報の継続収集や全報告の調査完了を含めません。`RV.2.1`はリスク対応計画へ渡す適用性・未確認範囲の情報に限定し、悪用可能性・被害規模の評価、優先度・対応の決定と実行を含めません。旧二関係の`high`は`medium`へ変更し、対応する特性を絞りました。

旧ATT&CK `v19.1 / T1195.001 / detects / medium`は非継承です。既知の汚染版をSBOMへ照合して利用先を特定するのは被害範囲の調査であり、攻撃者による依存・開発ツール改変を検知した証拠にはなりません。脅威シナリオの参照は[GOV-001の資料記録](../sources/README.md#ref-supply-chain-impact-001)に残します。新しい実装・テストコードは追加せず、実inventory・稼働先の網羅性や対応の実施は未確認です。

### 2026-10-03：DETECT-001のframework関係を再照合

[Scanner evidence trust boundary](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)の旧五関係を、[NIST SP 800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)、[NIST SSDF 1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)、[OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19#osps-vm-0602)へ照合しました。現行mappingにはNIST SP 800-190 `4.1.1 / supports/medium`だけを残し、`SCAN-2・3・4`がイメージ検査の対象・データ・範囲・完了状態を扱う部分的な設計関係としました。イメージの全層検査、build・registry・runtimeの継続可視性、方針gateは示しません。

旧SSDF `RV.1.1 / supports/high`は脆弱性情報の継続収集・調査であり、結果の信頼性を定めるだけでは足りません。旧SSDF `PW.4.1 / supports/medium`は製品へ取り込む第三者部品の採用・維持であり、scanner自身の選定と取得は対象が異なります。旧OSPS `VM-06.02 / supports/medium`は全コード変更の自動評価と違反時の拒否を求め、DETECT-001はその実行・強制を保証しません。旧NIST SP 800-190 `4.4.1 / supports/medium`は稼働中のcontainer runtimeのCVE監視・修復・保守されたruntimeへの配置を扱い、artifact検査結果の扱いだけでは満たしません。これら四関係を非継承とし、旧版・confidenceをこの台帳に保持します。新しい実装・テストコードは追加せず、liveのscanやCI拒否は未確認です。

### 2026-10-03：DEPS-004のframework関係を再照合

[Dependency change review](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)の旧五関係を、[OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19#osps-vm-0503)、[NIST SP 800-218](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)、[MITRE ATT&CK T1195.001](https://attack.mitre.org/versions/v19/techniques/T1195/001/)の本文と現行特性へ照合しました。[現行mapping](../mappings/frameworks.yaml)にはOSPS `VM-05.03 / supports/medium`の変更依存に対する既知脆弱性gateと、SSDF `PW.4.1 / supports/medium`の第三者部品採用レビューだけを、部分的な設計関係として残します。SSDFの対応propertyは`DEP-REVIEW-1・2`であり、merge gateの`DEP-REVIEW-3`をSSDF要件とはしません。

旧OSPS `VM-05.01 / supports/medium`は脆弱性・ライセンス両方のSCA所見に関する文書化された是正閾値を扱い、DEPS-004はこれを要求しないため非継承。旧`VM-05.02 / supports/high`はrelease前のSCA違反対応方針を扱い、変更依存のmerge前判断と時点・対象が異なるため非継承。旧ATT&CK `v19.1 / T1195.001 / mitigates/medium`は悪意ある依存・開発ツール改変に対し、既知脆弱性の差分gateだけで直接の緩和を主張できないため非継承です。旧版・confidenceをこの台帳に保持します。新しいcontrol・実装・テストコードは追加せず、実GitHubの拒否、悪意ある依存の検知、OSPS・SSDF適合性は確認していません。

### 2026-10-03：DEPS-003のframework関係を再照合

[Dependency artifact identity](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)の旧三関係を、ATT&CK T1195.001、NIST SSDF PW.4.1、OpenSSF OSPS BR-05.01の公式本文と現在の特性へ照合しました。[現行mapping](../mappings/frameworks.yaml)には、レビュー後の再解決・取得物差し替えに限定したATT&CK `mitigates/medium`を残し、取得物の完全性確認に対応するSSDF `PW.4.4 / supports/medium`を新しく記録しました。旧`PW.4.1 / supports/high`は部品の取得・維持と安全性の評価へ広すぎるため非継承、旧`OSPS-BR-05.01 / supports/medium`は標準ツール使用をDEPS-003の必須特性が要求しないため非継承です。旧関係の版と判断はこの台帳に保持します。

Hash一致は事前に承認したbytesとの一致であり、悪意ある内容、publisherの正当性、実際の全platform・依存経路の強制、SSDFまたはOSPSへの準拠を証明しません。新しい実装例・テストコードは追加せず、通常buildの実動作は未確認です。

### 2026-10-02：DEPS-002のframework関係を再照合

[Install execution policy](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)の旧2関係を[ATT&CK T1195.001](https://attack.mitre.org/versions/v19/techniques/T1195/001/)と[NIST SSDF PW.4.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の本文へ照合しました。ATT&CKの旧`mitigates/high`は、依存取得後の準備時実行を止める部分的な設計関係として`mitigates/medium/design-reviewed`へ変更しました。`DEP-EXEC-4`の評価不能時に許可しない判断も対応propertyへ加えました。後続のimport・testと開発ツール侵害は対象外です。

SSDF `PW.4.1`の旧`supports/high`は非継承とします。このtaskは安全な第三者部品の取得・維持、用途別評価、来歴、承認済み部品、更新を扱います。DEPS-002の準備処理の実行制御だけでは、これらの部品評価を直接支える関係を説明できません。部品の内容や出所を扱うDEPS-003・004の関係は別に再評価します。Control・pattern・pip実装例は既存のまま、実際のCIや開発端末での拒否は未確認です。

### 2026-10-01：DEPS-001のframework関係を再照合

[Dependency release cooldown](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)の旧ATT&CK T1195.001・NIST SSDF PW.4.1関係を、両者の公式本文と現在のDEP-AGE-1〜5へ照合しました。[Mapping](../mappings/frameworks.yaml)では二件を部分的な設計関係として記録し、例外管理のDEP-AGE-6を対応根拠から外しました。待機期間は公開直後の悪意ある版の自動採用を遅らせるものです。悪意ある版の検知、開発ツールの侵害、用途別レビュー、来歴、SSDF準拠は示しません。新しいcontrol・実装・テストコードは追加せず、実環境の強制は未確認です。

### 2026-10-01：Codex CLIのhardening観点をAI-004へ追加

利用者提供の[Codex CLI Hardening Cheatsheet](../sources/README.md#ref-codex-cli-hardening-001)を、既存のClaude Code版と同じく製品別の参考資料として記録しました。Trusted repositoryの設定優先順位、shell以外の通信、設定・履歴の残留を[AI-004の教材](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/learning.md)と[隔離設計](../engineering/ai-development-security/development-runtime-isolation/README.md)へ反映しました。Controlの新規特性・Codex設定例・実装例は増やしていません。現在の公式仕様と食い違う旧設定例は移植せず、実環境の強制は未検証です。

### 2026-09-30：SOURCE-004の失効対象を照合

SOURCE-001から受け取る端末状態の悪化を起点に、元の認証情報、組織への認可、既存セッション、別に残る鍵・アプリ権限を分けました。Controlに診断項目を追加し、教材・pattern・GitHub実装案を補修しました。GitHubの可変な公式資料は[Sources](../sources/README.md#spec-github-security-guidance)に確認日と限界を記録し、旧固定版のframework mappingは変更していません。実組織の失効や拒否は未確認です。[具体化判断](MIGRATION_PLAN.md#source-004の読み合わせと具体化判断)を参照してください。

### 2026-09-30：SOURCE-001の端末状態と継続アクセスを照合

旧Linux assessmentと移行済みcontrol・教材・patternを読み合わせました。登録、現在の観測、資産側のアクセス判断の区別を維持し、状態悪化時に新規ログインだけを止めて既存セッションが残る経路を明示しました。旧adapterは一部のOS設定を実際に読みますが、MDMと資産側の制限を観測しないため移植しません。今回の具体化判断は[計画](MIGRATION_PLAN.md#source-001の読み合わせと具体化判断)、旧項目の扱いは[移行対応表](ENDPOINT_MIGRATION.md)に記録しています。

### 2026-09-29：DETECT-001の指摘と解析失敗を照合

旧DVS-001〜008から移行したscanner証拠のcontrol・教材・patternを読み合わせました。必要な対象の一部で指摘が出て別の対象が解析不能な場合、検査全体を評価不能として受入を止め、既知の指摘も残す判断を補いました。旧adapterやfixtureを移す判断は変更せず、新しい実装例・テストコードは追加していません。[具体化判断](MIGRATION_PLAN.md#detect-001の読み合わせと具体化判断)と[Sources](../sources/README.md#ref-scanner-evidence-001)に範囲を記録しました。

### 2026-09-29：DETECT-003の部分観測と候補の状態を照合

旧Python verifierの候補照合・再出現判定と、移行済みcontrol・教材・patternを読み合わせました。部分取得で得た新候補は調査に残し、取得できなかった範囲の既存候補は消さない条件を補いました。台帳取得や全ページ確認に失敗した回を全件一致・是正完了にしません。旧collector不在と固定profileの非移植判断は維持し、新しい実装例・テストコードは追加していません。[具体化判断](MIGRATION_PLAN.md#detect-003の読み合わせと具体化判断)と[旧成果物の採否](EXTERNAL_ATTACK_SURFACE_MIGRATION.md)を参照してください。

### 2026-09-29：DESIGN-001の請求書例とASVSを照合

移行元controlを持たないObject access authorizationのpilotを読み合わせました。既存Python／SQLite例のテスト手順を現行pathへ直し、教材からの導線を整理しました。ASVS 5.0.0固定版のV8.2.1・V8.2.2を意味的に確認し、操作scopeと対象データのowner・tenant条件に限って二件の部分mappingを追加しました。Framework mappingは118件です。HTTP認証、全endpoint、組織への導入を示す関係ではありません。判断と未確認範囲は[計画](MIGRATION_PLAN.md#design-001の読み合わせと具体化判断)に記録しています。

### 2026-09-29：CODE-005の表示上の改行を再確認

旧Unicode source deceptionから移行したcontrol・教材・patternとPython限定実装を読み合わせました。既存scannerがコメント内の表示上の改行5種類を`PASS`にする見落としを補修し、位置とcode pointを報告する診断項目へ反映しました。旧6項目やSITF mappingの採否は変更せず、全言語の一律拒否にも広げません。詳細は[計画](MIGRATION_PLAN.md#code-005の読み合わせと具体化判断)と[Unicode移行記録](UNICODE_SOURCE_MIGRATION.md)に保持しています。

### 2026-09-29：IAC-001の保存planとapply結果を照合

旧Secure IaC Golden Pathの利用者提供資料、移行済みcontrol・教材・patternとTerraform公式のplan／apply仕様を再確認しました。保存planの指定前に承認記録とplan・targetを照合し、途中失敗後も一部変更を確認する条件を補いました。旧multi-cloud JSON verifierは引き続き非移植で、provider未選定の新しい実装例は追加していません。判断と実環境で未確認の範囲は[計画](MIGRATION_PLAN.md#iac-001の読み合わせと具体化判断)と[IaC移行記録](IAC_CHANGE_BOUNDARY_MIGRATION.md)に保持します。

### 2026-09-29：CONTAINER-005〜007の既存Kubernetes例を再確認

旧CONTAINER-001の`CNT-003..008`から分けた権限・network・resourceの三主題を照合しました。旧checkとframework関係は増やさず、既存教材の入口を平易にし、Kubernetes例の既存対象保護、network拒否時の宛先健全性、container単位budgetという選択を補修しました。追加実装を増やすより、既存例が何を観測し、何をまだ示さないかを明確にする判断です。

旧項目の採否は[Workload confinement](WORKLOAD_CONFINEMENT_MIGRATION.md)、[Network segmentation](NETWORK_SEGMENTATION_MIGRATION.md)、[Resource consumption](RESOURCE_CONSUMPTION_MIGRATION.md)、今回の具体化判断と実環境の未確認範囲は[計画](MIGRATION_PLAN.md#container-005007の読み合わせと具体化判断)に記録しました。47 control・47 pattern・116 framework mappingは保持しています。

### 2026-09-28：CONTAINER-003・004のnodeとruntime検知を照合

旧CONTAINER-003の移行先と、旧runtime threat detectionの12項目を読み合わせました。Host管理面がsensorの信頼へ与える影響、eventの対象ID欠落と稼働inventoryの照合、観測障害と検知なし、検知結果からGOV-001の影響調査・必要時のGOV-005のartifact置換への受け渡しを補いました。CONTAINER-004へ診断項目を追加し、旧fixture由来の固定した署名付き試験eventやdropゼロを普遍要件にしません。

NIST SP 800-190 §4.4.4の旧`RUNTIME-1..10 / detects / high`を`RUNTIME-2,3,4,7 / supports / medium / design-reviewed`へ再評価しました。Framework関係の件数は116件のままです。旧checkと合成adapterの非移植、47 control・47 patternも保持します。判断、資料の採否、live未確認の範囲は[計画](MIGRATION_PLAN.md#container-003004の読み合わせと具体化判断)と[Container host移行記録](CONTAINER_HOST_DAEMON_MIGRATION.md)へ記録しました。実装・テストコードは追加していません。

### 2026-09-28：CONTAINER-001・002の公開と使用許可を照合

旧CONTAINER-001・002の移行先を読み合わせ、OCI image indexと選択manifest、公開・保持・使用可否を分けました。`deprecated`を一律拒否と読める表現を直し、使用停止の判断をadmissionへ渡す条件と[GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)の稼働観測への受け渡しを補いました。両control配下に教材を追加しました。

旧checkとframework関係、47 control・47 pattern・116 framework mappingは保持しています。文書と診断項目で今回の範囲を完了し、実装・テストコードは追加していません。資料の採否、旧実装の非移植、実環境で未確認の範囲は[計画](MIGRATION_PLAN.md#container-001002の読み合わせと具体化判断)、[registry移行記録](CONTAINER_REGISTRY_MIGRATION.md)、[admission移行記録](DEPLOYMENT_ARTIFACT_ADMISSION_MIGRATION.md)に保持しています。

### 2026-09-28：GOV-002・005の例外と復旧完了を照合

旧GOV-002・005の移行先を読み合わせました。GOV-002では旧YAML形式・固定SHA-256・旧schema versionを必須としていた機械可読記録を、本文の製品非依存な判断へ揃え、診断項目を追加しました。GOV-005へ[旧digestが残る場面の教材](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md)を追加し、新digestの配布と旧digestの非稼働、GOV-003の元の期限とGOV-002の一時使用許可を分けました。

[GOV-003・005の例外consumer関係](../mappings/exception-consumers.yaml)を設計上の関係として追加しました。旧check ID、framework関係、47 control・47 pattern・116 framework mappingは保持しています。文書と診断項目で今回の範囲を完了し、実装・テストコードは追加していません。参照資料と実環境で未確認の範囲は[計画](MIGRATION_PLAN.md#gov-002005の読み合わせと具体化判断)、旧Recoveryの採否は[移行記録](DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md)に記録しました。

### 2026-09-28：GOV-001・003の影響調査と優先順位を照合

旧GOV-001・003の移行先を読み合わせ、検索0件の意味を収集範囲、取込・分析状態、検索範囲、稼働観測から再確認しました。[GOV-001教材](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/learning.md)を読みやすくし、[GOV-003教材](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/learning.md)をcontrol配下に追加しました。影響候補・範囲付き非該当・調査不能を区別し、後者の再調査担当・期限と暫定判断へ渡す設計に補修しました。

旧check IDとframework関係を保持し、47 control・47 pattern・116 framework mappingは変わりません。文書と診断項目を今回の成果物とし、実データ取得・対応のためのコードは追加していません。旧関係と採否は[Vulnerability priority移行記録](VULNERABILITY_PRIORITY_MIGRATION.md)、確認範囲は[計画](MIGRATION_PLAN.md#gov-001003の読み合わせと具体化判断)を参照してください。

### 2026-09-28：REL-003・004の取得地点・受入・分析を照合

利用者提供のSBOM lifecycle資料を固定commitから読み直し、既存教材と設計を補修しました。生成段階とhashの記載だけで完成物の収集を証明せず、共通base imageや供給者のSBOMを最終製品全体の一覧とは分けます。Dependency-Track 4.14.3のソース確認を受け、取込完了と後続分析完了の説明を分離しました。

既存CycloneDX実装のREADMEへ最短コピー手順と検査範囲を補い、9テストと使い捨てrepositoryでの導入・拒否・入力不足を確認しました。新規実装やテストコードは追加せず、REL-004は文書と診断項目で完了としました。旧check・framework関係は保持しています。採否は[Release SBOM](RELEASE_SBOM_MIGRATION.md)・[Supplier SBOM](SUPPLIER_SBOM_MIGRATION.md)、実運用で未確認の範囲は[計画](MIGRATION_PLAN.md#rel-003004の読み合わせと具体化判断)に記録しました。47 control・47 pattern・116 framework mappingです。

### 2026-09-28：REL-001・002・005の署名・配布・受入を照合

旧signature-provenance-verification、provenance-publication-distribution、artifact-signing-generationの移行先を読み合わせました。REL-001の診断項目と機械可読記録を補修し、署名が認証する対象、利用者の期待値、検証後の使用対象を区別しています。REL-002は既存教材を平易に書き直し、REL-005とともにcontrol・教材・設計を行き来できる案内を補いました。

旧check ID・framework関係を維持し、47 control・47 pattern・116 framework関係は変わりません。旧暗号fixtureや合成配布recordは移植せず、文書での完了と実環境の未確認を[移行計画](MIGRATION_PLAN.md#rel-001002005の読み合わせと具体化判断)へ記録しました。

### 2026-09-28：BUILD-001〜003の説明と来歴情報の出所を照合

旧build-containment、hosted-consistent-build、platform-provenance-generationの移行先を読み合わせました。BUILD-001の機械可読記録と本文を揃え、診断項目を追加。BUILD-003には[署名済みの自己申告を考える教材](../controls/records/build-security/psb-build-003-platform-provenance-generation/learning.md)をcontrol配下へ置き、三つの判断と後続consumerへつなぎました。

SLSA v1.2の再照合で、L3を例外なく全fieldがplatform由来と読める説明を修正しました。旧check ID・直接の仕様参照・framework関係は維持し、合成JSONやlocal署名の検査を基盤実装の証拠にはしません。47 control・47 pattern・116 framework関係を維持します。文書での完了と実環境で未確認の範囲は[移行計画](MIGRATION_PLAN.md#build-001003の読み合わせと具体化判断)へ記録しました。

### 2026-09-27：CICD-005・009・007の説明と既存GitHub例を照合

旧untrusted-pr-boundary、cache-provenance-isolation、runner-hardeningの行き先を読み合わせ、三つのcontrolへ診断項目を追加しました。既存のcontrol配下の教材と設計を補修し、外部cacheの復元とrunnerの残存状態、形式どおりのPR結果と独立した必須判断を分けています。

Cache・runnerの機械可読記録に残っていた製品profile固有の条件を本文へ揃え、旧check ID・参照資料・framework関係は保持しました。旧cache workflowやprovisionerは一括移植せず、具体的なGitHub条件は設計・資料記録へ残します。既存PR分離例にはcache不使用の設定とpush SHAのcheckout・照合を追加し、配置・確認・解除も具体化しました。危険な比較workflowは導入対象へ含めません。

具体化判断とローカル確認・実GitHubで未確認の範囲は[移行計画](MIGRATION_PLAN.md#cicd-005009007の読み合わせと具体化判断)へ記録しています。47 control・47 pattern・116 framework関係を維持します。

### 2026-09-27：DEPS-002〜004の説明を既存実装へ照合

旧install-script-execution、lockfile-integrity、dependency-change-reviewの行き先である三つのcontrol・教材・設計と、既存pip・GitHub例を読み合わせました。各controlに診断項目を追加し、更新の採用・内容の照合・準備コードの実行許可を分けています。教材は既存のcontrol配下で補修し、独立した洞察ファイルや新しい実装は作りません。

pipは既存状態を再利用するhash確認の限界を専用環境の導入へ戻し、固定Dependency Review Actionはsnapshot警告の期限後に判定を続ける制約を必須判断の接続条件へ戻しました。一次資料の追加確認と、ローカルの代表経路・実GitHubで未確認の範囲は[具体化判断](MIGRATION_PLAN.md#deps-002004の読み合わせと具体化判断)へ記録しています。旧native wrapperやsynthetic fixtureの一括移植を約束せず、47 control・47 pattern・116 framework関係を維持します。

### 2026-09-27：SOURCE-002・003の説明を既存実装へ照合

両control・設計・三つの既存実装を読み、[SOURCE-002の教材](../controls/records/source-protection/psb-source-002-secret-publication-boundary/learning.md)と[SOURCE-003の教材](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/learning.md)をcontrol配下へ追加しました。診断項目とローカルの実装確認、通知の配送と人の対応を区別し、参照資料の利用先と確認日を更新しています。

旧`scan-sensitive.py`から再編集したPython版に、merge結果で初めて追加された内容の検査漏れがあったため修正しました。公開情報監視はコードを増やさず、部分取得時の保存、検索失敗、再通知の限界と判断記録の外部分担を文書へ戻しました。具体化判断と確認範囲は[移行計画](MIGRATION_PLAN.md#source-002003の読み合わせと具体化判断)に記録しています。Control・pattern・framework関係は追加していません。

### 2026-09-27：移行状況と教材への導線を補修

[三領域の索引](MIGRATION_CANDIDATES.md)から古い候補・保留表記と現在状態の混在を除き、旧19件を現在の行き先へ結びました。SOURCE-003の限定実装とCICD-003の既存DETECT-001への配置も反映し、実導入が未確認であることと文書の完成を分けています。

全体一覧へIAC-001を追加し、既存11 domainの順序へ並べ直しました。三領域の入口から既存15教材へ直接進めるようにし、39教材のcontrol・設計への往復を確認しました。現在件数と次作業の正本を移行計画へ揃え、具体化判断を経ずに将来の実装を約束する案内も修正しました。新しいcontrol・教材・実装は追加していません。確認範囲は[構造レビュー](STRUCTURE_REVIEW.md#2026-09-27移行状況と教材への導線)に記録しています。

### 2026-09-27：CICD-003 Workflow analysisを既存要件へ配置

旧SAS-001〜005を、[DETECT-001](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)・その教材と[ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)へ分けました。共通要件とCI権限を重複したcontrolへせず、検査・結果表示・merge判断を選べる設計を残しています。機械可読記録に残った製品固有の署名方式・終了コード・fixture要求も本文へ揃えました。

文書と診断項目で完了とし、独自scanner・SARIF parser・導入workflowは追加しません。旧14 file・固定Actionの採否と2 framework関係は[移行判断](WORKFLOW_ANALYSIS_MIGRATION.md)、確認した一次資料は[Sources](../sources/README.md#spec-zizmor-workflow-analysis)へ記録しました。現在47 control・47 pattern・116 framework mappingです。実scanner・GitHubでの強制は未確認で、次は三領域の状態表記と教材・patternのたどりやすさをレビューします。

### 2026-09-27：CICD-002 Workflow input handlingを移行

旧INJ-001〜004を、[6特性のcontrol](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)、control配下の教材、[設計pattern](../engineering/cicd-security/workflow-data-and-command-boundary/README.md)、診断項目へ再編集しました。入力を変更できる主体と到達性、コード生成、引数の保持、許可する操作、呼出先の再解釈を分けています。

実効性を基準に必要な成果物を選び、今回は独自scanner・配布workflow・中央配布PoCを移しません。文書と診断項目で完了とし、実GitHub・対象shell・呼出先の拒否は未確認です。旧14 fileの採否、全直接式禁止profile、旧3 framework関係は[移行判断](WORKFLOW_INPUT_MIGRATION.md)へ記録しました。現在47 control・46 pattern・116 framework mappingで、次は旧CICD-003のworkflow検査と既存のscanner証拠境界との分担を判断します。

### 2026-09-27：CICD-004 Workflow authority minimizationを移行

旧PERM-001〜006を、[7特性のcontrol](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)、control配下の教材、[設計pattern](../engineering/cicd-security/purpose-bound-job-authority/README.md)、診断観点へ再編集しました。Jobの用途、標準token以外も含む実効権限、token発行、開始条件、呼出元の委譲、未確認を分けています。

[GitHub実装例](../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)に設定箇所、最短導入、無権限・読取り専用smoke workflow、成功・待機・開始拒否の確認、解除を追加しました。YAML、固定参照、shell構文、ローカルcopy・Git sourceを確認し、実GitHubの設定・権限付与・承認・拒否・API取得は未確認とします。独自のpermission判定器やSaaSの合成成功テストは作りません。旧6 framework関係は非継承で、現在46 control・45 pattern・116 framework mappingです。次は旧CICD-002の入力とshell解釈を選別します。採否と境界は[移行判断](WORKFLOW_AUTHORITY_MIGRATION.md)にあります。

### 2026-09-27：CICD-001 Workflow dependency identityを移行

旧ACT-001〜005・007を、[5特性のcontrol](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)、control配下の教材、[設計pattern](../engineering/cicd-security/reviewed-workflow-dependency-binding/README.md)、診断観点へ再編集しました。直接参照の形式、選ぶ版の出所・更新内容、固定コード内部の追加取得、検査とreviewの受入条件を分けています。

技術経路が明確な[Python / GitHub実装](../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)も追加しました。旧正規表現だけの行scannerをPyYAML 6.0.3の構造検査へ変更し、hash付き導入、12件のCLI、導入・smoke testをローカルで確認しました。Pinact v4.1.1は任意の修正補助です。実API更新・remote参照・内部取得のreview・GitHub merge保護・他platformは未確認とします。旧3 framework関係は非継承で、現在45 control・44 pattern・116 framework mappingです。次は旧CICD-004のworkflow権限を選別します。旧項目・参照資料・実装の採否は[移行判断](WORKFLOW_DEPENDENCY_MIGRATION.md)にあります。

### 2026-09-27：SOURCE-006 Source organization security postureを移行

旧GHO-001〜010を、[7特性のcontrol](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)、control配下の教材、[設計pattern](../engineering/source-protection/organization-baseline-and-drift-review/README.md)、診断観点へ再編集しました。共通方針の存在と必要対象への実適用、個別上書き、grant、現在状態とaudit、確認障害を分けました。Owner数・固定期限・Appのwrite全禁止は共通要件へ移しません。

技術経路が明確な[GitHubの設定確認手順](../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)も追加し、画面、GETによる補助、使い捨て対象でのsmoke test、解除方法を示しました。CLI 2.95.0の構文とAPI版2026-03-10の仕様を確認しましたが、live設定・収集・適用・拒否・IdP・監査配送・通知は未実施です。旧Python verifierと合成JSONは実装例へコピーせず、旧11 framework関係も非継承としました。現在44 control・43 pattern・116 framework mappingです。次は旧CICD-001のAction・reusable workflow参照を選別します。旧項目とrunbookの採否は[移行判断](SOURCE_ORGANIZATION_POSTURE_MIGRATION.md)に残しました。

### 2026-09-27：SOURCE-005 Repository recovery independenceを移行

旧4項目を、[6特性のcontrol](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)、control配下の教材、[設計pattern](../engineering/source-protection/independent-repository-backup-and-restore/README.md)、診断観点へ再編集しました。破壊操作、保管世代の削除権限、取得の鮮度、必要対象の照合、開発再開を分けました。

旧テストは実Git復元を観測しているため、その価値を[Git 2.47.2の実装例](../engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror/README.md)へ移しました。最短手順、解除方法と七件の実Gitテストを追加し、元の不在、タグ欠落・変更、破損、既存復元先、shallow source、取得中のref変更を確認しました。Gitの復元成功をcloud保持・GitHub設定・LFS・開発再開・RPO・RTOの証拠にしません。旧2件のframework関係は再照合していないため継承せず、現在43 control・42 pattern・116 framework mappingです。次はSOURCE-006の組織設定と監視を、既存controlとの重複を見ながら選別します。[移行判断](REPOSITORY_RECOVERY_MIGRATION.md)に旧項目・runbook・テストの採否を残しました。

### 2026-09-26：AI-007 Development agent work budgetを移行

旧AI-007の11項目を、[6特性のcontrol](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)、教材、[設計pattern](../engineering/ai-development-security/development-work-budget-gate/README.md)、診断観点へ再編集しました。個別操作の認可、runnerの資源制限と、一依頼の累積量・並列予約・再開・実行前停止を分けました。製品AIの予算設計は対象外です。

具体化できるローカル実行期限は[GNU timeout 9.7の実装例](../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)へ置き、六件の実processテストで正常・失敗・期限・KILL・子process・起動不能を観測しました。費用・token・tool呼び出しの共通予約や実agentの停止・provider請求・通知は未検証です。旧固定閾値と合成fixtureを実効証拠へ移さず、旧六件のframework関係は非継承としました。現在42 control・41 pattern・116 framework mappingです。次はSOURCE-005の復旧境界を選別します。旧ARB-001〜011の行き先と具体化条件は[移行判断](DEVELOPMENT_WORK_BUDGET_MIGRATION.md)に残しました。

### 2026-09-26：旧AI-005〜009の開発環境部分を選別

旧5件の[項目別の行き先](AI_DEVELOPMENT_SCOPE_REVIEW.md)を確認しました。AI-006の開発agentの操作・結果はAI-004の操作認可へ接続し、別controlを作りません。AI-007の作業単位の累積予算と実行前停止には独立した問題が残るため、次の主題に選びました。AI-005の持続的context、AI-008のagent間委譲、AI-009の長時間agentの停止・復旧は採用先の構成を確認するまで`deferred`です。製品AIの部分はai-security-foundryへ委ねます。旧fixtureはlive強制の証拠として移植しません。Control・pattern・framework mappingの件数は変わりません。

### 2026-09-26：AI-001 Repository agent guidanceを移行

旧`PSB-AI-001`の指示ファイルの同一性・変更承認と、開発agentの比較評価を[5特性のcontrol](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)、教材、[設計pattern](../engineering/ai-development-security/repository-agent-guidance-review/README.md)へ再編集しました。GitHub.com向けに[CODEOWNERSとbranch保護の例](../engineering/ai-development-security/repository-agent-guidance-review/implementations/github-codeowners/README.md)を加えましたが、実GitHubの設定・拒否、agentの読込み・比較評価は未実施です。

旧benchmarkは合成JSONの集計であり、62.50%→93.75%などの数値を実agentの改善として引き継ぎません。旧ATLAS `AML.T0081`・`AML.CS0041`とAgentic Top 10 `ASI04`の関係も新しい実証済みmappingへは移しません。旧AIG-001〜007の採否と製品AIを除く範囲は[詳細](REPOSITORY_AGENT_GUIDANCE_MIGRATION.md)に残しました。現在41 control・40 pattern・116 framework mappingです。当時の次作業は旧AI-005〜009の選別でした。

### 2026-09-26：AI-003 Development content injection boundaryを移行

旧`PSB-AI-003`を、開発agentが読む資料の出所、依頼の継続、独立した操作許可、拒否後の作業結果、証拠不足を扱う[5特性のcontrol](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、教材、[設計pattern](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)へ再編集しました。製品内AI・RAGは対象外とし、旧direct-user-promptはAI-004の管理方針・操作認可へ渡しました。旧AII-001〜010の採否は[対応表](DEVELOPMENT_CONTENT_INJECTION_MIGRATION.md)に残しました。

旧JSON verifierは実agentや実toolを動かさず、自己申告した結果の整合性を調べます。実装例へ移植せず、agentと強制点を選んだ後の限定実装条件を記録しました。旧ATLAS・Agentic Top 10・AISVSの`verifies`を今回の成功証拠として継承せず、framework mappingは追加していません。現在40 control・39 pattern・116 framework mappingです。次は旧`PSB-AI-001`の開発用guidanceとbenchmarkを選別します。

### 2026-09-26：SOURCE-003のGitHub indicator watchを追加

ユーザーが公開GitHubのコード・Issue・PR、少数の自社ドメイン・メールアドレスを選んだため、[限定実装](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)を追加しました。旧PoCの一括移植ではなく、候補の収集、人による精査、選択した候補のWebhook通知、重複抑制へ絞りました。模擬APIとWebhookで成功、重複、収集不完全、state破損を確認します。実GitHub検索、組織の指標・認証情報・通知先への導入は未確認です。この実装は公開サービスを台帳へ照合するDETECT-003ではなく、公開ソースの露出を扱うSOURCE-003へ配置しました。詳細は[計画](MIGRATION_PLAN.md#source-003の限定実装)と[旧PoCの移行記録](PUBLIC_EXPOSURE_MIGRATION.md)を参照してください。

### 2026-09-26：DETECT-003 External attack surface reconciliationを移行

旧`PSB-DETECT-003`を、所有を確認した起点、外部観測の範囲とhealth、候補の帰属、台帳との差、再出現、許可された調査範囲を扱う[7特性のcontrol](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)、教材、[設計pattern](../engineering/detection-verification/external-observation-and-inventory-reconciliation/README.md)へ再編集しました。

旧Python verifierには台帳照合・再出現判定の実装があります。ただし旧packageには外部collectorがなく、所有確認、台帳の正しさ、通知も検証しないため、限定profileをそのまま実装例へ移しません。CT・DNS・HTTPSの全三手段、HTTPS 443番、固定期限を一律の要件にせず、実装を始める条件を[移行記録](EXTERNAL_ATTACK_SURFACE_MIGRATION.md)へ記録しました。旧ATT&CKの`detects / high`とSSDF `RV.1.1`の関係は継承せず、framework mappingは追加していません。現在39 control・38 pattern・116 framework mappingです。次は旧`PSB-AI-003`を開発agentの範囲へ絞って選別します。

### 2026-09-26：Secure Codingの参照方針を決定

Web application／web serviceの共通要件は[ASVS 5.0.0](../sources/README.md#spec-owasp-asvs-5-0-0)へたどり、旧計画の`PSB-CODE-001〜004`を件数合わせで独自controlへ移しません。ユーザーの経験由来の脆弱性診断チェックリストは後日提供される独立した入力として扱い、原本、公開可否、旧`REF-USER-004`との同一性を確認してからASVSとの関係を評価します。現時点で項目や対応関係は作っていません。詳細は[計画](MIGRATION_PLAN.md#secure-codingの進め方)と[領域方針](REPOSITORY_DESIGN.md#secure-codingとasvs)を参照してください。Control、pattern、framework mappingの件数は変わりません。

### 2026-09-26：CODE-005 Unicode source reviewを移行

旧`PSB-CODE-005`を、sourceの表示、言語の字句解釈、識別子、受入側の検査、評価不能を扱う[5特性のcontrol](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)、教材、[設計pattern](../engineering/secure-coding/unicode-source-review/README.md)へ再編集しました。

実ソースを読む技術経路が明確なため、[Python 3.10限定scanner](../engineering/secure-coding/unicode-source-review/implementations/python/README.md)も作りました。Unicode制御文字、ASCII外の識別子、NFKC差分を検出し、対象ゼロ件、読めないencoding、構文エラー、symlinkを評価不能にします。旧profileの一律禁止を全言語のcontrolへ昇格しません。UTS #55／#39とPython字句規則を版付きで確認し、旧SITF `T-E011`の高確度mappingは非継承としました。Protected CI、review UI、実repositoryへの導入は未確認です。現在38 control・37 pattern・116 framework mappingです。次は旧`PSB-DETECT-003`の外部攻撃面の照合を選別します。詳細は[移行記録](UNICODE_SOURCE_MIGRATION.md)を参照してください。

### 2026-09-26：BUILD-002 Approved and consistent release buildを移行

旧`PSB-BUILD-002`を、producerによるbuilder選定、実際の実行経路、source・build定義、重要な外部入力、platform由来の記録、release昇格を扱う[6特性のcontrol](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)、教材、[設計pattern](../engineering/build-security/approved-release-build-process/README.md)へ再編集しました。

旧verifierは二つの合成JSONの値と形式を比較しますが、hosted実行、builderの能力、実artifact、platform発行の証拠、publish gateを観測しません。実装例へ移植せず、特定platformを選んだ後の実装・確認条件を[移行記録](CONSISTENT_BUILD_MIGRATION.md)に残しました。SLSA v1.2のproducer選定、一貫したbuild、条件付きhosted実行を`supports / medium / design-reviewed`で部分割当しました。現在37 control・36 pattern・116 framework mappingです。次は旧`PSB-CODE-005`のUnicode source deceptionを選別します。

### 2026-09-26：REL-005 Artifact signing generationを移行

旧`PSB-REL-005`を、承認したexact artifact、署名権限、鍵の保護、署名結果の検証、公開完了、release gateへ分けた[7特性のcontrol](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)、教材、[設計pattern](../engineering/release-integrity/artifact-signing-boundary/README.md)へ再編集しました。

旧verifierはOpenSSLで実際にEd25519署名とartifact bytesを照合しますが、KMS/HSM、鍵の非export性、透明性ログ、公開先、release gateは合成JSONの自己申告でした。独自envelopeとreceiptを実装例へ移さず、artifact形式・signer・公開先・consumer条件を選んだ後の限定実装条件を[移行記録](ARTIFACT_SIGNING_MIGRATION.md)に残しました。NIST SSDF `PS.2.1`を`supports / medium / design-reviewed`で部分割当し、旧OSPS 2件・ATT&CK 1件は非継承です。現在36 control・35 pattern・113 framework mappingです。次は旧`PSB-BUILD-002`のHosted consistent buildを選別します。

### 2026-09-25：REL-004 Supplier SBOM intake trustを移行

旧`PSB-REL-004`を、[7特性のcontrol](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)、教材、[設計パターン](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)へ再編集しました。供給者から届いたSBOMの署名・配送元を確認するだけでなく、利用者側の期待値、実際の製品・成果物、形式、隔離、訂正・撤回、限定した台帳取込を一つの受入境界として扱います。

旧合成Ed25519 verifierは暗号計算とbytes照合を実行しますが、独自envelope、手書き署名者状態、自己申告の台帳権限を全供給者の実装へ移すと受入済みと誤認させます。供給者と検証方式を選ぶまで実装例は保留し、必要な前提と成功・拒否・障害の確認条件を[移行記録](SUPPLIER_SBOM_MIGRATION.md)に残しました。NIST SSDF `PW.4.1`を`supports / medium / design-reviewed`で部分割当し、旧`RV.1.1`は非継承です。現在35 control・34 pattern・112 framework mappingです。次は旧`PSB-REL-005`のartifact signing generationを選別します。

### 2026-09-25：REL-003 Release SBOM identity and analysis boundaryを移行

旧`PSB-REL-003`を、source・build・deployment／operations observation、exact artifact binding、format・relationship、coverage claim、publication、analysis intake、processing health、deployment lookupへ分けた
[8特性のcontrol](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)と
[設計pattern](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)へ再編集しました。Source SBOMをfinal artifactの正本にせず、`complete`という値やupload受付を完全性・analysis完了へ変換しません。

旧verifierのうち、実artifactとSBOM digestを計算する部分は観測可能な価値があるため、[CycloneDX 1.7限定実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)として作り直しました。Artifact改変、pre-buildの誤用、dangling reference、型の不一致、JSON key重複、unknown composition、malformed JSONを含む9 testを実行しています。同梱する正常例は固定した公式CycloneDX 1.7 JSON Schemaでも確認しました。

旧fixtureの`immutable: true`、permission配列、手書き`BOM_PROCESSED` receipt、analyzer healthはlive storageやDependency-Trackを観測しないため非移植です。固定5分・365日・24時間も普遍要件から外しました。NIST SSDF `PS.3.2`と`RV.1.1`を`supports / medium / design-reviewed`で部分割当し、旧`PS.3.1 / supports / high`は非継承です。現在34 control・33 pattern・111 framework mappingです。次は旧`PSB-REL-004`のsupplier SBOM trustを選別します。詳細は[移行記録](RELEASE_SBOM_MIGRATION.md)を参照してください。

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
| `controls/dependency-security/dependency-change-review/README.md`、`control.yaml` | `split` | PSB-DEPS-004、そのcontrolの教材、ENG-DEPS-003。3旧checkを3特性へ再配置し、5件のframework関係を当時一旦保持。2026-10-03の再照合で2件を限定して残し、3件を非継承とした |
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
旧DVS-001〜008をSCAN-1〜8へ一対一で継承し、5件のframework mappingの版・ID・関係・confidence・対象を当時一旦保持しました。2026-10-03の再照合で1件を限定して残し、4件を非継承としています。旧`REF-DETECT-001..003`は役割名`REF-SCANNER-EVIDENCE-001`へ統合し、旧版、digest、採否、限界を残しました。
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
