# 設計・実装

解こうとしている設計問題から探してください。Patternは方式・強制点・代償を示し、製品固有の実装は各patternから参照します。
実装例がないpatternもあります。ガイダンスの存在は実環境の導入証拠ではありません。

## パイロットの設計パターン

| Domain | Pattern | 判断すること |
|---|---|---|
| Secure Coding | [Unicode source review](secure-coding/unicode-source-review/README.md) | 表示、字句解釈、識別子、受入側の検査をつなぐ |
| AI Development Security | [Agent extension admission](ai-development-security/agent-extension-admission/README.md) | 拡張の採用審査と実行時の照合・失効確認をつなぐ |
| AI Development Security | [Repository agent guidance review](ai-development-security/repository-agent-guidance-review/README.md) | 開発agentの指示変更と、その効果の評価を分ける |
| AI Development Security | [Untrusted development content boundary](ai-development-security/untrusted-development-content-boundary/README.md) | 読んだ資料の出所・依頼・実行権限を分ける |
| AI Development Security | [Development runtime isolation](ai-development-security/development-runtime-isolation/README.md) | ファイル・認証情報・通信の到達範囲と、管理方針・迂回経路を分ける |
| AI Development Security | [Development action authorization](ai-development-security/development-action-authorization/README.md) | 承認した操作と実行対象を一致させ、再利用・結果不明を扱う。旧AI-004の設計部分のみ先行移行 |
| Source Protection | [Source credential lifecycle](source-protection/source-access-credential-lifecycle/README.md) | 認証情報の発行・権限・失効 |
| Source Protection | [Secret checks before publication](source-protection/secret-checks-before-publication/README.md) | コミット・送信・受入・mergeの境界に検査を置き、hooks迂回と履歴の混入を扱う |
| Source Protection | [Public exposure observation and triage](source-protection/public-exposure-observation-and-triage/README.md) | Public source surfaceのcoverage、candidate state、triage、response handoffをつなぐ |
| Source Protection | [Managed developer endpoint](source-protection/managed-developer-endpoint/README.md) | 端末の登録・現在の状態・業務アクセスを分け、更新・監視・紛失時対応をつなぐ |
| Dependency Security | [Dependency release cooldown](dependency-security/dependency-release-cooldown/README.md) | 観測期間を置く方式の選択 |
| Dependency Security | [Install execution policy](dependency-security/install-execution-policy/README.md) | 準備用コードの許可と拒否 |
| Dependency Security | [Reviewed dependency intake](dependency-security/reviewed-dependency-intake/README.md) | 採用判断と通常build入力の接続 |
| Detection / Verification | [Scanner acquisition and evidence boundary](detection-verification/scanner-acquisition-and-evidence-boundary/README.md) | Scanner取得、data更新、実行状態、gate evidenceの分離 |
| Detection / Verification | [External observation and inventory reconciliation](detection-verification/external-observation-and-inventory-reconciliation/README.md) | 外部観測の範囲・帰属・台帳差分・再出現を結ぶ |
| CI/CD Security | [Untrusted PR boundary](cicd-security/untrusted-pr-boundary/README.md) | 未信頼producerと権限付きconsumerの分離 |
| CI/CD Security | [Workload federation boundary](cicd-security/workload-federation-boundary/README.md) | Workloadの認証・発行条件・cloud権限 |
| CI/CD Security | [CI state and runner lifecycle](cicd-security/ci-state-and-runner-lifecycle/README.md) | 再利用cacheと破棄するrunner資産 |
| Build Security | [Build execution boundary](build-security/build-execution-boundary/README.md) | 取得・実行・外側の強制・観測の分離 |
| Build Security | [Approved release build process](build-security/approved-release-build-process/README.md) | 承認builder、build定義、重要入力、release昇格を一つの経路として照合する |
| Build Security | [Platform-owned provenance generation](build-security/platform-owned-provenance-generation/README.md) | Build jobとprovenance生成・認証の権限を分け、consumerへ渡す契約を作る |
| Release Integrity | [Consumer artifact acceptance](release-integrity/consumer-artifact-acceptance/README.md) | 独立した期待値と使用gate |
| Release Integrity | [Provenance distribution and availability](release-integrity/provenance-distribution-and-availability/README.md) | Artifact digestからprovenanceの発見・取得・保持・no downgradeを設計する |
| Release Integrity | [Release SBOM identity and analysis intake](release-integrity/release-sbom-identity-and-analysis/README.md) | Final artifactとSBOMを結び、観測範囲、公開、analysis処理、deployment relationを分ける |
| Release Integrity | [Supplier SBOM intake boundary](release-integrity/supplier-sbom-intake-boundary/README.md) | 供給者SBOMの出所・対象を照合し、隔離から限定した取込先へ渡す |
| Release Integrity | [Artifact signing boundary](release-integrity/artifact-signing-boundary/README.md) | 承認した成果物、署名権限、鍵、署名、公開、release gateを接続する |
| Governance / Operations | [Incident impact and response planning](governance-operations/incident-impact-and-response-planning/README.md) | 製品影響・調査範囲・初動 |
| Governance / Operations | [Security exception decision boundary](governance-operations/security-exception-decision-boundary/README.md) | 元の失敗と例外decisionを分け、使用時に状態を評価する |
| Governance / Operations | [Evidence-bound vulnerability prioritization](governance-operations/vulnerability-priority-decision/README.md) | Finding・適用性・severity・known exploitationをpriority decisionへ結ぶ |
| Governance / Operations | [Credential exposure containment and recovery](governance-operations/credential-exposure-containment/README.md) | 旧authorityと派生sessionの封じ込め、consumer移行、拒否確認、影響調査をつなぐ |
| Governance / Operations | [Deployed artifact rebuild and replacement](governance-operations/deployed-artifact-recovery/README.md) | 影響artifactのclean rebuild、exact digest rollout、old digest非稼働をつなぐ |
| Secure Design / Coding | [Object access boundary](secure-design/object-access-boundary/README.md) | 対象・操作・tenantごとの認可 |
| Container / Cloud / IaC Security | [Runtime detection to triage](container-cloud-iac-security/runtime-detection-to-triage/README.md) | 検知・health・通知・担当者の初動 |
| Container / Cloud / IaC Security | [Deployment artifact admission boundary](container-cloud-iac-security/deployment-artifact-admission-boundary/README.md) | Consumer acceptanceをexact artifactの最終使用許可へ結ぶ |
| Container / Cloud / IaC Security | [Container registry publication and lifecycle](container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md) | Registry endpoint・権限・不変性・audit・withdrawalを設計する |
| Container / Cloud / IaC Security | [Infrastructure plan, apply, and drift boundary](container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md) | Source・依存・resolved plan・apply authority・provider上の現在状態を一つの変更として結ぶ |
| Container / Cloud / IaC Security | [Node runtime and management boundary](container-cloud-iac-security/node-runtime-management-boundary/README.md) | Runtime・kubelet・host管理面、node identity、更新・隔離・再登録を一つのlifecycleとして設計する |
| Container / Cloud / IaC Security | [Workload privilege and host boundary](container-cloud-iac-security/workload-privilege-and-host-boundary/README.md) | Workloadのprocess・kernel・host・filesystem・control-plane authorityを制限する |
| Container / Cloud / IaC Security | [Workload network allow boundary](container-cloud-iac-security/workload-network-allow-boundary/README.md) | 通信契約、既定拒否、両端のallow、実効性の確認を設計する |
| Container / Cloud / IaC Security | [Workload resource budget and pressure boundary](container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md) | Workload、tenant、nodeのresource budgetとpressure時の挙動をつなぐ |

関連するcontrolは[一覧](../controls/README.md)から選び、教材は各controlの`learning.md`を続けて読めます。
参照版・採否は[Sources](../sources/README.md)へ分けています。[マッピング](../mappings/README.md)は成果物間の関係であり導入の証拠ではありません。
現在地と次の主題は[進め方と移行計画](../docs/MIGRATION_PLAN.md#現在地と次の作業)を参照してください。
