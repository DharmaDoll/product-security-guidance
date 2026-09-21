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

### 2026-09-21：独立化の準備

旧ツリーへのローカルMarkdown参照114箇所を、コミット`f429877`の完全SHAを含む外部リンクへ置き換えました。
参照先がそのGitオブジェクトに存在することを確認し、資料の版・採否・保留判断は維持しています。
単独で動く`make check`、検査器のテスト、既存実装テストの入口を追加しました。[切り出し手順](REPOSITORY_CUTOVER.md)に公開前の判断を残しています。
この記録は準備の完了であり、新しいリモートリポジトリの作成・push完了を意味しません。

### 2026-09-21：SOURCE-001の端末管理設計を先行移行

[ENG-SOURCE-002](../engineering/source-protection/managed-developer-endpoint/README.md)と[教材](learning/managed-is-not-currently-trusted.md)を追加しました。
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
- 旧[AI-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)のAAR-008〜011、AAR-022〜024を、[ENG-AI-002](../engineering/ai-development-security/development-action-authorization/README.md)と[教材](learning/approval-is-bound-to-an-action.md)へ`split`。移行元は`3bfbeb21246bb2f58c55fa5212068805bca1719b`です。
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
| `controls/source-protection/source-access-credential-lifecycle/README.md` | `split` | コントロール、学習資料、設計パターン、GitHub実装例、洞察 | 認証情報のライフサイクルに関する特性を保持し、導入手順をコントロールから分離 |
| 同パッケージの`control.yaml` | `split` | 簡潔な`control.yaml`、フレームワーク対応関係 | 17件の確認項目をセキュリティ特性へ再編。参照していたフレームワークのバージョンとIDは保持し、新しい特性への割り当てをレビュー対象にした |
| 同パッケージの`secure/`、`insecure/`、検証器、期待結果 | `deferred` | なし | JSONメタデータの検査が実環境の権限制御を強化するか再評価するまで移さない |
| 同パッケージのGitHub導入手順 | `split` | GitHub実装例 | 製品固有の導入判断だけを再編集 |
| `REF-AI-004`、`REF-USER-001`、GitHubのフレームワーク登録情報 | `migrated` | 参照資料と仕様、フレームワーク対応関係 | 固定コミット、バージョン、採用範囲、制約を保持 |
| `controls/dependency-security/release-cooldown/README.md` | `split` | コントロール、学習資料、設計パターン、npm実装例、洞察 | 待機期間が保証することと、npm／プロキシ固有の手順を分離 |
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
| `controls/dependency-security/lockfile-integrity/README.md`、`control.yaml` | `split` | PSB-DEPS-003、共有教材、ENG-DEPS-003。5旧checkを5特性へ再配置し、3件のframework関係を保持 |
| 同パッケージのnative wrapper、runtime metadata、tamper test、期待結果 | `deferred` | 製品仕様と旧対応状態を保持。小さな独立実装として再レビューするまで一括では移さない |
| `controls/dependency-security/dependency-change-review/README.md`、`control.yaml` | `split` | PSB-DEPS-004、共有教材、ENG-DEPS-003。3旧checkを3特性へ再配置し、5件のframework関係を保持 |
| GitHub workflow | `migrated` | 製品別実装へfull SHA・最小権限・基本policyを保持。Live graphとmerge拒否は外部確認手順で扱う |
| `REF-DEPS-002`、native lock仕様、SLSA／SCVS／CISA等の隣接資料 | `migrated` | 版・ID・採否・除外理由と参照リンクを保持。参照一覧の拡張提案と基本workflowの範囲差を明記 |

共有教材は同じ採用判断とbuild入力の受け渡しを扱うため、一つを正本にした。
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
| `controls/cicd-security/runner-hardening/README.md`、`control.yaml` | `split` | PSB-CICD-007、共有教材、ENG-CICD-003。9旧checkを9特性へ配置、6framework関係を保持 |
| `controls/cicd-security/cache-provenance-isolation/README.md`、`control.yaml` | `split` | PSB-CICD-009、同教材・pattern。7旧checkを7特性へ配置、3framework関係を保持 |
| workflow、provisioner、marker test、期待結果 | `deferred` | 旧参照版を保持。Providerの実効cache設定、compute・storageの破棄、実際の否定ケースを再確認してから独立実装へ移す |
| `REF-CICD-014`、`REF-BUILD-001`、cache製品仕様、SITF | `migrated` | 参照版・リンク・採否・限界をsourcesへ保持。runtime sensorは候補のまま |

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

[Control](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)、[教材](learning/an-exception-is-not-a-pass.md)、[ENG-GOV-002](../engineering/governance-operations/security-exception-decision-boundary/README.md)へ分離しました。旧GEX-001〜008をEXCEPTION-1〜8へ一対一で継承し、旧framework mappingの版・ID・関係・confidence・対象を保持しています。
旧verifier、fixture、`psb-security-exception/v1`、30日上限は実装候補として保留しました。Live approval、信頼時刻、取消、policy engine、実gateの採用は未確認です。

### GOV-002 consumer接続（2026-09-20）

PSB-DEPS-001 `DEP-AGE-6`とPSB-DEPS-002 `DEP-EXEC-2`を、[exception consumer mapping](../mappings/exception-consumers.yaml)でGOV-002へ接続しました。
元の不合格property、exact target identity、control側に残すrisk判断、例外でも許可しない範囲を明示しています。Live enforcementは未確認で、他controlは意味的レビュー前にconsumerへ追加していません。

### DETECT-001追加移行（2026-09-20）

[Control](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)、[教材](learning/zero-findings-is-a-scoped-observation.md)、[ENG-DETECT-001](../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)へ分離しました。
旧DVS-001〜008をSCAN-1〜8へ一対一で継承し、5件のframework mappingの版・ID・関係・confidence・対象を保持しています。旧`REF-DETECT-001..003`は役割名`REF-SCANNER-EVIDENCE-001`へ統合し、旧版、digest、採否、限界を残しました。
Trivy、DockSec、Checkovの旧adapter・fixtureは保留し、現行配布物、live DB、coverage、CI gateを検証済みとは扱いません。SCAN-6だけをGOV-002のconsumerへ接続しました。

### AI-002追加移行（2026-09-20）

[Control](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)、[教材](learning/reviewing-an-agent-extension.md)、[ENG-AI-001](../engineering/ai-development-security/agent-extension-admission/README.md)へ再編集しました。
旧AID-001〜007をEXT-1〜7へ一対一で対応付け、脅威・対象・必要な理由を保持しています。旧metadata verifierの入力形式は保証目標にせず、内容審査の記録と審査の質、benchmarkの記録と実際の評価、承認と実行時の強制を区別しました。
旧REF-AI-001・REF-AI-002の今回関連する判断をREF-AGENT-EXTENSION-ADMISSION-001へ集約。既存REF-AI-004は正本への参照を維持し、資料全体の移行完了とは扱いません。
ATLAS `2026.05 (format 6.0.0)`の2件、Agentic Top 10 `2026 / ASI04`の1件、AISVS `1.0 / v1.0-C10.1.1..2`の2件は、旧関係・confidence・根拠・対象・レビュー日を保持した`migration-review-required`です。AISVSの`verifies`は旧関係を表し、今回の文書移行で検証した意味ではありません。
合成artifact、verifier、benchmark、revocation collectorは保留。旧AI-001・AI-003・AI-004は未移行の隣接境界として残し、製品固有設定・tool・外部サービスを導入していません。

### AI securityの担当範囲を限定（2026-09-20）

利用者の指示に基づき、[Security scope](SECURITY_SCOPE.md)を新設しました。AI Development Securityは開発端末・IDE・CLI・repository・CIでAIを使う開発環境に限定します。
製品自体のAI securityは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)の担当です。旧AI-010・AI-011・DEPS-005・DETECT-002は`out-of-scope`、旧AI-005〜009は開発環境に必要な部分の`scope-review-required`へ変更しました。
移行済みAI-002と16件の記録は維持します。前回報告の旧52件・差分36件は全件移行の残作業数として使いません。一般的なApplication Securityと本番監視は引き続き対象です。
旧成果物・参照仕様の削除や別PJへの移植は行っていません。別PJの個別coverageは今回検証していません。

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
