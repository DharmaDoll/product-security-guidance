# Portfolio migration review

## 今回の判断

この文書は初回に棚卸しした8 domainの候補と、その後の移行判断を保持します。現在の全件一覧は[Controls](../controls/README.md)、現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を正本とします。
読者が判断できる内容を増やすことが目的であり、旧パッケージの数を新構造へ揃えることは目的ではありません。

2026-09-16時点の旧`controls/*/*/control.yaml`には52件ありました。初回棚卸しの3 domainが19件、
今回の8 domainが33件で、旧Secure Design controlは0件でした。2026-09-25にrepository pilotから
[PSB-DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)を追加しています。
これは旧controlの移行や組織への導入を意味しません。

2026-09-20の[スコープ決定](SECURITY_SCOPE.md)により、製品自体のAI securityはai-security-foundryの担当です。
下記の旧件数は棚卸しの履歴です。`out-of-scope`を残作業へ加えず、`scope-review-required`は開発環境に必要な部分だけを再審査します。

今回の対象はメタデータ、READMEの主題・参照先、既存の計画と参照資料記録です。
実装コード・全検証器の意味的レビュー、製品の現在の仕様、実環境の採用状態は未確認です。
以下は候補の判断と移行状態です。移行済みでも実装・導入の完了やframework要件の充足を意味しません。

## 分析の根拠

- [参照資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md): 版、採否、除外理由、重要仕様を保持する出発点。参照資料の継承と本文の圧縮を別に扱う。
- [REF-PORTFOLIO-001](../sources/README.md#ref-portfolio-001): 七つのレイヤーで偏りを確認する。個別の要件へ自動変換しない。
- [Supply-chain attack control list](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md): 攻撃段階と前後の責任を確認する。アプリケーション固有の悪用経路をこの12段階だけへ押し込めない。
- [参照資料の方針](SOURCE_POLICY.md)、[成果物モデル](ARTIFACT_MODEL.md): control、教材、pattern、製品実装、評価を役割で分ける。

## 初回に棚卸しした8 domainと現在の扱い

表の`split候補`は必要な知識を再編集して実装と分ける方針、`deferred`は今回の追加pilotより後に扱う方針です。
教材は各controlの問いに分けるか正本へリンクし、controlの異なる保証境界は統合しません。旧controlへのリンクは移行元、新しい記録へのリンクは移行先です。

### Secure Design — 旧control 0件、repository pilot 1件

既存controlから移植できる内容はありません。[計画済み主題](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/PLANNED_CONTROLS.md)を起点に、
資産・主体・データフロー・信頼境界から設計を判断する教材を新たに検討します。
[REF-USER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-004)の組織チェックリストは原本未提供です。
ASVS等から原本を復元したり、空のcontrolを作ったりせず、原本の受領を待つ作業と公開教材の設計を分けます。

最初の候補だった「利用者が指定する対象へのアクセスを、どこで認可するか」は、2026-09-17に教材、pattern、
Python / SQLiteの限定実装として具体化し、2026-09-25に[PSB-DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)として
保証目標を明示しました。既存IDの移行ではなく、未提供の組織チェックリストやexact ASVS mappingを補完したものでもありません。

### Secure Coding — 1件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-CODE-005 Unicode source deception](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/secure-coding/unicode-source-deception/README.md) | `split候補`: 表示と解釈が異なるソース、レビューで見落とす条件、Python限定の検出実装 | 表示の曖昧さを検出しても、認可・入力処理等のアプリケーション欠陥は検証できない |

唯一の既存例を移すだけではSecure Codingの情報設計を検証したとは扱いません。
Secure Designのシナリオを、実際の認可処理と拒否テストへつなげる追加pilotが必要です。

### Build Security — 3件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-BUILD-001 Build containment](../controls/records/build-security/psb-build-001-build-containment/README.md) | `移行済み`: 入力、通信、権限、隔離、検知の役割を分けたガイダンス | 実sandbox・通信拒否・sensorは未確認 |
| [PSB-BUILD-002 Hosted consistent build](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/README.md) | `deferred`: 承認builder、固定した定義、利用者が変更できる範囲を残す | hostedであることは再現性・隔離・SLSA levelの証明ではない |
| [PSB-BUILD-003 Platform provenance generation](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md) | `移行済み`: platform側の来歴生成とjob側の自己申告を区別する | 来歴の生成、配布、consumerによる照合は別の責任。製品実装は未選定 |

### Container / Cloud / IaC Security — 5件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-CONTAINER-001 Deployment artifact admission](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) | `分割移行済み`: Exact artifact、consumer acceptance、final-stateの拒否境界。Privilege・host・filesystemは[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)、networkは[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)、resourceは[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)へ移行 | Live admission、workload・CNI・resource runtime enforcementは未確認 |
| [PSB-CONTAINER-002 Container registry publication boundary](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md) | `移行済み`: Endpoint、repository権限、変更不能性、audit、lifecycle | 登録内容の安全性とadmissionは別。Provider実装は未選定 |
| [PSB-CONTAINER-003 Container host and daemon boundary](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md) | `移行済み`: Runtime・kubelet・host管理面、node identity、更新・隔離・再登録を分けた。[旧成果物](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-host-daemon-hardening/README.md)のsynthetic evaluatorは非移植 | Workload設定はCONTAINER-005。対象OS／runtime／provider未選定のため実装は作らず、live nodeは未確認 |
| [PSB-CONTAINER-004 Runtime threat detection](../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) | `移行済み`: 観測、rule、配送、sensor health、対応判断を分けたガイダンス | Live sensor・配送・対応は未確認。CIの検知を本番の導入証拠にしない |
| [PSB-IAC-001 Infrastructure change authorization and drift](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | `移行済み`: Golden Pathを入口へ位置付け、source・依存、resolved plan、apply、provider状態、driftを結ぶ。旧synthetic verifierは非移植 | Plan検査、provider側の強制、現在状態を分けて接続。対象provider／resource未選定のため実装は作らず、live cloudは未確認 |

### Release Integrity — 5件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-REL-001 Signature / provenance verification](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) | `移行済み`: consumerが管理する署名者・builder・sourceの期待値をガイダンス化 | Crypto実装は保留。有効な署名でも期待しない生成条件なら拒否する |
| [PSB-REL-002 Provenance distribution and availability](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md) | `移行済み`: Artifact digestから一つ以上のprovenanceを発見・取得し、publication completion、immutability、retention、no downgradeを管理。旧synthetic verifierは非移植 | 生成はBUILD-003、consumer検証はREL-001。対象ecosystem未選定のためlive distributionは未確認 |
| [PSB-REL-003 SBOM binding / publication](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/README.md) | `split候補`: source・build・deploymentの観測を区別し、同一性でつなぐ | SBOM公開と分析処理完了、稼働製品への適用判断は別 |
| [PSB-REL-004 Supplier SBOM trust](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/README.md) | `deferred`: 外部供給者、署名者の状態、隔離と受入判断 | 署名はSBOMの網羅性や製品の無害性を証明しない |
| [PSB-REL-005 Artifact signing generation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/README.md) | `deferred`: 正確な署名対象、署名権限、鍵、公開完了を分ける | sign-only権限と署名対象の正当性は別 |

### AI Development Security — 旧11件を範囲別に選別

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-AI-001 Repository-owned AI security guidance](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/repository-owned-ai-security-guidance/README.md) | `deferred`: guidanceの出所、変更レビュー、baselineとの比較 | 指示を与えることと独立した強制・検証は別 |
| [PSB-AI-002 Agent extension dependency governance](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) | `移行済み`: 拡張の内容・権限・審査・期限・失効と実行環境への受け渡し | 稼働版の証明、内容審査の質、実行時強制は未確認 |
| [PSB-AI-003 Prompt / document injection containment](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/prompt-document-injection-containment/README.md) | `split候補`: repository文書・issue・tool出力による開発agentへの攻撃を扱う | 製品のchatbot・RAGへの攻撃は別PJの担当 |
| [PSB-AI-004 AI coding agent runtime hardening](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/README.md) | `記録移行済み`: [操作認可](../engineering/ai-development-security/development-action-authorization/README.md)・教材と[実行環境の隔離](../engineering/ai-development-security/development-runtime-isolation/README.md)を再編集 | [Control記録](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)を再編集。製品adapter・実環境は未検証 |
| [PSB-AI-005 Agent memory / context lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-memory-context-lifecycle/README.md) | `scope-review-required`: 開発agentの作業context・秘密情報・保存範囲だけを再審査 | 製品のmemory・tenant境界は別PJの担当 |
| [PSB-AI-006 Agent action integrity / output validation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-action-integrity-output-validation/README.md) | `scope-review-required`: 開発agentの変更・公開・deploy操作と結果の対応だけを再審査 | 製品内agentのaction処理は別PJの担当 |
| [PSB-AI-007 Agent resource budget monitoring](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-resource-budget-monitoring/README.md) | `scope-review-required`: 開発・CIでのagentの暴走防止に必要な上限・停止を再審査 | 製品の推論予算・サービス運用は別PJの担当 |
| [PSB-AI-008 Multi-agent trust / delegation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/multi-agent-trust-delegation/README.md) | `scope-review-required`: 開発agent間の作業・権限委譲だけを再審査 | 製品のmulti-agent構成は別PJの担当 |
| [PSB-AI-009 Rogue agent containment / recovery](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/rogue-agent-containment-recovery/README.md) | `scope-review-required`: 開発環境のagent停止と残存権限の失効を再審査 | 製品AI機能の封じ込め・復旧は別PJの担当 |
| [PSB-AI-010 AI application gateway / data egress](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-application-gateway-data-egress/README.md) | `out-of-scope`: ai-security-foundryへ委ねる | AI application gatewayは本PJへ移行しない |
| [PSB-AI-011 RAG corpus integrity / retrieval](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/rag-corpus-integrity-retrieval/README.md) | `out-of-scope`: ai-security-foundryへ委ねる | RAG corpus・retrievalは本PJへ移行しない |

AI領域は開発環境で守る資産と権限を特定してから、一般的な認可・外部入力・依存受入との共通教材を検討します。別PJの担当は[Security scope](SECURITY_SCOPE.md)で確認します。
製品固有のhookやadapterを一般原則へ置き換えず、現行仕様を再確認した実装だけを別に移します。

### Detection / Verification — 3件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-DETECT-001 Scanner evidence trust boundary](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) | `移行済み`: scanner自身の出所・DB・終了状態と検査対象を分離 | 実行成功、findingなし、coverage十分は別 |
| [PSB-DETECT-002 AI TEVV release gate](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/ai-tevv-release-gate/README.md) | `out-of-scope`: AI製品のTEVVはai-security-foundryへ委ねる | 開発用guidance・拡張の限定評価は旧AI-001の別境界として扱う |
| [PSB-DETECT-003 External attack surface reconciliation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/external-attack-surface-reconciliation/README.md) | `split候補`: 所有範囲、外部観測、帰属、再出現、source health | 自社domainが指す第三者IPをscan権限へ拡張しない。未観測を資産なしにしない |

### Governance / Operations — 5件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-GOV-001 Supply-chain impact assessment](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) | `移行済み`: packageからbuild・artifact・稼働製品への逆引きと初動のガイダンス | 実組織の対応能力と実対応は未確認 |
| [PSB-GOV-002 Security exception lifecycle](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) | `移行済み`: 共通lifecycleとcontrol固有risk判断を分離 | 例外が有効でも元の不合格が合格になるわけではない |
| [PSB-GOV-003 Product vulnerability priority decision](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md) | `migrated-guidance`: 適用性、known exploitation、severity、priority、期限、担当者 | 旧composite verifierは非移植。Adapterは観測可能な単位へ分ける |
| [PSB-GOV-004 Credential exposure containment](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) | `migrated-guidance`: 漏えい疑い、派生権限、consumer移行、古い権限の拒否、影響調査 | 旧synthetic verifierは非移植。Providerとcredential classを選定してから実装する |
| [PSB-GOV-005 Deployed artifact recovery](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) | `migrated-guidance`: current riskからclean rebuild・replacement・旧digest非稼働まで | 旧synthetic verifierは非移植。Builder・registry・deployment platform選定後に実装する |

## 参照資料を移す優先単位

この表は旧資料記録への追跡です。まだ移行していない資料へ新IDを確定せず、各pilotで役割・命名を見直します。
外部リンク、exact version、integrity記録、利用条件・除外理由は旧記録を正本として保持します。

| 主題 | 保持する仕様・資料 | 設計へ反映する判断 |
|---|---|---|
| Build→Release | [REF-BUILD-001](../sources/README.md#ref-build-001)、[NIST SP 800-204D記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-cicd-012)、[threat matrix記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-cicd-011)、[SLSA registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/slsa/README.md)、[Sigstore記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-003) | containment、来歴生成、署名、consumer照合を別の強制点としてつなぐ。SLSA source/build要件を区別する |
| Runtime / cloud / IaC | [IaC change資料](../sources/README.md#ref-iac-change-boundary-001)、[Container host資料](../sources/README.md#ref-container-host-daemon-001)、[Runtime detection資料](../sources/README.md#ref-container-003) | IaC plan・apply・actual state、container admission、host、観測、配送、health、対応を分ける。旧製品版やmutableな文書を現在の仕様と断定しない |
| PSIRT / exposure / refresh | [SBOM lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-002)、[Dependency-Track](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-001)、[REF-USER-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-005)、[KEV](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-002)、[FIRST maturity](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-003)、[FIRST Services 1.1](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-004)、[CVSS 4.0記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-005)、[NIST SP 800-61 Rev.3記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-006) | 正確な製品適用、担当者、対応期限・連絡、置換完了をつなぐ。PSIRT能力評価と個別controlの合格を分ける |
| Application / AI / scanner | [REF-USER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-004)、[AI設計資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md)、[ASVS registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-asvs/README.md)、[AISVS registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-aisvs/README.md)、[ATLAS registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/mitre-atlas/README.md)、[Trivy記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-detect-001) | 外部入力を権限へ昇格させない原則と製品固有の実装を分ける。exact要件・ATLAS content/format版を保持し、欠けた組織原本を補完しない |

上記の組合せと優先順位はリポジトリでの解釈です。資料の推奨を一括採用したという意味ではありません。

## 攻撃段階と受け渡しのレビュー

| 攻撃段階 | 主な脅威 | 対応候補・次の境界 |
|---|---|---|
| 3: AI開発経路 | 外部指示や拡張がtool権限へ昇格 | [AI-002](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)→[旧AI-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/README.md)→[旧AI-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-action-integrity-output-validation/README.md)。依存承認・実行時の保証目標は移行済み。実際の強制と一致は未検証 |
| 7→8: Build実行・来歴 | build中に秘密情報を取得し、自己申告の証跡を正規の来歴にする | [BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)→[BUILD-003](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)。実行境界とplatform生成境界を分離済み。製品実装と承認builderは未確認 |
| 9→10: Release・admission | 署名済みでも期待しない成果物を配布・実行し、正規workloadへ過大なhost権限を渡す | [REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)→[CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)でartifactを、[CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)でruntime authorityを別に判断する。Live enforcementは未確認 |
| 11→12: 本番・対応 | sensor停止、通知不達、未知資産、適用製品の誤認で対応が遅れる | [CONTAINER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/runtime-threat-detection/README.md)、[DETECT-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/external-attack-surface-reconciliation/README.md)→[GOV-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/supply-chain-incident-readiness/README.md)→[GOV-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/exploited-vulnerability-prioritization/README.md)。収集異常とsecurity findingを別に扱う |

Secure Design / Secure Codingは、この供給経路とは別に、正規利用者が他者のデータへアクセスする等の
アプリケーション内の悪用経路を扱います。ソースや署名が正規でも認可欠陥は成立します。

## 次の作業順序と一区切り

2026-09-17更新: [構造レビュー](STRUCTURE_REVIEW.md)で集約表・索引・参照anchorを修正しました。
2026-09-20更新: GOV-001、GOV-002、DETECT-001、AI-002の追加後に横断レビューと補修を行い、AI-004は操作認可の設計・教材を先行移行しました。その後の補修は[構造レビュー](STRUCTURE_REVIEW.md)、現在地と次作業は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)に記載します。

### 初回の作業順序（履歴・現在の指示ではない）

2026-09-17追記: Operations pilotとしてPSB-CONTAINER-004、教材、ENG-RUNTIME-001を再編集しました。
GOV-001はcontrol・教材・patternへ分離済みです。実対応・PSIRT能力評価は未実施です。
四つの異なる主題の初回再編集は揃いました。次は構造レビューで重複・参照欠落・入口の整合性を確認し、次batchを決めます。

2026-09-17追記: Application pilotとして[Object access boundary](../engineering/secure-design/object-access-boundary/README.md)、教材、Python / SQLiteの限定実装を追加しました。
既存control IDや組織チェックリストを流用せず、認証済みcontextの契約とDB条件を分けています。全endpoint・HTTP認証・並行処理は未確認。次はOperations pilotです。

2026-09-25追記: 上記教材を[PSB-DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)の隣へ移し、repository pilotとしてcontrol記録を追加しました。

2026-09-17追記: Consumer pilotの記録・教材・patternの再編集も完了しました。Crypto実装は保留し、次はApplication pilotへ進みます。

2026-09-17更新: Build pilotのcontrol・教材・pattern・参照資料の再編集は完了しました。
[移行台帳](MIGRATION.md)に保留した実装と未確認範囲を記録しています。次はConsumer pilotです。

1. **Build pilot**: PSB-BUILD-001を再編集。実行中の権限・通信をどこで制限するかと、sensorの観測・health・対応を分ける。実装を移す場合だけ実際の拒否挙動を検証する。
2. **Consumer pilot**: PSB-REL-001で、Buildの出力を誰の期待値で受け入れるか検証する。producerの自己申告をconsumer policyにしない。
3. **Application pilot**: Secure Designの一つの認可シナリオからSecure Codingの小さな実装・拒否テストへつなぐ。仕様・IDは着手時に決定し、原本未提供のチェックリストとは分離する。
4. **Operations pilot**: PSB-CONTAINER-004とPSB-GOV-001のうち一つの検知→初動シナリオを選ぶ。イベント、sensor health、配送、製品適用、担当者をつなぎ、PSIRT全体を満たすとは扱わない。
5. **構造レビュー**: control・教材・pattern・評価の重複、参照仕様の欠落、担当者と開発者の入口を読み通す。その結果で構造を調整し、次の移行batchを決める。

各回で有用な教材を正本として作り、複数domainへ複製しません。講義で生じた横断的な問いや見方は
まず教材の文脈に残し、独立成果物を先に作りません。ファイル数・移行件数・全レイヤーの充足は完了条件にしません。

この一区切りでは、基盤・consumer・アプリケーション・運用という異なる性質の内容で新構造が機能することを確認します。
個別実装の採否、exact mappingの再割当、参照IDの名称改革、現在の製品仕様の確認は各pilotの台帳へ残します。
棚卸しだけではcontrol indexやframework mappingに移行済みの関係を追加しません。
