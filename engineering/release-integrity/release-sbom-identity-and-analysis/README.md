# ENG-REL-003: Release SBOM identity and analysis intake

## 利用場面と推奨構造

Release artifactのcomponent inventoryを作り、公開・継続analysis・稼働影響調査へ渡す設計です。SBOMを一度生成する処理ではなく、異なる観測をexact identityでつなぐ流れとして扱います。

```text
source observation -----------------------> early feedback

final artifact bytes
   |         \
   |          -> artifact SHA-256
   v
build／post-build generator
   -> schema validation
   -> component identity + relationship consistency
   -> explicit coverage／composition state
   -> SBOM digest + serial + version
   -> artifact-to-SBOM binding receipt
   -> incomplete release
         |-- immutable artifact publication
         |-- immutable SBOM publication
         `-- intended-consumer retrieval
   -> exact analysis project intake
         -> accepted -> validated -> ingested -> analyzed
         -> failed／timeout／staleはERROR
   -> artifact digest <-> deployment observation
   -> GOV-001 impact assessment
```

## 1. Observationを分ける

| どこで採取・生成するか | 何を観測するか | 主な用途 | Releaseの正本にするか |
|---|---|---|---|
| PR・push時などのsource tree | Lockfileや依存関係定義、採用を意図したcomponent。Commitへ結ぶ | 変更への早期feedback | しない。後のbuildで加わるcomponentは見えない |
| Image build・package組立の後、公開前のfinal artifact | 完成したimage・archive・binaryの実bytes、含まれるOS packageやbinary等。Artifact digestへ結ぶ | 配布物のinventory | する。ただしgeneratorが観測できた範囲に限る |
| Deployment時と稼働中の環境 | 実際に配置されたartifact digestと、環境で追加観測したcomponent。Deployment IDへ結ぶ | 稼働影響の検索 | しない。Build時の記録と別の観測としてつなぐ |

これは[利用者提供のSBOM lifecycle資料](../../../sources/README.md#ref-release-sbom-lifecycle-001)にある三つの取得地点を、release判断へ落としたものです。PR・push、image build直後、deployment・稼働中は代表例であり、全製品に固定するtriggerではありません。新しいartifactが生成・変化する箇所を洗い出し、その後のどのbytesを観測したかを決めます。

資料にはsupplierから調達時に受け取るSBOMと、platform teamが作る共通base imageのSBOMもあります。これらはfinal artifactの観測を代用しません。出所と対象digestを保って関係付け、supplierの署名・受入判断は別の境界で扱います。

同じcatalogへ入れる場合も、document identity、取得時刻、tool・version・設定、subject、authorityを保持します。Source SBOMへOS packageを後付けしてbuild SBOMに見せたり、operations observationでrelease inventoryを上書きしたりしません。稼働中のmemory上のcomponentをすべて観測できたとも仮定しません。

## 2. Final artifactから生成・結合する

SBOM generatorは対象artifactの組立後に実行し、可能ならartifact自体をscanします。Ecosystem manifest、lockfile、container filesystem、archive、native binary、static link、vendor directory、plugin、download等、artifact typeごとのsurfaceを列挙し、採用toolが観測できる範囲と除外を記録します。

Binding recordには少なくとも次を含めます。

- Artifactのimmutable identityとcryptographic digest。
- SBOM bytesのdigest、format・version、serial、document version。
- Root component identityと、artifact digestを表すhash。
- Observation phase、generator identity・version・設定identity。
- Composition／coverage claimと既知の除外。
- 生成・検証result。失敗時はreleaseを止める状態。

ArtifactとSBOMを同じworkspaceで検査しても、その後別bytesへ置き換えられればbindingは切れます。検査したdigestをpublication requestとrelease manifestへ渡し、後段で再計算します。

## 3. Format validityとcoverageを分ける

Version-pinned schema validatorでformatを検査します。その後、組織のcontractとしてroot identity、versioned PURL等のcomponent identity、`bom-ref`の一意性、dependency・assemblyの参照整合性、composition stateを確認します。

Schema validationとrelationship consistencyは自動化できます。一方、`complete`の正当性は、generator方式、対象surface、除外、build recipe、比較対象で判断します。Toolが観測しないsurfaceがあれば`incomplete`や`unknown`を保ち、警告を消すために`complete`へ変えません。

## 4. ArtifactとSBOMを一緒に公開する

ArtifactとSBOMが別APIで公開されるなら、両方とbinding relationがintended consumerから取得可能になるまでreleaseを`preparing`または`incomplete`にします。Filenameの近接だけに頼らず、artifact digestからSBOM digest・locationを決められるmanifest、registry relation、metadata API等を使います。

保持期間は固定日数ではなく、artifactの取得、support、稼働、監査、incident調査の期間に合わせます。訂正は同じSBOM identityの内容を黙って上書きせず、新しいversionまたはidentityとsupersedes／withdrawn関係で示します。

## 5. Analysis intakeを独立した境界にする

Analysis platformのprojectをproduct nameだけで自動作成すると、似た名前やmutable versionへSBOMが混ざります。Exact project IDとrelease versionを先に決め、upload専用identityは必要なprojectと操作だけへ限定します。Portfolio検索、policy変更、system設定、project作成は別のauthorityにします。

SBOMはuntrusted inputです。Transport認証、size・timeout、schema、parser isolation、logの値最小化を設定します。API key、Authorization header、SBOM本文、internal endpoint、全findingを処理receiptへ複製しません。

## 6. 受付と処理完了を分ける

Provider固有の状態を次の共通意味へ正規化します。

| 状態 | 意味 | Release／判断での扱い |
|---|---|---|
| `ACCEPTED` | Transportがrequestを受け付けた | 完了ではない |
| `VALIDATED` | Formatとproviderの入力検査を通過 | Analysis完了ではない |
| `PROCESSED` | Expected projectで対象SBOMのingestion／analysisが完了 | SBOM digest・serial・project・時刻を照合して次へ渡す |
| `REJECTED` | Validationまたはpolicy違反 | Release／analysisを止める |
| `ERROR` | Processing failure、timeout、collector・analyzer・data障害、結果不完全 | Cleanにせず再試行・調査へ渡す |

Dependency-Track 4.14 documentationでは`BOM_CONSUMED`と`BOM_PROCESSED`が区別され、processing／validation failure eventもあります。実装時は対象releaseのOpenAPI、permission、notification schemaを再確認し、event名だけでなくSBOM・project identityを照合します。

## 7. Analysis healthと結果を分ける

Finding 0件は、対象componentが正しく識別され、必要なadvisory sourceがfreshで、paginationが完了し、parser・analyzerが正常だった場合にだけ結果として扱えます。PURL、CPE、alias、version rangeの品質によるfalse positive／negativeも残ります。

Receiptには、SBOM digest・serial、project ID・version、processing result、processed time、provider release・API contract、collection completeness、relevant data source healthを値を絞って残します。Health取得不能をhealthyへ補完しません。

## 8. Deploymentと影響調査へ渡す

Deployment recordはenvironment、deployment identity、observed artifact digest、observation time、collector identity・healthを持ちます。Release SBOMとartifact digestでjoinし、componentからartifact、deployment、ownerへ逆引きします。

Runtime observationで新しいcomponentを得ても、release SBOMを上書きしません。追加観測として関連付けます。Collectorのcoverage不足、権限不足、stale snapshot、page欠落は「該当deploymentなし」ではなく評価不能です。

## 方式の選択

| 判断 | 選択肢 | 主な代償 |
|---|---|---|
| 生成時点 | Source、build中、post-build scan、複数の併用 | 早期feedbackとfinal bytesのcoverageは同じではない |
| Format | CycloneDX、SPDX | Parser、schema、identity、relationship、consumer対応をformat・versionごとに検証する |
| Binding | Root component hash、release manifest、registry attachment、外部index | SBOM内のhashだけではpublication後の関係やauthenticityを保証しない |
| Publication | Release sidecar、package／OCI registry、metadata API | Consumer discovery、immutability、retention、accessが製品ごとに変わる |
| Analysis | Dependency-Track等のportfolio platform、ecosystem service、独自index | Project identity、非同期state、権限、data source healthのadapterが必要 |
| Operations join | Deployment inventory、CMDB、orchestrator、runtime collector | Collector coverageとartifact digestの取得可能性が制約になる |

## 典型的な失敗経路

- Source manifestから作ったSBOMをfinal binaryやimageの正本にする。
- Product version、filename、`latest`だけでartifactとSBOMを結ぶ。
- CycloneDX／SPDXとしてparseできることを、component coverageの証明にする。
- `complete`をgeneratorの観測能力・除外と照合しない。
- Artifactを先に公開し、SBOM失敗時もrelease completeにする。
- Publisher credentialからだけdownloadできる状態をconsumer availabilityとする。
- Analysis projectをauto-createし、似た名前やmutable versionへ混ぜる。
- Upload tokenまたは`BOM_CONSUMED`をanalysis完了にする。
- Processing failure、stale data、page欠落を0 findingsへ変える。
- Source、build、operationsのserialを再利用・上書きする。

## 具体実装

[CycloneDX 1.7 artifact binding](implementations/cyclonedx-artifact-binding/README.md)は、実artifact bytesのSHA-256とSBOM root hashを照合し、build／post-build phase、serial・version、versioned PURL、`bom-ref`、dependency relation、明示されたcomposition stateを検査します。標準libraryだけで動き、手元のrepositoryへ導入できます。

この実装はCycloneDX schema全体、generator coverage、publication、Dependency-Track、deployment catalogを実装しません。Productionでは公式schema validatorと、選んだstorage・analysis製品のadapterを追加します。

## 診断で確認する項目の正本

製品非依存の項目は[PSB-REL-003](../../../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md#failure-checks)にあります。具体実装ではartifact変更、phase違い、dangling reference、unknown composition、malformed JSONをローカルで確認します。Storageとanalysis platformでは、consumer access、部分公開、誤project、processing failure、timeout、stale data、pagination不足をlive environmentで追加します。

## このpatternが満たす特性と限界

[PSB-REL-003](../../../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)の`SBOM-REL-1`〜`8`を、observation、binding、format、coverage、publication、analysis intake、processing health、deployment joinへ配置します。

Pattern自体はSBOMを生成・公開せず、analysis platformへ接続しません。実装例が確認するのはartifact bindingとCycloneDX文書内の限定contractです。[Supplier SBOMの受入れ](../supplier-sbom-intake-boundary/README.md)はREL-004、vulnerability priorityはGOV-003、impact responseはGOV-001、scanner自身の証拠はDETECT-001が別に扱います。

## 根拠

- [REF-RELEASE-SBOM-LIFECYCLE-001](../../../sources/README.md#ref-release-sbom-lifecycle-001)
- [移行記録](../../../docs/RELEASE_SBOM_MIGRATION.md)
