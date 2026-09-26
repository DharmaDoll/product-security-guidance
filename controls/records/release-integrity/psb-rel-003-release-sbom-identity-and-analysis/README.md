# PSB-REL-003: Release SBOM identity and analysis boundary

学ぶ：[An accepted SBOM can still describe the wrong release](learning.md) ·
設計する：[Release SBOM identity and analysis intake](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)

## 問い

Release evidenceとして使うSBOMが、実際に配布するexact artifactを説明し、観測範囲と不明点を明示したまま公開・analysis処理・稼働影響調査へ渡るか。

## できてはいけないこと

Source manifestだけから作ったSBOM、別build向けのSBOM、対象artifactとの関係を名前やversionだけで推測したSBOMを、release artifactのcomponent inventoryとして扱ってはいけません。Formatが正しいことや`complete`という値があることだけで、vendored、statically linked、OS package、plugin、build時download等を観測できたと判断してはいけません。

Upload APIの受付、queue投入、`BOM_CONSUMED`、空のfinding一覧を、対象SBOMのvalidation・処理・最新dataによるanalysis完了と取り違えてはいけません。Parser、analyzer、data更新、pagination、権限、通知の失敗やtimeoutを「脆弱性なし」に変えてはいけません。

Source、build、deployment／operationsの観測を同じidentityへ上書きし、早期feedback用の一覧をreleaseの正本にしたり、稼働中のartifactとの関係を失わせたりしてはいけません。

## 適用範囲と非適用

Source・build・deployment／operationsで得るSBOM observation、release artifact digest、SBOM digest・serial・version、root component、component identity、relationship、completeness claim、公開経路、analysis target、upload identity、processing state、analysis data health、artifactからdeploymentへの受け渡しが対象です。

SBOM generator自体の取得・完全性、release artifactの署名・provenance検証、[supplierが提供するSBOMの受入れ](../psb-rel-004-supplier-sbom-intake-trust/README.md)、脆弱性の適用性・priority、実際の修復は別の境界です。このcontrolへの合格は、SBOMに未発見componentや脆弱性がないことを保証しません。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `SBOM-REL-1` | Source、build、deployment／operationsの観測を、取得時点、subject、tool・設定、identity、authority、既知のcoverageとともに分ける。Releaseの正本にはfinal artifactを観測したbuild／post-build SBOMを使い、source-only observationを代用しない |
| `SBOM-REL-2` | 配布する各artifactをcryptographic digestで列挙し、対応するSBOMのdigest、serial、version、root componentへ結ぶ。Filename、product version、tag、近接した保存場所だけで対応を推測しない |
| `SBOM-REL-3` | 採用formatとversionを固定してschemaを検証し、componentの機械可読なidentity、重複しない参照、解決可能なdependency／assembly relationを保つ。Unsupported・malformed・曖昧なidentityを受理しない |
| `SBOM-REL-4` | Artifact typeごとに観測すべきcomponent surfaceとgeneratorのcoverageを定め、complete、incomplete、unknown、redacted等を根拠に沿って明示する。Format validityやcomponent数だけから完全性を推論しない |
| `SBOM-REL-5` | Required SBOMとartifactからのrelationが、intended consumerから変更不能なidentityで取得できるまでreleaseをcompleteにしない。Artifactの利用・support・調査期間とSBOMの保持・訂正・withdrawalをそろえる |
| `SBOM-REL-6` | Analysis platformへ送るSBOMをexact project・release identityへ事前に結び、upload専用の最小権限を使う。Credential、SBOM本文、内部情報を不要なreceiptやlogへ複製しない |
| `SBOM-REL-7` | Transport受付、validation、ingestion、analysis完了を別状態にし、SBOM digest・serial・projectとの対応を確認する。失敗、timeout、古いanalysis data、部分取得、結果のpage欠落をcleanへ変換しない |
| `SBOM-REL-8` | Release artifact digestからdeployment／environmentの観測へ関係を保ち、source・build・operations inventoryを上書きせず検索できる。Collector不足や未観測を「稼働なし」へ変換しない |

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- ArtifactをSBOM生成後に変更しても、古いSBOMを同じreleaseへ結び付けて公開できてしまわないか。
- Source／pre-build SBOMを、final artifactを観測したrelease-authoritative SBOMとして登録できてしまわないか。
- Component参照の重複、存在しない`bom-ref`へのdependency、unsupported schema、parse不能を受理していないか。
- Generatorが扱わないecosystemや除外設定があるのに、`complete`へ自動変換していないか。
- Artifact公開後にSBOM公開が失敗・遅延した時、releaseが通常取得可能なcomplete状態にならないか。
- Intended consumerの権限ではSBOMを取得できないのに、publisherの管理権限からの確認だけで公開完了にならないか。
- Upload token、HTTP成功、`BOM_CONSUMED`だけでanalysis成功とせず、validation失敗、processing失敗、timeoutを別状態にできるか。
- 誤ったproject UUID・release version・SBOM digest・serialの処理通知を、対象releaseの結果として受理しないか。
- Analyzerやvulnerability dataの更新が止まった時、finding 0件をclean resultとして返さないか。
- Source、build、operations observationのserialやsubjectを上書きし、どのartifactがどこで稼働するか辿れなくならないか。

これらは診断観点です。[CycloneDX限定実装](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)はartifact bindingと文書内の一部だけを実行確認します。Storage、analysis platform、deployment catalogの項目は対象製品のlive evidenceが必要です。

## 実装判断

Release pipelineでは、final artifactの生成後にSBOMを作り、artifactとSBOMを同じimmutable identity graphへ入れてから公開します。Source SBOMは早期feedback、operations inventoryは配置・追加観測に使い、build／post-build SBOMを上書きしません。

Format parserとschema validator、artifact binding check、storage publication、analysis adapter、deployment catalogを一つの万能verifierへ押し込みません。各境界は実際の対象から証拠を取得し、後段へdigestと状態を渡します。

## このcontrolが直接保証しないこと

- Generatorがartifact内の全componentを発見したこと。
- SBOMの署名者、supplier、生成環境が信頼できること。
- SBOMに記載されたcomponentが脆弱性を含まないこと。
- Analysis platformのfindingが完全・正確であること。
- Artifactが全environmentへ安全に配置され、修復されたこと。
- SSDFその他のframeworkへの準拠や組織への導入済み状態。

## 根拠と関係

- [REF-RELEASE-SBOM-LIFECYCLE-001](../../../../sources/README.md#ref-release-sbom-lifecycle-001)
- [移行記録](../../../../docs/RELEASE_SBOM_MIGRATION.md)
- [成果物マッピング](../../../../mappings/pilot.yaml)
- [Frameworkマッピング](../../../../mappings/frameworks.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
