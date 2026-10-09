# コントロールを探す

ここは「何を満たすべきか」を探す入口です。まず下のDomain一覧で場面から選び、IDが分かっていれば[個別Control一覧](#個別controlidから直接開く)から本文へ進んでください。具体的な場面は各Controlの`learning.md`、方式の選択は[engineering](../engineering/README.md)で扱います。

## Domain一覧

現行の11 domainを示します。「主に確認すること」は探すための目安です。適用範囲と確認項目は個別Control本文で確かめてください。

| Domain | 主に確認すること | 主な場面 |
|---|---|---|
| [Secure Design](records/secure-design/README.md) | 操作ごとの許可をどこで確かめるか | アプリで利用者がデータや機能を操作する |
| [Secure Coding](records/secure-coding/README.md) | コードの変更をどう読んで受け入れるか | ソースのレビュー、Webアプリの共通要件を探す |
| [Source Protection](records/source-protection/README.md) | 開発端末・認証情報・リポジトリをどう守るか | 開発、共有、公開、復旧 |
| [Dependency Security](records/dependency-security/README.md) | 依存の版・取得経路・取得物・実行をどう選ぶか | 依存の追加や更新 |
| [CI/CD Security](records/cicd-security/README.md) | 外部入力と権限付きjobをどう分けるか | PR、workflow、runner、cache |
| [Build Security](records/build-security/README.md) | 正規のbuildとその実行権限・来歴をどう守るか | リリース用成果物を作る |
| [Container / Cloud / IaC Security](records/container-cloud-iac-security/README.md) | 成果物の使用と実行環境・構成変更をどう制御するか | 配備、稼働、インフラ変更 |
| [Release Integrity](records/release-integrity/README.md) | 公開物の同一性と出所をどう確かめるか | 署名、来歴、SBOM、配布・受入 |
| [AI Development Security](records/ai-development-security/README.md) | 開発agentの入力・拡張・権限をどう制限するか | IDE、CLI、CIでAIを使う開発 |
| [Detection / Verification](records/detection-verification/README.md) | 検査や外部観測の結果を信用できるか | スキャン結果、公開面の確認 |
| [Governance / Operations](records/governance-operations/README.md) | 問題発覚後の影響・対応・復旧をどう判断するか | PSIRT、例外、通知、復旧 |

AI Development Securityは開発に使うagentを対象とし、製品自体のAI securityは[別PJとの分担](../docs/SECURITY_SCOPE.md)に従います。Secure CodingのWebアプリ共通要件は[ASVS方針](../docs/MIGRATION_PLAN.md#secure-codingの進め方)、脅威モデルの作成は[ModelForge](https://github.com/DharmaDoll/ModelForge)を参照してください。

各Controlの「なぜ必要か」は具体的な失敗例、「フレームワークとの関係」は現在[照合済みの対応](../mappings/frameworks.yaml)とその限界を示します。対応の記載がない規格まで網羅した一覧や、組織への導入・準拠の証明ではありません。

この一覧にあることは、組織への導入や領域全体の対応完了を示しません。[11 domainの作業進捗](../docs/MIGRATION_PLAN.md#全11-domainの進捗)、[分類の境界](../docs/REPOSITORY_DESIGN.md)、[横断分析](../docs/ANALYSIS_LENSES.md)は別に記録しています。

## 個別Control（IDから直接開く）

この一覧は、読みたいControlを選ぶための索引です。右欄は各Controlが扱うことの一文要約です。詳しい要件や診断項目、教材、設計パターンはリンク先にあります。

### Secure Design

| Control | このControlが扱うこと |
|---|---|
| [DESIGN-001 Object access authorization](records/secure-design/psb-design-001-object-access-authorization/README.md) | 利用者が対象データへ行える操作を、要求ごとに確かめる。 |

### Secure Coding

| Control | このControlが扱うこと |
|---|---|
| [CODE-005 Unicode source review](records/secure-coding/psb-code-005-unicode-source-review/README.md) | ソースの見た目と処理系が読む文字・識別子の食い違いを見つける。 |

### Source Protection

| Control | このControlが扱うこと |
|---|---|
| [SOURCE-001 Developer endpoint trust](records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | 開発端末の現在の状態を確かめ、状態不明の端末からのアクセスを止める。 |
| [SOURCE-002 Secret publication boundary](records/source-protection/psb-source-002-secret-publication-boundary/README.md) | 共有先へ受け入れるコミットを検査し、秘密情報を含む変更を止める。 |
| [SOURCE-003 Public source exposure triage](records/source-protection/psb-source-003-public-source-exposure-triage/README.md) | 公開コード・Issue・PRに自社情報が出ていないか調べ、発見した内容を精査する。 |
| [SOURCE-004 Source credential lifecycle](records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | ソース管理用の認証情報の権限と期限を絞り、不要な権限を止める。 |
| [SOURCE-005 Repository recovery independence](records/source-protection/psb-source-005-repository-recovery-independence/README.md) | リポジトリを失っても、独立した保管コピーから開発を再開できるようにする。 |
| [SOURCE-006 Source organization security posture](records/source-protection/psb-source-006-source-organization-security-posture/README.md) | 組織のセキュリティ設定が対象リポジトリへ適用され続けるか確かめる。 |
| [SOURCE-007 Developer credential storage](records/source-protection/psb-source-007-developer-local-credential-storage/README.md) | 開発者の認証情報を保護された場所に置き、作業ファイルへ残さない。 |
| [SOURCE-008 Sensitive data repository admission](records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md) | 顧客データなどをGit履歴へ入れる前に、持込みを許すか判断する。 |

### Dependency Security

| Control | このControlが扱うこと |
|---|---|
| [DEPS-001 Dependency release cooldown](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 公開直後の依存版を、決めた待機期間中は実行・採用させない。 |
| [DEPS-002 Install execution policy](records/dependency-security/psb-deps-002-install-execution-policy/README.md) | 依存の取得と、install時にそのコードを実行する許可を分ける。 |
| [DEPS-003 Dependency artifact identity](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) | 承認した依存と、今回実際に取得する内容が一致するか確かめる。 |
| [DEPS-004 Dependency change review](records/dependency-security/psb-deps-004-dependency-change-review/README.md) | 依存更新の差分を審査し、審査した内容だけを取り込む。 |
| [DEPS-005 Dependency acquisition gate](records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md) | 管理プロキシなどで依存の取得経路と遮断を管理し、迂回と無検査の取得を防ぐ。 |

### CI/CD Security

| Control | このControlが扱うこと |
|---|---|
| [CICD-001 Workflow dependency identity](records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md) | 外部Actionなどを確認した版に固定し、実行中の追加取得も把握する。 |
| [CICD-002 Workflow input handling](records/cicd-security/psb-cicd-002-workflow-input-handling/README.md) | PR名などの外部入力をworkflowの命令に変えない。 |
| [CICD-004 Workflow authority minimization](records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md) | jobに必要な操作権限だけを渡し、実際の権限を確かめる。 |
| [CICD-005 Untrusted PR boundary](records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 外部PRが変えられるコード・成果物を権限付きjobへ渡さない。 |
| [CICD-006 Workload federation boundary](records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) | 承認したCI workloadだけが必要なcloud権限を取得できるようにする。 |
| [CICD-007 Runner lifecycle isolation](records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) | 前のjobの状態や権限が次のjobへ引き継がれないようにする。 |
| [CICD-009 Cache trust boundary](records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) | 未信頼の変更が保存したcacheを権限付きjobへ渡さない。 |

### Build Security

| Control | このControlが扱うこと |
|---|---|
| [BUILD-001 Build containment](records/build-security/psb-build-001-build-containment/README.md) | build中のコードへ不要な秘密情報・ファイル・通信・権限を渡さない。 |
| [BUILD-002 Approved and consistent release build](records/build-security/psb-build-002-approved-consistent-build/README.md) | 承認したbuilder・手順・入力でrelease用の成果物を作る。 |
| [BUILD-003 Platform provenance generation](records/build-security/psb-build-003-platform-provenance-generation/README.md) | build基盤が成果物の来歴を記録し、その成果物に結び付ける。 |

### Container / Cloud / IaC Security

| Control | このControlが扱うこと |
|---|---|
| [CONTAINER-001 Deployment artifact admission](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) | 受け入れたimageと実際に起動するimageのdigestを一致させる。 |
| [CONTAINER-002 Container registry publication boundary](records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md) | registryでの公開・上書き・削除を承認した主体だけに許す。 |
| [CONTAINER-003 Container host and daemon boundary](records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md) | workloadからhostやdaemonの管理権限へ広がらないようにする。 |
| [CONTAINER-004 Runtime threat detection](records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) | 稼働中の不審な動きと監視の停止を見つけ、担当者へ渡す。 |
| [CONTAINER-005 Workload privilege confinement](records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md) | workloadが侵害されても不要なhost・kernel・管理面に触れさせない。 |
| [CONTAINER-006 Workload network segmentation](records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) | workload間と外部への通信を必要な相手・経路へ絞る。 |
| [CONTAINER-007 Workload resource consumption bounds](records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md) | 一つのworkloadが共有資源を使い尽くせないよう上限を設ける。 |
| [IAC-001 Infrastructure change authorization and drift](records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | レビューした変更計画と実行内容・変更後の実環境を照合する。 |

### Release Integrity

| Control | このControlが扱うこと |
|---|---|
| [REL-001 Signature and provenance verification](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) | 成果物の署名・来歴を利用者の受入条件と照合する。 |
| [REL-002 Provenance distribution and availability](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md) | 成果物に対応する来歴を、必要な期間中に取得できるようにする。 |
| [REL-003 Release SBOM identity and analysis](records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md) | 完成した成果物の部品表を取得地点・範囲とともに記録し、成果物に結び付ける。 |
| [REL-004 Supplier SBOM intake trust](records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md) | 供給者の部品表を対象成果物と出所へ照合してから受け入れる。 |
| [REL-005 Artifact signing generation](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md) | 承認した成果物だけに、限定した権限で署名する。 |

### AI Development Security

| Control | このControlが扱うこと |
|---|---|
| [AI-001 Repository agent guidance](records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md) | 開発agentが読むリポジトリ指示の変更を審査し、文章で権限を増やさない。 |
| [AI-002 Agent extension dependency governance](records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) | Skill・MCP・pluginを審査した版と権限で導入する。 |
| [AI-003 Development content injection boundary](records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md) | 開発agentが読む文書やtool結果中の指示を、正規の依頼として扱わせない。 |
| [AI-004 Development agent runtime boundary](records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) | 開発agentが触れるファイル・秘密情報・toolを制限し、重要操作の承認を実行内容と結び付ける。 |
| [AI-007 Development agent work budget](records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md) | 開発agentの一作業に使える時間・費用・呼出し回数を制限する。 |

### Detection / Verification

| Control | このControlが扱うこと |
|---|---|
| [DETECT-001 Scanner evidence trust boundary](records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) | 検査の対象・完了・失敗を確かめてから「指摘なし」を判断する。 |
| [DETECT-003 External attack surface reconciliation](records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md) | 外から見えるサービスを台帳と照合し、未登録の公開面を見つける。 |

### Governance / Operations

| Control | このControlが扱うこと |
|---|---|
| [GOV-001 Supply-chain impact assessment](records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) | PSIRTが問題のある依存の影響範囲を調べ、未調査の範囲も対応判断へ渡す。 |
| [GOV-002 Security exception lifecycle](records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) | 一時的な例外を対象・承認・期限に限定し、期限後は元の制御へ戻す。 |
| [GOV-003 Product vulnerability priority decision](records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md) | 製品への影響・露出・悪用情報を踏まえ、対応担当者と期限を決める。 |
| [GOV-004 Credential exposure containment](records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) | 漏えい疑いの認証情報を止め、影響を調べ、古い権限が使えないことを確かめる。 |
| [GOV-005 Deployed artifact recovery](records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) | 影響する成果物を置き換え、古い成果物が稼働していないか確かめる。 |
| [GOV-006 Vulnerability report intake](records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md) | 脆弱性報告を安全に受け取り、取りこぼさず調査担当者へ渡す。 |
| [GOV-007 Vulnerability advisory and notification](records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md) | 影響する利用者へ対象と取るべき行動を知らせ、通知が届いたか確かめる。 |
| [GOV-008 Vulnerability remedy validation](records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md) | 修正した製品版で問題が解消したか確認し、その版を提供する。 |

## 依存の変更から成果物の使用まで読む

旧PJの[「Software supply-chain security: 7つの実装原則」](../sources/README.md#local-supply-chain-principles)を、現行Controlから辿れるようにしました。原文と現在の分担の違いはリンク先に記録しています。

例えば、依存を更新した製品のリリースを受け入れるときは、次の順で判断をつなぎます。各リンク先の教材で場面を読み、方式を決めるときに設計patternへ進めます。

1. [DEPS-004](records/dependency-security/psb-deps-004-dependency-change-review/README.md)で変更を採用するか決め、[DEPS-001](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)で公開直後の版を止める期間を決める。[DEPS-005](records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)で取得経路と遮断を確認し、[DEPS-003](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)で承認した依存とbuildが取得するbytesを結ぶ。
2. [DEPS-002](records/dependency-security/psb-deps-002-install-execution-policy/README.md)で取得時に動くコードを決める。[BUILD-001](records/build-security/psb-build-001-build-containment/README.md)で、許可したコードにも渡さない権限・通信を決める。
3. [BUILD-002](records/build-security/psb-build-002-approved-consistent-build/README.md)で正規のbuilderと手順を定め、[BUILD-003](records/build-security/psb-build-003-platform-provenance-generation/README.md)で成果物digestに結び付く来歴を生成する。成果物への署名を要求するなら[REL-005](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)で対象と署名権限を確認する。
4. [REL-002](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)で、そのdigestから利用者が来歴を取得できるようにする。[REL-001](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)で、利用者自身の期待値に照らして受け入れる。
5. Container imageを実行する場合は[CONTAINER-001](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)で、受け入れたexact digestを使用直前の許可へ結ぶ。許可後に実際に稼働した内容は別に確認する。
6. 後から問題が分かったときは[REL-003](records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)の成果物と部品の記録を使い、[GOV-001](records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)で製品と稼働先への影響を調べる。置き換えが必要なら[GOV-005](records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)で旧成果物が動いていないことまで確かめる。

前段の成功を次段の許可と読み替えません。どの段階も、必要な記録の欠落や評価不能を成功として渡さないことが条件です。この案内は読む順序であり、実環境への導入や一連の強制を確認した結果ではありません。

旧成果物の採否は[移行台帳](../docs/MIGRATION.md)、現在地・未確認範囲・次の作業は[移行計画](../docs/MIGRATION_PLAN.md#現在地と次の作業)を参照してください。
