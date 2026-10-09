# PSB-REL-002 Provenance distribution and availability

**利用者は、手元の成果物に対応する来歴を見つけて取得できるか。**

## なぜ必要か

例えば、一つのreleaseに複数OS向けのファイルがあっても、来歴ファイルが一つ置かれているだけでは、どれを説明するか分かりません。成果物を公開した後も、来歴だけ先に消えてはいけません。

## 満たすべきこと

1. **成果物ごとに対応を示す。** 来歴が必要な成果物・配布経路・利用者を決め、各成果物をdigestで列挙する（PROV-DIST-1）。Digestから対応する一つ以上の来歴と取得先へ辿れるようにし、release名やtagだけで結び付けない（PROV-DIST-2）。
2. **利用者が取得できるまで公開完了にしない。** 来歴と対応一覧が保存され、想定する利用者の権限と通信経路から取得できることを確かめる（PROV-DIST-3・4）。配布側で見えるだけでは足りない。
3. **変更・消失・要件低下を防ぐ。** 成果物、来歴、一覧をdigest等の変更不能なidentityへ結び付け、訂正は新しいidentityで示す（PROV-DIST-5）。成果物を利用・調査する期間は来歴も保持し（PROV-DIST-6）、欠落や取得失敗を理由に必須要件を自動で任意へ変えない（PROV-DIST-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 別OS・別digestの成果物へ、同じrelease名の来歴を誤って返さないか。複数の来歴の種類も失わないか。
- 成果物だけ公開できた場合や、来歴・一覧の公開が遅れた場合に、release完了としていないか。
- 配布側では取得できても、実際の利用者のidentity・地域・clientから取得できない状態を見逃さないか。
- Tagや一時URLの再解決、来歴・一覧の上書き、mirror・cacheの古い内容を識別できるか。
- 成果物が利用可能な期間中、cleanupやaccount削除で来歴だけ消えないか。部分取得や古いinventoryを完了扱いしないか。

これらは診断・設計レビューの確認項目であり、実際の配布先で試した結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L1「Producer distributes provenance」 | 成果物に対応する来歴を利用者が見つけて取得できるようにする、提供側の責任に関係する。 | 実releaseサービスでの公開・取得やSLSA levelは未確認。 |
| NIST SSDF 1.1 PS.2.1 | 成果物と結び付いた来歴を利用者へ提供することが、完全性確認の情報を利用可能にする一部を支える。 | 署名や利用者側の検証、実際の保持期間はここでは確認していない。 |

この2件の対象特性と条件は[マッピング](../../../../mappings/frameworks.yaml)にあります。来歴を置いたことだけで、利用者が検証できたことや規格への準拠を示しません。

## このコントロールの範囲

対象は成果物と来歴の対応、発見・取得、保管期間、公開完了の判定です。来歴の生成は[BUILD-003](../../build-security/psb-build-003-platform-provenance-generation/README.md)、取得した内容の認証と利用者の受入は[REL-001](../psb-rel-001-signature-provenance-verification/README.md)へ渡します。取得できた来歴の中身が正しいとは、このcontrolだけでは言えません。

配布先ごとのattachment、access、immutability、retentionは[engineering](../../../../engineering/release-integrity/provenance-distribution-and-availability/README.md)で選びます。文書と診断項目を今回の成果物とし、live配布は未確認です。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照仕様と採否](../../../../sources/README.md#spec-provenance-distribution)、[SLSA資料](../../../../sources/README.md#spec-slsa-1-2)、[移行記録](../../../../docs/MIGRATION_RELEASE.md#provenance-distribution-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
