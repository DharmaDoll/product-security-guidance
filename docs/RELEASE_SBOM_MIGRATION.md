# PSB-REL-003 Release SBOM 移行記録

## 結論

旧`PSB-REL-003`を[Release SBOM identity and analysis boundary](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)へ移行しました。Source・build・deployment／operationsの観測を別identityで保持し、final artifactを観測したSBOMをexact artifact digestへ結び、format・relationship・coverage、公開、analysis intake、処理health、稼働影響調査への受け渡しを分けます。

旧実装で実値を検査していたartifact／SBOM digest bindingは、[CycloneDX 1.7限定実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)として作り直しました。StorageやDependency-Trackの状態をJSON fieldで自己申告していた部分は移植せず、対象製品のlive evidenceが必要な境界として残しました。

## 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/scripts/verify.py)
- [利用者提供SBOM lifecycle資料](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)

## 旧checkの再配置

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

## 具体化判断

この主題では、final artifact bytesとCycloneDX文書の結合は技術経路と観測可能な失敗が明確です。文章だけでは、source SBOMの誤用、artifact差替え、dangling reference、composition stateの扱いを各利用者が再発明するため、Python標準libraryだけの限定実装を必要な成果物に選びました。

実装が確認するのは次の範囲です。

- CycloneDX 1.7 JSON、document serial・version。
- `build`／`post-build` observation。
- 実artifact SHA-256とroot component hashの一致。
- Root・componentのversion付きPURL、`bom-ref`の一意性、同一SBOM内のdependency・composition参照の解決。
- Root assemblyの明示されたcomposition state。`unknown`を拒否または`complete`へ変換せず出力。
- Malformed inputを`ERROR`とし、artifact内容をerrorへ表示しない。

実装しないのは、CycloneDX JSON Schema全体、generator coverageの証明、SBOM authentication、storage publication、consumer retrieval、Dependency-Track、advisory data、deployment catalogです。これらは対象製品、版、identity、network、retention、使い捨て環境を一組で選んだ実装が必要です。

## 旧実装をそのまま移さない理由

旧verifierのartifact SHA-256とSBOM root hash、SBOM bytes digestの計算は観測可能な性質でした。この部分は新しい小さな実装へ残しました。

一方、次はfixtureの自己申告値を比較しており、実効性を示しませんでした。

- `immutable: true`、HTTPS URL、retention日数、公開時刻によるstorage状態。
- API key source、permission配列、`auto_create: false`によるDependency-Track実権限。
- 手書きreceiptの`BOM_PROCESSED`、analyzer health、vulnerability data freshness。
- Source・build・deployment observationを列挙したpolicy JSONによるcollector実行状態。

これらを同じ汎用verifierへ戻すと、実際には接続していないstorageやanalysis platformを実装済みに見せます。Live adapterは、採用releaseのOpenAPI、permission、notification、project ACL、data source healthを取得し、正常、拒否、validation failure、processing failure、timeout、stale、partial resultを実環境で確認する必要があります。

## 参照仕様の再確認

2026-09-25にCycloneDX 1.7 JSON reference、公式schema、lifecycle phase、component compositionを確認しました。同梱する正常例は固定commitの公式JSON Schemaで検証しました。Lifecycleは観測時点を表し、compositionはinventory／relationshipのcomplete・incomplete・unknown等を明示する仕組みです。本リポジトリでは、これらのfieldをcoverageの自動証明にしません。

利用者提供のlifecycle資料は、sourceのPR・push、build後の完成物、deployment・稼働中という取得地点を選ぶ重要な入力でした。これを[設計patternの取得地点](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md#1-observationを分ける)へ明示しました。資料の「buildが最も重要」は、releaseの正本をfinal artifactへ結ぶ判断として採用し、全製品で固定trigger・完全coverage・runtime memoryの完全観測を保証する意味にはしません。Supplier提供SBOMの署名・受入れはREL-004へ分けます。

Dependency-Trackの4.14系公式documentationで、`BOM_CONSUMED`、`BOM_PROCESSED`、`BOM_PROCESSING_FAILED`、`BOM_VALIDATION_FAILED`と、`BOM_UPLOAD`・`PROJECT_CREATION_UPLOAD`等の権限の違いを再確認しました。旧4.14.3 adapter記録は設計入力として保持しますが、live 4.14.3 deploymentや現在推奨版を意味しません。

## Framework mapping

- NIST SSDF 1.1 `PS.3.2`を`SBOM-REL-1〜5・8`へ`supports / medium / design-reviewed`で追加します。Releaseごとのcomponent・dependency provenance dataを収集・維持・共有するtaskを、observation identity、artifact binding、coverage、publication、deployment relationが部分的に支援します。SBOMは一つの実現方式であり、SSDF準拠や完全なprovenance collectionは主張しません。
- NIST SSDF 1.1 `RV.1.1`を`SBOM-REL-6〜8`へ`supports / medium / design-reviewed`で追加します。Exact inventoryのanalysis intakeとhealth、deployment relationはcomponent vulnerability情報の継続調査を支援しますが、vulnerability情報の収集、適用性判断、responseをこのcontrolが完了するわけではありません。
- 旧`PS.3.1 / supports / high`は、release archive全体の成果をこのcontrolだけで満たすように見えるため継承しません。Archive protectionを実装・評価する別の成果物が必要です。

## 完了範囲と残る作業

完了したものは、8特性のcontrol、教材、設計pattern、CycloneDX限定実装と9 test、診断観点、参照資料、2件のframework mapping、成果物mapping、横断分析です。

未実施なのは、実SBOM generator、公式schema validatorの導入、実artifact typeでのcoverage評価、release storage、intended-consumer retrieval、live Dependency-Track、advisory data health、deployment catalogです。次の主題は旧`PSB-REL-004`のsupplier SBOM trustを、supplier identity、署名、対象artifact、失効状態、quarantine、受入判断から選別します。
