# PSB-BUILD-002: Approved and consistent release build

学ぶ：[同じbuilderでも、別の手順で作れば別のrelease](learning.md) · 設計する：[Approved release build process](../../../../engineering/build-security/approved-release-build-process/README.md)

## 問い

リリース担当者は、承認したビルド基盤で、レビューしたソース・手順・重要な入力から今回の成果物を作ったと判断できるか。

## できてはいけないこと

開発者端末や未承認のビルド基盤で作った成果物を、正規のリリース成果物として公開してはいけません。承認済みの基盤で動いたとしても、別のビルド定義、開始処理、重要なパラメーター、未承認の起動条件で作った成果物を同じ手順の結果にしてはいけません。ジョブ自身が書いた`hosted: true`や`assessed_level: 2`を、基盤の能力・実行場所の証拠にしてはいけません。

## 適用範囲と非適用

リリース成果物を作る側（producer）のビルド基盤（builder）選定、ビルド定義、ソース、外から渡す入力、実行経路、成果物と実行記録の対応、公開可能にする判断が対象です。目標とする保証水準を先に決め、SLSA Build L2以上を選ぶ場合はホステッド基盤での実行を必要条件にします。ホステッド基盤を使うだけでBuild L2を満たすわけではありません。

[BUILD-001](../psb-build-001-build-containment/README.md)はbuild中の権限・通信・隔離、[BUILD-003](../psb-build-003-platform-provenance-generation/README.md)はplatformによるprovenance生成と認証を扱います。本controlはproducerがどのbuilderと手順を承認し、今回の成果物がその経路を通ったかを扱います。[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)はconsumer独自の期待値で使用を決めます。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `CONSISTENT-BUILD-1` | 対象リリースと目標水準を決め、基盤の識別子・信頼境界・能力の証拠をレビューして承認する。URLや申告されたlevelだけで能力を認定しない |
| `CONSISTENT-BUILD-2` | 通常リリースは承認した基盤の出力だけを公開可能にする。目標水準がホステッド実行を求める場合はその経路を確認し、端末・代替経路を同じリリースとして通さない |
| `CONSISTENT-BUILD-3` | レビューしたソースとビルド定義を変更不能なrevisionへ結び、実際に使った定義を特定する。定義が別repositoryにある方式を排除せず、両方のrevisionを示す |
| `CONSISTENT-BUILD-4` | 採用したビルド方式（build type）、開始処理（entry point）、成果物に影響する外部パラメーターと起動条件の期待値を決め、予期しない変更を承認なしに通常リリースへ通さない |
| `CONSISTENT-BUILD-5` | 成果物の正確なdigestと、基盤を出所とする実行証拠を対応付け、基盤・ソース・定義・重要な入力を作り手側の期待値へ照合する。ジョブの自己申告だけでは基盤の事実としない |
| `CONSISTENT-BUILD-6` | 基盤不一致、手順の逸脱、証拠の欠落・不正、取得・評価の障害を公開の判定点で止める。不一致と評価不能を区別する |

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 開発者端末や未承認の基盤で作った同名・同versionの成果物を、通常リリースへ昇格できないか。
- 承認した基盤を使いながら、別のworkflow revision、script、開始処理で作った成果物を通せないか。
- ソースのrevisionだけを固定してビルド定義や外部パラメーターを変えた場合、承認済み手順として扱われないか。
- 手動起動、debug flag、別のbase image・依存入力など、採用した方式で重要な変更を見落とさないか。
- ジョブが書いたJSONの`hosted`、`builder.id`、`assessed_level`を基盤発行の証拠として受け入れないか。
- 実行記録の成果物digestを別のbytesへ付け替えてもリリースできないか。
- 基盤の能力評価や実行記録の取得失敗、parse不能、必須field不足を合格にしないか。
- 基盤の能力やビルド方式が変わったのに、古い承認結果を無条件で再利用しないか。

これらは設計・診断の確認項目です。実際のbuild platformやrelease gateで拒否を観測した結果ではありません。

## 実装判断

ビルド定義と入力を固定する目的は、異なる実行をすべて禁じることではなく、「今回どの手順を正規リリースと呼ぶか」を検証可能にすることです。ソースとビルド定義が別repositoryでも、双方のrevisionと選択関係を記録できます。許可するパラメーターは採用するビルド方式に合わせて決め、普遍的な完全一致リストを作りません。

基盤の承認記録と、今回実際に使ったことの証拠も別です。基盤の評価を一度保存しても、実行記録がジョブの自己申告だけなら代替経路を見抜けません。採用する基盤のprovenanceや実行APIから事実を取得し、成果物digestと結び付けます。

## このcontrolが直接保証しないこと

Buildの再現性、成果物の無害性、依存入力の完全性、platformの未侵害、強いbuild間隔離は保証しません。このcontrolだけでSLSA Build level、実環境への導入、consumer受入れを宣言しません。

## 根拠と関係

- [SPEC-CONSISTENT-BUILD-PRODUCER](../../../../sources/README.md#spec-consistent-build-producer)
- [移行記録](../../../../docs/CONSISTENT_BUILD_MIGRATION.md)
- [成果物マッピング](../../../../mappings/pilot.yaml)
- [Frameworkマッピング](../../../../mappings/frameworks.yaml)
