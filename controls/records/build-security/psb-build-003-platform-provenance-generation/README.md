# PSB-BUILD-003 Platform provenance generation

**ビルドの来歴を、ビルドjob自身の申告ではなく基盤が作っているか。**

## なぜ必要か

例えば、jobが`builder.id`や入力を書いたJSONを作り、基盤がそのまま署名しても、記録の中身が基盤で確認された事実にはなりません。成果物と実行条件を誰が記録し、誰が認証できるかを分けて判断します。

## 満たすべきこと

1. **基盤側で作る。** 対象となる成功ビルドごとに基盤のcontrol planeがprovenanceを生成し、ビルドjobから生成を省略・置換できないようにする（PROV-GEN-1）。対象成果物すべてを実際のbytesのdigestへ結び付ける（PROV-GEN-2）。
2. **記録の中身と情報源を示す。** 採用したschemaとbuild typeに必要な`buildDefinition`、`runDetails`、`buildType`、`externalParameters`、`builder.id`、ソース入力を解釈できるように記録する（PROV-GEN-3）。各fieldが基盤由来か、利用者由来か、基盤で検証されたかを区別する（PROV-GEN-4）。
3. **出所を認証し、失敗時は止める。** 利用者が出所と改変の有無を検証できる形で認証し、その能力をビルドjobへ渡さない（PROV-GEN-5）。記録の欠落、成果物との不一致、認証・生成の失敗を成功に変えず、通常の公開工程へ進めない（PROV-GEN-6）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- ビルド定義から生成処理を外す、失敗を無視する、job製のstatementへ差し替える場合に公開へ進めないか。
- Jobが`builder.id`、ソースrevision、外部入力を偽っても、基盤由来の事実として認証されないか。
- 成果物の変更、digestの差替え、一部出力の欠落、別runのstatement再利用を拒否するか。
- 認証前後の改変、未承認の認証identity、generatorや保存先の障害を成功に変えないか。
- 基盤が記録した利用者由来の入力を、承認済みのリリース入力と取り違えないか。

これらは診断・設計レビューの確認項目であり、実際の基盤で試した結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L1「Platform generates provenance」 | ビルド基盤が来歴を自動生成し、出力した成果物へ結び付ける責任に関係する。 | 実際に生成した来歴は未確認。 |
| SLSA Build track v1.2 Build L2「Platform authentic provenance」 | 基盤が確認した事実とjobから渡る値を分け、基盤の権限で来歴を認証する責任に関係する。 | 基盤の信頼境界、署名権限、利用者側の検証は未確認。 |

対象特性と例外は[マッピング](../../../../mappings/frameworks.yaml)にあります。このControlだけでSLSA Build L1・L2の達成を示しません。

## このコントロールの範囲

対象は基盤側の来歴生成、成果物との対応、各fieldの情報源、出所の認証です。SLSAの版やlevelによって利用者由来のfieldを許す条件は異なります。すべてを基盤が直接作ったと推測せず、[engineeringの情報源の整理](../../../../engineering/build-security/platform-owned-provenance-generation/README.md#責任と情報源)で採用方式の境界を確認します。来歴が正確でも、入力がリリース用に承認されたとは限りません。

ビルド中の権限は[BUILD-001](../psb-build-001-build-containment/README.md)、承認した手順との照合は[BUILD-002](../psb-build-002-approved-consistent-build/README.md)、来歴の配布は[REL-002](../../release-integrity/psb-rel-002-provenance-distribution-availability/README.md)、利用者の受入判断は[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)へ渡します。来歴は成果物の無害性を示しません。旧synthetic JSONとlocal keyによる例は基盤側の生成やidentity保護を示さないため移植していません。

[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、[Sources](../../../../sources/README.md#spec-platform-provenance-generation)、[移行記録](../../../../docs/MIGRATION_BUILD.md#platform-provenance-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
