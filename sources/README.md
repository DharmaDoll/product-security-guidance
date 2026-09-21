# 参照資料と仕様

このディレクトリは、コントロール、学習資料、設計パターン、実装例、横断分析の判断根拠を追跡するための
参照資料一覧です。旧リポジトリの
[`docs/SECURITY_GUIDANCE_SOURCES.md`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md)が担っていた役割を継承し、
資料を末尾の参考文献として並べるだけでなく、採用した判断、採用しなかった提案、限界まで記録します。

## REF-DEVELOPMENT-RUNTIME-RECONCILIATION-001

2026-09-21の受け渡しレビューでは、旧AI-002のAID-006〜007、AI-004のAAR-011・018・023と、SOURCE-004の認証情報ライフサイクルを突き合わせました。[失効時の責任分界](../engineering/ai-development-security/agent-extension-admission/README.md#失効を実行環境へ渡す)は本PJの統合的な設計判断です。外部規格がこの表や時間上限を規定するという主張ではありません。新規呼出しの拒否と既存処理の停止、認証情報の失効、外部結果の照合を分けています。製品の即時失効・停止機能、同期遅延、offline端末の対応は今回未検証です。

AI-004の記録への再編集時に、AISVS 1.0の固定commit `78775233666a2022dcfb82037e5e029116955c00`の[C9](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)と[C10](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)を2026-09-20に確認しました。対象はC9.2.1・C9.2.8・C9.3.1・C9.5.1・C10.1.2です。C9.2.8の暗号学的結合は方式依存のため保留、他の4件も開発環境の設計部分への対応です。旧`verifies`とconfidenceは履歴であり、実検証を意味しません。

### 役割と参照版

ENG-AI-001〜003の実行時照合・操作認可・通信・監査の追補に使用します。2026-09-20の[旧項目との対応表](../docs/AI_RUNTIME_MIGRATION.md)が移行範囲の正本です。

- 旧[AI-004 control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)、`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`のAAR-012〜021、025〜026。旧実装の契約とリポジトリ独自の判断として保持し、現行製品仕様とは扱いません。
- MCP公式[Tools specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)、2026-09-20確認。Tool一覧のpagination・変更通知、annotationsの信頼、入力検証・アクセス制御・監査に関する記述を参照。版付きURLですが取得物の固定digestは未記録のため`re-review-required`です。
- [拡張審査の固定資料](#ref-agent-extension-admission-001)、[操作認可](#ref-development-action-authorization-001)、[隔離](#ref-development-runtime-isolation-001)の参照版・採否を継承し、重複した仕様一覧を作りません。

### 採否・変更・限界

MCPの未信頼serverによるannotationsを許可判断へ昇格させず、tool追加時に再照合する判断を採用します。定期照合と未確認toolの拒否は本PJの運用設計です。Protocolへの対応だけで実装の安全性や完全な棚卸しを保証しません。
旧版の確認回数、1時間の鮮度、SQLite、公開HTTPS限定profile、固定した署名方式は普遍化せず、目的に応じた方式・閾値と実際の強制確認へ分けます。旧仕様や設定は削除しません。
通信許可と情報の送信許可、署名の正しさと収集データの真実性、事前判断と外部実行結果を区別します。Path制限にはその情報を確認できる強制点が必要であり、ホスト照合だけで実現したとは扱いません。
旧fixtureの成功、署名付きの合成snapshot、配送receiptを本番の採用証拠へ変換しません。製品adapter、暗号検証、実通信、中央ログ、通知先への配送は今回実行していません。

## REF-DEVELOPMENT-RUNTIME-ISOLATION-001

[ENG-AI-003](../engineering/ai-development-security/development-runtime-isolation/README.md)の設計入力です。2026-09-20に整理しました。

- 旧[AI-004の記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)、`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`のAAR-001〜007を継承。隔離、保護対象、認証情報、通信、公開承認、迂回禁止、管理方針の優先を設計へ再配置しました。AAR-005の公開承認の詳細はENG-AI-002へ渡します。
- [okdtとOWASPの固定版記録](#ref-agent-extension-admission-001)を保持。okdtのcommit `ffee64dfc818a5cd024628c1523d857685e0cc14`、OWASPのcommit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`、各CC BY-SA 4.0、旧レビュー2026-07-29を継承します。製品固有例を他のagentへそのまま適用しません。
- Anthropic公式[Sandboxing](https://code.claude.com/docs/en/sandboxing)、2026-09-20確認、可変資料のため`re-review-required`。OS境界と承認の違い、隔離を使えない場合と例外経路の確認が必要なことを設計入力にしました。設定例や既定値は移植せず、他製品への挙動推定もしません。

旧サンプルのダミー認証情報パスを守る条件は、実環境のファイル・環境変数・サービスへの到達経路を調べる設計へ広げました。これは本PJの解釈であり、旧fixtureがその全範囲を検証したという主張ではありません。
Hookや指示だけを隔離とする方式、隔離障害時の無制限な続行、許可ホストなら任意の情報を送信できるという判断は採用しません。
製品adapter、実際の拒否試験、端末全体の防御は未移行または未確認です。詳細な宛先制御AAR-020〜021とframework mappingは旧記録に保持します。

## REF-DEVELOPMENT-ACTION-AUTHORIZATION-001

### 役割・参照版

[Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)と[教材](../docs/learning/approval-is-bound-to-an-action.md)の設計入力です。開発環境に限定します。

- OWASP Cheat Sheet Series、AI Agent Security Cheat Sheet：固定版は[拡張審査の資料記録](#ref-agent-extension-admission-001)のcommit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`、CC BY-SA 4.0を継承。2026-09-20に[現行公開版のHuman-in-the-Loop Controls](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html#4-human-in-the-loop-controls)も確認。公開版は可変であり`re-review-required`、固定版との全文一致を確認した意味ではありません。
- 旧[AI-004 control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)、`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`：AAR-008〜011、AAR-022〜024の設計判断を再編集。これはリポジトリ独自の解釈と合成検証の契約であり、製品仕様ではありません。
- OS隔離を前提とする判断の旧出典は[同資料記録](#ref-agent-extension-admission-001)のokdt固定版`ffee64dfc818a5cd024628c1523d857685e0cc14`へ追跡できます。製品別設定は今回移植せず、現在の挙動も未確認です。

### 採否と限界

採用するのは、提案と実行を分け、承認を特定の対象・引数・期限へ結び付け、再利用と評価失敗を拒否する判断です。
旧資料の設計を開発用の公開・変更操作へ絞り、300秒の固定期限は組織が決める値へ変更しました。Shell経由の迂回、応答喪失時の再送、承認台帳の並行使用は旧AI-004から引き継ぐ設計課題です。
単純な承認済みフラグ、操作名だけのリスク分類、hookだけによる強制、秘密情報を含む監査は採用しません。サンプルコードも移植していません。
資料はガイダンスであり、認可サービス、実行先の重複防止、製品のhook、実環境の監査を検証した証拠ではありません。旧mappingの原記録を保持し、移行先には現在の設計との対応理由と保留範囲を別記しました。

## REF-AGENT-EXTENSION-ADMISSION-001

この資料の利用範囲は[AIを使う開発環境](../docs/SECURITY_SCOPE.md)です。AISVSやAgentic Top 10を参照しても、製品自体のAI securityを本PJの対象へ拡張しません。

### 役割・利用先・参照時点

PSB-AI-002のEXT-1〜7、ENG-AI-001、Reviewing an agent extensionの設計入力です。
2026-09-20に旧資料記録とcontrolの判断を再編集しました。以下の版と確認日は旧レビューの記録であり、製品の現行仕様を再確認した日ではありません。
旧verifierは審査結果の申告や合成benchmarkを照合しており、内容審査の品質・実環境の強制を自動で証明するものではありません。

| 資料・参照版 | 今回採用する判断 | 採用しない範囲・残る確認 |
|---|---|---|
| OWASP Cheat Sheet Series: [AI Agent Security Cheat Sheet](https://github.com/OWASP/CheatSheetSeries/blob/9feea5a6b5afdeb3277ad5f49262a62f86e018fb/cheatsheets/AI_Agent_Security_Cheat_Sheet.md)、commit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`（2026-06-27）、旧レビュー2026-07-29、CC BY-SA 4.0 | Tool権限の限定、明示的な認可、反復可能な悪用シナリオ評価、機微情報を除いた証拠を設計へ使う | ガイダンスであり検証標準ではない。Input sanitizationや追加model呼出しを認可境界としない。Memory・RAG・予算・multi-agentの推奨は今回の対象外 |
| Riotaro OKADA / okdt: [Claude Code Hardening Cheat Sheet](https://github.com/okdt/claude-code-hardening-cheatsheet/blob/ffee64dfc818a5cd024628c1523d857685e0cc14/Claude_Code_Hardening_Cheat_Sheet.en.md)、commit `ffee64dfc818a5cd024628c1523d857685e0cc14`（2026-04-02）、旧レビュー2026-07-29、CC BY-SA 4.0 | 外部指示の審査から、OS隔離・ファイル・通信制限を実行環境へ引き渡す境界に使う | コミュニティ資料。Command patternやhookだけによる隔離は採用しない。製品固有設定の移植や他clientの挙動推定はしない |
| [GitHub MCP公式資料の固定記録](#ref-ai-004)、commit `3778a41476e31a072430cfee7c5d31c5f72def60`、旧レビュー2026-08-05、MIT | 正規の取得元、tool schema、更新方式を審査し、認証情報と実行権限の担当を分ける | Floating imageや広いscopeを採用しない。固定したsourceがremote serverの稼働内容と同じだとは推定しない。認証方式の現行対応は導入時に再確認 |

変更して採用する点: 旧5件のfixtureの成功を成功状態から外し、実際に読み込む内容へ承認を対応付けられることを保証目標にする。
旧profileのMCP・Skillのinventory照合、plugin・外部promptの`deny-not-installed`は歴史的な実装範囲として残す。
旧PSB-AI-001のbenchmarkは未移行です。AI-004はcontrol記録をガイダンス移行しましたが、実行時強制の実装・導入は未確認です。

分析には[REF-PORTFOLIO-001](#ref-portfolio-001)の外部依存・platform・governanceと、[攻撃段階](#local-supply-chain-attack-stages)の段階3を用いる。これらをEXT特性の検証要件へ変換しない。

## SPEC-MITRE-ATLAS-2026.05

- 区分: `threat-taxonomy`。発行者MITRE。Content release `2026.05`、data format `6.0.0`、旧registryレビュー2026-07-27。
- 固定source: [ATLAS data](https://github.com/mitre-atlas/atlas-data/tree/da9ebf9b66e6902ad97c267e2a20af0bd996a60f)、tag `v2026.05`、commit `da9ebf9b66e6902ad97c267e2a20af0bd996a60f`。
- 対象`dist/v6/ATLAS-2026.05.yaml`のSHA-256: `defd9014c6d5f5954460ef438faea583fcb1830ff81e85709628efb43037cc3a`。旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/mitre-atlas/registry.json)から継承。
- 今回の利用: `AML.T0010.005`と`AML.T0110`について、拡張の供給経路と有害なtoolの導入という異なる攻撃行動を整理する。旧mappingレビュー2026-08-05。
- 限界: 攻撃行動の分類であり、準拠要件や実行時の防御成功を意味しない。移行による完全対応の主張はしない。

## SPEC-OWASP-AISVS-1.0

- 区分: `normative-specification`。発行者OWASP。Version `1.0`、CC BY-SA 4.0、旧registry・mappingレビュー2026-08-25。
- 固定source: [AISVS 1.0](https://github.com/OWASP/AISVS/tree/78775233666a2022dcfb82037e5e029116955c00/1.0)、commit `78775233666a2022dcfb82037e5e029116955c00`、English requirements tree `a8102d4e67cdf92348a32a18bbee2417d633a075`。
- 公式PDF `1.0/dist/AISVS-1.0.pdf`のSHA-256: `ff15584843a53d4fd2b52940c98cb15f9ebe1340151d90d54bb74db9cf8468f6`。旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-aisvs/registry.json)から継承。
- 今回の利用: `v1.0-C10.1.1`のMCP取得元・完全性と、`v1.0-C10.1.2`の許可するMCP・toolの関係を再レビューする入力。固定ID、版、旧`verifies`関係と対象checkを保持する。
- 限界: 新構造ではガイダンス移行であり、上記要件の検証完了を意味しない。AISVS level達成・準拠を主張せず、一般applicationのASVS評価も代替しない。

## 何に使うか

この一覧は「どの外部資料を、どのバージョンで、どう解釈し、何を採用・除外したか」に答えます。
各成果物は、参照資料IDを使って「その資料が、この判断のどこに影響したか」という問いに答えます。

参照資料記録はコントロール要件そのものではなく、組織への導入や準拠の証拠でもありません。
フレームワーク対応関係は[フレームワーク対応関係](../mappings/frameworks.yaml)で別に管理します。

## 参照資料の区分

| 値 | 用途 | 例 |
|---|---|---|
| `normative-specification` | 要件または仕様の正確な意味を確認する | NIST SSDF |
| `threat-taxonomy` | 攻撃者の挙動やリスク分類を整理する | MITRE ATT&CK |
| `vendor-guidance-registry` | 製品固有の安全な構成と、提供元の証拠を解釈する | GitHub Docs |
| `product-specification` | 設定項目、メタデータ、依存関係の解決時の挙動を確認する | npm CLI文書 |
| `implementation-guidance` | 設計・導入候補を発見し、採否を判断する | Dependency Cooldowns |
| `portfolio-analysis-input` | 分野の偏りや空白を横断的に確認する | AwesomeProductSecurity Overview |
| `repository-synthesis` | 複数コントロールを攻撃経路や受け渡しで読み直す | サプライチェーン攻撃コントロール一覧 |
| `user-supplied-input` | リポジトリ利用者が提供した原文を追跡する | 開発端末ハードニング資料 |
| `threat-research` | 攻撃経路と設計上の落とし穴を具体化する | GitHub Security Lab |
| `incident-research` | 脅威シナリオを具体化する | 公開インシデント報告 |

## 利用ルール

1. 公開リポジトリがある資料は、可能な限りコミット、タグ、ダイジェストで固定する。
2. 最新URLしかない資料は、確認日と`re-review-required`を持たせ、固定済みと表現しない。
3. 製品文書を、製品に依存しないコントロールの境界へそのまま昇格させない。
4. コミュニティの一覧は機能発見に使えても、公式な製品仕様の代わりにはしない。
5. 資料の推奨を採用しない場合も、セキュリティ上重要であれば除外理由を残す。
6. フレームワークIDとの関係はマッピングで表し、参照資料記録を準拠マッピングにしない。
7. コントロールや実装例を変更する際、参照する仕様を削除せず、置換先または非採用理由を残す。
8. 資料へのリンクだけで採用済みとせず、どの判断に使い、どこを変更し、何を採用しなかったかを記録する。
9. ポートフォリオ資料と攻撃段階の一覧は、空白を発見する分析軸として使う。表を埋めるために要件や成果物を自動生成しない。

## パイロットで使用する参照資料

### 規範仕様と脅威分類

<a id="spec-github-security-guidance"></a>

#### SPEC-GITHUB-SECURITY-GUIDANCE — GitHubのセキュリティガイダンス一覧

- 区分: `vendor-guidance-registry`
- 発行者: GitHub
- 基準とするコミット: `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`
- 参照コミット日: `2026-07-24`
- 一覧のレビュー日: `2026-07-27`
- 変更不能な参照元:
  [github/docs commit](https://github.com/github/docs/commit/b17436de8f10c3e7f6a185d6813bf94bc82d22f8)
- パイロットで使用する参照ページID:
  - `GHSC-SECURE-ACCOUNTS` — アカウントの保護
  - `GH-ADMIN-CREDENTIAL-TYPES` — GitHubの認証情報種別
  - `GH-ADMIN-SAML-IAM` — SAMLによるIDとアクセス管理
  - `GH-ADMIN-SCIM-ORGANIZATIONS` — 組織のSCIMライフサイクル
  - `GHAS-REF-SECURE-USE` — GitHub Actionsの安全な利用
  - `GHAS-REF-PULL-REQUEST-TARGET` — 権限付きPRイベントの信頼境界
  - `GHAS-CONCEPT-COMPROMISED-RUNNERS` — runner侵害時の影響範囲
  - `GH-ADMIN-ACTIONS-REPOSITORY` — repository単位のActions設定
- 利用箇所: `PSB-SOURCE-004`／`SRC-AUTH-1..6`、`PSB-CICD-005`／`PR-BOUNDARY-1..6`
- 限界: GitHub固有の実装根拠であり、GitHub環境の安全性や正式な準拠を証明しない。

製品文書へのリンク:

- [Best practices for securing accounts](https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-accounts)
- [GitHub credential types](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types)
- [SAML identity and access management](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)
- [SCIM for organizations](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [Compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners)
- [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)

<a id="spec-nist-ssdf-1-1"></a>

#### SPEC-NIST-SSDF-1.1 — NIST SP 800-218

- 区分: `normative-specification`
- 基準とする刊行物: NIST SP 800-218、SSDFバージョン`1.1`、2022年
- 公式資料: [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- パイロットで使用する要件ID: `PS.3.1`、`PW.4.1`
- 利用箇所: `PSB-SOURCE-004`, `PSB-DEPS-001`
- 限界: マッピングは特定のプラクティスを支援する関係であり、SSDF準拠を意味しない。

<a id="spec-mitre-attack-v19-1"></a>

#### SPEC-MITRE-ATTACK-v19.1 — MITRE ATT&CK Enterprise

- 区分: `threat-taxonomy`
- 基準とするコンテンツのバージョン: `v19.1`
- 公式資料: [MITRE ATT&CK version history](https://attack.mitre.org/resources/versions/)
- パイロットで使用する技術ID: `T1078`、`T1552.001`、`T1195.001`
- 利用箇所: `PSB-SOURCE-004`, `PSB-DEPS-001`
- 限界: 攻撃者の挙動との関係を示すもので、検証要件や準拠要件ではない。

<a id="spec-openssf-osps-2026-02-19"></a>

#### SPEC-OPENSSF-OSPS-2026.02.19 — OpenSSF OSPS Baseline

- 区分: `normative-specification`
- バージョン／タグ: `2026.02.19`／`v2026.02.19`
- 参照コミット: `e67ae247ebfb2fd758c9d186335e60cad0a74e78`
- レビュー対象文書のSHA-256:
  `54d13befdb1ae4c63b8612acabc1f0d716874be4187d25801d6ba2d6eee98271`
- パイロットで使用する要件ID: `OSPS-AC-01.01`、`OSPS-BR-01.03`
- 参照先: [OpenSSF OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19)
- 利用箇所: `PSB-SOURCE-004`／`SRC-AUTH-2`、`PSB-CICD-005`／`PR-BOUNDARY-1..5`
- 限界: プロジェクトの成熟度またはOSPS適合性の判定ではない。

<a id="spec-owasp-agentic-2026"></a>

#### SPEC-OWASP-AGENTIC-2026 — OWASP Top 10 for Agentic Applications

- 区分: `threat-taxonomy`
- 基準とする刊行物: `OWASP Top 10 for Agentic Applications 2026`
- 公開日: `2025-12-09`
- パイロットで使用する分類: `ASI03`、`ASI04`（PSB-AI-002の追加移行）
- 公式資料:
  [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- 利用箇所: `PSB-SOURCE-004`のGitHub MCP適用時
- 追加利用箇所: `PSB-AI-002`のEXT-1〜6。旧レビュー2026-08-05のASI04関係を移行レビュー中で継承。旧registryでは公式PDFの自動取得が拒否されており、artifact hashは未記録。刊行年・公開日・URLの固定をPDFの完全性検証と読み替えない。
- 限界: エージェント型AIのリスク分類全体への対応や、AIエージェントの安全性を意味しない。

### ポートフォリオ分析の入力

<a id="ref-portfolio-001"></a>

#### REF-PORTFOLIO-001 — AwesomeProductSecurityのプロダクトセキュリティ概観

- 区分: `portfolio-analysis-input`
- 状態: `adopted-partially`
- 発行者: DharmaDoll
- 対象: AIおよびエージェント型システムを含む、ソフトウェアライフサイクル全体のプロダクトセキュリティ
- 基準とするコミット: `DharmaDoll/AwesomeProductSecurity@50f2e81f0062de112f7522280e76b92d8849fa1e`
- コミット日: `2026-07-10`
- ソースのSHA-256: `5b524004739bc00eae0faabb0f8c12fc3d37a976249e0650131fce8143903ffc`
- レビュー日: `2026-08-05`
- 変更不能な参照元:
  [Overview.md](https://github.com/DharmaDoll/AwesomeProductSecurity/blob/50f2e81f0062de112f7522280e76b92d8849fa1e/Overview.md)
- 最新の参照先:
  [AwesomeProductSecurity Overview](https://github.com/DharmaDoll/AwesomeProductSecurity/blob/main/Overview.md)
- ライセンス: レビューしたリポジトリでは未宣言。本文を複製せず、参照と独自の分析結果だけを保持する。
- 利用箇所: [横断分析の軸](../docs/ANALYSIS_LENSES.md)、`PSB-SOURCE-004`、`PSB-DEPS-001`、`PSB-CICD-005`

採用した内容:

- アプリケーション、プラットフォームとインフラストラクチャ、運用、PSIRTと脆弱性管理、外部依存と
  サプライチェーン、ガバナンス、教育と文化という七つの観点で、試作版の偏りと空白を確認する。
- モデル出力を信頼済み入力にせず、認可と強制をモデルの外側に置く。この判断は、MCPやAIツールへ
  認証情報を渡した後のツール認可を`PSB-SOURCE-004`の外側に残す根拠の一つとする。
- 本番監視、復旧、ガバナンス、教育の対象内の空白を、技術コントロールの存在で埋めたことにしない。
- 資料が扱うAI application gateway、モデル／データ、RAG、AI製品のTEVVは[Security scope](../docs/SECURITY_SCOPE.md)に従いai-security-foundryの担当とし、本PJの移行待ちへ追加しない。

採用しなかった内容:

- 資料に登場する製品名を、この試作版の必須依存関係にはしない。
- 例示されたKPIや期間を、既定の合格基準にはしない。
- 資料に挙げられたフレームワークを、個別に版と出典を確認せずマッピングしない。

限界:

- 項目単位の参考文献を持つ規範資料ではないため、フレームワーク識別子や準拠主張の根拠には使わない。
- 七つのレイヤーとの対応は、ポートフォリオ上の位置を示すだけで、実装済み、導入済み、十分な対応範囲を意味しない。
- コンテンツフィルターやガードレールモデルは多層防御であり、独立した認可境界の代わりにはしない。

### 旧一覧から引き継いだレビュー済みガイダンス

<a id="ref-cicd-005"></a>

#### REF-CICD-005 — GitHub Actions Best Practice 2025

- 区分: `implementation-guidance`
- 状態: `adopted-partially`
- 発行者・著者: Shunsuke Suzuki
- 発表日: `2025-03-11`、旧レビュー日: `2026-07-30`
- 変更不能な参照元: [発表資料](https://github.com/suzuki-shunsuke/slides/blob/9a323208ecda2b3e27ffe279098537182566cee0/marp/github-actions-best-practice-2025.md)
- 最新の参照先: [GitHub Actions Best Practice 2025](https://suzuki-shunsuke.github.io/slides/github-actions-best-practice-2025)
- 基準版のライセンス: [MIT](https://github.com/suzuki-shunsuke/slides/blob/9a323208ecda2b3e27ffe279098537182566cee0/LICENSE)
- 利用箇所: `PR-BOUNDARY-2`、GitHub Actions実装例。
- 採用した内容: default denyとjob単位のpermission、checkout後にcredentialを残さない設定、full commit SHA、fork PRを未信頼として扱う設計。
- 変更して採用した内容: 個別のGitHub設定をコントロール要件にせず、製品非依存の権限境界とGitHub固有の実装へ分離した。
- 採用しなかった内容: 資料に登場するtool、App、組織全体のremediation手順を、この例の必須依存関係にはしない。
- 限界: 製品挙動は公式仕様とlive runで確認する。性能や開発者体験の推奨は、境界の迂回や確認漏れに関係する場合だけ扱う。

<a id="ref-cicd-010"></a>

#### REF-CICD-010 — Preventing pwn requests

- 区分: `threat-research`
- 旧一覧の状態: `adopted`、新構造での状態: `adopted-partially`
- 発行者: GitHub Security Lab、著者: Jaroslav Lobačevski
- 公開日: `2021-08-03`、旧レビュー日: `2026-07-30`
- 参照先: [Keeping your GitHub Actions and workflows secure Part 1](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)
- 変更不能な公開版: 未特定、`re-review-required`
- 再利用可能な記事ライセンス: 未特定。本文を複製せず、リンクと独自の要約だけを保持する。
- 利用箇所: `PR-BOUNDARY-1`、`PR-BOUNDARY-2`、`PR-BOUNDARY-4`、`PR-BOUNDARY-5`、学習ノート、設計パターン。
- 採用した内容: fork PRと派生成果物を未信頼として扱う。権限イベントでPR headを実行しない。actor、label、古い承認を恒久的な信頼判断にしない。
- 変更して採用した内容: 最初の実装は、metadata-only例外や`workflow_run`を実装せず、無権限のPR検証とmerge後のfresh runへ分ける。
- 採用しなかった内容: 記事のartifact受け渡し例を、そのまま実装しない。受動的なデータにもconsumer側の独立した設計と検証が必要なため。
- 限界: 記事は脅威と設計根拠であり、現在のGitHubの既定値や導入済み状態を証明しない。例の存在をlive evidenceにしない。

<a id="ref-ai-004"></a>

#### REF-AI-004 — GitHub MCPの公式な認証・ガバナンスガイダンス

- 区分: `implementation-guidance`
- 状態: `adopted-partially`
- 発行者: GitHub
- 基準とするリポジトリのコミット: `github/github-mcp-server@3778a41476e31a072430cfee7c5d31c5f72def60`
- コミット日／レビュー日: `2026-08-05`
- 基準版のライセンス: MITライセンス
- 変更不能な参照元:
  - [README](https://github.com/github/github-mcp-server/blob/3778a41476e31a072430cfee7c5d31c5f72def60/README.md)
  - [Policies and governance](https://github.com/github/github-mcp-server/blob/3778a41476e31a072430cfee7c5d31c5f72def60/docs/policies-and-governance.md)
- 最新の製品文書:
  [Setting up the GitHub MCP Server](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server)
- 利用箇所: `SRC-AUTH-1`、`SRC-AUTH-3..6`、GitHub実装例
- 採用した内容: OAuthの優先、範囲を限定したPATによる代替、子プロセスだけへの受け渡し、読み取り専用のツール公開。
- 証明できないこと: IDEでの秘密情報の保存方法、実際の組織ポリシー、実行ファイルの完全性、実行時の認可。

<a id="ref-user-001"></a>

#### REF-USER-001 — 開発端末ハードニングガイドライン

- 区分: `user-supplied-input`
- 旧リポジトリでの状態: `adopted`、パイロットでの利用: `adopted-partially`
- 提供日: `2026-07-28`
- 旧リポジトリの[提供原文](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/user-supplied-endpoint-hardening-guideline-ja.md)
- 外部参考文献／ライセンス: 未提供
- 利用箇所: `SRC-AUTH-2`、`SRC-AUTH-4`、`ENG-SOURCE-002`（2026-09-21追加。詳細は次の参照資料記録）
- 採用した内容: フィッシング耐性のある認証、保護された鍵／秘密情報の保管、短命な認証情報という考え方。
- 限界: 開発端末ハードニング全体は`PSB-SOURCE-004`へ統合しない。原文を再配布できるかも未確定。

<a id="ref-developer-endpoint-baseline-001"></a>

#### REF-DEVELOPER-ENDPOINT-BASELINE-001 — Developer endpoint design inputs

- 区分: `repository-synthesis`。利用者提供資料と旧controlの実装ガイドを、端末管理の設計へ再編集した記録。
- 状態: `adopted-partially`。棚卸し日: `2026-09-21`。外部製品の現行仕様を検証した日ではない。
- 参照したリポジトリの版: `3bfbeb21246bb2f58c55fa5212068805bca1719b`。
- 入力を区別して保持:
  - [REF-USER-001](#ref-user-001)の2026-07-28提供原文。製品名は例示で、独立した規範資料ではない。
  - [10項目のCSV](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/developer-endpoint-operational-baseline.csv)と[対応説明](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/operational-baseline.md)。引用元は`source 1`のみで、題名・著者・版・URLは未提供。Phase 2という原入力のラベルを移行順序の根拠にしない。
  - [29項目の実装ガイド](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/check-implementation-guide.md)と[旧metadata](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/control.yaml)。DEH-011はリポジトリ独自の追加で、10項目の原入力へ混ぜない。
- 利用先: [ENG-SOURCE-002](../engineering/source-protection/managed-developer-endpoint/README.md)、[教材](../docs/learning/managed-is-not-currently-trusted.md)、[29項目の対応表](../docs/ENDPOINT_MIGRATION.md)。REF-USER-001を廃止・改名するものではない。
- 採用: 暗号化、画面ロック、更新、権限、アプリ、バックアップ、EDRの稼働確認、集中管理、物理保護を個人の注意に依存させない設計。
- 変更して採用: 「最新版」をサポート対象・適用期限・例外管理へ具体化。登録済み、現在の観測、アクセス許可を分離し、通知・失効・復旧の責任を接続。通信設定の配布だけを迂回防止と見なさない。これらはリポジトリの設計判断で、外部仕様の要求とは主張しない。
- 不採用: ローカルhookやrequired checkによるあらゆる流出の防止、署名によるコード安全性や端末健全性の保証、遠隔環境への移動による接続元端末保護の省略。特定MDM・EDR・クラウド製品の必須化と、宣言fixtureの成功による導入済み判定も採らない。
- 保留: SOURCE-001のcontrol記録と旧4件のframework関係、Linux収集器、製品別設定、実際の通知・隔離・失効・復旧。旧参照仕様は削除せず、対応表から追跡する。
- 限界: 提供資料の外部参考文献と再配布条件は未解決。今回は原文を複製せず参照する。独立リポジトリ化の前に利用条件と、旧ツリーを参照するリンクの移管方法を確認する。

<a id="ref-deps-001"></a>

#### REF-DEPS-001 — Takumi Guard — 依存パッケージレジストリプロキシ

- 区分: `implementation-guidance`
- 状態: 隣接パターンとして`adopted-partially`
- 発行者: Flatt Security／Shisho Cloud
- レビュー日: `2026-07-31`
- 変更不能な文書の版: 未特定、`re-review-required`
- 最新の参照先:
  - [Takumi Guard](https://shisho.dev/docs/t/guard/)
  - [Quickstart](https://shisho.dev/docs/t/guard/quickstart/)
  - [npm proxy configuration](https://shisho.dev/docs/t/guard/quickstart/npm/)
  - [Limitations](https://shisho.dev/docs/t/guard/limitation/)
- 利用箇所: `PSB-DEPS-001`に隣接する管理プロキシの選択肢。
- 限界: 提供元の遮断一覧は168時間の待機を強制するものではなく、待機期間の代わりにしない。

<a id="ref-deps-004"></a>

#### REF-DEPS-004 — Dependency Cooldownsの運用互換性一覧

- 区分: `implementation-guidance`
- 状態: `adopted-partially`
- 発行者: mprpic／Dependency Cooldownsのコントリビューター
- ライセンス: MIT
- レビュー日: `2026-08-10`
- レビュー対象を変更不能な版で固定していないため、状態は`re-review-required`
- 機能発見に使った資料:
  - [Dependency Cooldowns](https://cooldowns.dev/)
  - [mprpic/cooldowns](https://github.com/mprpic/cooldowns)
- 候補の確認に使用した公式製品仕様:
  - [npm configuration](https://docs.npmjs.com/cli/v11/using-npm/config/)
  - [npm install](https://docs.npmjs.com/cli/install/)
  - [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
  - [uv dependency resolution](https://docs.astral.sh/uv/concepts/resolution/)
  - [uv settings](https://docs.astral.sh/uv/reference/settings/)
  - [pnpm dependency resolution settings](https://pnpm.io/settings/dependency-resolution)
  - [Yarn configuration](https://yarnpkg.com/configuration/yarnrc/)
  - [Yarn security features](https://yarnpkg.com/features/security)
  - [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)
- 利用箇所: `DEP-AGE-1..6`、npm実装例。
- 採用した内容: パッケージマネージャー標準の制限、CIの検査、プロキシを区別し、設定の優先順位、
  メタデータ欠落、回避経路を確認する。
- 採用しなかった内容: 補助スクリプトの実行、全体設定の暗黙変更、外部例の時間をポリシー基準にすること。

### リポジトリ内で継承する分析資料

<a id="local-supply-chain-attack-stages"></a>

#### LOCAL-SUPPLY-CHAIN-ATTACK-STAGES — サプライチェーン攻撃段階と代表経路

- 区分: `repository-synthesis`
- 状態: `adopted-partially`
- 作成者: このリポジトリ
- 基準とする版: `product-security-controls@511fcb4d0e17a1e177c2bca802d9473233688e16`
- 原文: [`docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md)
- 利用箇所: [横断分析の軸](../docs/ANALYSIS_LENSES.md)、`PSB-SOURCE-004`、`PSB-DEPS-001`、`PSB-CICD-005`

採用した内容:

- 開発端末から検知・復旧までの十二段階を、コントロールの配置と前後の受け渡しを確認する軸にする。
- 「開発ツールからソース改ざん」「悪意ある依存パッケージから本番環境」という代表経路を、
  単一コントロールで終わらない残余リスクの確認に使う。
- リポジトリ内のテスト用データに合格したことと、実環境へ導入済みであることを分ける。

採用しなかった内容:

- 原文にある全コントロールを、この三件のpilotへ移したことにはしない。
- 攻撃段階との関係を、各コントロールの合格条件やフレームワーク対応関係に置き換えない。

限界:

- このリポジトリが編集した横断索引であり、外部の規範資料や脅威分類ではない。
- 段階は調査順序を助けるもので、攻撃が常に同じ順番で進むことや、脅威を網羅することを意味しない。
- 原文の多くのリンク先は試作対象外であり、`experiments/next-repository/`へ移行済みとは扱わない。

### パイロットで使用する製品仕様

<a id="spec-npm-cli-11"></a>

#### SPEC-NPM-CLI-11 — npmの最低待機時間の挙動

- 区分: `product-specification`
- 旧コントロールから引き継いだ実装の最低バージョン: npm `11.10.0`
- 対象設定: `min-release-age`、単位は日
- 公式文書:
  - [npm configuration v11](https://docs.npmjs.com/cli/v11/using-npm/config/)
  - [npm install](https://docs.npmjs.com/cli/install/)
  - [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
- 旧レビューで使用したリリース履歴:
  [npm CLI changelog for 11.10.0](https://github.com/npm/cli/blob/latest/CHANGELOG.md#11100-2026-02-11)
- レビュー状態: npm CLIのソースを特定のタグまたはコミットで固定していないため、`re-review-required`。
- 利用箇所: npm実装例、`DEP-AGE-3..5`。
- 限界: 未知の設定キーが保存されることや、`npm config get`に値が表示されることだけでは、
  依存関係の解決時に設定が強制されることを証明しない。

<a id="spec-npm-registry-metadata"></a>

#### SPEC-NPM-REGISTRY-METADATA — npmレジストリのパッケージメタデータ

- 区分: `product-specification`
- 公式資料:
  [npm registry package metadata response](https://github.com/npm/registry/blob/main/docs/responses/package-metadata.md)
- レビュー状態: URLは変更され得る`main`を指すため、本番向け連携を採用する前に、変更不能な改訂で固定する。
- 利用箇所: `DEP-AGE-1`、`DEP-AGE-2`。
- 限界: レジストリメタデータのスキーマを参照しても、レジストリ自体が侵害されていないことや、
  公開時刻の真正性は証明しない。

<a id="incident-context-retained-for-learning"></a>

### 学習用に残すインシデント事例

- `RESEARCH-DEPS-CHECKMARX`:
  [Bitwarden statement on the Checkmarx supply-chain incident](https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127)
- `RESEARCH-DEPS-AXIOS`:
  [Axios npm supply-chain compromise postmortem](https://github.com/axios/axios/issues/10636)

これらは脅威シナリオを具体化する資料です。待機期間のしきい値、製品仕様、コントロールの合格条件は定義しません。

## パイロットの追跡関係

<a id="spec-install-execution-policy"></a>

### SPEC-INSTALL-EXECUTION-POLICY — Install-time executionの製品仕様と設計ガイダンス

- 区分: `product-specification`。下記の横断ガイダンスは実装候補・設計入力として区別する。
- 移行元: `controls/dependency-security/install-script-execution/README.md`と`control.yaml`。
- 利用先: `PSB-DEPS-002 / DEP-EXEC-1..4`、`ENG-DEPS-002`、pip実装例。
- 固定改訂: 未特定。変更可能なURLのため`re-review-required`。
- 採用判断: パッケージの取得と準備用コードの実行許可を分け、未承認実行を拒否する。
- 変更して採用: 製品ごとのdefault・設定キーをcontrolの定義にせず、製品別実装へ置く。
- 不採用: 全許可、名前だけのtrustを将来versionの承認にすること、拒否後の無条件source fallback。
- 限界: 製品文書は組織の実効設定、CI配線、実行環境の隔離を証明しない。各リンクの本文は複製しない。

#### pip — 今回確認した仕様

発行者はpip project。公式文書の表示版は`26.2.1`、確認日は`2026-09-16`。
source候補を除外するoptionとhash確認を別の特性として採用する。
build用依存の分離をOS権限のsandboxと解釈しない。直接指定のsource入力やlocal projectを
wheel限定のindex取得経路へ混ぜず、製品設定と入力の両方を確認する。

- [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)
- [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/)

ローカルテストの使用版は出力に記録する。上記文書の表示版とテスト環境の版は同一とは限らず、
新しい版を導入する際は再確認が必要。wheelの安全性や後続実行の隔離は保証しない。

#### npm、pnpm、Bun — 保持した仕様と次のレビュー対象

以下は旧成果物の参照仕様を保持したもの。今回は現在の製品挙動・版を再確認しておらず、
旧READMEのdefaultや最低versionを新構造へ確定仕様として移さない。
許可機能、許可単位、優先順位、更新時の違いを再確認してから実装例へ移す。

- npm / 発行者npm・GitHub: [npm 12 default変更の告知](https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/)、[install-script approvals](https://docs.npmjs.com/cli/v11/commands/npm-install-scripts/)、[lifecycle scripts](https://docs.npmjs.com/cli/using-npm/scripts/)
- pnpm / 発行者pnpm: [Build Settings](https://pnpm.io/settings/build)、[approve-builds](https://pnpm.io/cli/approve-builds)、[supply-chain security](https://pnpm.io/supply-chain-security)
- Bun / 発行者Bun: [install](https://bun.com/docs/pm/cli/install)、[trusted dependencies](https://bun.com/guides/install/trusted)、[bunfig.toml](https://bun.com/docs/runtime/bunfig)

#### 横断ガイダンスとmapping候補 — 省略せず保持

以下は旧成果物から引き継ぐ設計・調査入力。今回は全文再レビューしておらず、追加要件や必須製品へ変換しない。

- OWASP: [NPM Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)、[Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
- CISAほか: [Recommended Practices for Developers](https://www.cisa.gov/sites/default/files/2023-12/ESF_SECURING_THE_SOFTWARE_SUPPLY_CHAIN_DEVELOPERS.pdf)、旧リンクの版は`2023-12`パス。刊行版・digestを追加確認する。
- OpenSSF OSPS: `2026.02.19 / OSPS-BR-05.01`は旧READMEにあった関連候補。標準package manager利用だけで実行抑止を証明しないため、direct mappingは追加しない。[参照要件](https://baseline.openssf.org/versions/2026-02-19#osps-br-0501)

旧`control.yaml`のATT&CK `v19.1 / T1195.001`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`は
版・ID・関係・confidenceを保持し、特性への再配置は`migration-review-required`とする。
旧レビュー担当は`product-security`、日付は`2026-07-27`。これは今回のレビュー日ではない。

| 成果物 | 直接参照する資料ID | マッピングが参照する資料ID |
|---|---|---|
| `PSB-SOURCE-004` | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-AI-004`, `REF-USER-001` | `SPEC-NIST-SSDF-1.1`, `SPEC-MITRE-ATTACK-v19.1`, `SPEC-OPENSSF-OSPS-2026.02.19`, `SPEC-OWASP-AGENTIC-2026` |
| GitHubのソースアクセス認証情報実装例 | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-AI-004` | 同上。ただしMCP利用時に限るマッピングを含む |
| `PSB-DEPS-001` | `REF-DEPS-004`, `SPEC-NPM-REGISTRY-METADATA` | `SPEC-NIST-SSDF-1.1`, `SPEC-MITRE-ATTACK-v19.1` |
| npmの待機期間実装例 | `SPEC-NPM-CLI-11`, `REF-DEPS-004` | コントロールのマッピングを自動継承しない |
| 管理プロキシの選択肢 | `REF-DEPS-001` | 待機期間のマッピングを自動継承しない |
| `PSB-CICD-005` | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-CICD-005`, `REF-CICD-010` | `SPEC-OPENSSF-OSPS-2026.02.19` |
| GitHub ActionsのPR境界実装例 | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-CICD-005`, `REF-CICD-010` | コントロールのマッピングを自動継承しない |
| 横断分析 | `REF-PORTFOLIO-001`, `LOCAL-SUPPLY-CHAIN-ATTACK-STAGES` | コントロールやフレームワークの対応関係へ自動変換しない |
| `PSB-DEPS-002`、Install execution policy pattern、pip実装例 | `SPEC-INSTALL-EXECUTION-POLICY` | `SPEC-MITRE-ATTACK-v19.1`, `SPEC-NIST-SSDF-1.1`。実装へ自動継承しない |

<a id="spec-workload-federation"></a>

## SPEC-WORKLOAD-FEDERATION — GitHub・AWS・OIDCのfederation仕様

- 区分: `product-specification`。OIDC Coreはprotocol仕様、Terraformは実装候補として区別する。
- 発行者: GitHub、AWS、OpenID Foundation、HashiCorp。
- 利用先: `PSB-CICD-006 / FED-1..6`、`ENG-CICD-002`、学習ノート、GitHub Actions / AWS実装例。
- 移行元: `controls/cicd-security/audience-bound-oidc-federation/README.md`と`control.yaml`。
- 今回確認日: `2026-09-16`。GitHub OIDC reference、AWS OIDC role、STS APIを確認。他資料の全文再レビューは未完了。
- 文書の固定改訂: 未特定の製品URLは`re-review-required`。ActionとOIDC Coreは下記の参照版を保持。
- 採用: Token検証、audience・subject、保護job、操作権限と有効期間を別の判断として扱う。
- 変更して採用: 旧AWS例の900秒・account・roleをcontrol全体の固定値にせず、製品別profileへ置く。
- 明確化: 旧長期keyの保管場所の削除と、provider側の失効・旧権限が使えないことの確認を区別する。派生sessionはインシデント対応と接続する。
- 不採用: Token識別子やsynthetic ledgerからAWSのsingle-use replay防止を主張すること、Environment subjectだけでbranch・workflowを固定したと扱うこと。
- 限界: 現在のtrust・Environment・role権限・inventory・交換結果は、live確認なしに導入済みとは言えない。

旧参照仕様を以下へ保持する。今回確認した資料と引き継いだ未再確認資料を混同しない。

- GitHub: [OIDC concept](https://docs.github.com/en/actions/concepts/security/openid-connect)、[OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)、[OIDC REST API](https://docs.github.com/en/rest/actions/oidc)、[deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- AWS: [OIDC role作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)、[AssumeRoleWithWebIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)、[IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)、[CloudTrail userIdentity](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html)、[STS condition keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#condition-keys-sts)
- AWS Action: [固定commit e6de054238d6b7531b4efff3b6587d9aade6a06c](https://github.com/aws-actions/configure-aws-credentials/commit/e6de054238d6b7531b4efff3b6587d9aade6a06c)、[project](https://github.com/aws-actions/configure-aws-credentials)。旧例のv6.2.3を保持し、今回runtimeやAction全体を再レビューしたとは扱わない
- Protocol: [OpenID Connect Core 1.0 / errata set 1参照版](https://openid.net/specs/openid-connect-core-1_0-18.html)。Provider固有のclaim対応・session・replayの保証に読み替えない
- Terraform AWS provider: [OIDC provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_openid_connect_provider)、[IAM role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role)、[role policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy)。旧導入候補を保持するのみで、provider pin・lock・実環境planは別途必要

Frameworkは旧GitHub registryの固定commit、OSPS `2026.02.19 / OSPS-AC-04.02`、ATT&CK `v19.1 / T1552.001`を保持。
GitHub page IDは`GHAS-CONCEPT-OIDC`と`GHAS-REF-OIDC`。旧レビューは`product-security / 2026-09-06`、
新特性への割当は移行レビュー中。今回の製品文書確認によってregistryの固定版を更新したとは扱わない。

<a id="ref-cicd-009"></a>

## REF-CICD-009 — OIDC・Trusted Publishingの残存リスク分析

- 区分: `threat-research`、状態: `adopted-partially`、発行者: GMO Flatt Security。
- 公開日: `2026-07-02`、旧レビュー日: `2026-07-30`。今回は旧参照記録を移行し、記事全文の再レビューは未完了。
- [原文](https://blog.flatt.tech/entry/2026-github-actions-security-part3)。固定公開版・再利用ライセンスは未特定。本文を複製せず、リンクと独自の解釈を保持する。
- 利用先: `FED-2..4`、学習ノート、pattern。製品claim仕様はSPEC-WORKLOAD-FEDERATIONで別に確認する。
- 採用: 短命化を窃取防止と解釈せず、buildと認証・公開jobを分け、交換後の権限と監査も限定する。
- 変更して採用: Cloud federationとpackage-registry Trusted Publishingを独立した受け入れ境界として扱う。
- 不採用: 旧記録にあるoffline replay契約をAWSのsingle-use保証として残すこと。
- 限界: 旧一覧はoffline contractと記述するが、現行旧controlはlive確認を必要とするmanual reference。記事とfixtureの存在は実環境導入を証明しない。

横断分析にはREF-PORTFOLIO-001とLOCAL-SUPPLY-CHAIN-ATTACK-STAGESを使い、直接の製品仕様・特性根拠と区別する。

<a id="spec-ci-cache-boundary"></a>

## SPEC-CI-CACHE-BOUNDARY — CI cacheの読み書きと内容の信頼

- 役割・発行者: GitHubの製品仕様を直接の根拠とし、周辺資料は設計レビューに使う。
- 版: GitHubのmutableな公式仕様を2026-09-16に確認。旧workflowのruntimeとAction固定値は再検証前の履歴として保持する。
- 利用先: `PSB-CICD-009 / CACHE-1..7`、`ENG-CICD-003`、共有教材。
- 採用: writerとconsumerの信頼、cache scope、内容の制限、復元後の照合を分ける。現在の`cache-mode`によるread/write制限と再利用workflowの実効設定も確認する。
- 限界: key一致、hit、署名のないarchiveの展開を真正性の証拠にしない。公式仕様の確認は組織の設定・実行結果の確認ではない。

保持した参照仕様・ガイダンス:

- [GitHub cache concepts](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching)、[cache reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)、[REST cache API](https://docs.github.com/en/rest/actions/cache)、[actions/cache](https://github.com/actions/cache)。
- [zizmor cache-poisoning audit](https://docs.zizmor.sh/audits/#cache-poisoning): 静的な候補検出。実効scopeや内容の安全性を証明しない。
- [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/): download cacheを復元した後も、承認済みhashと通常installの照合を行うための仕様。
- [OWASP CI/CD-SEC-9](https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-09-Improper-Artifact-Integrity-Validation)、[SLSA v1.2 Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)、`SPEC-NIST-SSDF-1.1`: 隣接する設計入力。cache制限だけでartifact integrityやbuild levelを満たすとは扱わない。
- 旧実装のPython [3.13.15](https://www.python.org/downloads/release/python-31315/)、actions/cache `27d5ce7f107fe9357f9df03efb73ab90386fccae`、checkout `de0fac2e4500dabe0009e67214ff5f5447ce83dd`、setup-python `a309ff8b426b58ec0e2a45f0f869d46889d02405`を保持。今回はworkflowを移植せず、runtimeと実効挙動を再レビューする。
- 旧frameworkレビュー: product-security、2026-09-07。関係は保持し、新しい特性への割当はレビュー中。

<a id="ref-cicd-014"></a>

## REF-CICD-014 — Runner lifecycleの製品ガイダンス

- 発行者・役割: GitHubのrunner運用仕様を直接の根拠とし、Takumi RunnerとStepSecurityは実装・検知の候補として扱う。
- 版: 旧資料レビュー2026-08-11。GitHub self-hosted referenceは2026-09-16に確認。他リンクの現在の挙動は再レビューが必要。
- 利用先: `PSB-CICD-007 / RUNNER-1..9`、`ENG-CICD-003`、共有教材。
- 採用: job単位の割当、compute・storage破棄、外部ログ保存を別の条件として扱う。
- 不採用・限界: ephemeral登録やjob終了だけをhost破棄の証拠にしない。製品候補は導入済みでも必須でもない。旧資料のE3 syntheticと旧controlのE1 external-referenceは実環境の採用証拠へ昇格させない。

保持した仕様・候補:

- [GitHub-hosted runners](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners)、[self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)、[secure use](https://docs.github.com/en/actions/reference/security/secure-use)。
- [Runner group access](https://docs.github.com/en/enterprise-cloud@latest/actions/how-tos/manage-runners/self-hosted-runners/manage-access)、[旧一覧のaccess URL](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access)、[monitor and troubleshoot](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot)、[self-hosted REST / JIT registration](https://docs.github.com/en/rest/actions/self-hosted-runners)。
- Takumi Runnerの[quickstart](https://shisho.dev/docs/t/runner/quickstart/)、[ephemeral architecture](https://shisho.dev/docs/t/runner/architecture/ephemeral/)、[limitations](https://shisho.dev/docs/t/runner/limitation/)。
- [StepSecurity detections](https://docs.stepsecurity.io/harden-runner/detections): 実行中の検知候補。host破棄・隔離の代替ではない。
- 旧frameworkレビュー: product-security、2026-09-02。関係は保持し、新しい特性への割当はレビュー中。

<a id="ref-build-001"></a>

## REF-BUILD-001 — CI/CD runtime sensorの調査候補

- 発行者: cicd-sensor project。役割は製品候補の発見であり、直接の導入要件ではない。
- 参照版: [commit `6e08deb2221c19a854d8d3be7ce37c659c15bce9`](https://github.com/cicd-sensor/cicd-sensor/tree/6e08deb2221c19a854d8d3be7ce37c659c15bce9)、旧レビュー2026-07-30。
- 利用先: `ENG-CICD-003`のruntime detectionとの境界、次のBuild Security移行の評価入力。
- 採用: process・file・networkの観測、sensor health、検知後の対応を独立して評価する。
- 保留: 未導入。旧時点ではinterfaceはpre-releaseとして扱っていた。採用前に版・integrity、kernelと実行権限、秘密情報の除去、収集失敗を再確認する。
- ライセンス: 同commitの[Apache-2.0 LICENSE](https://github.com/cicd-sensor/cicd-sensor/blob/6e08deb2221c19a854d8d3be7ce37c659c15bce9/LICENSE)とeBPF等の構成要素のライセンスを個別に確認する。
- 限界: telemetryの取得はsandbox、通信制限、runner破棄の代替ではない。sensor停止をclean判定へ変換しない。

## SPEC-SITF-1.0.0 — Supply-chain Infrastructure Threat Framework

- 発行者・役割: Wizの脅威分類。準拠要件ではない。
- 参照版: `1.0.0@d1d1536`、[commit `d1d1536da5cbc7107fb90ab3f5a4b1f62b21ea59`](https://github.com/wiz-sec-public/SITF/tree/d1d1536da5cbc7107fb90ab3f5a4b1f62b21ea59)。
- 利用先: `PSB-CICD-009`の旧`T-C007`関係をframework mappingへ保持。特性割当はレビュー中。
- 限界: 攻撃行動との関係であり、cacheの安全性、導入済み状態、分類体系の完全な網羅を証明しない。

## パイロット対象外の移行状態

<a id="ref-container-003"></a>

## REF-CONTAINER-003 — Falco runtime event / health guidance

- 発行者・役割: Falco Projectの製品ガイダンス。利用先はPSB-CONTAINER-004、ENG-RUNTIME-001と教材。
- 旧参照版: [Falco 0.44.0](https://github.com/falcosecurity/falco/releases/tag/0.44.0)、レビュー2026-07-31。今回binaryを取得・導入していない。
- 保持する仕様: [JSON output](https://falco.org/docs/outputs/formatting/#json-output)、[supported fields](https://falco.org/docs/reference/rules/supported-fields/)、[metrics](https://falco.org/docs/metrics/)。
- 採用: Structured event、対象identity、rule/configの版、kernel・store・output dropをイベント件数と別に評価する。
- 変更して採用: 旧fixtureのsequence・完全性は収集契約として扱い、全kernel挙動の観測を証明するとは解釈しない。
- 保留・限界: 2026-09-17のmetrics取得は移転先へredirectしたが本文を取得できなかった。製品の現在のcontractは`re-review-required`。Driver・kernel・権限・性能・更新integrity・retentionは採用先の責任。製品必須要件ではない。

<a id="ref-container-004"></a>

## REF-CONTAINER-004 — Sysdig runtime forwarding / health guidance

- 発行者・役割: Sysdigの製品ガイダンス。利用先はPSB-CONTAINER-004、ENG-RUNTIME-001と教材。
- 旧contractレビュー: 2026-07-31。Immutable文書commitは未確定。`13.0.0-fixture`は合成schema値で推奨versionではない。
- 保持する仕様: [Event forwarding](https://docs.sysdig.com/en/sysdig-secure/event-forwarding/)、[runtime policy events](https://docs.sysdig.com/en/sysdig-secure/runtime-policy-events/)、[agent health](https://docs.sysdig.com/en/sysdig-monitor/integrations/integration-library/sysdig-agent-health/)。
- 採用: Event配列の正規化、workload/imageとの結合、agent・connection・license・drop・forwarding・配送の独立確認。
- 保留・限界: 2026-09-17のforwardingページ取得は失敗。現在のcontractは`re-review-required`。API、subscription、導入、通知先、retention、対応は未確認。購入推薦・製品必須要件ではない。

<a id="ref-runtime-response-handoff-001"></a>

## REF-RUNTIME-RESPONSE-HANDOFF-001 — 初動と製品適用の入力

- 役割: 旧資料記録を用いた横断設計入力。利用先はENG-RUNTIME-001のtriage→製品適用→対応境界。
- 保持する正本: [NIST SP 800-61 Rev.3記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-006)、[FIRST maturity](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-003)、[FIRST Services Framework 1.1](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-004)、[Dependency-Track](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-001)、[SBOM lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-002)。版・snapshot・integrity・採否・除外理由の詳細は旧記録を保持し、移植は各主題で再レビューする。
- 採用: Evidence保全、担当者、独立承認、正確なartifact/deployment同一性と完全性の区別。
- 不採用・限界: Eventだけで全製品の影響を確定しない。PSIRT成熟度をこのpilotの存在から推定しない。GOV-001はガイダンス移行済みだが、組織能力評価は未実施。

## REF-SUPPLY-CHAIN-IMPACT-001

### 役割・利用先・参照時点

PSB-GOV-001、ENG-GOV-001、Impact教材の設計入力。2026-09-17に旧参照記録を移行したもので、外部仕様を現行版へ再確認した記録ではありません。
旧REF-REL-001・REF-REL-002の確認日2026-07-31と、旧GOV-001のfixture契約を保持します。

### 保持する参照仕様

- Dependency-Track公式: [製品](https://dependencytrack.org/)、[4.14.3 release](https://github.com/DependencyTrack/dependency-track/releases/tag/4.14.3)、[CI/CD](https://docs.dependencytrack.org/usage/cicd/)、[notifications](https://docs.dependencytrack.org/integrations/notifications/)、[permissions](https://docs.dependencytrack.org/administration/users-and-permissions/)、[REST API](https://docs.dependencytrack.org/integrations/rest-api/)、[next docs](https://dependencytrack.github.io/docs/next/)。4.14.3 normalized fixtureを参照。旧JAR SHA-256は`11a5c85616b745803b5653016d9da2195f2e23ac66fe6a85d2ae2b4661d393a9`。現在推奨する実行版を意味せず、この移行ではdownloadしない。
- CISA/NSA等: [SBOM consumption guidance, 2024-08](https://www.cisa.gov/sites/default/files/2024-08/SECURING_THE_SOFTWARE_SUPPLY_CHAIN_RECOMMENDED_PRACTICES_FOR_SOFTWARE_BILL_OF_MATERIALS_CONSUMPTION-508.pdf)、[CISA resources](https://www.cisa.gov/topics/cyber-threats-and-advisories/sbom/sbomresourceslibrary)。SBOMの受領だけでなく、継続利用と製品影響調査へ使う。
- CycloneDX: [SBOM](https://cyclonedx.org/capabilities/sbom/)、[OBOM](https://cyclonedx.org/capabilities/obom/)、[1.7 JSON](https://cyclonedx.org/docs/1.7/json/)。旧adapterの対応schemaは1.7。OBOMを引用しても全稼働資産の収集済みを主張しない。
- SPDX: [specifications](https://spdx.dev/use/specifications/)、[3.0.1 specification](https://spdx.dev/wp-content/uploads/sites/31/2024/12/SPDX-3.0.1-1.pdf)。参照仕様として保持するが、旧adapterのSPDX対応は主張しない。
- 利用者提供SBOM lifecycle資料: [旧正本](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)。外部の書誌情報が未提供であり、一次仕様と同じ確度で扱わない。
- Incident対応のNIST・FIRST資料は[REF-RUNTIME-RESPONSE-HANDOFF-001](#ref-runtime-response-handoff-001--初動と製品適用の入力)を正本とする。Frameworkのexact版は[SSDF](#spec-nist-ssdf-11--nist-sp-800-218)、[ATT&CK](#spec-mitre-attack-v191--mitre-attck-enterprise)とmappingで保持する。

### 採用・変更・不採用・限界

採用: exact componentからSBOM、build、artifact、deploymentへの照合、検索の全page・ACL・鮮度・処理health、owner承認付きdry-run。
変更: 旧保全先頭の固定runbookを、緊急封じ込めとの並行条件も決める設計判断として説明する。検索一致を侵害確定へ昇格させない。
不採用: 分析基盤だけを真実の正本にすること、検索結果からの破壊的自動対応、fixtureの成功による導入済み判定。
Uploadは事前作成project UUIDとBOM_UPLOADを基本とし、検索用VIEW_PORTFOLIO・VIEW_VULNERABILITYから分離する。BOM_CONSUMEDを処理完了と取り違えず、BOM_PROCESSEDの待機を有界にするという旧判断を保持するが、現行権限・event契約はadapter実装前に再確認する。
AutoCreateのためのPROJECT_CREATION_UPLOADや広い管理権限は既定にしない。Validation失敗、timeout、pagination不足をcleanへ変換しない。
5系のAPI・配布・notification変更は再レビューしてから対応する。旧記録にある5.0.3観測やSPDX 3.1 RC情報を現在の最新情報として引き継がない。
Supplier signatureの旧REL-004 fixtureは別の保証対象であり、このcontrolへ統合しない。
Live API・collectorの完全性、process-loaded component、実対応・復旧は資料だけでは証明できない。

## REF-SECURITY-EXCEPTION-LIFECYCLE-001

### 役割と参照資料

PSB-GOV-002とENG-GOV-002における例外lifecycleの設計入力。旧controlで2026-08-05にレビューした
[NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)と
[OpenSSF Security Baseline 2026-02-19](https://baseline.openssf.org/versions/2026-02-19)を保持します。
Exact framework関係はmappingへ分離し、この資料記録だけから準拠を主張しません。

### 採用・変更・不採用・限界

採用: exact control/check/target、独立したowner・reviewer・approver、理由・risk・代替策・是正先、上限付き期限、使用時の状態評価、取得・解析障害のfail-closed処理。
変更: 旧`psb-security-exception/v1`の具体schemaと30日上限は唯一の標準ではなく、設計patternの一候補として保留する。新構造ではproperty identityと組織policyに合わせる。
不採用: 例外による元checkの`PASS`化、全controlのrisk判断を共通serviceへ移すこと、SHA-256だけによる承認真正性の主張、fixture成功による組織導入判定。
限界: NIST SSDFとOpenSSF Baselineは、repository固有のrole数、state名、schema、期間を直接規定する資料として扱わない。Ticket system、信頼時刻、取消、通知、policy engine、実gateの証拠は別途必要。

<a id="spec-nist-sp-800-190"></a>

## SPEC-NIST-SP-800-190 — Container security guidance

- 発行者・版: NIST、SP 800-190、September 2017。[公式publication](https://csrc.nist.gov/pubs/sp/800/190/final)。
- 利用先: PSB-CONTAINER-004の旧`4.4.4`関係を保持。旧レビューproduct-security、2026-07-31。
- 限界: Exact framework関係を保持しただけで、実検知・導入・準拠の証拠へ昇格させない。新しい特性への割当はレビュー中。

<a id="ref-application-authorization-001"></a>

## REF-APPLICATION-AUTHORIZATION-001 — Object認可の設計ガイダンス

- 発行者・役割: OWASP、[Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)。設計ガイダンスであり規格のrequirement IDではない。
- 参照版: Mutableな公式文書を2026-09-17確認。固定commitは未確定、`re-review-required`。再配布せずリンク・要約で使用。
- 利用先: `ENG-DESIGN-001`、請求書の教材、Python / SQLite限定実装。
- 採用: 認証と認可を分け、既定拒否、対象と操作ごとの確認、信頼する情報源、サーバー側の強制、拒否テストを設計へ反映。
- 変更して採用: 一般的な属性・関係の設計を、このpilotではtenant・owner・操作scopeへ限定。List・export等は要検討として残す。
- 不採用: 複雑なpolicy engineの追加、roleだけで個々の対象を許可する設計、IDの推測困難性だけによる保護。
- 限界: HTTP認証、session失効、並行処理、監査配送、全endpointと実組織の導入は未確認。
- 仕様の次のレビュー対象: [ASVS 5.0.0 registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-asvs/README.md)の固定commit `5cf9b032440be53ce345ab3c130fda46ba1ce7a2`、公式English JSON SHA-256 `bcdbec214d70abcfad9284a31d4f9e5134305831d628aad3aa85d7e26626cb35`を保持。Exact requirement本文との意味的照合前なので、新しいframework mappingは追加しない。
- [組織チェックリストREF-USER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-004)は引き続き原本未提供。この公開教材をその原本の復元・代替として扱わない。

<a id="spec-consumer-artifact-verification"></a>

## SPEC-CONSUMER-ARTIFACT-VERIFICATION — Consumerの受入仕様

- 利用先: `PSB-REL-001 / ACCEPT-1..5`、`ENG-REL-001`、教材。期待値の管理と強制点の選択はリポジトリでの解釈。
- 仕様: [SLSA v1.2 Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)、[Build provenance](https://slsa.dev/spec/v1.2/build-provenance)、predicate `https://slsa.dev/provenance/v1`を保持。2026-09-17確認。
- 採用: Consumer-owned trust root、署名者とbuilderの対応、subjectとの結合、build type・外部parameter等の期待値照合。受取側・registry・monitorの設置場所を分ける。
- 変更して採用: Producer提供policyも独立した認証・変更承認を通す。初回値を基準にする方式は初回信頼の限界を教材へ残す。
- 不採用: Builderが自己申告したlevelの自動承認、署名成功だけでの無害性判定、欠落時の無検証fallback。
- 保持した隣接仕様: [npm CLI v9 audit signatures](https://docs.npmjs.com/cli/v9/commands/npm-audit/#audit-signatures)。Registry signatureの補助検証であり、このcontrolの来歴期待値照合の代替ではない。旧版URLを保持し、採用時に`re-review-required`。
- Mapping根拠: `SPEC-SLSA-1.2`（Build track）、`SPEC-NIST-SSDF-1.1 / PS.2.1`、`SPEC-OPENSSF-OSPS-2026.02.19 / OSPS-BR-06.01`。旧レビューproduct-security、2026-07-27の関係を保持。特性割当はレビュー中。
- 保留: 旧Ed25519 JSON署名fixtureの公開鍵・crypto終了状態を再レビューしてから独立実装にする。Keyless、失効、timestamp、transparency、使用gateの実環境は未確認。


<a id="spec-build-containment"></a>

## SPEC-BUILD-CONTAINMENT — Buildの実行権限と強制境界

- 役割: 旧Build controlの設計根拠と参照仕様を保持する記録。製品非依存の構造・確認方法はリポジトリでの解釈。
- 利用先: `PSB-BUILD-001 / BUILD-1..6`、`ENG-BUILD-001`、学習ノート。
- 採用: 実行コードから秘密情報・公開権限を分離し、外側で通信・隔離を強制する。観測とhealthを区別する。
- 変更して採用: 旧JSONのread-only、telemetry等の宣言を実効性の証拠にせず、採用先の拒否・収集確認へ分ける。
- 不採用: 旧JSON計画・検証器・期待結果を実行時封じ込めの実装として移植しない。短命OIDCの15分上限は旧例のpolicyであり、一般要件として継承しない。
- 限界: Provider固有の強制、sensor、実環境は未確認。旧frameworkレビューproduct-security、2026-07-27の版・ID・関係を保持し、新しい特性への割当はレビュー中。

保持した参照仕様:

- [GitHub automatic token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication): 旧参照URLを保持。現在の設定・実効権限は採用時に再確認する（`re-review-required`）。Token permissionsはhostやcloud権限を制限するものではない。
- [SLSA v1.2 Build track basics](https://slsa.dev/spec/v1.2/build-track-basics): 2026-09-17確認。Build L3のrun間隔離・来歴署名用secret分離を設計入力に使う。Build trackへの関係でありSource trackやlevel達成の主張ではない。
- `SPEC-NIST-SSDF-1.1`のPW.6.1、`SPEC-OPENSSF-OSPS-2026.02.19`のOSPS-BR-01.03: 旧mapping根拠を保持。実環境を検証した関係へ昇格させない。
- [cicd-sensor固定snapshot](https://github.com/cicd-sensor/cicd-sensor/tree/6e08deb2221c19a854d8d3be7ce37c659c15bce9): 採否・ライセンス・制限は`REF-BUILD-001`を正本とし、未導入の候補として保持。

<a id="spec-slsa-1-2"></a>

## SPEC-SLSA-1.2 — SLSAのversion付き仕様

- 発行者・版: SLSA、1.2。[Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)を2026-09-17確認。
- 利用先: `PSB-BUILD-001`の旧`build-track-basics#build-l3-hardened-builds`関係。正確なidentifierの旧正本は[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/slsa/README.md)。
- 採用: Buildの隔離と来歴の生成・署名権限を分ける設計根拠。
- 限界: このcontrolはplatform assessment、level全体、Source trackの保証を行わない。特性割当はレビュー中。

<a id="spec-dependency-lock-identity"></a>

### SPEC-DEPENDENCY-LOCK-IDENTITY — Native lockとartifact完全性の仕様

- 区分: `product-specification`。下記の横断ガイドは設計入力として区別する。
- 発行者: npm、pnpm、pip、Astral、Yarn、Bunの各project。
- 利用先: `PSB-DEPS-003 / DEP-ID-1..5`、`ENG-DEPS-003`、共有学習ノート。
- 移行元: `controls/dependency-security/lockfile-integrity/README.md`と`control.yaml`。
- 固定した文書改訂: 未特定。変更可能なURLは`re-review-required`。
- 今回の確認日: `2026-09-16`。npm ci v11とuv project syncの公式文書を確認。他製品の現在の挙動は未再確認。
- 採用: manifestとlockの対応、全対象依存の記録、hash照合、通常buildでlockを書き換えないことを別特性として扱う。
- 変更して採用: package manager別wrapperとsynthetic fixtureの一括移植をせず、設計判断と製品仕様を残す。
- 不採用: frozenという名前だけでmanifest鮮度を推論すること、versionだけでbytesの同一性を主張すること。
- 限界: 配布ファイルの同一性は安全性・originの正当性・導入済み状態を証明しない。

旧成果物が参照した仕様は以下を保持する。旧runtimeのpnpm `11.25.0`等は旧実装の基準であり、
今回の新しい実装対応版として認定しない。YarnとBunの旧例はreference-only、他製品の旧tamper testも
移行先で再実行したとは扱わない。

- npm: [package-lock.json v10](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json/)、[npm ci v11](https://docs.npmjs.com/cli/v11/commands/npm-ci/)、[version指定なしのnpm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
- pnpm: [lockfile](https://pnpm.io/lockfile)、[install](https://pnpm.io/cli/install)
- pip: [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)。今回のpip挙動検査は[SPEC-INSTALL-EXECUTION-POLICY](#spec-install-execution-policy)の限定範囲のみ
- uv: [project lock layout](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile)、[project sync](https://docs.astral.sh/uv/concepts/projects/sync/)、[CLI / uv pip sync](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync)。`--locked`による鮮度確認と`--frozen`による更新回避を区別する
- Yarn: [install](https://yarnpkg.com/cli/install)、[checksumBehavior](https://yarnpkg.com/configuration/yarnrc/#checksumBehavior)
- Bun: [install](https://bun.com/docs/pm/cli/install)、[lockfile](https://bun.com/docs/pm/lockfile)、[auto-install](https://bun.com/docs/runtime/auto-install)

隣接ガイドも省略しない。下記は今回全文を再レビューしておらず、direct mappingの追加根拠にはしない。

- [SLSA v1.2](https://slsa.dev/spec/v1.2/)：build input・provenanceとの受け渡し。旧来どおりdirect mappingなし
- [OWASP SCVS](https://scvs.owasp.org/)：component検証の設計入力。採用する要件・版は別途レビュー
- [CISA developer supply-chain guide](https://www.cisa.gov/resources-tools/resources/securing-software-supply-chain-recommended-practices-guide-developers)：取得・利用の連鎖を考える入力。正確な刊行版は再確認

ATT&CK `v19.1 / T1195.001`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`、
OSPS `2026.02.19 / OSPS-BR-05.01`は旧mappingの版・ID・関係・confidenceを保持する。
旧レビューは`product-security / 2026-08-31`、新特性への割当は移行レビュー中。

<a id="ref-deps-002"></a>

### REF-DEPS-002 — GitHub dependency review guidance

- 区分: `implementation-guidance`、発行者: GitHub、状態: `adopted-partially`。
- 旧一覧のレビュー日: `2026-07-31`、今回のconcept文書確認日: `2026-09-16`。
- 固定文書改訂: 未特定、`re-review-required`。ActionのREADMEのみ下記のcommitで固定。
- 利用先: `PSB-DEPS-004 / DEP-REVIEW-1..3`、`ENG-DEPS-003`、学習ノート、GitHub実装例。
- 採用: current base/head比較、対応依存の差分と既知脆弱性判定、必須merge gateへの接続。
- 変更して採用: GitHubを必須製品にせず、比較・判定・強制の責任を製品非依存で定義する。
- 不採用: license・Scorecard・origin・provenance等を基本workflowが判定済みと扱うこと。追加policyは別に明示する。
- 限界: advisoryのない悪意、coverage不足、実効ruleset、全platform・依存の完全性をActionの存在だけで証明しない。

参照仕様:

- [Dependency review concepts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)
- [Configure dependency review action](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action)
- [Dependency review REST API](https://docs.github.com/en/rest/dependency-graph/dependency-review)
- [Reviewing dependency changes](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-dependency-changes-in-a-pull-request)
- [Action README / configuration](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/README.md#configuration)：旧実装のfull SHAを保持。更新時はsemantic diffをレビュー
- [Trivy filesystem](https://trivy.dev/docs/latest/target/filesystem/)、[repository](https://trivy.dev/docs/latest/target/repository/)：旧READMEの隣接比較資料。今回未再確認。継続SCAや代替profile候補であり、base/head差分を自動的に満たさない

旧参照一覧はlicense、取得元、来歴、独立承認、期限付き例外を拡張提案として掲げ、synthetic fixture中心と
記述している。一方、移行元の現行`PSB-DEPS-004`はGitHub Actionの既知脆弱性gateとlive ruleset確認を中心とする。
この範囲差を隠さず、拡張提案を基本実装の保証に昇格させない。追加する際は根拠と観測範囲を別途レビューする。

旧mappingのOSPS `2026.02.19 / OSPS-VM-05.01..03`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`、
ATT&CK `v19.1 / T1195.001`を保持する。旧レビューは`product-security / 2026-09-03`、割当は移行レビュー中。
OSPSの参照記録に対する今回の利用範囲は`OSPS-BR-05.01`、`OSPS-VM-05.01`、`OSPS-VM-05.02`、
`OSPS-VM-05.03`へ広がる。刊行版・commitは既存の`SPEC-OPENSSF-OSPS-2026.02.19`を維持し、
移行によって適合性を新たに認定したとは扱わない。

| 追加移行の成果物 | 直接の根拠 | 横断分析の入力 |
|---|---|---|
| PSB-DEPS-003 | SPEC-DEPENDENCY-LOCK-IDENTITY | REF-PORTFOLIO-001、LOCAL-SUPPLY-CHAIN-ATTACK-STAGES |
| PSB-DEPS-004 | REF-DEPS-002 | 同上 |
| ENG-DEPS-003、共有教材 | 上記二資料の役割を分けて利用 | 同上 |

旧`docs/SECURITY_GUIDANCE_SOURCES.md`にある他の`REF-*`は削除または否定していません。このパイロットの対象外として
旧参照資料一覧に残し、対応するコントロール／パターンを移すときに、参照資料記録ごと移行します。

## REF-SCANNER-EVIDENCE-001

### 役割・利用先・参照時点

PSB-DETECT-001、ENG-DETECT-001、Zero findings教材の設計入力。旧`REF-DETECT-001..003`を役割に合わせて統合しました。
旧レビュー日2026-07-30（Trivy）・2026-07-31（DockSec）・2026-08-14（Checkov比較）を保持し、この移行では外部仕様や現在の配布物を再確認していません。

### 保持する製品資料とidentity

- Trivy: [v0.72.0](https://github.com/aquasecurity/trivy/releases/tag/v0.72.0)、reviewed source `8a32853686209a428179bb3a1688802b25691564`、Linux archive SHA-256 `bbb64b9695866ce4a7a8f5c9592002c5961cab378577fa3f8a040df362b9b2ea`、[signature verification](https://trivy.dev/latest/docs/advanced/signatures/)、[offline operation](https://trivy.dev/latest/docs/advanced/air-gap/)、[GHSA-69fq-xp46-6x23](https://github.com/advisories/GHSA-69fq-xp46-6x23)。旧GitHub API観測では2026-07-30にimmutable。現在推奨するversionという意味ではない。
- OWASP DockSec: [project](https://owasp.org/DockSec/)、reviewed source `4ddcb5285f437c0e84a42c748b0f61f56543e344`、[PyPI 2026.7.5](https://pypi.org/project/docksec/2026.7.5/)、wheel SHA-256 `7f8781db7651216556c86c71ab45527bc484801b974ff264fe0ebe7f70a6f5fb`。旧確認時はTrusted Publishingなし。
- Checkov: 旧比較対象3.3.8 sdist SHA-256 `a65e5cda0337e7770436eeadabb1f65c6ce4ad7f5b145a7f801bfdf14f1aea05`、[mutable policy index](https://www.checkov.io/5.Policy%20Index/github_configuration.html)。実行dependencyとしては不採用。
- Frameworkのexact版は[SSDF](#spec-nist-ssdf-11--nist-sp-800-218)、[OpenSSF Baseline](#spec-openssf-osps-20260219--openssf-osps-baseline)、[NIST SP 800-190](#spec-nist-sp-800-190--container-security-guidance)をmappingから参照する。

### 採用・変更・不採用・限界

採用: Scanner release・publisher・実行binaryのidentity、DB・policy identity、network取得とoffline scanの分離、clean・finding・errorの区別、secret redaction、固有価値に基づくtool選定、AI remediationとgateの分離。
変更: Trivyをcontrolの名前や唯一の実装にせず、scanner acquisitionとevidence contractへ一般化。DockSecは製品固有の実装候補として保留する。
不採用: DockSec公式Actionは旧review時に内部でmutable `latest`と`curl | sh`を使用していたため不採用。External tool installer、`install-skill`、`--no-redact`、AI scoreによるrelease decisionも不採用。Checkovは固有のblocking valueが示されるまで追加しない。
限界: 固定hashはpublisher identity・semantic safety・transitive dependency完全性を単独で保証しない。Application-level offline optionはOS network isolationではない。Fixture detectionはlive coverage、最新DB、未知脆弱性を証明しない。製品採用時に現行release、署名方式、依存、CLI contractを再レビューする。
