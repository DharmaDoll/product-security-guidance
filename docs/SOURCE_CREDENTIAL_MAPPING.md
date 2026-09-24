# Source credential lifecycle framework reconciliation

2026-09-23から24日にかけて、[PSB-SOURCE-004 Source credential lifecycle](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)の
framework対応を、公式本文と旧記録に照らして再評価しました。

移行元は`product-security-controls@91fdb7661b38723ce6fb38da93cf3c68b701e521`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/source-access-credential-lifecycle/control.yaml)です。
旧記録の削除や意味の書換えは行わず、この文書に履歴として保持します。

## SSDFの結論

旧`PS.3.1`対応は継承しません。NIST SP 800-218の`PS.3.1`は、リリースごとに保持すべきファイル、
完全性検証情報、provenanceを安全にarchiveする要件です。SOURCE-004の認証情報とセッションの
発行・範囲・保管・棚卸し・失効・監査とは、対象資産、目的、強制点が異なります。

SOURCE-004に近い要件は`PS.1.1`です。これはsource、executable、configuration-as-codeを最小権限で保管し、
許可した人・tool・serviceだけにアクセスさせることを扱います。SRC-AUTH-1〜6は、そのアクセス境界を成立・維持する
認証情報ライフサイクルとして`PS.1.1`を部分的に支援します。この関係を`design-reviewed / medium`で新規に記録します。

これは番号の機械的な置換ではありません。`PS.3.1`との旧関係を非継承とし、別の原文との関係を独立して評価した結果です。
SOURCE-004だけでは、すべてのcodeの保管、repositoryの変更保護、code owner review、commit signing、実環境の最小権限を
実現または証明しません。

## 残る8件の結論

2026-09-24に、GitHubの固定commitにある4文書、Enterprise ATT&CK v19.1の固定STIX、
OSPS Baseline 2026.02.19の版付き本文を確認しました。7件を`design-reviewed`へ移し、意味が広すぎた
property割当とconfidenceを次のように修正しました。

| Mapping | 現行の割当 | 判断 |
|---|---|---|
| `GHSC-SECURE-ACCOUNTS` | `SRC-AUTH-2,4,5`／`supports`／`medium` | SSO・2FA、SSH秘密鍵保護・短命証明書、SCIMによる失効を部分的に支援。旧割当のscope、workload ID、auditは本文が直接扱わない |
| `GH-ADMIN-CREDENTIAL-TYPES` | `SRC-AUTH-1,3,5`／`supports`／`medium` | 認証情報とuser・installation・repository・workflowの対応、存続期間、失効手段を選択判断に使う。保管やaudit要件ではないため旧`high`を維持しない |
| `GH-ADMIN-SAML-IAM` | `SRC-AUTH-5`／`supports`／`medium` | SAML identity、session、authorized credentialの表示・失効を支援。SAML自体をphishing-resistant MFAと解釈せず、旧`SRC-AUTH-2`割当を外す |
| `GH-ADMIN-SCIM-ORGANIZATIONS` | `SRC-AUTH-5`／`supports`／`medium` | Organization membershipのprovisioning・deprovisioningを支援。すべてのcredentialとsessionの失効を保証しない |
| `T1078` | `SRC-AUTH-1..5`／`mitigates`／`medium` | 権限の重複、休眠account、盗まれた有効なcredentialの悪用可能性と期間を減らす部分的関係 |
| `T1552.001` | `SRC-AUTH-4`／`mitigates`／`medium` | File内に回収可能なtoken・private keyを残さない境界との直接関係。memory、process、password store全体には拡張しない |
| `OSPS-AC-01.01` | `SRC-AUTH-2`／`supports`／`medium` | OSPSは機微なrepository resourceのreadまたはmodify時のMFAを要求する。SOURCE-004はcredential発行・機微変更だけを扱うため部分対応とし、旧`high`を維持しない |
| `ASI03` | 旧割当を保留 | 公式landing pageとPDFのmedia metadataまでは確認。公式PDFの自動取得がHTTP 403で拒否され、ASI03本文を再確認できていないため`migration-review-required`を維持 |

GitHubの製品文書は、SOURCE-004の製品非依存な特性を定義する根拠ではありません。固定版の製品挙動と
実装選択の対応を示す資料です。ATT&CKとAgentic Top 10は脅威分類であり、合格条件や準拠要件ではありません。
OSPSとの関係も、要件全体への対応やプロジェクトの成熟度を示しません。

## セキュリティ特性ごとの判断

| SOURCE-004特性 | PS.3.1 | PS.1.1との関係 | 限界 |
|---|---|---|---|
| SRC-AUTH-1 | 非継承 | 主体・resource・operation・期限への権限結合が、code accessの最小権限を直接支援 | Repository側の権限モデルと実効設定は別に必要 |
| SRC-AUTH-2 | 非継承 | 発行・機微変更時の強固な認証が、許可主体以外による権限取得を減らす | PS.1.1自体が特定の認証方式を要求するとは解釈しない |
| SRC-AUTH-3 | 非継承 | task限定のworkload IDが、許可したtool・serviceだけにaccessを与える設計を支援 | Workload federation条件と実行後の操作認可は別の境界 |
| SRC-AUTH-4 | 非継承 | 認証情報の保護とconsumer限定の受渡しが、repository access境界の迂回を減らす | Code storage自体の完全性・可用性・機密性を保証しない |
| SRC-AUTH-5 | 非継承 | 棚卸しと失効が、現在必要な主体だけにaccessを維持する | 失効処理と関連sessionの実効性は実環境の証拠が必要 |
| SRC-AUTH-6 | 非継承 | 所有者・resourceに結び付く監査が、version controlのaccountabilityを支援 | 変更内容のレビューや全変更の追跡を単独では保証しない |

全特性を`PS.1.1`へ対応させるのは、各特性が同じ強さでSSDFを実装するという意味ではありません。
認証情報ライフサイクルが、許可された主体だけにcode accessを限定する一つの下位設計である、という部分的な関係です。

## PS.3.1を引き継ぐ先

現行ポートフォリオには、release filesと関連するintegrity・provenance dataのarchiveを一体で扱うcontrolはありません。
[PSB-REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)は、consumerが使用前に
artifactと署名・provenanceを照合する境界であり、producerによるrelease保存の要件ではありません。
したがって`PS.3.1`をPSB-REL-001へ移し替えず、release preservationの空白として残します。

## 旧記録

次は現在のmappingではありません。旧版、関係、confidence、根拠、対象check、reviewer、review日をそのまま保持します。

```yaml
framework: nist-ssdf
version: 1.1 (SP 800-218, 2022)
id: PS.3.1
relationship: supports
confidence: medium
rationale: Controlled development credentials and protected access to repositories
  support protection of code from unauthorized access and modification.
reviewer: product-security
review_date: '2026-08-05'
applies_to:
- SCL-001
- SCL-002
- SCL-003
- SCL-004
- SCL-005
- SCL-006
- SCL-007
- SCL-008
- SCL-009
- SCL-010
- SCL-011
- SCL-012
- SCL-013
- SCL-014
- SCL-015
- SCL-016
- SCL-017
```

残る8件の旧記録は次のとおりです。`SCL-*`は移行元の個別checkであり、現行の`SRC-AUTH-*`と同じ粒度ではありません。
この表は比較用の要約で、文字単位の旧正本は上記の固定commitに残します。旧mappingの`relationship`、`confidence`、
対象check、reviewer、review日と根拠の意味を保持し、現行判断との差を追跡します。

| ID | 旧relationship／confidence | 旧対象check | 旧review | 旧根拠 |
|---|---|---|---|---|
| `GHSC-SECURE-ACCOUNTS` | `supports / medium` | `SCL-001..017` | `product-security / 2026-08-05` | Credential selection、phishing-resistant authentication、protected storage、review、revocationがsecure GitHub account useを支援する |
| `GH-ADMIN-CREDENTIAL-TYPES` | `supports / high` | `SCL-001,002,003,004,005,008,009,010,011,013,014,015` | `product-security / 2026-08-14` | Provider taxonomyによりuser・App・workflow・SSH credentialのidentity、lifetime、SSO authorization、storage、review、revocationを区別する |
| `GH-ADMIN-SAML-IAM` | `supports / medium` | `SCL-007,009,010,013,014` | `product-security / 2026-08-14` | SAML authenticationとcredential authorizationがsource access boundaryを支援する |
| `GH-ADMIN-SCIM-ORGANIZATIONS` | `supports / medium` | `SCL-009,010` | `product-security / 2026-08-14` | SCIM membership removalがoffboardingとaccess reviewを支援する |
| `T1078` | `mitigates / medium` | `SCL-001,002,003,004,005,007,008,009,010,013,014,015,016` | `product-security / 2026-08-05` | Least privilege、bounded lifetime、review、revocationによりstolen valid credentialのpersistとimpactを減らす |
| `T1552.001` | `mitigates / medium` | `SCL-006,008,015` | `product-security / 2026-08-05` | Credential helper、hardware protection、credential-free configurationによりfile内のtoken・private keyを減らす |
| `OSPS-AC-01.01` | `supports / high` | `SCL-007` | `product-security / 2026-08-05` | Phishing-resistant MFAとcentralized authenticationがsensitive project actionへのMFAを支援する |
| `ASI03` | `mitigates / high` | `SCL-013,014,015,016,017` | `product-security / 2026-08-05` | OAuth優先、限定PAT fallback、child-only delivery、read-only tool surfaceによりidentity・delegated privilege abuseを減らす |

## 根拠と状態

- [NIST SP 800-218公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の`PS.1.1`（PDF p.17、印刷ページ9）と`PS.3.1`（PDF p.18、印刷ページ10）を2026-09-23に確認しました。
- GitHubの4文書は`github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`の本文を2026-09-24に確認しました。Credential types、SAML、SCIMのSHA-256は旧registry記録と一致し、Account securityは今回`5def696244c0bc300adf532acdb4d4a40ae0eabd0c218afbc969a028847c3e1b`を記録しました。
- Enterprise ATT&CK v19.1の公式STIXはSHA-256 `bdf1ce86a4e604214c5076d37ae4dcb322678afc528df8492e6fdc1b554f5da3`が旧registry記録と一致し、`T1078`と`T1552.001`を2026-09-24に確認しました。
- [OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19#osps-ac-0101)の`OSPS-AC-01.01`本文を2026-09-24に確認しました。
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)はlanding page、公開日、WordPress media ID `52216`、PDF size `1,274,186 bytes`を確認しました。PDF本文は自動取得がHTTP 403で拒否されたため、ASI03の現行mappingをレビュー済みへ変更していません。
- 現行mappingは[frameworks.yaml](../mappings/frameworks.yaml)、参照版と採否は[Sources](../sources/README.md#spec-nist-ssdf-1-1)を正本とします。
- この照合は資料とcontrolの意味をレビューしたものです。SSDF準拠、実環境の権限制御、SOURCE-004全体の導入済み状態を示しません。
