# SOURCE-003 Public source exposure migration

移行元は`product-security-controls@91fdb7661b38723ce6fb38da93cf3c68b701e521`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/public-repository-exposure/control.yaml)と
[README](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/public-repository-exposure/README.md)です。

## 結論

旧成果物の成果は、組織に関係する公開source surfaceを攻撃者に近い視点で反復観測し、初出・変更・再出現、
期限付き判断、観測障害を区別してresponseへ渡すことです。この成果を
[PSB-SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)の6特性と
[ENG-SOURCE-004](../engineering/source-protection/public-exposure-observation-and-triage/README.md)へ再編集しました。

旧PoCが選んだGitHub Actions、Python standard library、public Search API、Gist delta、専用state branch、
sanitized JSONという具体構成は移植しません。この方式は一つの実装候補ですが、採用provider、対象surface、
認証view、state store、通知・case管理によって適切な設計が変わります。Fixture testの成功も実環境のcoverage、
通知、responseを証明しません。

この判断は、具体実装を避ける一般方針ではありません。SOURCE-002ではGit/Gitleaksの技術経路が明確で、
検査対象と拒否境界をcodeで具体化する価値が高いため代表実装を追加しました。SOURCE-003では、providerと運用を
選ぶ前に旧PoCを正本化すると、製品固有の制限と一つのstate方式がcontrolの意味へ逆流するため保留します。

## 旧checkの配置

| 旧check | 旧成果 | 現行配置 | 判断 |
|---|---|---|---|
| `MON-001` | Owned domainにanchorしたreconnaissance query | `PUBLIC-EXPOSURE-1,2` | 所有・許可したindicatorと、query identity・coverageを分けて移行 |
| `MON-002` | Public code・Issue・PR・Gistの収集とsanitization | `PUBLIC-EXPOSURE-2,3,6` | Surface coverage、値の最小化、partial collectionの失敗を分けて移行 |
| `MON-003` | Exact review stateとrecurrence通知 | `PUBLIC-EXPOSURE-4,5` | Occurrence stateとownerのtriage decisionへ抽象化して移行 |
| `MON-004` | Public search identityとstate writerの分離 | `PUBLIC-EXPOSURE-2,3,6` | GitHub workflow要件ではなく、observation view・state integrity・healthの設計へ移行 |
| `MON-005` | Browser-only reconnaissanceのhuman baseline | `PUBLIC-EXPOSURE-2,5` | 自動化できないsurfaceと人の判断をcoverage・triageへ移行。Browser GETを必須方式にしない |
| `MON-006` | Collection・state failureをcleanにしない | `PUBLIC-EXPOSURE-6` | Provider、state、通知、stale observationまで含むhealth propertyへ移行 |

## 旧実装の扱い

| 旧成果物 | 扱い | 理由 |
|---|---|---|
| `scripts/monitor-public-exposure.py` | 非移植 | GitHub providerと独自state contractを選んだPoC。現在のAPI挙動・coverage・運用への適合を未確認 |
| `secure/.github/workflows/public-exposure-monitor.yml` | 非移植 | Trusted triggerや権限分離は再利用できる設計入力だが、採用repositoryとnotificationなしでは導入結果にならない |
| `secure/domain-monitor.json`、`secure/state/findings.json` | 非移植 | Synthetic configurationとsample stateを組織のevidenceにしない |
| `insecure/domain-monitor.json` | 非移植 | 問題のある状態を表す比較fixtureをcontrol記録へ置かない。確認項目は現行controlへ移行 |
| `tests/`、`expected-results/` | 非移植 | 旧PoCのbehavior testであり、現行のprovider-neutral propertiesを検証する実装対象がまだない |
| `PUBLIC_EXPOSURE_MONITOR_POC_SPEC.md` | 要点をpatternへ移行 | Coverage、redaction、occurrence、failure semanticsは再利用。GitHub固有interfaceは旧固定commitに保持 |

将来GitHub実装を採用する場合も、旧fileをそのまま復活させません。対象GitHub API版、検索identity、
観測surface、result上限、state store、notificationの受領、retention、response ownerを確定し、
`engineering/source-protection/public-exposure-observation-and-triage/implementations/`へ新しい実装例として置きます。

## 旧framework mapping

次は現行mappingではありません。旧版、関係、confidence、対象check、根拠、reviewer、review日を履歴として保持します。

| Framework / ID | 旧relationship／confidence | 旧対象check | 旧review | 旧根拠 |
|---|---|---|---|---|
| MITRE ATT&CK v19.1 / `T1593.003` | `detects / high` | `MON-001,002,005` | `product-security / 2026-08-26` | Owned-domain searchでpublic code repository reconnaissanceを防御側から再現し、攻撃者が発見できる情報を検出する |
| MITRE ATT&CK v19.1 / `T1552.001` | `detects / medium` | `MON-002,005` | `product-security / 2026-08-26` | Domainにanchorしたpublic code・Gist検索でfile内credentialまたは周辺設定の候補を探す |
| NIST SSDF 1.1 / `RV.1.1` | `supports / medium` | `MON-001,002,003,005,006` | `product-security / 2026-08-26` | Public surfaceの反復収集、review state、browser baseline、失敗の明示が潜在的security issueの識別・確認を支援する |
| OpenSSF OSPS 2026.02.19 / `OSPS-BR-07.01` | `supports / low` | `MON-002,003,005` | `product-security / 2026-08-26` | Public fileとcollaboration contentのcredential候補監視がsecret取扱いを補助する |

2026-09-24、固定版の原文と現行6特性を再照合し、`T1593.003`だけを
`PUBLIC-EXPOSURE-1,2,4,5,6 / detects / medium / design-reviewed`として現行mappingへ追加しました。
これはpublic code repositoryから標的情報を探す攻撃経路と、同じ公開面に現れた候補を防御側が観測する設計の
部分的な関係です。攻撃者の検索行動そのものを検知する意味ではなく、旧`high` confidenceは維持しません。

次の3件は非継承です。

- `T1552.001`: Local file systemやremote file shareを含むfile内credentialの探索・取得を扱う。SOURCE-003は
  public surfaceのcandidate triageであり、secret検出を必須方式にせず、domain matchからcredentialの存在や有効性を確認しない。
- `RV.1.1`: Softwareとthird-party componentの潜在的脆弱性について、acquirer、user、public sourceから情報を集め、
  credible reportを調査するtask。SOURCE-003の主対象は、公開source surfaceにある組織情報・credential・設定の露出であり、
  software vulnerability reportの収集ではない。
- `OSPS-BR-07.01`: Version controlへのunencrypted sensitive dataの意図しない保存を防止する要件。
  事後観測とtriageだけではpreventを満たさない。この関係はSOURCE-002の公開前・受入境界に割り当て済み。

## 参照資料

- [REF-PUBLIC-SOURCE-EXPOSURE-001](../sources/README.md#ref-public-source-exposure-001)に、固定GitHub文書、採用した判断、非採用の実装、限界を記録しました。
- 旧PoCのREADMEが参照したGitHub Search、Gists、Code Search syntaxは、2026-09-24に
  `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`の固定本文で再確認しました。
- Enterprise ATT&CK v19.1の固定STIXで`T1593.003`と`T1552.001`、NIST SP 800-218公式PDFで`RV.1.1`、
  OSPS Baseline 2026.02.19で`OSPS-BR-07.01`を2026-09-24に確認しました。
- 実環境のsearch、credential、public candidate、notification、responseにはアクセスしていません。
