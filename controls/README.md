# コントロール一覧

コントロールは、製品やツールに依存しない形で「何を満たすべきか」を定義します。
具体的な実装方法から探す場合は[設計・実装](../engineering/README.md)を使用してください。

## Domain一覧

現行の11 domainを基本分類として継承しています。移行状況はこの試作版の成果物の有無を示し、
組織への導入や領域全体の対応完了を意味しません。

| Domain | 分野の入口 | 移行状況 |
|---|---|---|
| [Secure Design](records/secure-design/README.md) (`secure-design`) | 脅威モデリング、信頼境界、abuse case、設計上の判断 | 一部整備：Object access authorization |
| [Secure Coding](records/secure-coding/README.md) (`secure-coding`) | ASVSを共通要件の参照先とし、固有の失敗経路と実装判断を掘り下げる | 一部移行：Unicode source review。利用者の診断チェックリストは後日受領予定 |
| [Source Protection](records/source-protection/README.md) (`source-protection`) | 開発端末、Git、repository、ソースアクセス権限、公開露出 | 一部移行：Developer endpoint trust、Secret publication boundary、Public source exposure triage、Source credential lifecycle |
| [Dependency Security](records/dependency-security/README.md) (`dependency-security`) | 選定・取得、cooldown、install実行、lock・artifact同一性、更新レビュー | 一部移行：下記4件 |
| [CI/CD Security](records/cicd-security/README.md) (`cicd-security`) | Workflow、外部Action、権限、PR、OIDC、cache、runnerの境界 | 一部移行：PR、workload federation、cache、runner lifecycle |
| [Build Security](records/build-security/README.md) (`build-security`) | Build隔離、承認済みbuilder、一貫した実行、provenance生成 | 一部移行：Build containment、Approved and consistent release build、Platform provenance generation |
| [Container / Cloud / IaC Security](records/container-cloud-iac-security/README.md) (`container-cloud-iac-security`) | Cloud・IaC、registry、container admission、host、runtime | 一部移行：Infrastructure change authorization and drift、Deployment artifact admission、Container registry publication、Container host and daemon boundary、Runtime threat detection、Workload privilege confinement、Workload network segmentation、Workload resource consumption bounds |
| [Release Integrity](records/release-integrity/README.md) (`release-integrity`) | Artifact署名、provenance、SBOM、supplier intake、配布時の検証 | 一部移行：Artifact signing generation、Signature and provenance verification、Provenance distribution and availability、Release SBOM identity and analysis、Supplier SBOM intake trust |
| [AI Development Security](records/ai-development-security/README.md) (`ai-development-security`) | 開発端末・IDE・CLI・CIで使うAI agent、Skill、MCP、plugin、指示、操作権限 | 一部移行：Repository agent guidance、Agent extension、Development content injection、Runtime boundary。製品自体のAI securityは[別PJの担当](../docs/SECURITY_SCOPE.md) |
| [Detection / Verification](records/detection-verification/README.md) (`detection-verification`) | 脆弱性・秘密情報・設定・外部露出を検出し、結果の信頼性を確認する共通基盤 | 一部移行：Scanner evidence trust boundary |
| [Governance / Operations](records/governance-operations/README.md) (`governance-operations`) | Ownership、例外、評価、PSIRT、インシデント対応、復旧、継続運用 | 一部移行：Impact assessment、Security exception lifecycle、Vulnerability priority、Credential containment、Artifact recovery |

七つのレイヤーと攻撃段階は[横断分析](../docs/ANALYSIS_LENSES.md)、分類の境界は
[リポジトリ設計](../docs/REPOSITORY_DESIGN.md)で確認できます。

## 移行済みのコントロール記録

記録の再編集と、製品実装の移植・実環境の採用は別です。41件の記録があります。

| Domain | Control | 判断すること |
|---|---|---|
| `secure-design` | [PSB-DESIGN-001 Object access authorization](records/secure-design/psb-design-001-object-access-authorization/README.md) | 認証済み利用者による対象・操作・tenant越境を防ぐ |
| `secure-coding` | [PSB-CODE-005 Unicode source review](records/secure-coding/psb-code-005-unicode-source-review/README.md) | 見た目と処理系が読むソースの違いを、変更の受入前に見つける |
| `ai-development-security` | [PSB-AI-004 Development agent runtime boundary](records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) | 実効権限、実行時照合、操作許可、監査の境界を管理する |
| `ai-development-security` | [PSB-AI-001 Repository agent guidance](records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md) | 開発agentの指示をレビューし、実際の作業への効果を確かめる |
| `ai-development-security` | [PSB-AI-003 Development content injection boundary](records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md) | 文書やtool出力を正規の依頼・実行許可に変えない |
| `ai-development-security` | [PSB-AI-002 Agent extension dependency governance](records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) | 審査した拡張の内容・権限・期限を実際の利用へ結び付ける |
| `build-security` | [PSB-BUILD-001 Build containment](records/build-security/psb-build-001-build-containment/README.md) | 実行中の権限・通信・観測を分けて制限する |
| `build-security` | [PSB-BUILD-002 Approved and consistent release build](records/build-security/psb-build-002-approved-consistent-build/README.md) | 承認builderと、今回の成果物に使ったsource・定義・重要入力を照合する |
| `build-security` | [PSB-BUILD-003 Platform provenance generation](records/build-security/psb-build-003-platform-provenance-generation/README.md) | Build jobの自己申告とplatformが生成・認証するprovenanceを分ける |
| `cicd-security` | [PSB-CICD-005 Untrusted PR boundary](records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 未信頼の実行・派生状態を権限付き処理から分ける |
| `cicd-security` | [PSB-CICD-006 Workload federation boundary](records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) | Cloud権限の発行条件と交換後の権限を限定する |
| `cicd-security` | [PSB-CICD-007 Runner lifecycle isolation](records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) | Runnerの割当・一jobの隔離・破棄を確認する |
| `cicd-security` | [PSB-CICD-009 Cache trust boundary](records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) | Cacheの保存者・内容・consumerの信頼を分ける |
| `container-cloud-iac-security` | [PSB-CONTAINER-001 Deployment artifact admission](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) | Consumerが受け入れたexact artifactを最終的な使用許可へ結び付ける |
| `container-cloud-iac-security` | [PSB-CONTAINER-002 Container registry publication boundary](records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md) | OCI artifactの公開権限・不変性・監査・lifecycleを管理する |
| `container-cloud-iac-security` | [PSB-CONTAINER-003 Container host and daemon boundary](records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md) | Runtime・kubelet・host管理面とnode identityを制限し、一nodeの侵害をclusterへ広げない |
| `container-cloud-iac-security` | [PSB-CONTAINER-004 Runtime threat detection](records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) | 検知と観測障害を区別して担当者へ渡す |
| `container-cloud-iac-security` | [PSB-CONTAINER-005 Workload privilege confinement](records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md) | 侵害されたworkloadから不要なkernel・host・filesystem・control-plane authorityへの到達を制限する |
| `container-cloud-iac-security` | [PSB-CONTAINER-006 Workload network segmentation](records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) | 必要なworkload通信だけを両端で許可し、実際の到達性で強制を確認する |
| `container-cloud-iac-security` | [PSB-CONTAINER-007 Workload resource consumption bounds](records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md) | 一workloadのCPU・memory・PID・local storage・object消費が共有capacityへ広がる範囲を制限する |
| `dependency-security` | [PSB-DEPS-001 Dependency release cooldown](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 公開直後の採用を観測期間で制限する |
| `dependency-security` | [PSB-DEPS-002 Install execution policy](records/dependency-security/psb-deps-002-install-execution-policy/README.md) | 取得の許可と準備用コードの実行許可を分ける |
| `dependency-security` | [PSB-DEPS-003 Dependency artifact identity](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) | 承認した依存graphと取得bytesを照合する |
| `dependency-security` | [PSB-DEPS-004 Dependency change review](records/dependency-security/psb-deps-004-dependency-change-review/README.md) | 依存更新の差分とmerge判断を結び付ける |
| `detection-verification` | [PSB-DETECT-001 Scanner evidence trust boundary](records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) | Tool・data・対象・実行状態を検査結果へ結び付ける |
| `detection-verification` | [PSB-DETECT-003 External attack surface reconciliation](records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md) | 外部からの観測候補を所有台帳へ照合し、調査範囲と観測障害を分ける |
| `governance-operations` | [PSB-GOV-001 Supply-chain impact assessment](records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) | 影響候補と調査不能を分け、承認付き初動へ渡す |
| `governance-operations` | [PSB-GOV-002 Security exception lifecycle](records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) | 例外をexact scope・独立承認・期限付きdecisionとして扱う |
| `governance-operations` | [PSB-GOV-003 Product vulnerability priority decision](records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md) | 適用性とrisk signalsからowner・priority・組織期限を導出する |
| `governance-operations` | [PSB-GOV-004 Credential exposure containment](records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) | 旧authority・派生session・consumer・影響調査を結び付けてclosureを判断する |
| `governance-operations` | [PSB-GOV-005 Deployed artifact recovery](records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) | New digestの置換とold digestの非稼働を独立して確認する |
| `release-integrity` | [PSB-REL-001 Signature and provenance verification](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) | 認証した成果物をconsumerの期待値へ照合する |
| `release-integrity` | [PSB-REL-002 Provenance distribution and availability](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md) | Exact artifactから対応するprovenanceを発見・取得し、利用期間中の欠落・上書き・取得不能を扱う |
| `release-integrity` | [PSB-REL-003 Release SBOM identity and analysis](records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md) | Final artifactとSBOMを結び、coverage・公開・analysis処理・稼働影響への受け渡しを分ける |
| `release-integrity` | [PSB-REL-004 Supplier SBOM intake trust](records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md) | 供給者SBOMを期待する製品・成果物・出所へ照合し、未確認の情報を通常台帳から隔離する |
| `release-integrity` | [PSB-REL-005 Artifact signing generation](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md) | 承認したexact artifactと署名権限を分け、署名・検証材料の公開までをrelease完了条件にする |
| `source-protection` | [PSB-SOURCE-001 Developer endpoint trust](records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | 端末の保護基準・現在の状態・業務アクセスと紛失時対応を結び付ける |
| `source-protection` | [PSB-SOURCE-002 Secret publication boundary](records/source-protection/psb-source-002-secret-publication-boundary/README.md) | hooks・受入・CIの検査範囲と拒否境界を分ける |
| `source-protection` | [PSB-SOURCE-003 Public source exposure triage](records/source-protection/psb-source-003-public-source-exposure-triage/README.md) | Public source surfaceの観測範囲・再出現・triage・観測障害を分ける |
| `source-protection` | [PSB-SOURCE-004 Source credential lifecycle](records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | 認証情報の発行・権限・失効を管理する |

保留した実装と未確認範囲は[移行台帳](../docs/MIGRATION.md)、次の優先主題は[横断レビュー](../docs/STRUCTURE_REVIEW.md)を参照してください。
