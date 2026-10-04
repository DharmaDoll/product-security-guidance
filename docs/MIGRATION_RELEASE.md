# Release Integrity — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [PSB-REL-005 Artifact signing generation 移行記録](#artifact-signing-migration)
- [PSB-REL-003 Release SBOM 移行記録](#release-sbom-migration)
- [PSB-REL-004 Supplier SBOM 移行記録](#supplier-sbom-migration)
- [PSB-REL-002 Provenance distribution 移行記録](#provenance-distribution-migration)

<a id="artifact-signing-migration"></a>

<a id="artifact-signing-migration--psb-rel-005-artifact-signing-generation-移行記録"></a>
## PSB-REL-005 Artifact signing generation 移行記録

<a id="artifact-signing-migration--結論"></a>
### 結論

旧`PSB-REL-005`を[Artifact signing generation](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)へ移行しました。署名対象の確定、対象の承認と署名権限、鍵の管理、署名結果の検証、公開完了、release gateを分けました。[教材](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/learning.md)、[設計pattern](../engineering/release-integrity/artifact-signing-boundary/README.md)、診断観点を追加しました。

旧verifierはOpenSSLでEd25519署名を検証し、artifactの実bytesをhashしていたため、その部分の観測価値はあります。しかし旧`generate_fixture_bundle.py`はlocal fileのprivate keyで署名し、KMS/HSM、鍵の非export性、公開先の変更不能性、透明性ログの包含、release gateの状態をJSONへ書いていました。旧verifierの`PASS`はその主張をlive providerで確認していません。独自statementと合成receiptを新しいrelease signing実装として移植しません。

<a id="artifact-signing-migration--移行元"></a>
### 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/scripts/verify.py)
- [旧fixture generator](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/scripts/generate_fixture_bundle.py)

<a id="artifact-signing-migration--旧checkの再配置"></a>
### 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `ASG-001` exact release artifact | `ART-SIGN-1` | 実bytes/digestの固定を保持。Git tag・full revisionを全artifactへ一律要求しない |
| `ASG-002` short-lived authorization | `ART-SIGN-2` | 対象と操作を限定。固定5分、nonce形式、OIDC audienceを全方式の普遍要件にしない |
| `ASG-003` signer state | `ART-SIGN-3` | 鍵・identityの保護と状態確認を保持。非exportable KMS/HSM/keylessという固定列挙は方式の選択肢にする |
| `ASG-004` signed statement | `ART-SIGN-1・4` | 対象と承認の結合を保持。独自statement envelopeを標準としない。自己申告の署名時刻をtrusted timestampとしない |
| `ASG-005` signature validity | `ART-SIGN-4` | 採用形式とconsumer信頼根拠で実暗号検証する。Ed25519と固定公開鍵digestは限定profileの選択 |
| `ASG-006` publication / transparency | `ART-SIGN-5` | exact artifactから署名を取得できることを保持。HTTPS、透明性ログ、公開形式は選択したprofileに従う |
| `ASG-007` release gate | `ART-SIGN-6` | 必要な署名・検証・公開が揃わないreleaseを止める。fixtureの`BLOCK`値を実gateの証拠にしない |
| `ASG-008` minimal evidence / errors | `ART-SIGN-6・7` | 秘密情報を複製せず、評価不能を成功にしない |

<a id="artifact-signing-migration--主題ごとの具体化判断"></a>
### 主題ごとの具体化判断

今回必要な成果物は、provider-neutralなcontrol、教材、実装判断に使うpattern、診断観点、参照資料、mappingです。具体実装は作りません。署名対象をfileとOCI manifestのどちらにするか、signer、release承認の強制点、公開先、consumerの信頼条件が未選定だからです。旧local cryptographyだけを移してもsigner custody、対象認可、公開、release gateは実証できません。

2026-09-28の読み合わせでも文書と診断項目で完了とし、実装例の不在は残作業にしません。採用先で導入・確認に役立つ場合の前提と完了条件は[pattern](../engineering/release-integrity/artifact-signing-boundary/README.md#具体化判断)へ記載しました。Sigstore/Cosignの公式`sign-blob`/`verify-blob`は採用候補として明記し、特定方式への実装済み・導入済みという主張はしません。

<a id="artifact-signing-migration--参照資料とmapping"></a>
### 参照資料とmapping

旧`REF-REL-003`は[新しい役割別記録](../sources/README.md#ref-artifact-signing-boundary-001)へ再編集しました。2026-09-26にSigstoreのblob署名、検証、binary取得・検証の公式文書とNIST SSDF 1.1 `PS.2.1`を確認しました。Cosign固有のbundle、certificate identity、透明性証拠を、全方式に必須のフィールドへ変換しません。

NIST SSDF 1.1 `PS.2.1`は署名を含むsoftware integrity verification informationを取得者へ提供する課題です。`ART-SIGN-4・5・6`を`supports / medium / design-reviewed`で部分割当します。旧`high` confidenceは実公開が未確認のため継承しません。旧OpenSSF `OSPS-BR-06.01`、`OSPS-AC-04.01`、ATT&CK `T1553.002`は、今回その正確な版と要件本文で再照合していないため新しいmappingへ継承しません。脅威との関連をframework準拠や防御完了とは扱いません。[SLSA Build Track Basics 1.2](https://slsa.dev/spec/v1.2/build-track-basics)を2026-09-26に再確認し、Build L2が署名を要求する対象はprovenanceであって、独立したartifact signing要件ではないため、本controlをSLSA Build levelへ割り当てません。

<a id="artifact-signing-migration--完了範囲と残る作業"></a>
### 完了範囲と残る作業

7特性のcontrol、教材、pattern、診断観点、参照資料、framework・成果物・横断mappingを追加しました。実signer、key policy、署名・公開・取得、gateの拒否は未実施です。次の移行候補は旧`PSB-BUILD-002`のHosted consistent buildとし、builderの承認、一貫したbuild定義、利用者が変更できる範囲を選別します。

<a id="release-sbom-migration"></a>

<a id="release-sbom-migration--psb-rel-003-release-sbom-移行記録"></a>
## PSB-REL-003 Release SBOM 移行記録

<a id="release-sbom-migration--結論"></a>
### 結論

旧`PSB-REL-003`を[Release SBOM identity and analysis boundary](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)へ移行しました。Source・build・deployment／operationsの観測を別identityで保持し、final artifactを観測したSBOMをexact artifact digestへ結び、format・relationship・coverage、公開、analysis intake、処理health、稼働影響調査への受け渡しを分けます。

旧実装で実値を検査していたartifact／SBOM digest bindingは、[CycloneDX 1.7限定実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)として作り直しました。StorageやDependency-Trackの状態をJSON fieldで自己申告していた部分は移植せず、対象製品のlive evidenceが必要な境界として残しました。

<a id="release-sbom-migration--移行元"></a>
### 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/scripts/verify.py)
- [利用者提供SBOM lifecycle資料](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)

<a id="release-sbom-migration--旧checkの再配置"></a>
### 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `SBM-001` CycloneDX identity | `SBOM-REL-3` | Format・version、document identity、component identity、参照整合性へ再編集。CycloneDXの全利用者へPURLを一律要求せず、限定実装のrelease contractではversion付きPURLを要求 |
| `SBM-002` exact artifact binding | `SBOM-REL-2` | 実artifact bytesとSBOM root hash、SBOM digest・serial・versionの結合を保持。限定実装で実値を確認 |
| `SBM-003` complete graph | `SBOM-REL-3・4` | Relationship consistencyとcoverage claimを分離。`aggregate: complete`の存在だけを完全性の証明にしない |
| `SBM-004` publication | `SBOM-REL-5` | Immutable identity、consumer retrieval、retention、no downgradeを保持。固定5分・365日・public HTTPSを普遍要件から外す |
| `SBM-005` Dependency-Track upload | `SBOM-REL-6` | Exact targetと最小権限をprovider-neutralな成果へ変更。旧4.14.3 fixtureを現在のlive adapterとして移植しない |
| `SBM-006` processing completion | `SBOM-REL-7` | Transport受付、validation、ingestion、analysis完了を分離。Digest・serial・projectへ結ぶ考えを保持 |
| `SBM-007` sanitized／fresh evidence | `SBOM-REL-6・7` | 値の最小化とdata healthを保持。固定24時間を全data sourceの普遍値にしない |
| `SBM-008` lifecycle timing | `SBOM-REL-1` | Source・build・deployment observationを保持。全productへPR、push、継続refreshという固定triggerを要求せず、phaseと責任で表す |
| `SBM-009` catalog identity | `SBOM-REL-1・8` | Observationを上書きせず、commit、artifact digest、deployment identityを関係として保持 |

<a id="release-sbom-migration--具体化判断"></a>
### 具体化判断

この主題では、final artifact bytesとCycloneDX文書の結合は技術経路と観測可能な失敗が明確です。文章だけでは、source SBOMの誤用、artifact差替え、dangling reference、composition stateの扱いを各利用者が再発明するため、Python標準libraryだけの限定実装を必要な成果物に選びました。

実装が確認するのは次の範囲です。

- CycloneDX 1.7 JSON、document serial・version。
- 文書に記載された`build`／`post-build` phase。実際の生成経路や観測対象までは確認しない。
- 実artifact SHA-256とroot component hashの一致。
- Root・最上位componentのversion付きPURL、`bom-ref`の一意性、それらへのdependency・composition参照の解決。入れ子のcomponent、service、外部BOMの参照は対象外。
- Root assemblyの明示されたcomposition state。`unknown`を拒否または`complete`へ変換せず出力。
- Malformed inputを`ERROR`とし、artifact内容をerrorへ表示しない。

実装しないのは、CycloneDX JSON Schema全体、generator coverageの証明、SBOM authentication、storage publication、consumer retrieval、Dependency-Track、advisory data、deployment catalogです。採用先でこれらを確認する方法を選びます。既存の製品連携で足りるかも含め、追加実装は導入・確認に役立つ場合だけ選びます。

<a id="release-sbom-migration--旧実装をそのまま移さない理由"></a>
### 旧実装をそのまま移さない理由

旧verifierのartifact SHA-256とSBOM root hash、SBOM bytes digestの計算は観測可能な性質でした。この部分は新しい小さな実装へ残しました。

一方、次はfixtureの自己申告値を比較しており、実効性を示しませんでした。

- `immutable: true`、HTTPS URL、retention日数、公開時刻によるstorage状態。
- API key source、permission配列、`auto_create: false`によるDependency-Track実権限。
- 手書きreceiptの`BOM_PROCESSED`、analyzer health、vulnerability data freshness。
- Source・build・deployment observationを列挙したpolicy JSONによるcollector実行状態。

これらを同じ汎用verifierへ戻すと、実際には接続していないstorageやanalysis platformを実装済みに見せます。Live adapterは、採用releaseのOpenAPI、permission、notification、project ACL、data source healthを取得し、正常、拒否、validation failure、processing failure、timeout、stale、partial resultを実環境で確認する必要があります。

<a id="release-sbom-migration--参照仕様の再確認"></a>
### 参照仕様の再確認

2026-09-25にCycloneDX 1.7 JSON reference、公式schema、lifecycle phase、component compositionを確認しました。同梱する正常例は固定commitの公式JSON Schemaで検証しました。Lifecycleは観測時点を表し、compositionはinventory／relationshipのcomplete・incomplete・unknown等を明示する仕組みです。本リポジトリでは、これらのfieldをcoverageの自動証明にしません。

利用者提供のlifecycle資料は、sourceのPR・push、build後の完成物、deployment・稼働中という取得地点を選ぶ重要な入力でした。これを[設計patternの取得地点](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md#1-observationを分ける)へ明示しました。資料の「buildが最も重要」は、releaseの正本をfinal artifactへ結ぶ判断として採用し、全製品で固定trigger・完全coverage・runtime memoryの完全観測を保証する意味にはしません。Supplier提供SBOMの署名・受入れはREL-004へ分けます。

Dependency-Trackの4.14系公式documentationで、`BOM_CONSUMED`、`BOM_PROCESSED`、`BOM_PROCESSING_FAILED`、`BOM_VALIDATION_FAILED`と、`BOM_UPLOAD`・`PROJECT_CREATION_UPLOAD`等の権限の違いを再確認しました。旧4.14.3 adapter記録は設計入力として保持しますが、live 4.14.3 deploymentや現在推奨版を意味しません。

<a id="release-sbom-migration--2026-09-28の読み合わせ"></a>
#### 2026-09-28の読み合わせ

利用者提供資料は上記固定commitの原文をローカルの旧repositoryで読み直しました。教材をソース・完成物・稼働環境の三地点から辿る説明へ改め、共通base imageや供給者のSBOMを最終製品全体の一覧と取り違えない判断を補いました。

Dependency-Track 4.14.3のソースで、`BOM_PROCESSED`の通知後に後続分析イベントが配送されることを確認しました。設計の`PROCESSED`を取込完了と分析完了に分けています。参照版、根拠、採否は[参照資料記録](../sources/README.md#ref-release-sbom-lifecycle-001)を正本とします。

限定実装はphaseとhashの申告を照合するもので、完成物からの生成を証明しません。READMEにその境界と最短導入手順を補い、既存9テストをPython 3.13.5で確認しました。空白を含むパスの使い捨てrepositoryへのコピー、正常例、再配置時の上書き防止、repository直下以外への配置拒否、成果物変更時の終了コード1、入力不足時の終了コード2も確認しました。実際の生成ツールや分析サービスは呼び出していません。実装・テストコードは変更していません。

<a id="release-sbom-migration--2026-10-04の導入手順再確認"></a>
#### 2026-10-04の導入手順再確認

使い捨てrepositoryへ限定scriptをcopyし、同梱のartifactとSBOMで`PASS/0`、artifact変更で`REJECT/1`、artifact欠落で`ERROR/2`、copy解除を確認しました。既存9テストはPython 3.13.5で通過しています。導入先の`tools`や`tools/sbom`がsymlinkならcopyを止める条件と、手元の試行を解除する一ファイル限定の手順をREADMEへ補いました。実SBOM generator、schema validator、公開、Dependency-Track、deployment catalogを接続した結果ではありません。

<a id="release-sbom-migration--framework-mapping"></a>
### Framework mapping

- NIST SSDF 1.1 `PS.3.2`を`SBOM-REL-1〜5・8`へ`supports / medium / design-reviewed`で追加します。Releaseごとのcomponent・dependency provenance dataを収集・維持・共有するtaskを、observation identity、artifact binding、coverage、publication、deployment relationが部分的に支援します。SBOMは一つの実現方式であり、SSDF準拠や完全なprovenance collectionは主張しません。
- NIST SSDF 1.1 `RV.1.1`を`SBOM-REL-6〜8`へ`supports / medium / design-reviewed`で追加します。Exact inventoryのanalysis intakeとhealth、deployment relationはcomponent vulnerability情報の継続調査を支援しますが、vulnerability情報の収集、適用性判断、responseをこのcontrolが完了するわけではありません。
- 旧`PS.3.1 / supports / high`は、release archive全体の成果をこのcontrolだけで満たすように見えるため継承しません。Archive protectionを実装・評価する別の成果物が必要です。

<a id="release-sbom-migration--完了範囲と残る作業"></a>
### 完了範囲と残る作業

完了したものは、8特性のcontrol、教材、設計pattern、CycloneDX限定実装と9 test、診断観点、参照資料、2件のframework mapping、成果物mapping、横断分析です。

未実施なのは、実SBOM generator、公式schema validatorの導入、実artifact typeでのcoverage評価、release storage、intended-consumer retrieval、live Dependency-Track、advisory data health、deployment catalogです。次の主題は旧`PSB-REL-004`のsupplier SBOM trustを、supplier identity、署名、対象artifact、失効状態、quarantine、受入判断から選別します。

<a id="supplier-sbom-migration"></a>

<a id="supplier-sbom-migration--psb-rel-004-supplier-sbom-移行記録"></a>
## PSB-REL-004 Supplier SBOM 移行記録

<a id="supplier-sbom-migration--結論"></a>
### 結論

旧`PSB-REL-004`を[Supplier SBOM intake trust](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)へ移行しました。供給者から受け取ったSBOMを通常の部品台帳へ入れる前に、利用者側の期待値、出所と内容、対象製品・成果物、形式と欠落、隔離と評価不能、訂正・撤回、取込先を判断します。[設計パターン](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)と教材、診断観点を作りました。

旧実装の合成Ed25519 envelopeは移植していません。暗号計算とbytes照合は実際に行いますが、独自envelope、手書きの署名者状態、JSONで自己申告する台帳権限では、実際の供給者からの受入れを示せません。署名方式と供給者を選ばない段階で独自形式を標準経路にしない判断です。

旧envelopeの`signed_at`は署名対象に含まれる自己申告時刻であり、それだけで署名がその時刻に行われた証拠にはなりません。旧test用の`--as-of`とstatus snapshotも現在の失効状態を証明しません。時刻・失効の判断には、採用する方式の検証可能な証拠と信頼した状態sourceが必要です。

<a id="supplier-sbom-migration--移行元"></a>
### 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/scripts/verify.py)
- [利用者提供のSBOM lifecycle資料](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)

<a id="supplier-sbom-migration--旧checkの再配置"></a>
### 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `SUP-001` 署名者の認証 | `SUP-INTAKE-1・2` | 利用者側の信頼根拠と出所確認を保持。Ed25519だけを全供給者の唯一方式にしない |
| `SUP-002` 製品と成果物の同一性 | `SUP-INTAKE-3` | 署名付きでも別製品を拒否する成果を保持。SBOMと実成果物のdigest関係を認証された情報で確かめる |
| `SUP-003` CycloneDX構造 | `SUP-INTAKE-4` | 対応形式・版と参照関係を検証。形式の成功を網羅性にしない |
| `SUP-004` 署名者の有効状態 | `SUP-INTAKE-2・6` | 時刻・失効・交代を採用方式ごとに評価。現在の期限だけで過去の署名を一律に決めない |
| `SUP-005` 隔離 | `SUP-INTAKE-5` | 不一致と評価不能を分け、どちらも通常取込を止める |
| `SUP-006` 取込権限 | `SUP-INTAKE-7` | 正確な取込先と必要な操作だけを許す。JSONの許可一覧では実権限を証明しない |
| `SUP-007` 証拠の最小化 | `SUP-INTAKE-7` | 判断に必要な値だけを残す。供給者の非公開inventoryをログへ複製しない |
| `SUP-008` 検証障害 | `SUP-INTAKE-5` | 暗号検証器・状態取得の失敗を受入成功にしない |

<a id="supplier-sbom-migration--主題ごとの具体化判断"></a>
### 主題ごとの具体化判断

読者が今できるべき判断は、受渡し方式、利用者側の期待値、署名者または配送元の信頼根拠、成果物との結び方、通常台帳へ渡す条件の選択です。供給者と方式を選ばずに具体実装を置くと、旧fixtureと同じ独自envelopeを正解に見せます。そのため今回はcontrol、教材、pattern、診断観点、参照資料、mappingを必要な成果物とし、実装例は作りません。

2026-09-28の読み合わせでも、文書と診断項目で今回の範囲は完了としました。実装例の不在は残作業にしません。供給者と対象製品・成果物、署名または認証済み配送方式、利用者側の信頼根拠、時刻・失効・訂正のsource、使い捨ての台帳取込先が決まり、導入・確認に役立つ場合だけ限定実装を検討します。選んだ場合は、検証したbytesの使用、正常な受入候補、別製品・改変・未知署名者の隔離、状態取得・検証器障害、通常台帳への迂回拒否を観測します。固定公開鍵だけの暗号テストを、供給者受入れの完了とはしません。

教材からcontrolと設計へ戻るリンク、共通base imageのSBOMと最終製品の一覧を区別する説明も補いました。利用者提供資料の再確認と採否は[参照資料記録](../sources/README.md#ref-release-sbom-lifecycle-001)に保持します。

<a id="supplier-sbom-migration--参照資料と境界"></a>
### 参照資料と境界

2026-09-25にCISAのSBOM consumption資料、CycloneDX 1.7、Sigstore bundleの公式文書、NIST SSDF 1.1を確認しました。CISA資料はSBOMの出所・完全性を配送方法も含めて確認し、不一致を取込前に解消する判断を支えます。署名は一つの方式であり、すべての供給者へ同じ方式を要求する根拠にはしません。採否と限界は[REF-SUPPLIER-SBOM-INTAKE-001](../sources/README.md#ref-supplier-sbom-intake-001)に保持します。

[REL-003](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)のCycloneDX限定実装は自組織のfinal artifactとbuild／post-build SBOMを結ぶものです。供給者から受け取った署名の身元や調達対象を判定する道具として再利用しません。[REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)の成果物使用判断とも別です。

<a id="supplier-sbom-migration--framework-mapping"></a>
### Framework mapping

NIST SSDF 1.1 `PW.4.1`を`SUP-INTAKE-1〜4・6`へ`supports / medium / design-reviewed`で部分割当します。第三者componentの出所情報を取得・維持し、採用リスクの評価へ渡す一部を支援します。供給者製品やcomponentの安全性、採用審査全体、準拠は主張しません。

旧`RV.1.1`は継承しません。潜在的な脆弱性情報の収集・調査は本controlの直接の成果ではなく、REL-003の分析やGOV-001の影響調査へ渡す仕事です。

<a id="supplier-sbom-migration--完了範囲と残る作業"></a>
### 完了範囲と残る作業

7特性のcontrol、教材、設計pattern、診断観点、参照資料、framework・成果物・横断mappingを追加しました。旧実装の暗号テストが成功していたことと、供給者の認証・失効・通常台帳での隔離が実証されたことを区別しています。実供給者、実署名・配送方式、状態source、台帳取込を使う実装と評価は未実施です。次の移行候補は旧`PSB-REL-005`のartifact signing generationです。

<a id="provenance-distribution-migration"></a>

<a id="provenance-distribution-migration--psb-rel-002-provenance-distribution-移行記録"></a>
## PSB-REL-002 Provenance distribution 移行記録

<a id="provenance-distribution-migration--結論"></a>
### 結論

旧`PSB-REL-002`を[Provenance distribution and availability boundary](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)へ移行しました。Producerがprovenanceを生成した事実ではなく、intended consumerが取得したexact artifactから対応する一つ以上のprovenanceを発見・取得し続けられることを扱います。

旧成果物の一対一固定、public HTTPS、5分、365日は普遍要件として継承しません。SLSA v1.2のartifact-level binding、一artifactから複数attestationを扱える関係、publish時の同伴、複数配布場所、immutabilityを基に、scope、relation、publication completion、consumer access、immutability、retention、no downgradeの7特性へ再編集しました。

<a id="provenance-distribution-migration--移行元"></a>
### 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/scripts/verify.py)

<a id="provenance-distribution-migration--旧5項目の扱い"></a>
### 旧5項目の扱い

| 旧項目 | 移行先 | 判断 |
|---|---|---|
| `RPD-001` 一artifact・一provenance | `PROV-DIST-1`・`2` | 変更して採用。Artifact digest bindingを保持し、一artifactから一つ以上のattestationへたどれる構造へ変更 |
| `RPD-002` immutable・authenticated・discoverable・accessible | `PROV-DIST-2`・`4`・`5` | 採用。Exact host、public、HTTPS、同一pathという旧fixture固有条件は方式へ移す |
| `RPD-003` 5分以内・365日保持 | `PROV-DIST-3`・`6` | 変更して採用。固定値を外し、release completionとartifactのconsumption・support・investigation windowへ結ぶ |
| `RPD-004` protected family no downgrade | `PROV-DIST-7` | 採用。Policy flagだけでなくartifact／relation inventoryとconsumer retrievalを確認する |
| `RPD-005` verification failureはERROR | `PROV-DIST-7` | 採用。Pagination、scope、stale observation、access、replica、parser等の失敗を分ける |

<a id="provenance-distribution-migration--旧実装を移さない理由"></a>
### 旧実装を移さない理由

旧`verify.py`はnetwork、release API、object storage、registry、TLS、consumer clientへ接続せず、fixture内の次のfieldを比較していました。

- `immutable: true`、`available: true`、`authentication: tls-server-authenticated`
- `access: public`と固定host・path
- Artifact・provenanceのsynthetic digestとtimestamp
- 5分、365日、protected familyのBoolean
- `publication_probe.source: release-api`という自己申告

これはmanifest schemaのtestにはなりますが、object上書き、consumer authorization、registry relation、replication、cache、garbage collection、retention、withdrawal、実取得を確認しません。また一artifactにつきprovenance digestを一つだけ許し、SLSAが推奨するartifactからattestationへの一対多を表せません。

対象ecosystemを選ばないままfield名を変えても同じ問題が残るため、Python verifier、secure／insecure JSON、expected output、固定値を移植しません。2026-09-28の読み合わせで、文書と診断項目を今回の完了範囲とし、実装例の不在は残作業にしない判断へ更新しました。導入・確認に役立つ場合だけ、[patternの開始条件](../engineering/release-integrity/provenance-distribution-and-availability/README.md#実装を作る開始条件)に沿って限定実装を検討します。

<a id="provenance-distribution-migration--framework-mapping"></a>
### Framework mapping

SLSA v1.2のproducer `Distribute provenance`は、producerがartifact consumerへprovenanceを配布し、対応できるpackage ecosystemへ委譲できる要件です。`PROV-DIST-1`〜`7`はその配布境界を具体化するため、旧`verifies / high`を`supports / medium / design-reviewed`へ変更します。SLSA Build L1以上の達成やproducer・platform・consumer全体の評価は主張しません。

NIST SSDF `PS.2.1`はsoftware acquirerがsoftware releaseのintegrityを検証できる情報を利用可能にするtaskです。Provenanceのartifact binding、consumer access、retentionは一つの実現方法なので、旧`supports / high`を`supports / medium / design-reviewed`へ変更します。SSDF全体への準拠、signature生成、acquirer側の実検証は別です。

<a id="provenance-distribution-migration--完了範囲と残る作業"></a>
### 完了範囲と残る作業

完了したものは、7特性のcontrol、複数artifactの具体的な教材、artifact digestからconsumer retrievalまでのpattern、診断観点、参照資料、2件のframework mapping、成果物mapping、横断分析です。

未実施なのは、registry／release service、artifact、attestation format、producer／consumer identity、retention policyの選定とlive upload・retrieval・deletion・downgrade確認です。実装時には正常公開だけでなく、artifact追加、複数attestation、部分公開、consumer access拒否、上書き、削除、stale index、probe failureを実serviceで確認します。
