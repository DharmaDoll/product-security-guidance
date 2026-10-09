# コントロールを探す

ここは「何を満たすべきか」を探す入口です。まず下のDomain一覧で場面から選び、IDが分かっていれば[個別Control一覧](#個別controlidから直接開く)から本文へ進んでください。具体的な場面は各Controlの`learning.md`、方式の選択は[engineering](../engineering/README.md)で扱います。

## Domain一覧

現行の11 domainを示します。「主に確認すること」は探すための目安です。適用範囲と確認項目は個別Control本文で確かめてください。

| Domain | 主に確認すること | 主な場面 |
|---|---|---|
| [Secure Design](records/secure-design/README.md) | 操作ごとの許可をどこで確かめるか | アプリで利用者がデータや機能を操作する |
| [Secure Coding](records/secure-coding/README.md) | コードの変更をどう読んで受け入れるか | ソースのレビュー、Webアプリの共通要件を探す |
| [Source Protection](records/source-protection/README.md) | 開発端末・認証情報・リポジトリをどう守るか | 開発、共有、公開、復旧 |
| [Dependency Security](records/dependency-security/README.md) | 依存の版・取得物・実行をどう選ぶか | 依存の追加や更新 |
| [CI/CD Security](records/cicd-security/README.md) | 外部入力と権限付きjobをどう分けるか | PR、workflow、runner、cache |
| [Build Security](records/build-security/README.md) | 正規のbuildとその実行権限・来歴をどう守るか | リリース用成果物を作る |
| [Container / Cloud / IaC Security](records/container-cloud-iac-security/README.md) | 成果物の使用と実行環境・構成変更をどう制御するか | 配備、稼働、インフラ変更 |
| [Release Integrity](records/release-integrity/README.md) | 公開物の同一性と出所をどう確かめるか | 署名、来歴、SBOM、配布・受入 |
| [AI Development Security](records/ai-development-security/README.md) | 開発agentの入力・拡張・権限をどう制限するか | IDE、CLI、CIでAIを使う開発 |
| [Detection / Verification](records/detection-verification/README.md) | 検査や外部観測の結果を信用できるか | スキャン結果、公開面の確認 |
| [Governance / Operations](records/governance-operations/README.md) | 問題発覚後の影響・対応・復旧をどう判断するか | PSIRT、例外、通知、復旧 |

AI Development Securityは開発に使うagentを対象とし、製品自体のAI securityは[別PJとの分担](../docs/SECURITY_SCOPE.md)に従います。Secure CodingのWebアプリ共通要件は[ASVS方針](../docs/MIGRATION_PLAN.md#secure-codingの進め方)、脅威モデルの作成は[ModelForge](https://github.com/DharmaDoll/ModelForge)を参照してください。

この一覧にあることは、組織への導入や領域全体の対応完了を示しません。[11 domainの作業進捗](../docs/MIGRATION_PLAN.md#全11-domainの進捗)、[分類の境界](../docs/REPOSITORY_DESIGN.md)、[横断分析](../docs/ANALYSIS_LENSES.md)は別に記録しています。

## 個別Control（IDから直接開く）

52件の題名と、レビュー時に特に確認する点です。各Controlの問い、適用範囲、教材、設計パターンはリンク先にあります。

### Secure Design

| Control | レビューで特に確認すること |
|---|---|
| [DESIGN-001 Object access authorization](records/secure-design/psb-design-001-object-access-authorization/README.md) | ログイン済みでも、要求ごとに対象・操作・tenantの許可を確認する。 |

### Secure Coding

| Control | レビューで特に確認すること |
|---|---|
| [CODE-005 Unicode source review](records/secure-coding/psb-code-005-unicode-source-review/README.md) | レビュー画面に見える文字と、処理系が読む文字・識別子を照合する。 |

### Source Protection

| Control | レビューで特に確認すること |
|---|---|
| [SOURCE-001 Developer endpoint trust](records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | 管理台帳への登録や古い正常結果だけで、状態不明の端末を許可し続けない。 |
| [SOURCE-002 Secret publication boundary](records/source-protection/psb-source-002-secret-publication-boundary/README.md) | 手元のhookを省略しても、共有先の受入判断が欠けない。 |
| [SOURCE-003 Public source exposure triage](records/source-protection/psb-source-003-public-source-exposure-triage/README.md) | 検索失敗を候補なしとせず、発見後の担当と判断を残す。 |
| [SOURCE-004 Source credential lifecycle](records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | 古いトークンやセッションが退職・紛失後も使えないか確認する。 |
| [SOURCE-005 Repository recovery independence](records/source-protection/psb-source-005-repository-recovery-independence/README.md) | 元のリポジトリを消せる権限で復旧用コピーまで消せない。 |
| [SOURCE-006 Source organization security posture](records/source-protection/psb-source-006-source-organization-security-posture/README.md) | 管理画面の既定値だけで、既存・移管済みの対象を確認済みにしない。 |
| [SOURCE-007 Developer credential storage](records/source-protection/psb-source-007-developer-local-credential-storage/README.md) | 実際の値を`.env`などの作業ファイルに残さず、別の処理へ広く渡さない。 |
| [SOURCE-008 Sensitive data repository admission](records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md) | secret scanの検出なしを、実データの受入許可にしない。 |

### Dependency Security

| Control | レビューで特に確認すること |
|---|---|
| [DEPS-001 Dependency release cooldown](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 判定は依存のコードが動く前に行う。 |
| [DEPS-002 Install execution policy](records/dependency-security/psb-deps-002-install-execution-policy/README.md) | 取得を認めただけで準備用スクリプトに開発環境の権限を渡さない。 |
| [DEPS-003 Dependency artifact identity](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) | 名前やversionだけでなく、今回使うartifactの同一性を確認する。 |
| [DEPS-004 Dependency change review](records/dependency-security/psb-deps-004-dependency-change-review/README.md) | レビューした変更と、mergeで実際に入る変更を一致させる。 |

### CI/CD Security

| Control | レビューで特に確認すること |
|---|---|
| [CICD-001 Workflow dependency identity](records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md) | 表面の参照だけでなく、その実行中に取得される外部コードも判断する。 |
| [CICD-002 Workflow input handling](records/cicd-security/psb-cicd-002-workflow-input-handling/README.md) | 入力をコマンドや許可された操作の変更へ昇格させない。 |
| [CICD-004 Workflow authority minimization](records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md) | 設定上の希望ではなく実際の権限を確認し、不要な書込みを許さない。 |
| [CICD-005 Untrusted PR boundary](records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 後続ジョブもPR由来のスクリプトや成果物を実行しない。 |
| [CICD-006 Workload federation boundary](records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) | 発行時の条件だけでなく、交換後に実際にできる操作も確認する。 |
| [CICD-007 Runner lifecycle isolation](records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) | 前のjobが残した状態や権限を次のjobが利用できない。 |
| [CICD-009 Cache trust boundary](records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) | 未信頼の変更が保存した内容を権限付きjobが実行・利用しない。 |

### Build Security

| Control | レビューで特に確認すること |
|---|---|
| [BUILD-001 Build containment](records/build-security/psb-build-001-build-containment/README.md) | 許可したbuildでも不要な秘密情報や外部通信を使えない。 |
| [BUILD-002 Approved and consistent release build](records/build-security/psb-build-002-approved-consistent-build/README.md) | 承認した手順と今回の成果物に使ったsource・設定・重要入力を結び付ける。 |
| [BUILD-003 Platform provenance generation](records/build-security/psb-build-003-platform-provenance-generation/README.md) | jobの自己申告を来歴の証拠にせず、成果物そのものへ結び付ける。 |

### Container / Cloud / IaC Security

| Control | レビューで特に確認すること |
|---|---|
| [CONTAINER-001 Deployment artifact admission](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) | 検証したdigestと実際に起動するdigestを一致させる。 |
| [CONTAINER-002 Container registry publication boundary](records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md) | 承認していない主体が既存のartifactを差し替えられない。 |
| [CONTAINER-003 Container host and daemon boundary](records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md) | 一つのnodeを侵害されてもcluster全体の管理権限へ広がらない。 |
| [CONTAINER-004 Runtime threat detection](records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) | 監視が止まった状態を異常なしと扱わない。 |
| [CONTAINER-005 Workload privilege confinement](records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md) | 不要なhost・kernel・管理面へ到達させない。 |
| [CONTAINER-006 Workload network segmentation](records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) | 設定の宣言だけでなく、実際に届く経路を確認する。 |
| [CONTAINER-007 Workload resource consumption bounds](records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md) | CPUだけでなくmemory、PID、storageなどの上限と失敗時を確認する。 |
| [IAC-001 Infrastructure change authorization and drift](records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | レビューしたplanと実行するplan、変更後の実環境を一致させる。 |

### Release Integrity

| Control | レビューで特に確認すること |
|---|---|
| [REL-001 Signature and provenance verification](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) | 署名が有効なだけでなく、利用者が期待する出所・内容と一致する。 |
| [REL-002 Provenance distribution and availability](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md) | 受け取った成果物のdigestに対応する来歴が、利用時まで欠けずに残る。 |
| [REL-003 Release SBOM identity and analysis](records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md) | SBOMをどの時点・場所で取得したかを明らかにし、実際のrelease内容からずれない。 |
| [REL-004 Supplier SBOM intake trust](records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md) | 未確認のSBOMを正しい台帳として扱わない。 |
| [REL-005 Artifact signing generation](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md) | 署名権限と対象artifactを固定し、別の内容へ署名しない。 |

### AI Development Security

| Control | レビューで特に確認すること |
|---|---|
| [AI-001 Repository agent guidance](records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md) | 指示の変更を独立してレビューし、文章だけで操作権限を増やさない。 |
| [AI-002 Agent extension dependency governance](records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) | 審査した版と実際に読み込む版・権限が一致する。 |
| [AI-003 Development content injection boundary](records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md) | 未信頼の内容を依頼者の指示や実行許可へ昇格させない。 |
| [AI-004 Development agent runtime boundary](records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) | 重要操作は内容を人が確認し、実行側が承認と実際の引数を照合する。 |
| [AI-007 Development agent work budget](records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md) | 再試行や子作業で残り予算を作り直さず、上限で止まる。 |

### Detection / Verification

| Control | レビューで特に確認すること |
|---|---|
| [DETECT-001 Scanner evidence trust boundary](records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) | 取得・解析の失敗を「指摘なし」へ変えない。 |
| [DETECT-003 External attack surface reconciliation](records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md) | 部分的な収集でも候補を残し、未確認の範囲を公開サービスなしと扱わない。 |

### Governance / Operations

| Control | レビューで特に確認すること |
|---|---|
| [GOV-001 Supply-chain impact assessment](records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) | 調べられなかった範囲を影響なしとせず、初動担当へ渡す。 |
| [GOV-002 Security exception lifecycle](records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) | 例外が元の問題を「合格」に変えたり、別の対象へ使い回されたりしない。 |
| [GOV-003 Product vulnerability priority decision](records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md) | スコアだけで決めず、担当者と対応期限を決める。 |
| [GOV-004 Credential exposure containment](records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) | 新しい値の発行だけで終えず、古い権限の拒否を確かめる。 |
| [GOV-005 Deployed artifact recovery](records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) | 新しい成果物の配布と、古い成果物がもう動いていないことを別々に確かめる。 |
| [GOV-006 Vulnerability report intake](records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md) | 窓口障害、情報不足、重複判定で報告を失わず、未公開の内容を安全に扱う。 |
| [GOV-007 Vulnerability advisory and notification](records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md) | 修正の公開、告知の公開、通知の到達を分けて確認し、訂正を届ける。 |
| [GOV-008 Vulnerability remedy validation](records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md) | 変更、修正の検証、利用者への提供を別々に確認する。 |

## 依存の変更から成果物の使用まで読む

例えば、依存を更新した製品のリリースを受け入れるときは、次の順で判断をつなぎます。各リンク先の教材で場面を読み、方式を決めるときに設計patternへ進めます。

1. [DEPS-004](records/dependency-security/psb-deps-004-dependency-change-review/README.md)で変更を採用するか決め、[DEPS-001](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)で公開直後の版を止める期間を決める。[DEPS-003](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)で、承認した依存とbuildが取得するbytesを結ぶ。
2. [DEPS-002](records/dependency-security/psb-deps-002-install-execution-policy/README.md)で取得時に動くコードを決める。[BUILD-001](records/build-security/psb-build-001-build-containment/README.md)で、許可したコードにも渡さない権限・通信を決める。
3. [BUILD-002](records/build-security/psb-build-002-approved-consistent-build/README.md)で正規のbuilderと手順を定め、[BUILD-003](records/build-security/psb-build-003-platform-provenance-generation/README.md)で成果物digestに結び付く来歴を生成する。成果物への署名を要求するなら[REL-005](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)で対象と署名権限を確認する。
4. [REL-002](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)で、そのdigestから利用者が来歴を取得できるようにする。[REL-001](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)で、利用者自身の期待値に照らして受け入れる。
5. Container imageを実行する場合は[CONTAINER-001](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)で、受け入れたexact digestを使用直前の許可へ結ぶ。許可後に実際に稼働した内容は別に確認する。

前段の成功を次段の許可と読み替えません。どの段階も、必要な記録の欠落や評価不能を成功として渡さないことが条件です。この案内は読む順序であり、実環境への導入や一連の強制を確認した結果ではありません。

旧成果物の採否は[移行台帳](../docs/MIGRATION.md)、現在地・未確認範囲・次の作業は[移行計画](../docs/MIGRATION_PLAN.md#現在地と次の作業)を参照してください。
