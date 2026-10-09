# PSB-REL-001 Signature and provenance verification

**署名が正しくても、その成果物を自分たちが使ってよいか確認できるか。**

## なぜ必要か

例えば、正規のbuilderが別のsourceやdebug設定で作った成果物にも、有効な来歴の署名が付くことがあります。利用者は署名だけでなく、使うファイルと自分たちの期待値を照合します。

## 満たすべきこと

1. **使うファイルを結び付ける。** 実際に使うbytesのdigestを、認証した来歴のsubjectへ照合し、確認後も別の内容へ差し替えない（ACCEPT-1）。
2. **利用者の信頼根拠で確認する。** 来歴の署名を、利用者が承認した鍵やidentityで検証する（ACCEPT-2）。配布物に同梱された鍵やpolicyを自動で信頼しない。来歴の形式、署名者とbuilder、build type、source、revision、外部入力を利用者側の期待値へ照合する（ACCEPT-3）。
3. **要求を下げず、失敗時は止める。** 保護する成果物に必要な署名・来歴を維持し、変更は独立して承認する（ACCEPT-4）。取得、解析、暗号検証の失敗を合格にせず、拒否と評価不能を区別して使用を止める（ACCEPT-5）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 別成果物の有効な署名・来歴や、未承認の鍵・policyを同梱しても受け入れられないか。
- 正しい署名でも、想定外のbuilder、forkのsource、未承認revisionや外部入力を拒否するか。
- 必要な署名・来歴の欠落、取得失敗、解析失敗、timeoutで検証不要の経路へ切り替わらないか。
- 検証後のファイルや可変tagの差替え、古いpolicyや別digestの合格結果の再利用を許さないか。

これらは診断・設計レビューの確認項目であり、実際の使用を止めた結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L2 | 成果物と来歴を結び、利用者が認める信頼の根から署名を確かめる部分を支える。 | 生成側の要件やhosted build、Build L2の達成は示さない。 |
| SLSA Build provenance v1.2 | Subject、builder、build type、外部入力を利用者の期待値へ照合する設計に関係する。 | 来歴の生成や実際の検証器の動作は未確認。 |

対象特性と残る範囲は[マッピング](../../../../mappings/frameworks.yaml)にあります。有効な署名だけで成果物の使用許可やSLSA levelを判断しません。

## このコントロールの範囲

対象は利用者が取得した成果物、認証した来歴、利用者自身の期待値、使用直前の受入です。成果物への署名と来歴への署名は対象が違うため、両方を要求するならそれぞれ確認します。署名の生成は[REL-005](../psb-rel-005-artifact-signing-generation/README.md)、来歴の配布は[REL-002](../psb-rel-002-provenance-distribution-availability/README.md)、container実行直前の強制は[CONTAINER-001](../../container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)へ渡します。合格しても成果物の無害性は示せません。

期待値の管理と検証結果を使用する場所は[engineering](../../../../engineering/release-integrity/consumer-artifact-acceptance/README.md)で選びます。旧crypto実装は移植せず、liveの署名検証・使用拒否も未確認です。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照仕様と採否](../../../../sources/README.md#spec-consumer-artifact-verification)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
