# PSB-REL-001 Signature and provenance verification

**署名が正しくても、その成果物を自分たちが使ってよいか確認できるか。**

## なぜ必要か

例えば、正規のbuilderが別のsourceやdebug設定で作った成果物にも、有効な来歴の署名が付くことがあります。利用者は署名だけでなく、使うファイルと自分たちの期待値を照合します。

## 満たすべきこと

1. **使うファイルを結び付ける。** 実際に使うbytesのdigestを、認証した来歴のsubjectへ照合し、確認後も別の内容へ差し替えない（ACCEPT-1）。
2. **利用者の信頼根拠で確認する。** 来歴の署名を、利用者が承認した鍵やidentityで検証する（ACCEPT-2）。配布物に同梱された鍵やpolicyを自動で信頼しない。来歴の形式、署名者とbuilder、build type、source、revision、外部入力を利用者側の期待値へ照合する（ACCEPT-3）。
3. **要求を下げず、失敗時は止める。** 保護する成果物に必要な署名・来歴を維持し、変更は独立して承認する（ACCEPT-4）。取得、解析、暗号検証の失敗を合格にせず、拒否と評価不能を区別して使用を止める（ACCEPT-5）。

## 期待値と検証場所を選ぶ

受取処理に成果物のコードを実行させず、検証方針を成果物側から書き換えられない場所へ置きます。
認証した署名者とbuilderの組合せを確認し、build typeの意味に沿って外部parameterを照合します。
意味を確認していない外部入力は既定で拒否し、許容できると判断したものだけ通します。

署名対象の種類も先に確認します。成果物への署名、ビルド来歴、SBOMなどの別の証明を混同せず、採用形式で必要な種類を検証します。SLSA Provenance v1なら`predicateType`も照合します。成果物署名を要求する場合は[Artifact signing boundary](../psb-rel-005-artifact-signing-generation/README.md)から検証材料を受け取り、来歴の取得は[配布設計](../psb-rel-002-provenance-distribution-availability/design.md)へ接続します。

## 検証を置く場所と代償

| 場所 | 利点・残る境界 |
|---|---|
| Registryの登録時 | 多くの利用者へ一括適用できる。登録後のregistry侵害・再配布・使用直前の差替えは別 |
| 利用者の取得・使用時 | 利用者の期待値と実際のbytesを照合できる。Verifier配布、policy更新、全使用経路のgateが必要 |
| 継続監視 | 多数の成果物の変化を監視できる。通知だけでは使用を止めない。利用者の対応と結合が必要 |

期待値を作り手から提供してもらう場合も、出所を確かめる変更経路と利用者の承認を用意します。
新鍵、builder、repository、最低信頼条件を自動学習せず、変更レビューと適用期限を管理します。

## 検証結果を使用許可へつなぐ

無害な試験成果物と試験鍵で、検証結果だけでなく実際の使用が止まったことも確認します。解析失敗だけでなく、署名は正しいが条件が想定外のケースも試します。

固定公開鍵なら、鍵の配布・交代・失効を管理します。Keylessならissuer・certificate identity・trust root・有効期間・
方式固有のtransparency証拠等を検証します。方式の違いを単一の`signature_valid`フラグへ隠しません。
Digest照合後も同じbytesを使い、可変tagの再解決や未検証pathへの切替を許可しません。

検証結果を別の処理へ渡す場合は、対象digest、使用したpolicy版と信頼根拠、判断と確認時点を結び付け、成果物側から結果を差し替えられないようにします。使用直前の再検証か、保護された結果と変更不能な対象の照合を選びます。前者は検証基盤の可用性、後者は結果の保護とpolicy変更時の再評価が必要です。

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

期待値の管理と検証結果を使用する場所は[検証を置く場所](#検証を置く場所と代償)で選びます。旧crypto実装は移植せず、liveの署名検証・使用拒否も未確認です。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照仕様と採否](../../../../sources/README.md#spec-consumer-artifact-verification)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

工程間の受け渡しは[ビルドした成果物を署名・公開し、使用するまで](../../../../engineering/release-build-to-use.md)で確認できます。
