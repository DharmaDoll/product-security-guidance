# PSB-CICD-009 Cache trust boundary

**CIのcacheから戻したファイルを、誰が保存し、どのjobが使うか把握しているか。**

## なぜ必要か

例えば、新しいrunnerでも、前のjobが保存したtoolをcacheから戻して実行すれば、そのjobの影響を受けます。Cache keyが一致するだけでは、中身が承認済みとは言えません。

## 満たすべきこと

1. **保存者と利用者を分ける。** 取得ファイル用cacheへ保存できる処理をレビューした範囲に絞る（CACHE-1）。未信頼PRは復元だけを許し、信頼済み処理が使う範囲へ保存させない（CACHE-3）。公開・deploy・署名のjobは、このCI cacheを直接にも呼出先経由にも使わない（CACHE-6）。
2. **再利用する中身を限定する。** 用途、形式の版、OS、architecture、runtime、レビューしたlock digestで取得対象を識別する（CACHE-2）。秘密情報、ソース、展開済みの依存環境、tool、起動ファイル、build出力は、この取得cacheに入れない（CACHE-4）。
3. **復元しても照合する。** 完全一致しない結果や失敗・部分復元を使わず、正規の取得へ戻る。一致した場合も、承認したhashと依存関係を利用前に確認する（CACHE-5）。全保存者・利用者と現在の挙動を確認できなければ、導入済みと扱わない（CACHE-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 未信頼PRや呼出先workflowが、信頼済みのjobが使うcache範囲へ保存できないか。
- Lockの欠落、別OS・runtime・用途、prefix一致で、別の内容を復元して使えないか。
- 保存pathを広げたり自動cacheを使ったりすると、認証情報、展開済み環境、tool、build出力が混ざらないか。
- 同じkeyの改変ファイル、復元の中断・部分展開があっても、利用前の照合を飛ばさないか。
- 公開・deploy・署名jobに、setup Actionや呼出先を通るcache利用が残らないか。取得失敗を導入済みと扱っていないか。

これらは設計レビューの確認項目です。実際に試す場合は使い捨てcacheと無害なファイルを使い、実施結果は別に残します。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| Supply-chain Incident Taxonomy and Framework T-C007 | 未信頼jobが保存したcacheを特権jobが使う経路を部分的に妨げる。 | Cacheの正確なkeyや全復元経路を規定するものではない。 |
| OpenSSF OSPS Baseline 2026.02.19 OSPS-BR-01.03 | 未信頼の変更から特権CI資産へ到達させない判断を、cache経由へ適用する。 | OSPSはcacheの全面禁止を求めない。 |

両者の詳しい対応と限界は[マッピング](../../../../mappings/frameworks.yaml)にあります。実際の保存・復元・実行の拒否は未確認です。

## このコントロールの範囲

対象は依存の取得ファイルを再利用するcacheです。展開済み環境や実行toolの共有を、このcacheの許可に含めません。取得物の同一性は[DEPS-003](../../dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、未信頼PRから権限付き処理への経路は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、runnerに残る状態は[CICD-007](../psb-cicd-007-runner-lifecycle-isolation/README.md)へ渡します。高権限jobが使わなくても、非特権jobの改ざんや停止は別に残ります。

保存・復元の選び方とGitHub固有の挙動は[engineering](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)を参照してください。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-ci-cache-boundary)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
