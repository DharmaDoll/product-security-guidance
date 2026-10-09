# PSB-BUILD-002 Approved and consistent release build

**今回のリリース成果物は、承認した基盤と手順で作られたか。**

## なぜ必要か

例えば、正規のbuilderを使っても、別のビルド定義やdebug用の入力で作れば、レビューした手順の成果物とは言えません。開発者端末で作った同名のファイルを通常リリースへ置く経路も止める必要があります。

## 満たすべきこと

1. **正規の作り方を決める。** 対象リリースと目標とする保証水準を決め、builderの識別子、能力、信頼境界を確認して承認する（CONSISTENT-BUILD-1）。通常リリースへはその基盤の出力だけを進め、目標水準がhosted実行を求める場合は実際の経路も確認する（CONSISTENT-BUILD-2）。Hostされた基盤を選んだだけで、その水準を満たしたとは言えない。
2. **手順と入力を固定する。** レビューしたソースとビルド定義のrevision、実際に使った定義を特定する（CONSISTENT-BUILD-3）。Build type、開始処理、成果物に影響する外部入力と起動条件の期待値を決め、変更は再承認する（CONSISTENT-BUILD-4）。
3. **今回の成果物と照合する。** 正確な成果物digestを、基盤を出所とする実行情報へ結び付け、承認した基盤・手順・入力と比較する（CONSISTENT-BUILD-5）。Jobが自分で書いた記録を基盤の証拠にしない。不一致や証拠の欠落・取得失敗では通常リリースへ進めない（CONSISTENT-BUILD-6）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 開発者端末や未承認の基盤で作った同名・同版のファイルを、通常リリースへ昇格できないか。
- 承認builderでも、別のworkflow、script、開始処理、重要な外部入力で作った成果物を通せないか。
- Jobが書いた`hosted: true`や`builder.id`を、基盤が発行した事実として受け入れていないか。
- 実行記録の成果物digestを別のファイルへ付け替えても通らないか。
- 基盤の能力評価や記録が古い、欠けている、取得できない場合に合格としないか。

これらは診断・設計レビューの確認項目であり、実際のビルドや公開経路で試した結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L1「Appropriate build platform」 | 求める保証に合うbuilderを選び、その能力を確認する責任に関係する。 | 実際のbuilder評価・選定は未実施。 |
| SLSA Build track v1.2 Build L1「Consistent build process」 | Source、build定義、重要な外部入力を版で結び、release用の手順を揃える判断に関係する。 | 同一repositoryや単一の起動方法を規格が一律に要求するわけではない。 |
| SLSA Build track v1.2 Build L2「Hosted build platform」 | Build L2以上を選ぶ場合、端末でなく承認したhosted基盤で作る条件に関係する。 | このControl自体はBuild L2以上の選択・達成を示さない。 |

3件は[マッピング](../../../../mappings/frameworks.yaml)で対象特性と条件を分けています。実際のbuild runやSLSA levelの達成は未確認です。

## このコントロールの範囲

対象はリリースを作る側が承認するbuilder、手順、入力と、今回の成果物がその経路を通ったかの判断です。実行中の隔離は[BUILD-001](../psb-build-001-build-containment/README.md)、基盤による来歴の生成は[BUILD-003](../psb-build-003-platform-provenance-generation/README.md)、利用者自身の受入判断は[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)へ渡します。この判断だけで再現性や成果物の無害性は示せません。

基盤の評価、許す手順、公開を止める場所は[engineering](../../../../engineering/build-security/approved-release-build-process/README.md)で選びます。旧JSONの自己申告型検証器は、hosted実行や基盤発行の記録を確かめられないため移植していません。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、[Sources](../../../../sources/README.md#spec-consistent-build-producer)、[移行記録](../../../../docs/MIGRATION_BUILD.md#consistent-build-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
