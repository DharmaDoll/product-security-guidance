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

[Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)と[教材](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/learning.md)の設計入力です。開発環境に限定します。

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
- SOURCE-004照合: 2026-09-24に固定commitの4文書を確認。Credential types
  `a32f63447dc398af6c8f4ec19af95557f0e1ea96bf2aca062df99e8ce935a167`、SAML
  `d8a3f3bf0fdcd1594bbb1a46a7d140d54780ba3a674a5a8d094d675f92c8d83e`、SCIM
  `703054c52df8ad431d6201252f83293a884d0ebef47213bdc16ade66f53c575b`は旧registryのSHA-256と一致。
  Account securityは旧registryにhashがなく、今回
  `5def696244c0bc300adf532acdb4d4a40ae0eabd0c218afbc969a028847c3e1b`を記録。
  採否とproperty割当は[SOURCE-004照合記録](../docs/SOURCE_CREDENTIAL_MAPPING.md)を参照。
- 限界: GitHub固有の実装根拠であり、GitHub環境の安全性や正式な準拠を証明しない。SAMLを
  phishing-resistant MFA、SCIMを全credentialとsessionの失効、credential taxonomyを保管・audit要件と解釈しない。

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
- 現行mappingで使用する要件ID: `PO.5.2`、`PS.1.1`、`PS.2.1`、`PW.4.1`。初期パイロットのSOURCE-004は`PS.3.1`を使用していたが、2026-09-23の公式本文照合で非継承とし、`PS.1.1`への部分的な設計関係を新規評価した。[SOURCE-004照合記録](../docs/SOURCE_CREDENTIAL_MAPPING.md)を参照
- 利用箇所: `PSB-SOURCE-001 / ENDPOINT-1・2・3・4・7`、`PSB-SOURCE-004 / SRC-AUTH-1〜6`、`PSB-REL-001 / ACCEPT-1・2・3・4`、`PSB-REL-002 / PROV-DIST-1〜7`、`PSB-DEPS-001`
- 限界: マッピングは特定のプラクティスを支援する関係であり、SSDF準拠を意味しない。

<a id="spec-mitre-attack-v19-1"></a>

#### SPEC-MITRE-ATTACK-v19.1 — MITRE ATT&CK Enterprise

- 区分: `threat-taxonomy`
- 基準とするコンテンツのバージョン: `v19.1`
- 公式資料: [MITRE ATT&CK version history](https://attack.mitre.org/resources/versions/)
- 固定取得物: `attack-stix-data` tag `v19.1`、commit `6c3719993d0401de199203ecc3f369544d9e091c`、
  Enterprise STIX SHA-256 `bdf1ce86a4e604214c5076d37ae4dcb322678afc528df8492e6fdc1b554f5da3`。
  2026-09-24に取得hashの一致と`T1078`・`T1552.001`本文を確認。
- パイロットで使用する技術ID: `T1078`、`T1552.001`、`T1593.003`、`T1195.001`
- 利用箇所: `PSB-SOURCE-003`, `PSB-SOURCE-004`, `PSB-DEPS-001`
- 限界: 攻撃者の挙動との関係を示すもので、検証要件や準拠要件ではない。SOURCE-004との採否と範囲は
  [照合記録](../docs/SOURCE_CREDENTIAL_MAPPING.md)を参照。

<a id="spec-openssf-osps-2026-02-19"></a>

#### SPEC-OPENSSF-OSPS-2026.02.19 — OpenSSF OSPS Baseline

- 区分: `normative-specification`
- バージョン／タグ: `2026.02.19`／`v2026.02.19`
- 参照コミット: `e67ae247ebfb2fd758c9d186335e60cad0a74e78`
- レビュー対象文書のSHA-256:
  `54d13befdb1ae4c63b8612acabc1f0d716874be4187d25801d6ba2d6eee98271`
- パイロットで使用する要件ID: `OSPS-AC-01.01`、`OSPS-BR-01.03`。SOURCE-002で`OSPS-BR-07.01`を追加（2026-09-23に版付き公式本文を確認）
- 参照先: [OpenSSF OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19)
- SOURCE-004照合: 2026-09-24に`OSPS-AC-01.01`のrequirementとrecommendationを確認。
  機微なrepository resourceのreadまたはmodify時のMFAに対し、SRC-AUTH-2はcredential発行・機微変更だけを扱う
  部分対応とした。
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
- 成果物metadata: 2026-09-24に公式WordPress APIのmedia ID `52216`、公開日`2025-12-09`、
  PDF size `1,274,186 bytes`、公式`source_url`を確認。直接取得はHTTP 403で拒否され、artifact hashとASI03本文は未確認。
- 利用箇所: `PSB-SOURCE-004`のGitHub MCP適用時
- 追加利用箇所: `PSB-AI-002`のEXT-1〜6。旧レビュー2026-08-05のASI04関係を移行レビュー中で継承。旧registryでは公式PDFの自動取得が拒否されており、artifact hashは未記録。刊行年・公開日・URLの固定をPDFの完全性検証と読み替えない。
- 限界: エージェント型AIのリスク分類全体への対応や、AIエージェントの安全性を意味しない。
  SOURCE-004のASI03関係は、正確な本文を再取得してproperty割当とconfidenceを照合するまで
  `migration-review-required`を維持する。

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
- 利用先: [PSB-SOURCE-001](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)のENDPOINT-1〜8、[ENG-SOURCE-002](../engineering/source-protection/managed-developer-endpoint/README.md)、[教材](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/learning.md)、[29項目の対応表](../docs/ENDPOINT_MIGRATION.md)。REF-USER-001を廃止・改名するものではない。
- 採用: 暗号化、画面ロック、更新、権限、アプリ、バックアップ、EDRの稼働確認、集中管理、物理保護を個人の注意に依存させない設計。
- 変更して採用: 「最新版」をサポート対象・適用期限・例外管理へ具体化。登録済み、現在の観測、アクセス許可を分離し、通知・失効・復旧の責任を接続。通信設定の配布だけを迂回防止と見なさない。これらはリポジトリの設計判断で、外部仕様の要求とは主張しない。
- 不採用: ローカルhookやrequired checkによるあらゆる流出の防止、署名によるコード安全性や端末健全性の保証、遠隔環境への移動による接続元端末保護の省略。特定MDM・EDR・クラウド製品の必須化と、宣言fixtureの成功による導入済み判定も採らない。
- 2026-09-22の追加レビュー: 旧commit `3bfbeb21246bb2f58c55fa5212068805bca1719b`のcontrolと実装ガイドを確認し、直接扱う11項目をENDPOINT-1〜8へ再編集。診断で確認する項目を記載し、実施済みとは扱わない。
- Framework照合: [NIST SSDF 1.1公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)のPO.5.2（本文p.9）、PS.3.1（p.10）、PW.4.1（p.12）を2026-09-22確認。端末保護のPO.5.2を部分的な設計根拠として採用。PS.3.1のrelease保存を端末保護全般へ転用せず、PW.4.1の部品取得は隣接領域に残す。
- 脅威分類の照合: MITRE公式[T1552.001](https://attack.mitre.org/techniques/T1552/001/)・[T1555](https://attack.mitre.org/techniques/T1555/)の公開本文を2026-09-22確認。ファイル・password storeからの認証情報取得は、今回分離した認証情報保管・検査側の境界として扱う。可変ページのため`re-review-required`であり、旧v19.1全体の再検証ではない。旧4件は[対応表](../docs/ENDPOINT_MIGRATION.md#旧実装とframework-mapping)に原記録と非継承理由を保持する。
- 変更・不採用: PO.5.2の実装例を固定製品・暗号方式・期限の一律要件に変換しない。MFAは認証情報側の責任と接続し、旧4件の対応を新controlへ機械的に割り当てない。診断で確認する項目と状態によるアクセス判断は本PJでの具体化。
- 保留: Linux収集器、製品別設定、実際の通知・隔離・失効・復旧。旧参照仕様は削除せず、対応表から追跡する。
- 限界: 提供資料の外部参考文献と再配布条件は未解決。今回は原文を複製せず参照する。提供原文は複製せず固定した旧版へリンクし、再配布条件は引き続き未確認として保持する。

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
| `PSB-GOV-003`、`ENG-GOV-005` | `REF-VULNERABILITY-PRIORITY-001` | `SPEC-NIST-SSDF-1.1 / RV.1.1・RV.2.1` |
| `PSB-GOV-005`、`ENG-GOV-004` | `REF-DEPLOYED-ARTIFACT-RECOVERY-001` | `SPEC-NIST-SSDF-1.1 / RV.1.1・RV.2.1`、`SPEC-MITRE-ATTACK-v19.1 / T1195.002`。旧OSPS関係の非継承理由は移行記録に保持 |
| `PSB-GOV-004`、`ENG-GOV-003` | `REF-CREDENTIAL-EXPOSURE-CONTAINMENT-001` | `SPEC-MITRE-ATTACK-v19.1 / T1078`。旧SSDF・OSPS関係の非継承理由は`CREDENTIAL_EXPOSURE_MIGRATION.md`に保持 |
| `PSB-SOURCE-003`、`ENG-SOURCE-004` | `REF-PUBLIC-SOURCE-EXPOSURE-001` | `SPEC-MITRE-ATTACK-v19.1 / T1593.003`。旧3件の非継承理由は`PUBLIC_EXPOSURE_MIGRATION.md`に保持 |
| `PSB-SOURCE-004` | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-AI-004`, `REF-USER-001` | `SPEC-NIST-SSDF-1.1`, `SPEC-MITRE-ATTACK-v19.1`, `SPEC-OPENSSF-OSPS-2026.02.19`, `SPEC-OWASP-AGENTIC-2026` |
| GitHubのソースアクセス認証情報実装例 | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-AI-004` | 同上。ただしMCP利用時に限るマッピングを含む |
| `PSB-DEPS-001` | `REF-DEPS-004`, `SPEC-NPM-REGISTRY-METADATA` | `SPEC-NIST-SSDF-1.1`, `SPEC-MITRE-ATTACK-v19.1` |
| npmの待機期間実装例 | `SPEC-NPM-CLI-11`, `REF-DEPS-004` | コントロールのマッピングを自動継承しない |
| 管理プロキシの選択肢 | `REF-DEPS-001` | 待機期間のマッピングを自動継承しない |
| `PSB-CICD-005` | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-CICD-005`, `REF-CICD-010` | `SPEC-OPENSSF-OSPS-2026.02.19` |
| GitHub ActionsのPR境界実装例 | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-CICD-005`, `REF-CICD-010` | コントロールのマッピングを自動継承しない |
| 横断分析 | `REF-PORTFOLIO-001`, `LOCAL-SUPPLY-CHAIN-ATTACK-STAGES` | コントロールやフレームワークの対応関係へ自動変換しない |
| `PSB-DEPS-002`、Install execution policy pattern、pip実装例 | `SPEC-INSTALL-EXECUTION-POLICY` | `SPEC-MITRE-ATTACK-v19.1`, `SPEC-NIST-SSDF-1.1`。実装へ自動継承しない |
| `PSB-CONTAINER-005`、`ENG-CONTAINER-003`、Kubernetes実装例 | `REF-WORKLOAD-CONFINEMENT-001` | `SPEC-NIST-SP-800-190 / 4.4.3`。Credential、resource、networkへ自動拡張しない |
| `PSB-CONTAINER-006`、`ENG-CONTAINER-004`、Kubernetes実装例 | `REF-WORKLOAD-NETWORK-SEGMENTATION-001` | `SPEC-NIST-SP-800-190 / 4.3.3・4.4.2`。Kubernetes固有fieldやlive CNI enforcementへ自動拡張しない |
| `PSB-CONTAINER-007`、`ENG-CONTAINER-005`、Kubernetes実装例 | `REF-WORKLOAD-RESOURCE-BOUNDS-001` | `SPEC-NIST-SP-800-190 / 4.4.3`。固定resource値やKubernetes固有のquota・evictionへ自動拡張しない |
| `PSB-CONTAINER-003`、`ENG-CONTAINER-006` | `REF-CONTAINER-HOST-DAEMON-001` | `SPEC-NIST-SP-800-190 / 4.3.1・4.3.5・4.5.1〜4.5.5・4.6`。特定OS／runtime／providerの設定やlive node evidenceへ自動拡張しない |
| `PSB-IAC-001`、`ENG-CONTAINER-007` | `REF-IAC-CHANGE-BOUNDARY-001` | Framework mappingは非継承。特定IaC tool・provider・resource・live stateへ自動拡張しない |
| `PSB-REL-002`、`ENG-REL-002` | `SPEC-PROVENANCE-DISTRIBUTION` | `SPEC-SLSA-1.2 / producer-distributes-provenance`、`SPEC-NIST-SSDF-1.1 / PS.2.1`。Level達成・live配布へ自動拡張しない |

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
- 利用先: `PSB-CICD-009 / CACHE-1..7`、`ENG-CICD-003`、PSB-CICD-009の教材。
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
- 利用先: `PSB-CICD-007 / RUNNER-1..9`、`ENG-CICD-003`、PSB-CICD-007の教材。
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
- 固定PDF SHA-256: `0ebad52c4a3aba971b3a707b056e57238d1c4ad8f212dffd461ff9f5fed1bdb6`。旧registry review `2026-07-30`から保持し、2026-09-24に`4.1.5`と`4.4.5`、2026-09-25に`2.3`、`3.4.3`、`4.3.1`、`4.3.3`、`4.3.5`、`4.4.2`、`4.4.3`、`4.5.1`〜`4.5.5`、`4.6`を公式PDFで再照合。
- 利用先: `PSB-CONTAINER-001`の`4.1.5`・`4.4.5`関係、`PSB-CONTAINER-003`の`4.3.1`・`4.3.5`・`4.5.1`〜`4.5.5`・`4.6`関係、`PSB-CONTAINER-005`と`PSB-CONTAINER-007`の`4.4.3`関係、`PSB-CONTAINER-006`の`4.3.3`・`4.4.2`関係、PSB-CONTAINER-004の旧`4.4.4`関係。
- 限界: 2017年のcontainer guidanceであり、現在のKubernetes APIや製品設定を規定しない。Exact部分関係を、実導入・完全coverage・準拠の証拠へ昇格させない。

<a id="ref-container-host-daemon-001"></a>

## REF-CONTAINER-HOST-DAEMON-001 — Container nodeのruntime・管理・identity境界

### 役割・利用先・参照版

[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)と
[ENG-CONTAINER-006](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)の設計入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`4.3.1`、`4.3.5`、`4.5.1`〜`4.5.5`、`4.6`を2026-09-25に公式PDFで再照合。Orchestrator admin、node identity・isolation、minimal host、shared kernel、component update、host access・audit、filesystem、hardware trustの上位成果に使用。
- Kubernetes `1.37`: [Kubelet authentication／authorization](https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/)、[API server bypass risks](https://kubernetes.io/docs/concepts/security/api-server-bypass-risks/)、[Node authorization](https://kubernetes.io/docs/reference/access-authn-authz/node/)、[Security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)を2026-09-25に確認。Kubelet endpoint、`nodes/proxy`、static Pod、runtime socket、Node authorizer、NodeRestrictionの設計入力に使用。現行URLは可変で`re-review-required`。
- Containerd: [Operator Security Guidelines](https://github.com/containerd/containerd/blob/82f33ce76db81e47393be1cbdb6eba3343687fc5/docs/security/OPERATOR_GUIDELINES.md)、`containerd/containerd@82f33ce76db81e47393be1cbdb6eba3343687fc5`を2026-09-25に確認。Kernel・containerd・runc／shimのpatch、runtime／NRI socket、directory・binary・service・config、trusted plugin、debug／metrics endpointの実装候補に使用。
- Docker公式: [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)と[Rootless mode](https://docs.docker.com/engine/security/rootless/)を2026-09-25に確認。Local socket、SSH／mutual TLS、credential authority、daemonとcontainerのuser namespace化を方式比較へ使用。可変資料であり、導入時に対象Docker Engine版で再確認する。
- 移行元: 旧[PSB-CONTAINER-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-host-daemon-hardening/README.md)。旧check、fixture、mappingの採否は[移行記録](../docs/CONTAINER_HOST_DAEMON_MIGRATION.md)に保持。

### 採否と限界

- 採用: Purposeとsensitivityを持つnode pool、complete component inventory、bounded update／replacement、runtime・kubelet・補助endpoint、protected state、unique node identity、least node authority、host-side isolation、管理操作、live evidence health、侵害nodeの隔離・失効・再登録。
- 変更して採用: 旧rootless／user namespace／kernel lockdownとSecure Boot／TPMを全platform共通の合格条件にせず、threat、runtime、provider capabilityに応じて選び、unsupportedやfallbackを通常状態へ変換しない。固定path・modeはcontainerd等の対象実装へ限定する。
- 分離: Workloadのnon-root、capability、hostPath、seccomp profile指定等はCONTAINER-005、runtime eventとdeliveryはCONTAINER-004、resource pressureはCONTAINER-007が扱う。Cluster control plane全体、cloud account、developer endpoint、CI runnerはこの資料から自動的に対応済みとしない。
- 不採用: Provider-neutralな`policy.json`とsynthetic host evidenceによる実装済み判定、`Ready`状態によるnode trust、rootless名称だけによる隔離証明、CIS Docker Benchmarkの未確認版へのmapping、hardware attestationを提供しないplatformの無条件合格。
- 限界: Kubernetes、containerd、Docker資料は各製品の一部の仕様・guidanceであり、他runtime・OS・managed providerの挙動を規定しない。Live node、socket、listener、process、credential、patch service、audit delivery、attestationは未確認。具体実装は対象platformと使い捨てnode poolを選んでから追加する。

<a id="ref-deployment-artifact-admission-001"></a>

## REF-DEPLOYMENT-ARTIFACT-ADMISSION-001 — Exact artifactを使用許可へ結ぶ資料

### 役割・利用先・参照版

[PSB-CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と
[ENG-CONTAINER-001](../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)の設計入力です。

- SLSA `1.2`: [Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)と[Build provenance](https://slsa.dev/spec/v1.2/build-provenance)。固定版・限界は[SPEC-SLSA-1.2](#spec-slsa-12--slsaのversion付き仕様)。Exact subject、consumer-owned expectation、authenticityをadmission decisionへ渡す根拠として利用。
- NIST SP 800-190、September 2017: 固定版は[SPEC-NIST-SP-800-190](#spec-nist-sp-800-190--container-security-guidance)。`4.1.5`のtrusted image／registry、discrete cryptographic identity、execution前のsignature validationと、`4.4.5`のrun前baseline、user identity、auditを2026-09-24に公式PDFで確認。
- Kubernetes project: `kubernetes/website@e95679cfa58a843e90bf8575d8b0db548dae452b`の[Admission webhook good practices](https://github.com/kubernetes/website/blob/e95679cfa58a843e90bf8575d8b0db548dae452b/content/en/docs/concepts/cluster-administration/admission-webhooks-good-practices.md)を旧`REF-CONTAINER-002`から保持。2026-09-24に現行の[Policies](https://kubernetes.io/docs/concepts/policy/)、[Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)、[webhook guidance](https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/)も確認。現行URLは可変で`re-review-required`。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)。旧check、fixture、mappingの採否は[移行記録](../docs/DEPLOYMENT_ARTIFACT_ADMISSION_MIGRATION.md)に保持。

### 採否と限界

- 採用: 全artifactのexact digest、consumer expectation、final-state validation、作成・更新経路のcoverage、評価障害の拒否、policy・decision identityとaudit。
- 変更して採用: 使用境界でREL-001を直接再実行する方式に固定せず、exact digest・target・policy・期限へ結合した認証済みdecision receiptも許す。KubernetesのCEL・webhookは選択肢でありcontrol要件にしない。
- 分離: Non-root、capability、host、filesystem、seccompは[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)、networkは[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)、resource availabilityは[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)へ分割した。Registry access・immutability・retentionは旧CONTAINER-002の責任。
- 不採用: Tag、annotation、CIのpass表示、producerのSLSA level自己申告、署名成功だけによる無害性判断、evaluator障害時の通常allow。
- 限界: Kubernetes公式文書は製品仕様・guidanceであり、live clusterの強制証拠ではない。Current docsには将来versionを含む可変内容があるため、実装時に対象cluster versionとAPIを固定する。NIST 4.4.5全体やSLSA level、全deployment platformへの適用を主張しない。

<a id="ref-workload-confinement-001"></a>

## REF-WORKLOAD-CONFINEMENT-001 — Workload privilegeとhost境界

### 役割・利用先・参照版

[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)、
[ENG-CONTAINER-003](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)、
[Kubernetes代表実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)の設計・実装入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`3.4.3`と`4.4.3`を2026-09-25に公式PDFで再照合。Privileged mode、sensitive host mount、MAC、seccomp、read-only root filesystemを、侵害されたcontainerからhost・他containerへ進む経路とruntime configuration baselineの根拠に使用。
- Kubernetes `1.37`: [Release一覧](https://kubernetes.io/releases/)で2026-08-26 releaseとsupported minorを2026-09-25に確認。[Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)、[Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)、[Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)、[Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)の現行公式文書を同日に確認。実装例の対象minor、field、mode、failure behaviorの根拠に使用。現行URLは可変で、別minorへの導入時は再確認する。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)の`CNT-003..008`。項目ごとの採否は[移行記録](../docs/WORKLOAD_CONFINEMENT_MIGRATION.md)に保持。

### 採否と限界

- 採用: 全container経路の列挙、non-root、privilegedと権限昇格の拒否、capabilityの既定drop、runtime既定以上のseccompと利用可能なMAC、host接続の拒否、read-only root filesystem、不要なcontrol-plane credentialの自動付与禁止、final workloadのfail-closed強制。
- 変更して採用: Kubernetesの`restricted`を製品非依存のcontrol要件にせず、代表実装でversionを`v1.37`へ固定する。Pod Security Standardsが一括して扱わないread-only root filesystemとservice account tokenはValidating Admission Policyで補う。
- 分離: `CNT-007`は[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)、`CNT-008`は[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)へ移行した。Node／daemon hardeningは[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)、実行後の観測は`PSB-CONTAINER-004`へ渡す。
- 不採用: `warn`・`audit`だけによる強制済み判定、profile versionの`latest`追従、広いnamespace／user exemption、IaC検査のpassによるlive cluster強制の証明、旧synthetic verifierによる導入済み判定。
- 限界: Kubernetes資料は製品仕様・guidanceであり、live clusterの設定・拒否・runtime適用の証拠ではない。代表実装はLinux PodとKubernetes 1.37向けで、Windows、全runtime class、実際のAppArmor／SELinux状態、明示的にprojectしたtokenのRBAC・audience・期限、resource、networkを確認しない。Networkは別の実装例で扱い、この実装の検証結果へ混ぜない。NIST 4.4.3をKubernetes固有fieldや完全なhost境界の規定として扱わない。

<a id="ref-workload-network-segmentation-001"></a>

## REF-WORKLOAD-NETWORK-SEGMENTATION-001 — Workload networkのallow境界

### 役割・利用先・参照版

[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)、
[ENG-CONTAINER-004](../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)、
[Kubernetes代表実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)の設計・実装入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`3.3.3`、`3.4.2`、`4.3.3`、`4.4.2`を2026-09-25に公式PDFで再照合。Sensitivityに応じたvirtual network、狭いinterface、network境界でのegress制御、application-aware filtering、flowと異常の観測を上位の設計根拠に使用。
- Kubernetes `1.37`: [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)、[NetworkPolicy API](https://kubernetes.io/docs/reference/kubernetes-api/networking-resources/network-policy-v1/)、[Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)を2026-09-25に確認。既定では非分離、ingressとegressの独立性、allowの加算、通信両端の許可、default deny、DNSへの影響、CNIによる強制、反映遅延、`hostNetwork`・NAT・L4/APIの限界を採用。
- Kubernetes `v1.37.0` source: [test image manifest](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/utils/image/manifest.go)と[agnhost VERSION](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/images/agnhost/VERSION)を2026-09-25に確認。代表実装の`registry.k8s.io/e2e-test-images/agnhost:2.66.1`、`connect`、`netexec`の版を固定する根拠に使用。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)の`CNT-008`。採否は[移行記録](../docs/NETWORK_SEGMENTATION_MIGRATION.md)に保持。

### 採否と限界

- 採用: Workload間の通信契約、ingress／egressの既定拒否、source egressとdestination ingressの双方での最小allow、基盤flowの明示、sensitivity zoneと外部egress、enforcement coverage、live connectivityによる許可・拒否の確認。
- 変更して採用: 旧default-deny policyの存在確認を、実際の通信が両側の許可で成立することと、一時的な片側許可の削除で再び拒否されることの確認へ広げる。Kubernetes NetworkPolicyをcontrol全体の必須技術にはせず、代表実装に限定する。
- 分離: Process・kernel・host・filesystem権限は`PSB-CONTAINER-005`、実行後の検知・triageは`PSB-CONTAINER-004`が扱う。Core NetworkPolicyで表せないFQDN、service identity、gateway強制、TLS、明示deny、全cluster共通policyは製品固有の実装判断へ渡す。
- 不採用: API objectの存在、syntheticな`enforcement_available: true`、単一のdefault-deny YAMLだけによる実効性の主張。DNSや外向き通信を全環境へ共通する固定allowとして埋め込むこと。
- 限界: Kubernetes公式文書は製品仕様・guidanceであり、対象clusterのCNI、NetworkPolicy coverage、反映完了、実通信を証明しない。代表実装はKubernetes 1.37、IPv4、TCP/8080、Pod IP間の通信だけを扱い、DNS、IPv6、SCTP、ICMP、`hostNetwork`、node traffic、NAT後のidentity、service mesh、外部egress、network telemetryを確認しない。NISTの上位成果をKubernetesのselectorや具体policyへ自動変換しない。

<a id="ref-workload-resource-bounds-001"></a>

## REF-WORKLOAD-RESOURCE-BOUNDS-001 — Workload resource budgetとpressure境界

### 役割・利用先・参照版

[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)、
[ENG-CONTAINER-005](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)、
[Kubernetes代表実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)の設計・実装入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`2.3`、`3.4.3`、`4.4.3`を2026-09-25に公式PDFで再照合。Containerごとのresource allocation、runtimeがresource usageを分離する役割、runtime configuration standardの継続的な評価・強制を上位の設計根拠に使用。
- Kubernetes `1.37`: [Resource management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)、[Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)、[Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)、[Node-pressure Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/)、[PID limits and reservations](https://kubernetes.io/docs/concepts/policy/pid-limiting/)、[Reserve Compute Resources for System Daemons](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/)、[Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)、[Kubernetes CEL](https://kubernetes.io/docs/reference/using-api/cel/)を2026-09-25に確認。Request／limit、in-place resize、quota、default mutation、node allocatable、reservation、pressure／eviction、PID、local storage、CEL failure behaviorの根拠に使用。
- Kubernetes `v1.37.0` source: Network実装と同じ[test image manifest](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/utils/image/manifest.go)と[agnhost VERSION](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/images/agnhost/VERSION)を使用し、代表実装のtest imageを`2.66.1`へ固定。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)の`CNT-007`。採否は[移行記録](../docs/RESOURCE_CONSUMPTION_MIGRATION.md)に保持。

### 採否と限界

- 採用: Workload resource budget、requestとruntime ceilingの区別、tenant aggregate quota、PID・local storage、node allocatable・reservation・pressure、create／update／resize／debugの強制、quota・runtime・event・healthの観測。
- 変更して採用: 旧CPU `1000m`、memory `512Mi`、PID `256`を普遍的な上限にせず、workload測定とcapacity reviewで決める実装profileへ移す。Admission fieldの確認をruntime enforcementの証明にせず、各強制点の証拠を分ける。
- 分離: Applicationのrate limit、autoscaling、replica冗長性、PDB、persistent storage durability／IOPS、network bandwidth、availability SLOは別の設計へ渡す。Process・host権限はCONTAINER-005、network reachabilityはCONTAINER-006、runtime異常のtriageはCONTAINER-004が扱う。
- 不採用: 固定上限を全workloadへ適用すること、`pids_limit_enforced: true`等のsynthetic Booleanを実効証拠にすること、requestだけをceiling、namespace quotaだけをcluster capacity、limitの存在だけをapplication availabilityとして扱うこと。
- 限界: Kubernetes公式文書は製品仕様・guidanceであり、対象clusterのquota admission、kubelet、runtime、cgroup、filesystem計測、node reservation、pressure、event deliveryを証明しない。代表実装はCPU／memory／ephemeral-storageのfieldとnamespace quotaだけをlive APIで確認する構成で、PID、node pressure、cgroup実効値、storage hard cap、capacity、全controller・providerを確認しない。NISTのresource allocationをKubernetesの具体値や完全なavailability保証へ変換しない。

<a id="ref-container-registry-publication-001"></a>

## REF-CONTAINER-REGISTRY-PUBLICATION-001 — OCI registry publicationとlifecycle

- 利用先: `PSB-CONTAINER-002 / REGISTRY-1..7`、`ENG-CONTAINER-002`、移行記録。
- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`4.2.1`〜`4.2.3`を2026-09-24に公式PDFで再照合。Registry接続、stale image、authentication／authorizationの上位成果に使用。
- Open Container Initiative: [Distribution Specification v1.1.1](https://github.com/opencontainers/distribution-spec/releases/tag/v1.1.1)と[Image Specification v1.1.1のdescriptor](https://github.com/opencontainers/image-spec/blob/v1.1.1/descriptor.md)を2026-09-24に確認。どちらも確認時の最新release。Descriptorの必須`mediaType`、`digest`、`size`と取得bytesの照合をartifact identityの入力に使う。
- 旧実装根拠: [OWASP Docker Security Cheat Sheet固定版](https://github.com/OWASP/CheatSheetSeries/blob/cb62ae45198d07302082d4725fc3bdfe24b25dd3/cheatsheets/Docker_Security_Cheat_Sheet.md)、commit `cb62ae45198d07302082d4725fc3bdfe24b25dd3`、旧review `2026-07-30`。製品commandを普遍要件にせず、registry／supply-chain設計の補助資料に限定。
- 移行元: 旧[PSB-CONTAINER-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-registry-security/README.md)。採否は[移行記録](../docs/CONTAINER_REGISTRY_MIGRATION.md)に保持。
- 採用: Exact endpoint、repository／action scope、short-lived publisher、descriptor digest、protected release、attributable audit、bounded non-deployable lifecycle、evidence health。
- 変更して採用: NISTの上位成果をprovider-neutral contractへ分解する。`active`等のstate名、期限、federation、tag protectionはrepository interpretationでありNIST要件とは扱わない。
- 不採用: Digestだけによるpublisher信頼、tagの同一性、scanner errorをquarantine成功にすること、削除だけによる全consumerからのwithdrawal、synthetic policyによるlive導入証明。
- 限界: OCI specificationはcontent identityとdistribution APIを定義しても、組織の認可・immutability・audit・retention policyを規定しない。Provider、edition、API、replication、backup、legal retentionは実装時に別途確認する。

<a id="ref-application-authorization-001"></a>

## REF-APPLICATION-AUTHORIZATION-001 — Object認可の設計ガイダンス

- 発行者・役割: OWASP、[Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)。設計ガイダンスであり規格のrequirement IDではない。
- 参照版: Mutableな公式文書を2026-09-17確認。固定commitは未確定、`re-review-required`。再配布せずリンク・要約で使用。
- 利用先: `PSB-DESIGN-001 / OBJECT-AUTH-1..6`、`ENG-DESIGN-001`、請求書の教材、Python / SQLite限定実装。
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

- 発行者・版: SLSA、1.2。[Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)と[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)を2026-09-24確認。
- 固定source: tag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。正確なlocal identifierと責任主体は旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/slsa/README.md)を保持。
- 利用先: `PSB-BUILD-001`の旧`build-track-basics#build-l3-hardened-builds`関係、`PSB-BUILD-003`のprovenance生成2件、`PSB-REL-001`のconsumer検証2件、`PSB-REL-002`のproducer distribution関係。
- 採用: Buildの隔離と来歴の生成・署名権限を分ける設計根拠。
- 限界: 各controlは責任主体の一部だけを扱う。Platform assessment、level全体、Source track、組織のSLSA達成を保証しない。

<a id="spec-provenance-distribution"></a>

## SPEC-PROVENANCE-DISTRIBUTION — Artifactとprovenanceの配布仕様

### 役割・利用先・参照版

[PSB-REL-002](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)、
[ENG-REL-002](../engineering/release-integrity/provenance-distribution-and-availability/README.md)と教材の直接の設計入力です。

- SLSA、version `1.2`、status `Approved`。[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)のproducer `Distribute provenance`と[Distributing provenance](https://slsa.dev/spec/v1.2/distributing-provenance)を2026-09-25に確認。固定sourceは[SPEC-SLSA-1.2](#spec-slsa-1-2)と同じtag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。Community Specification License 1.0。
- NIST SP 800-218、SSDF `1.1`、2022年。[SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)の`PS.2.1`を利用。2026-09-25にtask title「software integrity verification informationをsoftware acquirerへ利用可能にする」範囲を再照合。
- 移行元: 旧[PSB-REL-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/README.md)。旧check、fixture、mappingの採否は[移行記録](../docs/PROVENANCE_DISTRIBUTION_MIGRATION.md)に保持。

### 採用・変更・不採用

- 採用: Producerがprovenanceをconsumerへ配布する責任、artifact単位のbinding、artifactからattestationへのrelation、publish時の同伴、複数の配布場所、immutability、consumerが受け入れられるformat。
- 変更して採用: SLSAの上位仕様を、artifact family・channel scope、exact digest inventory、partial publication、consumer-view access、retention、no downgrade、collection healthへ具体化する。Package ecosystemへ委譲する場合もconsumer retrievalを確認する。
- 不採用: 一releaseにつき一provenance、一artifactにつき一attestationへの固定、public accessの必須化、同じhost・pathだけを許すこと、固定5分・365日、`immutable: true`・`available: true`の自己申告による導入済み判定。

### Mappingと限界

SLSA `build-l1#producer-distributes-provenance`とSSDF `PS.2.1`を`supports / medium / design-reviewed`で現行特性へ部分割当する。SLSA local IDは固定版registryの識別子であり、controlだけによるBuild L1以上の達成を示さない。SSDFのtaskはprovenanceだけを唯一の実現方法として指定しない。

SLSAは特定registry、release service、API、認証方式、保持日数、availability SLOを規定しません。SSDFもartifact-attestation relationや配布実装を規定しません。Live publication、consumer retrieval、immutability、replication、garbage collection、retention、withdrawalは未検証です。

<a id="spec-platform-provenance-generation"></a>

## SPEC-PLATFORM-PROVENANCE-GENERATION — Platform provenance生成仕様

- 区分: `normative-specification`と、このリポジトリでの責任分離。
- 発行者・版: SLSA、1.2。固定sourceは`SPEC-SLSA-1.2`と同じtag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。
- 確認日: 2026-09-24。[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)、[Build provenance](https://slsa.dev/spec/v1.2/build-provenance)、[Assessing build platforms](https://slsa.dev/spec/v1.2/assessing-build-platforms)の公式v1.2公開版を確認。
- 利用先: `PSB-BUILD-003 / PROV-GEN-1..6`、`ENG-BUILD-002`、移行記録。
- 採用: Platformによるprovenance生成、output digestによるsubject識別、`buildDefinition`・`runDetails`・`buildType`・`externalParameters`・`builder.id`、control-plane由来の必須data、consumerが検証できるauthenticity、tenantの改変を抑止する境界。
- 変更して採用: SLSA level profileをcontrolの合否にせず、生成coverage、artifact binding、field source、認証、失敗時のhandoffへ分解する。Signatureは代表的方式だが、consumerがauthenticityを検証できる別方式も排除しない。
- 不採用: `invocationId`を全採用先で必須とする旧要件、jobが作ったJSONへplatformが署名すれば全fieldがplatform由来になるという解釈、provenanceが成果物の無害性や完全な依存inventoryを証明するという解釈。
- 限界: SLSA Build L2ではsubjectとL2必須でないfieldにtenant由来の例外があり、`resolvedDependencies`の完全性はbest effort。L3の強いunforgeability、signing secret保護、全fieldのplatform生成・検証、build間隔離は別途platform assessmentが必要。
- 実装判断: Providerと認証profileが未選定のため製品実装は作らない。旧synthetic statementとlocal OpenSSL検証をplatform実装の証拠として移植しない。

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
| ENG-DEPS-003、PSB-DEPS-003・004の各教材 | 上記二資料の役割を分けて利用 | 同上 |

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


## REF-SECRET-PUBLICATION-001

### 役割・利用先・参照版

PSB-SOURCE-002のSECRET-1〜7とENG-SOURCE-003の設計入力です。2026-09-23に公開文書を確認しました。
Git仕様は実行箇所の根拠、GitHub文書は製品での対応確認の入力、旧資料は移行判断の履歴として分けます。
下記のGit・GitHub公開URLは可変資料で固定digest未記録のため`re-review-required`です。製品実装を採用する時点で再確認します。

- Git公式：[githooks](https://git-scm.com/docs/githooks)（確認時の文書表示は2.54.0最終更新）、[git-config / core.hooksPath](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corehooksPath)、[git-push](https://git-scm.com/docs/git-push)。Hookの呼出し点、実行権限、設定変更・省略可能性を確認。
- Git公式：[git-receive-pack / Quarantine environment](https://git-scm.com/docs/git-receive-pack#_quarantine_environment)。受信したオブジェクトの隔離とref更新の境界を確認。受入拒否を、送信前の阻止と同じ意味にしない。
- GitHub公式：[Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)。受入時検査とbypass・除外権限の区別を設計へ使用。全経路・全形式の検出や導入済み状態を推論しない。[Troubleshootingの参照URL](https://docs.github.com/en/code-security/secret-scanning/troubleshooting-secret-scanning-and-push-protection/troubleshooting-push-protection-and-secret-scanning)は今回本文取得に失敗し、制限値・全対応範囲は確認できていない。
- 旧SOURCE-002：[README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md)と[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/control.yaml)。Commit `f42987759218c9b8daf3924320542a1935ef78e0`の13項目・4件の旧関係を[対応表](../docs/GIT_HOOKS_MIGRATION.md)へ保持。
- 旧実装候補：[Gitleaks v8.30.0 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.0)。旧READMEのcontainer digest `sha256:691af3c7c5a48b16f187ce3446d5f194838f91238f27270ed36eef6359a574d9`は履歴として保持し、現行実装へ継承しない。

### 規範資料と旧mappingの扱い

[OpenSSF OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19)のOSPS-BR-07.01本文と推奨を2026-09-23に確認しました。
暗号化されていない機微情報をVCSへ意図せず保存しないという成果を、検査範囲と拒否境界の設計へ採用します。
版・既存固定commitは[SPEC-OPENSSF-OSPS-2026.02.19](#spec-openssf-osps-20260219--openssf-osps-baseline)を継承し、要件全体への適合は主張しません。

旧ATT&CK v19.1 / T1552.001は認証情報保管と公開の範囲を分け、今回の新特性への直接割当を保留します。
SSDF 1.1 / PS.3.1は[端末管理の照合](../docs/ENDPOINT_MIGRATION.md#旧実装とframework-mapping)と同じくrelease保存との意味の不一致があるため継承しません。
CISA/FBIの[Product Security Bad Practices Version 2, January 2025](https://www.cisa.gov/sites/default/files/2025-01/joint-guidance-product-security-bad-practices-508c_0.pdf)は今回本文取得に失敗しました。
旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/cisa-product-security-bad-practices/registry.json)のPDF SHA-256 `c0431ac502e8bcf5ae2e4f2f47249a2aae6ead00e0af6542bd29adac850a9d3e`を保持し、現物を再照合したとは扱いません。
`CISA-PSBP-PP-08`は旧registryのローカルIDであり、CISAが発行した恒久IDではありません。旧関係と根拠は対応表に保存し、新規割当は保留します。

### 採否と限界

- 採用：コミット予定の内容・メッセージ・導入履歴の区別、検査障害の拒否、検出値の非表示、ローカルhooksから独立した受入判断。
- 変更して採用：repository-owned hooksを唯一の方式にせず、中央配布も変更権限と実効設定から評価。対象ref・内容と結果の結合、除外の期限・承認は本PJで具体化する。
- 不採用：固定した5 MiB、拡張子だけの安全判定、特定のhook frameworkやDockerの必須化、Gitleaks併用だけによる全検出の主張。CIでのmerge拒否を送信前の防止と扱わない。
- 限界：未知形式、符号化・分割された値、全PII・機密データ、LFS等の外部内容の完全検査は保証しない。代表実装の隔離テストは実施したが、実環境への導入・診断は未実施。旧自動テストの成功を今回の成果へ移さない。

<a id="ref-public-source-exposure-001"></a>

## REF-PUBLIC-SOURCE-EXPOSURE-001

### 役割・利用先・参照版

[PSB-SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)と
[ENG-SOURCE-004](../engineering/source-protection/public-exposure-observation-and-triage/README.md)の設計入力です。
GitHub固有の実装をcontrolへ固定せず、public observationのcoverage、値の最小化、occurrence state、
triage、failure semanticsを具体化するために使います。

- 発行者: GitHub。区分: `product-specification-and-guidance`
- 固定commit: `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`、commit日`2026-07-24`
- 2026-09-24に確認した固定文書:
  - [REST search](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/rest/search/search.md)、SHA-256 `5d843ab038a0ab6475fafef13c7b79e3ec0566df006755aae0c63632f334417e`
  - [REST gists](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/rest/gists/gists.md)、SHA-256 `ee298d05e995f5b3b44e91292a27ea9ac496ff697eaea57a042cb8d4a5caf9e4`
  - [Code Search syntax](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/search-github/github-code-search/understanding-github-code-search-syntax.md)、SHA-256 `8c5ae09003613732a13c3924c07f3acf77c1d655bc1c5d8e58247f478afc68cb`
- 移行元: [旧SOURCE-003](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/public-repository-exposure/README.md)。
  旧PoCのcheck、実装、mappingは[移行記録](../docs/PUBLIC_EXPOSURE_MIGRATION.md)で再配置。

### 採用・変更・不採用

- 採用: Searchにはresult・repository scope・rate・timeoutによる制限があり、`incomplete_results`を返し得ること、
  Gist contentとfile listがtruncatedになり得ること、query syntaxとqualifierがprovider仕様であること。
  これらを0 findingsとcollection failureを分ける設計根拠にする。
- 変更して採用: GitHubの具体的な上限値やqueryをcontrolの普遍要件にせず、採用実装がproviderごとの上限、
  cursor、truncation、認証viewを記録するpropertyへ一般化する。Public-only identity、deduplication、期限付きreview、
  notification handoffは旧PoCから継承した本リポジトリの設計判断として区別する。
- 不採用: GitHub Actions、Python、専用Git state branch、browser GET queryを唯一または必須の解法にしない。
  Match本文の永続保存、credential validation、HTML scraping、rate-limit回避、第三者資産のactive probingを採用しない。
- Mapping照合: 2026-09-24に固定版の原文を確認し、ATT&CK `T1593.003`だけを現行6特性へ部分割当。
  ATT&CK `T1552.001`、SSDF `RV.1.1`、OSPS `OSPS-BR-07.01`は対象成果が異なるため非継承。
  詳細は[移行記録](../docs/PUBLIC_EXPOSURE_MIGRATION.md#旧framework-mapping)を参照。

### 限界

固定GitHub文書は一つのprovider仕様であり、他providerや一般Web indexのcoverageを説明しません。
Searchは公開contentの完全なinventoryではなく、0件は過去・cache・clone・画像・binary・難読化された値の不存在を
示しません。今回、実GitHub search、Gist収集、組織indicator、credential、通知、responseを実行していません。
将来の製品実装では採用時点のAPI版、認証要件、利用条件、retention、料金・plan、provider変更を再確認します。

<a id="ref-credential-exposure-containment-001"></a>

## REF-CREDENTIAL-EXPOSURE-CONTAINMENT-001

### 役割・利用先・参照版

[PSB-GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)と
[ENG-GOV-003](../engineering/governance-operations/credential-exposure-containment/README.md)のincident response設計入力です。

- 発行者: National Institute of Standards and Technology (NIST)。区分: `incident-response-guidance`。
- 参照刊行物: `NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile`。
- 公開日: `2025-04-03`。確認日: `2026-09-24`。
- 公式資料: [NIST CSRC publication page](https://csrc.nist.gov/pubs/sp/800/61/r3/final)、[DOI 10.6028/NIST.SP.800-61r3](https://doi.org/10.6028/NIST.SP.800-61r3)。Rev.3がRev.2を置き換えたこともpublication pageで確認。
- 移行元: [旧PSB-GOV-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/credential-exposure-containment/README.md)。旧check、実装、mappingの採否は[移行記録](../docs/CREDENTIAL_EXPOSURE_MIGRATION.md)に保持。

### 採用・変更・不採用

- 採用: Incident responseを一回の秘密情報交換ではなく、準備、検知、対応、復旧と継続改善をrisk managementへ統合する考え方。RespondとRecoverを分け、組織のowner・communication・証拠・復旧判断へ接続する。
- 変更して採用: Credential incidentに必要なsecret-free authority graph、class別封じ込め、bounded replacement、consumer disposition、旧authorityの独立した拒否確認、exposure-window identityを本リポジトリで具体化する。
- 不採用: 旧controlにあった4時間のauthorization上限、七つのsurface、固定したevidence-first順序をNIST要件として扱わない。緊急封じ込めが必要な場合は、保全と並行して判断理由・失う証拠を記録する。
- 実装判断: NIST自身がRev.3の実施詳細は技術・環境・組織により変わると説明しているため、provider-neutralなrevoke scriptを作らない。Providerとcredential classが決まった時点で公式API仕様を別のimplementation sourceとして追加する。

### Mappingと限界

ATT&CK `v19.1 / T1078`は漏えいしたvalid accountの継続利用を制限する設計関係として部分割当します。
NIST SSDF `RV.2.1`はsoftware vulnerabilityのrisk response計画、OSPS `AC-04.01`はCI/CDの未指定permissionのdefaultを
対象とするため非継承です。NIST SP 800-61 Rev.3は本リポジトリのframework mappingや準拠判定には使いません。

同刊行物は特定providerのcredential失効、session invalidation、signing trust、replacement scope比較、audit retention、
安全なdenial probeを規定しません。これらは旧成果物と攻撃経路を再評価したrepository interpretationです。
本移行ではlive provider、credential、consumer、audit、response exerciseを検証していません。

<a id="ref-deployed-artifact-recovery-001"></a>

## REF-DEPLOYED-ARTIFACT-RECOVERY-001

### 役割・利用先・参照版

[PSB-GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)と
[ENG-GOV-004](../engineering/governance-operations/deployed-artifact-recovery/README.md)の設計入力です。

- NIST SP 800-218、SSDF `1.1`、2022年。[公式資料](https://csrc.nist.gov/pubs/sp/800/218/final)の`RV.1.1`と`RV.2.1`を2026-09-24に照合。固定版と限界は[SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)を使用。
- NIST SP 800-61 Rev.3、2025年4月。[公式資料](https://csrc.nist.gov/pubs/sp/800/61/r3/final)を2026-09-24に確認。Incident responseとrecoveryをrisk managementへ接続する上位ガイダンスとして利用。
- 旧成果物: [PSB-GOV-005 Deployed artifact refresh](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/deployed-artifact-refresh/README.md)。旧check・fixture・mappingの採否は[移行記録](../docs/DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md)に保持。

### 採用・変更・不採用

- 採用: Softwareとcomponentのpotential vulnerability情報を継続して収集・調査し、risk情報からremediation等を計画するSSDFの成果。RespondとRecoverを分け、復旧判断を継続的risk managementへ戻すNIST SP 800-61 Rev.3の考え方。
- 変更して採用: Exact deployed digest、artifact-bound SBOM、current evidence、distinct replacement digest、targetごとのobserved deployment、old digest非稼働を一つのcaseへ結ぶ。これは旧controlを再評価した本リポジトリの具体化。
- 不採用: 旧fixtureのsynthetic deadlineを組織SLAにしない。Signatureやfresh rebuildだけで現在安全と判断しない。Tag更新、build success、partial rolloutをclosureにしない。
- 実装判断: Builder、registry、admission、deployment platformを選定していないため、provider-neutralなverifierを作らない。具体実装時に各製品の公式contractを追加する。

### Mappingと限界

SSDF `RV.1.1`は`ARTIFACT-RECOVERY-2`、`RV.2.1`は`ARTIFACT-RECOVERY-3`だけへ部分割当します。
ATT&CK `T1195.002`はcompromised application softwareの残存を減らすrebuild・replacementとの設計関係です。
OSPS `DO-04.01`はreleaseごとのsupport scope・durationをproject documentationへ記載する要件であり、
support evidenceを消費する本controlの実行成果ではないため非継承です。

これらの資料はclean rebuildの具体条件、provenance生成、registry publication、admission、全deploymentの観測、old digest removalを
単独では定義しません。Provenance生成は`PSB-BUILD-003`、registry publicationは`PSB-CONTAINER-002`、artifactの使用許可は`PSB-CONTAINER-001`へ分離し、live provider／admissionは未実装です。End-to-end recoveryは未検証です。

<a id="ref-vulnerability-priority-001"></a>

## REF-VULNERABILITY-PRIORITY-001

[PSB-GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)と
[ENG-GOV-005](../engineering/governance-operations/vulnerability-priority-decision/README.md)の設計入力です。

- NIST SP 800-218、SSDF `1.1`の`RV.1.1`・`RV.2.1`。固定版は[SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)。2026-09-24に公式本文を照合。
- CISA [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)と公式JSON・CSV・JSON Schema。継続更新data sourceであり、2026-09-24に公式pageがprioritization inputと説明することを確認。Snapshotの時刻・完全性・schema・digest・healthを別途必要とする。
- FIRST [CVSS v4.0 Specification Document](https://www.first.org/cvss/v4.0/specification-document)、document version `1.2`。2026-09-24にBase・Threat・Environmental・Supplementalの役割を確認。
- FIRST [PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1)。2026-09-24に公式version一覧と、PSIRTの責任・service・outcomeを扱う高水準frameworkであることを確認。
- 旧成果物: [PSB-GOV-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/exploited-vulnerability-prioritization/README.md)。採否は[移行記録](../docs/VULNERABILITY_PRIORITY_MIGRATION.md)に保持。

採用するのは、credible vulnerability情報を継続収集・調査すること、risk responseを計画すること、KEV掲載・非掲載・取得不能を
分けること、CVSS metricの意味とprovenanceを保持すること、PSIRT caseへownerと次の処理を割り当てることです。
CVSSをbusiness risk・SLA・悪用予測にせず、KEV非掲載を未悪用・低riskにせず、CISA due dateを組織期限へ自動変換しません。
PSIRT frameworkの参照を組織能力の導入証拠にしません。Live feed、calculator、inventory、ticket、PSIRT運用は未検証です。

## REF-GITLEAKS-HOOKS-001

### 役割・利用先・参照版

[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)の製品仕様と取得物の記録です。
2026-09-23にGitleaks公式release API、v8.30.1のREADME・source、Git公式文書を確認しました。

- Gitleaks `v8.30.1`、release公開日時 `2026-03-21T02:17:58Z`。[同tagのLICENSE](https://github.com/gitleaks/gitleaks/blob/v8.30.1/LICENSE)はMIT License。Binaryやsourceを本repositoryへ収録せず、利用者が取得・照合する手順だけを示す。
- Linux x64 archive `gitleaks_8.30.1_linux_x64.tar.gz`：release assetのSHA-256 `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb`と取得物が一致。
- archive内の`gitleaks` binary：本PJで計算したSHA-256 `88f91962aa2f93ac6ab281d553b9e125f5197bbbce38f9f2437f7299c32e5509`。実行結果は`8.30.1`。
- Gitleaks公式：[v8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1)、[README](https://github.com/gitleaks/gitleaks/blob/v8.30.1/README.md)、[`stdin`実装](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/stdin.go)、[共通設定とtimeout・redact](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/root.go)、[file input処理](https://github.com/gitleaks/gitleaks/blob/v8.30.1/sources/file.go)、[組込み設定](https://github.com/gitleaks/gitleaks/blob/v8.30.1/config/gitleaks.toml)。
- Git公式：[githooks](https://git-scm.com/docs/githooks)、[git-receive-packのquarantine](https://git-scm.com/docs/git-receive-pack#_quarantine_environment)、[git cat-file](https://git-scm.com/docs/git-cat-file)、[git rev-list](https://git-scm.com/docs/git-rev-list)。

### 採否と限界

- 採用：固定binary、固定した組込みrule、`stdin`、完全redaction、JSON report、timeout、検出専用exit code。候補repositoryの設定・ignore・allow commentを受け入れない。
- 変更して採用：Gitleaks自身にGit履歴範囲を求めさせず、管理側adapterがGit object graphを列挙して内容を渡す。これによりローカルと受信側で同じ検査処理を使い、候補内の設定変更から分離する。
- 不採用：hook実行時のdownload、mutable tag、Docker必須化、候補repositoryの`.gitleaks.toml`・`.gitleaksignore`、無期限baseline、検出値を含むverbose出力。
- 限界：GitHub release assetのdigest照合は独立したpublisher署名ではない。組込みルールとallowlist、stdinのpath文脈欠落、scannerの解析・MIME識別、分割処理に由来する検出限界が残る。代表実装は未知形式を安全とせず拒否するが、全秘密情報の検出を保証しない。Gitleaks文書とrelease URLは可変であり、更新時は再確認する。

<a id="ref-iac-change-boundary-001"></a>

## REF-IAC-CHANGE-BOUNDARY-001

### 役割・利用先・参照時点

[PSB-IAC-001](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)、
[ENG-CONTAINER-007](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)と教材の設計入力です。
Terraform／OPAの公開仕様と、旧成果物を作る際のユーザー提供guidanceを区別します。公開URLは可変で固定digestを記録していないため、implementationを選ぶ時点で再確認が必要です。

- HashiCorp Terraform [plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)、[CLI workflow](https://developer.hashicorp.com/terraform/cli/run)、[show command](https://developer.hashicorp.com/terraform/cli/commands/show)、[JSON output format](https://developer.hashicorp.com/terraform/internals/json-format)。2026-09-25に確認。Speculative planと保存plan、保存planをapplyする経路、create／update／delete／replace、unknown・sensitive表現、JSON format versionを確認。
- HashiCorp Terraform [dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)。2026-09-25に確認。Lock fileは現在provider dependencyだけを追跡し、remote moduleのversion selectionは記録しない。Provider checksumはtrust on first use等の限界を持つ。
- HashiCorp Terraform [refresh command](https://developer.hashicorp.com/terraform/cli/commands/refresh)、[refresh-only](https://developer.hashicorp.com/terraform/tutorials/state/refresh)、[resource drift](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift)、[import](https://developer.hashicorp.com/terraform/cli/import)。2026-09-25に確認。`refresh`はdeprecatedで、review可能な`-refresh-only`が推奨される。Terraform stateへの取込みとprovider全体のresource inventoryを同じ成果にしない。
- Open Policy Agent [Terraform integration](https://www.openpolicyagent.org/docs/terraform)。2026-09-25に確認。Terraform plan JSONをpolicy inputにできる一方、unknown value、dynamic block、function evaluation等、plan時点で得られない情報がある。同tutorialの例はTerraform 0.12.6を前提とし、latestで未テストと明記されているため、現行implementationのversion根拠には使わない。
- 旧ユーザー提供資料：[IaC・CI・Policy as CodeによるGolden Path](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/docs/user-supplied-golden-path-guideline-ja.md)。提供日`2026-07-28`、提供元`repository user`、区分`user-supplied guidance`。外部標準、正式な組織policy、独立検証済み資料ではない。
- 旧成果物：[README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/README.md)、[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/control.yaml)、[verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/scripts/verify.py)。旧12項目、fixture、mappingの採否は移行記録に保持する。

### 採用・変更・不採用

- 採用：安全な既定値と狭いinterfaceを持つGolden Path、sourceよりresolved planを評価すること、保存planをapplyへ渡すこと、planのunknown・sensitive data、provider上の現在状態との照合。
- 変更して採用：Golden Pathを合格条件ではなく使いやすい入口とする。Module／provider／policy／targetをchange identityへ含め、plan decisionを保存plan・apply・receiptへ結ぶ。Provider hookは実coverageだけを記録し、driftは管理resourceと未管理resource、collection healthを分ける。
- 不採用：AWS／GCP／Azureの共通fieldを一つのJSON contractで自己申告すること、固定15分・24時間等を普遍要件にすること、reusable workflowへ他controlの`implemented`一覧を複製すること、provider側の全経路強制を文字列で宣言すること、破壊的修正をgeneric scriptへ許すこと。

### Mappingと限界

旧OpenSSF OSPS `OSPS-QA-03.01`・`OSPS-QA-04.02`・`OSPS-AC-04.01`、NIST SSDF `PW.6.1`、GitHub Secure Buildsは、IaC plan・apply・provider状態への直接要件ではないため継承しない。詳細は[旧framework mapping](../docs/IAC_CHANGE_BOUNDARY_MIGRATION.md#旧framework-mapping)に記録する。

Terraform資料はTerraform固有の挙動であり、OpenTofu、CloudFormation、Pulumi、managed IaC platformへ自動適用しません。OPA資料もpolicy engine一般の完全性や、個々のprovider schema・resource security ruleを定義しません。本移行では実plan、cloud apply、provider guardrail、inventory、drift、remediationを実行していません。
参照したWeb文書の再利用licenseは個別に確認しておらず、本repositoryには原文を収録せず要約とlinkだけを置きます。ユーザー提供資料のlicenseも未指定です。
