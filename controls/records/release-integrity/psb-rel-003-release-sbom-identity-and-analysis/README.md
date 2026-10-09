# PSB-REL-003 Release SBOM identity and analysis

**そのSBOMは、実際に配布する成果物の何を、どこで調べて作ったものか。**

## なぜ必要か

例えば、sourceのmanifestから作ったSBOMは早い段階の確認に役立ちます。しかし、ビルド中に加わった部品までは示せません。リリースの部品表として使うなら、完成した成果物を調べた範囲と、その成果物との対応が必要です。

## 満たすべきこと

1. **取得地点を区別する。** Source、build後、稼働環境での観測を、時点・対象・tool・観測範囲とともに別々に残す。リリースの正本には完成した成果物を調べたbuild後のSBOMを使い、sourceだけの一覧で代用しない（SBOM-REL-1）。
2. **成果物と部品表を結び付ける。** 配布する各成果物のdigestをSBOMのdigest・serial・root componentへ結び付ける（SBOM-REL-2）。採用形式を検証し、部品の識別子と関係をたどれるようにする（SBOM-REL-3）。Generatorが観測できない部品や不明な範囲を示し、形式の正しさや部品数から「完全」と推測しない（SBOM-REL-4）。
3. **公開と分析の結果を分ける。** 利用者が成果物からSBOMを取得できるまでreleaseを完了にしない（SBOM-REL-5）。分析先では対象project・releaseと取込権限を限定し（SBOM-REL-6）、受付、検証、取込、脆弱性分析完了を別の状態として追う。障害や古い分析データを「脆弱性なし」にしない（SBOM-REL-7）。
4. **稼働先まで辿る。** 成果物のdigestとdeployment・environmentの観測を結び、source・build・稼働時の一覧を上書きしない。観測できない状態を「稼働なし」にしない（SBOM-REL-8）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- SBOM生成後に成果物を変えたり、sourceだけのSBOMをbuild後の正本として登録したりできないか。
- 共通base imageのSBOMを、アプリケーションを追加した最終image全体の部品表にしていないか。
- 参照切れ、未対応形式、generatorの対象外があるのに「完全」としていないか。
- 成果物だけ公開できたときや、利用者がSBOMを取得できないときもrelease完了にしていないか。
- Upload受付や取込通知だけで分析完了とせず、誤project、処理失敗、古いデータ、結果のpage欠落を区別できるか。
- Source・build・稼働時の観測を上書きし、どの成果物がどこで動くか見失っていないか。

これらは診断項目です。[CycloneDX限定実装](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)は文書内の結び付きの一部だけを確認します。公開、分析、稼働先との対応は実環境で未確認です。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| NIST SSDF 1.1 PS.3.2 | どの時点で集めた部品情報かを示し、完成した成果物とSBOMを結び付けて提供する部分を支える。 | SBOMだけで部品の来歴全体や配布・稼働先の網羅性は証明できない。 |
| NIST SSDF 1.1 RV.1.1 | 対象と状態が分かる分析結果を、部品の脆弱性調査へ渡す部分を支える。 | 実際の脆弱性情報源、分析完了、製品への適用判断は未確認。 |

2件は[マッピング](../../../../mappings/frameworks.yaml)上の部分的な設計関係です。SBOMの生成・公開や分析を実環境で完了した証拠、SSDFへの準拠ではありません。

## このコントロールの範囲

対象は自組織のrelease SBOMの取得地点、完成物との対応、公開、分析、稼働先への受け渡しです。供給者のSBOMの受入は[REL-004](../psb-rel-004-supplier-sbom-intake-trust/README.md)、脆弱性の適用性や修復の判断は別に行います。SBOMに記載のない部品や未知の脆弱性がないことまでは示せません。

取得地点と対象の選び方、分析先の状態管理は[engineering](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)を参照してください。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料と採否](../../../../sources/README.md#ref-release-sbom-lifecycle-001)、[移行記録](../../../../docs/MIGRATION_RELEASE.md#release-sbom-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
