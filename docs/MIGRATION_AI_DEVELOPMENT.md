# AI Development Security — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [旧AI-005〜009の移行判断](#ai-development-scope-review)
- [AI runtime migration reconciliation](#ai-runtime-migration)
- [Development content injectionの移行判断](#development-content-injection-migration)
- [Development agent work budgetの移行判断](#development-work-budget-migration)
- [Repository agent guidanceの移行判断](#repository-agent-guidance-migration)

<a id="ai-development-scope-review"></a>

<a id="ai-development-scope-review--旧ai-005009の移行判断"></a>
## 旧AI-005〜009の移行判断

旧`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の[AI-005〜009](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security)を、開発者端末・IDE・CLI・repository・CIで使うcoding agentの範囲で読み直した記録です。[Security scope](SECURITY_SCOPE.md)に従い、製品のAI機能、RAG、製品内memory・multi-agent構成、AI製品のTEVVは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)へ委ねます。委ねることは、別PJでの実装済み状態を意味しません。

読者は開発agentを採用・設計・診断する担当者です。守るのは開発作業の継続、ソースと認証情報、外部サービス、変更・公開・deploy権限です。旧パッケージは合成JSONを検査し、live agent・tool・providerでの強制を確認していません。以下の対応は移行判断であり、実環境の検証結果ではありません。

| 旧control | 開発環境での判断 | 製品AIとの境界 |
|---|---|---|
| [AI-005 Memory / context lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-memory-context-lifecycle/README.md) | `deferred`。開発agentが作業をまたいで再利用するcontextを保存・再読込する構成なら、出所を失った指示や秘密情報が次の作業へ入る独立した失敗経路がある。採用する保存・検索経路を選んでから再評価する | 顧客memory、tenant隔離、providerのbackup・vector index・削除保証は対象外 |
| [AI-006 Action integrity / output validation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-action-integrity-output-validation/README.md) | `split`。開発agentの操作提案、対象・引数、承認、実行、結果不明は既存[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と[操作認可pattern](../engineering/ai-development-security/development-action-authorization/README.md)へ接続する。別controlは作らない。採用するtool adapterが決まれば、結果が要求に対応するかを製品別実装で確認する | 製品内agentのaction処理・application authorizationは対象外 |
| [AI-007 Resource budget monitoring](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-resource-budget-monitoring/README.md) | `split`、[開発作業予算へ移行](MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)。個別操作の認可やrunner資源上限と分け、累積量・予約・実行前停止を設計。Linux timeoutの実行期限だけを限定実装 | AI製品の推論予算、サービス運用、顧客向け利用制限は対象外 |
| [AI-008 Multi-agent trust / delegation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/multi-agent-trust-delegation/README.md) | `deferred`。開発agentが別のagentへ作業を渡す構成を採用した時に、親の対象・権限・予算を越える経路を確認する。単なる子processやtool呼出しは[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の実行境界から始める | 製品のorchestrator、tenant間委譲、汎用multi-agent protocolは対象外 |
| [AI-009 Rogue agent containment / recovery](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/rogue-agent-containment-recovery/README.md) | `deferred`。長時間・自律実行する開発agentを採用した時に、process停止と残存権限の失効、送信済み操作の照合、再開条件を横断して設計する。現行の[AI-002失効の受け渡し](../engineering/ai-development-security/agent-extension-admission/README.md#失効を実行環境へ渡す)とAI-004を、全体の停止・復旧完了と読み替えない | AI製品のincident control plane・fallback・復旧設計は対象外 |

<a id="ai-development-scope-review--旧項目の行き先"></a>
### 旧項目の行き先

表の対応は旧IDを新しい要件IDへ一対一で継承するものではありません。採用先が未定の項目は、適用要否も未確定です。

| 旧項目 | 残す問い・扱い |
|---|---|
| AIM-001〜004 | 再利用する開発contextの出所、保存前の確認、秘密情報、量を問う。未信頼資料の扱いは[AI-003](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、認証情報の管理は[SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)と接続する。固定byte上限は継承しない |
| AIM-005〜007 | 作業をまたぐcontextの読込範囲・期限・削除を、実際の保存機能がある場合に評価する。旧user／session／taskの完全一致や5分以内の削除を共通要件にしない |
| AIM-008〜009 | 内容を抑えた証拠とlive未検証の区別を残す。旧tombstone fixtureを削除保証にしない |
| AAI-001〜006 | 構造化した操作、対象と引数、独立した許可、承認と実行の結び付き、再実行防止をAI-004の[DEV-RUNTIME-5〜8](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と操作認可patternへ渡す。特定のdigest形式や300秒の承認を一律に要求しない |
| AAI-007〜008 | Tool結果の対象・要求への対応と結果不明時の照合。後者はAI-004のDEV-RUNTIME-7に含む。前者は実際のtool adapterと結果schemaを選んだ場合に限定実装で確認する |
| AAI-009〜010 | 記録の最小化と合成fixture／liveの区別をAI-004のDEV-RUNTIME-9と実装時の検証条件に残す |
| ARB-001〜004 | 作業ID、計測元、利用量・費用・経過時間、上限と判定不能をAI-007へ残す。旧token数、金額、900秒を移さない。特性ごとの対応は[移行判断](MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)が正本 |
| ARB-005〜009 | Tool呼出し、retry、子作業の累積上限と、新しい操作を実行する前の停止をAI-007へ残す。警告80%、alert 120秒、特定の異常回数は採用先の基準ではない。重要操作の個別許可と結果不明はAI-004へ渡す |
| ARB-010〜011 | 秘密を含まない観測と、fixtureがlive enforcementを示さないことを残す |
| MAD-001〜005 | 実際に開発agent間委譲を使う場合に、依頼元・委譲先・親作業・対象・権限の上限を確認する。Ed25519やtenant分類を共通要件にしない |
| MAD-006〜010 | 子作業の予算・期限・再送・隔離・応答の結び付きを、AI-007とAI-004へ接続して採用先で評価する。1 hop、5分、署名付きresponseは旧fixtureの方式 |
| MAD-011 | 証拠不足とlive未検証を区別する |
| RRC-001〜006 | 開発agent自身から独立した停止経路、対象の特定、停止結果、残存する認証情報・承認・外部操作の照合を、長時間実行agentの採用時に設計する。[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)は認証情報漏えい時の封じ込めであり、agent停止全体の代替ではない |
| RRC-007〜010 | Agentに依存しない手作業への切替と、新しい権限での段階再開を採用先の運用に合わせて評価する。旧二者署名、60秒停止、15分fallback、5分canaryを移さない |
| RRC-011 | 証拠保全とlive未検証を区別する |

<a id="ai-development-scope-review--具体化と再開する条件"></a>
### 具体化と再開する条件

AI-007は[control・教材・設計・診断観点とLinuxの実行期限例](MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)へ具体化しました。[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の単一操作認可、[CI runner lifecycle](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、[workload resource bounds](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)とは異なる境界です。費用・呼び出しの共通予約は、採用するagentと版、利用量の取得元、実行前に拒否できるhookまたはgateway、使い捨て環境が決まった時に限定実装へ進みます。

AI-005は持続的なcontext保存、AI-008はagent間委譲、AI-009は長時間・自律実行と停止経路が、実際の開発環境で確認できた時に再開します。各主題について固有の失敗経路と強制点が説明できなければ、別controlは作らず既存controlと実装判断へつなぎます。

<a id="ai-runtime-migration"></a>

<a id="ai-runtime-migration--ai-runtime-migration-reconciliation"></a>
## AI runtime migration reconciliation

<a id="ai-runtime-migration--判断と範囲"></a>
### 判断と範囲

旧PSB-AI-004の26項目を、開発環境向けの3つの設計パターンへ再配置しました。[Control記録](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)も10の特性へ再編集しました。製品adapter・検証器は保留です。
移行元は`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`の[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)です。製品自体のAI securityは[対象外](SECURITY_SCOPE.md)です。

<a id="ai-runtime-migration--旧項目と判断の正本"></a>
### 旧項目と判断の正本

| 旧項目 | 残す判断 | 設計の正本 |
|---|---|---|
| AAR-001〜004、006〜007 | 隔離、保護対象、認証情報、通信、迂回、管理方針 | [Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md) |
| AAR-005、008〜011 | 公開承認、操作分類、対象・期限・再利用防止 | [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md) |
| AAR-012、018 | 拡張とtoolの同一性、実行時一覧の完全性と鮮度 | [Agent extension admission](../engineering/ai-development-security/agent-extension-admission/README.md) |
| AAR-013〜017 | 効果の限定、人の注意、実行前の強制、発行者の認証、不可分な消費 | [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md) |
| AAR-019〜021 | 監査の最小化、宛先と接続先の照合 | [Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md) |
| AAR-022〜024 | Hook障害、結果不明、commandの間接呼出し | [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md) |
| AAR-025〜026 | 端末網羅、配送・通知、収集元と順序の認証 | [Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md) |

旧仕様・根拠は[SOURCES](../sources/README.md#ref-development-runtime-reconciliation-001)と旧controlに保持します。旧サンプルの時間・回数・DB・署名方式を普遍的な要件へ変換しません。新しい実装方式の選択肢は、旧実装で確認済みの挙動と区別します。

<a id="ai-runtime-migration--control記録へまとめる方針"></a>
### Control記録へまとめる方針

PSB-AI-004の中心は「開発agentに渡す実効権限を、外側の管理方針と現在の操作許可の範囲に収めること」とします。
AI-002は拡張を採用してよいかを所有し、AI-004側は実際の読み込み・呼出しがその承認と一致するかを所有します。認証情報の発行・失効はSOURCE-004、buildの実行境界はBUILD-001に残します。
この境界で10特性を定義し、旧15関係を設計上の直接対応・部分対応・保留へ再割当しました。移行先に旧実装があるかのような根拠文は持ち込みません。

<a id="ai-runtime-migration--未完了"></a>
### 未完了

- Framework mappingの正式な再レビュー。旧関係は移行レビュー中であり、実検証ではありません。
- 製品別の設定優先順位、hook失敗、拡張一覧、実通信、監査収集の現在の挙動の確認。
- 実装を移す場合の安全な拒否・並行消費・配送障害試験。
- 実環境の鍵管理、収集者の信頼、通知先、運用責任者の確認。

これらを完了したと推論せず、control記録は17件、patternは17件です。

<a id="development-content-injection-migration"></a>

<a id="development-content-injection-migration--development-content-injectionの移行判断"></a>
## Development content injectionの移行判断

旧[`PSB-AI-003`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/prompt-document-injection-containment/control.yaml)の対象を、開発agentが読むrepository文書、Issue・PR、Web/API応答、tool出力へ絞りました。移行元の固定revisionは`f42987759218c9b8daf3924320542a1935ef78e0`です。[Security scope](SECURITY_SCOPE.md)に従い、製品のchatbot・RAGは本PJへ戻しません。

読者は開発agentの設計者と診断担当者です。旧パッケージでは「合成run-resultsの構造が正しい」と「実agentが注入を拒否する」が近くに置かれていました。今回の完了条件は、出所・依頼・実行の境界、正当な作業の継続、診断観点を説明できることです。製品別実装の完了や実環境での成功を含めません。

| 旧項目 | 移行先と判断 |
|---|---|
| AII-001〜002 | [DEV-CONTENT-1〜2](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)：入力面ごとの出所と依頼の権限を分ける。6個の固定fixtureとSHA-256一致を普遍要件にしない |
| AII-003〜007 | DEV-CONTENT-3と[設計](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)：注入から保護設定変更、認証情報、通信、依存導入、特権操作への経路を扱う。実際の拒否・隔離は[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の責任 |
| AII-008 | DEV-CONTENT-4と[教材](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/learning.md)：拒否と元の作業の完了を分ける。固定出力digestをあらゆる作業の合格条件にしない |
| AII-009〜010 | DEV-CONTENT-5：最小限の証拠、未実施・判定不能の区別。合成fixtureの`PASS`をlive containmentへ読み替えない |

旧direct-user-prompt scenarioは、資料中の間接注入と異なり、依頼者の権限・管理方針の問題です。管理方針と実行側の拒否はAI-004へ渡し、AI-003の診断件数へ混ぜません。旧packageのWeb/API scenarioは、開発agentが実際に読む場合だけ対象です。旧AISVS C2やAgentic Top 10は製品AI全体の要件・リスク分類を含むため、開発環境の成功証拠として旧8件の`verifies` mappingを継承しません。詳細な出典と採否は[参照資料](../sources/README.md#ref-development-input-trust-001)に保持します。

旧資料ID `REF-AI-001`（Claude Code Hardening Cheatsheet）は製品固有の参考、`REF-AI-002`（OWASP AI Agent Security Cheat Sheet）は開発環境に該当する部分だけを新しい`REF-DEVELOPMENT-INPUT-TRUST-001`へ統合しました。旧IDを新しい成果物の別名として使いません。

旧`secure/`・`insecure/`、`scripts/verify.py`はJSON中の申告値と整合性を検査します。実際のmodel、tool、認証情報パス、通信、実行前の拒否は動かしません。このため本PJの`implementations/`へコピーしません。対象agent・版、入力取得元、toolの強制点、保護対象、使い捨て環境、無効なcanary、元の作業の期待結果を決めたら、その一構成へ限定した実装とsmoke testを作ります。成功、拒否、取得・判断失敗を観測し、旧fixtureとの違いを明示します。

この主題で必要と判断した成果物は[control](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、control配下の教材、[設計pattern](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)、診断観点です。具体実装は上記の採用先が選ばれるまで保留します。旧52件の件数合わせや、すべてのagentを代表する汎用test runnerは作りません。

<a id="development-work-budget-migration"></a>

<a id="development-work-budget-migration--development-agent-work-budgetの移行判断"></a>
## Development agent work budgetの移行判断

旧[PSB-AI-007](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-resource-budget-monitoring/control.yaml)を、開発agentの一依頼に属する累積量と次の実行前の停止へ絞りました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-26です。[旧AI-005〜009の選別](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)からの具体化で、製品の推論サービスや顧客向け予算設計は本PJへ移しません。

| 旧項目 | 移行先・採否 |
|---|---|
| ARB-001 | [DEV-BUDGET-1〜2](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)：責任を持つ作業、計測元、必要情報を確認する。旧AI-004の固定digest、二種類のprovider、七scenarioを一律に要求しない |
| ARB-002〜003 | DEV-BUDGET-2〜3：利用量と実行中の予約、次の消費可能量、通貨・単位・価格の不明を分ける。旧20,000／8,000／28,000 token、500,000 USD micro-unitを共通上限にしない |
| ARB-004 | DEV-BUDGET-3〜4：外側の実行期限と実際の停止。旧900秒は移さない。具体例の時間は例として選び、実環境の適正値としない |
| ARB-005〜007 | DEV-BUDGET-1〜3：tool、再試行、子作業の累積量と割当。旧20 tool call、重要操作一回、retry三回、深さ四を共通要件にしない |
| ARB-008 | DEV-BUDGET-5：繰り返す拒否、承認再利用、hook障害を実行方針・調査へ渡す。異常回数の固定閾値は採用先で決める。単一操作の認可はAI-004を再実装しない |
| ARB-009 | DEV-BUDGET-3〜6と[設計](../engineering/ai-development-security/development-work-budget-gate/README.md)：判断と実停止を結ぶ。警告80%とalert 120秒を外し、通知と強制を区別。終了時の要約・読取りも有限の予約に含める |
| ARB-010〜011 | DEV-BUDGET-2・6：証拠不足をゼロへ変換せず、秘密情報を増やさず、合成fixtureと実強制を区別する |

旧verifierは合成session countersから判断し、申告されたbreaker・alert receiptを照合します。Model・toolを起動せず、並列の予約、provider usage、費用請求、実停止、実通知を観測しません。旧JSON、危険なoverlay、verifierは本PJの実装例へコピーしません。

必要な成果物は[control](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)、control配下の教材、設計pattern、診断観点と判断しました。ローカル実行時間の経路は製品を選ばず具体化できるため、GNU coreutils 9.7の[Linux timeout例](../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)を追加しました。実processの成功・停止・起動失敗を六件で観測しますが、予算control全体の検証や実agentの停止確認ではありません。

実装から戻す境界は、期限後の停止猶予、子processの所属、監視process自身の停止、再起動での予算初期化、外部操作の結果不明です。費用・token・呼び出しの共通予約は、agent・版、利用量と料金の取得元、実行前強制点、使い捨て対象が選ばれた時に限定実装へ進みます。これが必要な採用先では、時間だけの例で完了扱いにしません。

旧frameworkのATLAS `2026.05 / AML.T0034.002・AML.T0029・AML.M0024`、Agentic Top 10 `2026 / ASI08`、AISVS `1.0 / v1.0-C9.1.2・v1.0-C12.2.2`は履歴として保持します。製品AI全体やlive providerへの関係を含むため、旧`verifies / high`などを本PJの実証済み関係へ移しません。今回はframework mappingを追加せず116件のままです。直接の設計入力とその限界は[REF-DEVELOPMENT-WORK-BUDGET-001](../sources/README.md#ref-development-work-budget-001)へ分けます。旧資料ID`REF-AI-002`の汎用agentガイダンスは開発環境に必要な部分だけ再参照し、新しいIDの別名として残しません。

<a id="repository-agent-guidance-migration"></a>

<a id="repository-agent-guidance-migration--repository-agent-guidanceの移行判断"></a>
## Repository agent guidanceの移行判断

旧[`PSB-AI-001`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/repository-owned-ai-security-guidance/control.yaml)を、開発agentが読むrepository所有の指示と、その開発作業への影響に絞りました。固定した移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。製品が顧客へ提供するAI機能の設計、RAG、AI製品のTEVVは[ai-security-foundryとの分担](SECURITY_SCOPE.md)に従い対象外です。

| 旧項目 | 残す判断と移行先 |
|---|---|
| AIG-001 | [DEV-GUIDE-1〜2](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)：実際に読む指示の場所・版と変更の独立レビュー。4ファイル・単一bundle digestを普遍要件にしない |
| AIG-002 | DEV-GUIDE-2〜3：指示に保護策を弱める意味を混ぜない。Hashと自己申告のsemantic reviewを承認の代わりにしない。実行時の拒否は[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) |
| AIG-003〜005 | DEV-GUIDE-4：同条件で指示の効果を比較し、安全上の逸脱、作業の達成、過剰拒否を分ける。旧4課題×2回、改善20ポイント、false block 15%等はfixture固有の値 |
| AIG-006〜007 | DEV-GUIDE-5：run・scorer・証拠の不足とlive未実施を成功へ変えない。生の秘密・prompt・出力を公開repositoryへ置かない |

旧`secure/benchmark/`の初期状態hashは実repositoryのsnapshotではなく合成識別子です。`guided-results.json`と`baseline-results.json`はagentを起動せずに用意した結果で、旧verifierはその整合と集計を検査します。62.50%→93.75%という値は、現在のagentや指示の効果ではありません。旧CodeGuard profileもrepository所有の例であり、外部製品の動作や利用中の設定を示しません。旧実験prompt、結果JSON、verifierは本PJの実装・評価へコピーしません。

必要な成果物は[control](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)、control配下の教材、[設計パターン](../engineering/ai-development-security/repository-agent-guidance-review/README.md)、診断観点、技術経路が明確な[GitHubの変更レビュー例](../engineering/ai-development-security/repository-agent-guidance-review/implementations/github-codeowners/README.md)です。GitHub例はCODEOWNERSとbranch保護の接続を示しますが、レビュー担当者・保護branch・bypass・実GitHubの拒否結果は未設定・未確認です。したがって具体実装の設計はあり、採用先での動作確認は残作業です。開発agent比較の実装はagent・版、作業群、実行権限、観測元を選んだ時に限定して作ります。

旧framework mappingのATLAS `AML.T0081`、`AML.CS0041`、Agentic Top 10 `ASI04`は、変更の脅威との関連を示しますが、今回のGitHub設定や実agent効果の確認ではありません。旧`detects`・`mitigates`の確度をそのまま継承せず、新しいframework mappingは追加しません。版と採否は[参照資料](../sources/README.md#ref-development-guidance-001)に保持します。

旧資料ID `REF-AI-001`のClaude Code固有部分は製品採用時の参考にとどめ、`REF-AI-002`の一般的なagent guidanceは開発環境に当たる部分だけ新しい資料記録へ統合しました。旧IDを新しい成果物の別名として残しません。
