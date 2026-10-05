# コントロール一覧

本PJは、セキュリティ上の成果をcontrolで定め、設計と実装の選択を[engineering](../engineering/README.md)で扱います。具体的な場面から理解する教材は各controlの`learning.md`、導入状況の判定は[assessments](../assessments/README.md)、成果物同士の関係は[マッピング](../mappings/README.md)、資料の出所と採否は[Sources](../sources/README.md)にあります。[docs](../docs/ARTIFACT_MODEL.md)には対象範囲、文書の役割、横断分析、移行の記録を置きます。

## Domain一覧

下のtreeは、現行の11 domainと51 controlの全体像です。各行に扱う問題と、レビュー時に特に確かめたい点を示します。主な所属先だけを示し、隣の領域との関係はリンク先で確認します。どのdomainも記録があるだけで、組織への導入や領域全体の対応完了を意味しません。七つのレイヤーと攻撃段階は[横断分析](../docs/ANALYSIS_LENSES.md)、分類の境界は[リポジトリ設計](../docs/REPOSITORY_DESIGN.md)を参照してください。

- **[Secure Design](records/secure-design/README.md)** — アプリで何を許可・拒否し、どこで強制するかを決める。脅威モデルの作成は[ModelForge](https://github.com/DharmaDoll/ModelForge)へ。
  - [DESIGN-001 Object access authorization](records/secure-design/psb-design-001-object-access-authorization/README.md) — 利用者が対象データへ行える操作を決める。**ログイン済みでも、要求ごとに対象・操作・tenantの許可を確認する。**
- **[Secure Coding](records/secure-coding/README.md)** — コードの解釈と変更の受入を扱う。Webアプリ共通の観点は[ASVS方針](../docs/MIGRATION_PLAN.md#secure-codingの進め方)へ。
  - [CODE-005 Unicode source review](records/secure-coding/psb-code-005-unicode-source-review/README.md) — 見た目と処理系の解釈が違うソース変更を見つける。**レビュー画面に見える文字だけで判断せず、実際の文字列と実行される内容を照合する。**
- **[Source Protection](records/source-protection/README.md)** — 開発端末、ソース管理、公開、復旧を扱う。
  - [SOURCE-001 Developer endpoint trust](records/source-protection/psb-source-001-developer-endpoint-trust/README.md) — 端末の現在の状態を開発サービスへのアクセスに反映する。**管理台帳への登録や古い正常結果だけで、状態不明の端末を許可し続けない。**
  - [SOURCE-002 Secret publication boundary](records/source-protection/psb-source-002-secret-publication-boundary/README.md) — 秘密情報を含むコミットやpushを検査して止める。**手元のhookを省略しても、共有先の受入判断が欠けない。**
  - [SOURCE-003 Public source exposure triage](records/source-protection/psb-source-003-public-source-exposure-triage/README.md) — 公開コード・Issue・PRで見つけた自社情報を確認につなぐ。**検索失敗を候補なしとせず、発見後の担当と判断を残す。**
  - [SOURCE-004 Source credential lifecycle](records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) — ソース管理用の認証情報の権限と有効期間を管理する。**古いトークンやセッションが退職・紛失後も使えないか確認する。**
  - [SOURCE-005 Repository recovery independence](records/source-protection/psb-source-005-repository-recovery-independence/README.md) — リポジトリを失っても別に守ったコピーから開発を再開する。**元のリポジトリを消せる権限で復旧用コピーまで消せない。**
  - [SOURCE-006 Source organization security posture](records/source-protection/psb-source-006-source-organization-security-posture/README.md) — 組織の共通設定を対象のリポジトリへ適用し続ける。**管理画面の既定値だけで、既存・移管済みの対象を確認済みにしない。**
  - [SOURCE-007 Developer credential storage](records/source-protection/psb-source-007-developer-local-credential-storage/README.md) — 開発端末の認証情報を保護された場所に置き、必要な処理へ渡す。**実際の値を`.env`などの作業ファイルに残さず、別の処理へ広く渡さない。**
- **[Dependency Security](records/dependency-security/README.md)** — 依存の採用、取得、更新を扱う。
  - [DEPS-001 Dependency release cooldown](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) — 公開直後の依存版を一定期間待ってから採用する。**待機条件と例外を実際の解決・取得より前に適用する。**
  - [DEPS-002 Install execution policy](records/dependency-security/psb-deps-002-install-execution-policy/README.md) — 依存の取得と、install時のコード実行を分けて許可する。**取得を認めただけで準備用スクリプトに開発環境の権限を渡さない。**
  - [DEPS-003 Dependency artifact identity](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) — 承認した依存と実際に取得した内容を一致させる。**名前やversionだけでなく、今回使うartifactの同一性を確認する。**
  - [DEPS-004 Dependency change review](records/dependency-security/psb-deps-004-dependency-change-review/README.md) — 依存更新の差分を読んで採否を決める。**レビューした変更と、mergeで実際に入る変更を一致させる。**
- **[CI/CD Security](records/cicd-security/README.md)** — workflowの入力、実行権限、runnerを扱う。
  - [CICD-001 Workflow dependency identity](records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md) — 外部Actionなどをレビューした版へ固定する。**表面の参照だけでなく、その実行中に取得される外部コードも判断する。**
  - [CICD-002 Workflow input handling](records/cicd-security/psb-cicd-002-workflow-input-handling/README.md) — PR名など外部入力をworkflow内で安全に扱う。**入力をコマンドや許可された操作の変更へ昇格させない。**
  - [CICD-004 Workflow authority minimization](records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md) — jobごとに必要な権限と開始条件を決める。**設定上の希望ではなく実際の権限を確認し、不要な書込みを許さない。**
  - [CICD-005 Untrusted PR boundary](records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) — 外部PRのコードと権限付き処理を分ける。**PRが変えられるコードや成果物を、秘密情報を持つjobが無条件に信頼しない。**
  - [CICD-006 Workload federation boundary](records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) — CIからクラウド権限を得る条件を絞る。**発行時の条件だけでなく、交換後に実際にできる操作も確認する。**
  - [CICD-007 Runner lifecycle isolation](records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) — jobを実行するrunnerを割当て、隔離して片付ける。**前のjobが残した状態や権限を次のjobが利用できない。**
  - [CICD-009 Cache trust boundary](records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) — cacheを保存できる人と使うjobを分ける。**未信頼の変更が保存した内容を権限付きjobが実行・利用しない。**
- **[Build Security](records/build-security/README.md)** — build中の実行と成果物の来歴を扱う。
  - [BUILD-001 Build containment](records/build-security/psb-build-001-build-containment/README.md) — buildに渡す権限・ファイル・通信を制限する。**許可したbuildでも不要な秘密情報や外部通信を使えない。**
  - [BUILD-002 Approved and consistent release build](records/build-security/psb-build-002-approved-consistent-build/README.md) — 承認したbuilderと入力でrelease用成果物を作る。**承認した手順と今回の成果物に使ったsource・設定・重要入力を結び付ける。**
  - [BUILD-003 Platform provenance generation](records/build-security/psb-build-003-platform-provenance-generation/README.md) — build基盤が成果物の来歴を記録する。**jobの自己申告を来歴の証拠にせず、成果物そのものへ結び付ける。**
- **[Container / Cloud / IaC Security](records/container-cloud-iac-security/README.md)** — 配布物の使用、実行環境、インフラ変更を扱う。
  - [CONTAINER-001 Deployment artifact admission](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) — 受け入れたcontainer imageだけを使用直前に許可する。**検証したdigestと実際に起動するdigestを一致させる。**
  - [CONTAINER-002 Container registry publication boundary](records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md) — registryへの公開・上書き・削除を管理する。**承認していない主体が既存のartifactを差し替えられない。**
  - [CONTAINER-003 Container host and daemon boundary](records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md) — containerのhost・daemon管理面を守る。**一つのnodeを侵害されてもcluster全体の管理権限へ広がらない。**
  - [CONTAINER-004 Runtime threat detection](records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) — 稼働中の不審な動きを見つけて担当へ渡す。**監視が止まった状態を異常なしと扱わない。**
  - [CONTAINER-005 Workload privilege confinement](records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md) — 侵害されたworkloadの権限を閉じ込める。**不要なhost・kernel・管理面へ到達させない。**
  - [CONTAINER-006 Workload network segmentation](records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) — workload間の通信を必要な相手と操作へ絞る。**設定の宣言だけでなく、実際に届く経路を確認する。**
  - [CONTAINER-007 Workload resource consumption bounds](records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md) — 一つのworkloadが共有資源を使い尽くす範囲を制限する。**CPUだけでなくmemory、PID、storageなどの上限と失敗時を確認する。**
  - [IAC-001 Infrastructure change authorization and drift](records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md) — インフラ変更の計画・実行・後の差分を確認する。**レビューしたplanと実行するplan、変更後の実環境を一致させる。**
- **[Release Integrity](records/release-integrity/README.md)** — 署名、来歴、SBOMの生成・配布・受入を扱う。
  - [REL-001 Signature and provenance verification](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) — 利用者が署名と来歴を確かめて成果物を受け入れる。**署名が有効なだけでなく、利用者が期待する出所・内容と一致する。**
  - [REL-002 Provenance distribution and availability](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md) — 成果物から対応する来歴を取得できるようにする。**受け取った成果物のdigestに対応する来歴が、利用時まで欠けずに残る。**
  - [REL-003 Release SBOM identity and analysis](records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md) — 最終成果物とSBOMを結び付け、分析へ渡す。**SBOMをどの時点・場所で取得したかを明らかにし、実際のrelease内容からずれない。**
  - [REL-004 Supplier SBOM intake trust](records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md) — 供給者から受け取ったSBOMを対象の製品へ結び付ける。**未確認のSBOMを正しい台帳として扱わない。**
  - [REL-005 Artifact signing generation](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md) — 正規の成果物へ署名を作り、検証材料を公開する。**署名権限と対象artifactを固定し、別の内容へ署名しない。**
- **[AI Development Security](records/ai-development-security/README.md)** — 開発に使うagent・拡張・toolを扱う。製品AIの設計は[別PJ](../docs/SECURITY_SCOPE.md)へ。
  - [AI-001 Repository agent guidance](records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md) — 開発agentが読むリポジトリ指示を管理する。**指示の変更を独立してレビューし、文章だけで操作権限を増やさない。**
  - [AI-002 Agent extension dependency governance](records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) — 導入するSkill・MCP・pluginの内容と権限を審査する。**審査した版と実際に読み込む版・権限が一致する。**
  - [AI-003 Development content injection boundary](records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md) — agentが読む文書やtool結果に混じった指示を扱う。**未信頼の内容を依頼者の指示や実行許可へ昇格させない。**
  - [AI-004 Development agent runtime boundary](records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) — agentが実行中に触れるファイル・秘密情報・toolを制限する。**重要操作は内容を人が確認し、実行側が承認と実際の引数を照合する。**
  - [AI-007 Development agent work budget](records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md) — 一作業で使う時間・費用・呼出し回数を制限する。**再試行や子作業で残り予算を作り直さず、上限で止まる。**
- **[Detection / Verification](records/detection-verification/README.md)** — 検査結果と外部の観測を判断に使える形にする。
  - [DETECT-001 Scanner evidence trust boundary](records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) — scannerの結果が何をどこまで調べたか示す。**取得・解析の失敗を「指摘なし」へ変えない。**
  - [DETECT-003 External attack surface reconciliation](records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md) — 外から見えるサービス候補を組織の台帳へ照合する。**部分的な収集でも候補を残し、未確認の範囲を公開サービスなしと扱わない。**
- **[Governance / Operations](records/governance-operations/README.md)** — 影響調査、例外、優先順位、漏えい対応、復旧を扱う。
  - [GOV-001 Supply-chain impact assessment](records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) — 問題のある部品・成果物がどこに使われたか調べる。**調べられなかった範囲を影響なしとせず、初動担当へ渡す。**
  - [GOV-002 Security exception lifecycle](records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) — 一時的な例外の対象、承認者、期限を管理する。**例外が元の問題を「合格」に変えたり、別の対象へ使い回されたりしない。**
  - [GOV-003 Product vulnerability priority decision](records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md) — 脆弱性の適用性と影響から対応順序を決める。**スコアだけで決めず、影響する製品と担当・期限へ結び付ける。**
  - [GOV-004 Credential exposure containment](records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) — 認証情報の漏えい疑いを受け、古い権限を止める。**新しい値の発行だけで終えず、古い値・派生セッションの拒否を確かめる。**
  - [GOV-005 Deployed artifact recovery](records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) — 配布済みの問題ある成果物を入れ替える。**新しい成果物の配布と、古い成果物がもう稼働していないことを別々に確かめる。**
  - [GOV-006 Vulnerability report intake](records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md) — 製品の脆弱性報告を調査担当へ渡す。**窓口障害、情報不足、重複判定で報告を失わず、未公開の内容を安全に扱う。**
  - [GOV-007 Vulnerability advisory and notification](records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md) — 影響する利用者へ脆弱性と取るべき行動を知らせる。**修正の公開、告知の公開、通知の到達を分けて確認し、訂正を届ける。**
  - [GOV-008 Vulnerability remedy validation](records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md) — 修正を主張する製品・版で問題の解消を確かめる。**変更、修正の検証、利用者への提供を別々に確認する。**

## 依存の変更から成果物の使用まで読む

例えば、依存を更新した製品のリリースを受け入れるときは、次の順で判断をつなぎます。各リンク先の教材で場面を読み、方式を決めるときに設計patternへ進めます。

1. [DEPS-004](records/dependency-security/psb-deps-004-dependency-change-review/README.md)で変更を採用するか決め、[DEPS-001](records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)で公開直後の版を止める期間を決める。[DEPS-003](records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)で、承認した依存とbuildが取得するbytesを結ぶ。
2. [DEPS-002](records/dependency-security/psb-deps-002-install-execution-policy/README.md)で取得時に動くコードを決める。[BUILD-001](records/build-security/psb-build-001-build-containment/README.md)で、許可したコードにも渡さない権限・通信を決める。
3. [BUILD-002](records/build-security/psb-build-002-approved-consistent-build/README.md)で正規のbuilderと手順を定め、[BUILD-003](records/build-security/psb-build-003-platform-provenance-generation/README.md)で成果物digestに結び付く来歴を生成する。成果物への署名を要求するなら[REL-005](records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)で対象と署名権限を確認する。
4. [REL-002](records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)で、そのdigestから利用者が来歴を取得できるようにする。[REL-001](records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)で、利用者自身の期待値に照らして受け入れる。
5. Container imageを実行する場合は[CONTAINER-001](records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)で、受け入れたexact digestを使用直前の許可へ結ぶ。許可後に実際に稼働した内容は別に確認する。

前段の成功を次段の許可と読み替えません。どの段階も、必要な記録の欠落や評価不能を成功として渡さないことが条件です。この案内は読む順序であり、実環境への導入や一連の強制を確認した結果ではありません。

旧成果物の採否は[移行台帳](../docs/MIGRATION.md)、現在地・未確認範囲・次の作業は[移行計画](../docs/MIGRATION_PLAN.md#現在地と次の作業)を参照してください。
