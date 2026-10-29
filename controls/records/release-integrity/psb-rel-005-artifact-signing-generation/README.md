# PSB-REL-005 Artifact signing generation

**承認した成果物そのものに、許可した主体だけが署名しているか。**

## なぜ必要か

例えば、正規の署名鍵を使っても、承認後に`latest`が指す先を変えれば別の成果物へ署名できます。署名できる権限と、今回どのbytesへ署名してよいかは別に決めます。

## 満たすべきこと

1. **署名対象を固定する。** 承認したreleaseと成果物のbytesまたはdigestを結び付け、署名器へ渡す実際の対象を再確認する（ART-SIGN-1）。File名や可変tagだけで判断しない。
2. **署名権限を限定する。** 署名できるworkload、操作、対象release、signer、期限を絞る（ART-SIGN-2）。鍵やidentityを保護・交代できるようにし、未信頼のbuild処理や一般の編集権限から分ける（ART-SIGN-3）。
3. **結果を検証して渡す。** 採用形式で正確な成果物に署名し、予定する利用者の信頼条件で結果を確認する（ART-SIGN-4）。署名と必要な検証材料を利用者が成果物から取得できるようにし（ART-SIGN-5）、署名・検証・公開の失敗ではreleaseを完了にしない（ART-SIGN-6）。対象、signer、判断結果を記録しつつ、tokenや秘密鍵を一般ログへ残さない（ART-SIGN-7）。

## 署名対象を確定する

承認者が判断したrelease IDと成果物を、署名要求の前にdigestで固定します。署名器には、承認記録にあるdigestと、実際に署名するbytesまたはOCI manifestから計算したdigestが一致することを強制できる場所を設けます。署名後に別のファイルを同名で置く、registry tagを動かす、bundleを別digestに添付する経路も確認します。Source revisionやbuild IDは追跡に役立ちますが、署名したbytesとの関係を別に検証しなければ同一性の代わりにはなりません。

## 対象の承認と署名権限を分ける

Workload federationは「誰が署名サービスへ接続できるか」を決めます。署名対象の承認は「今回どのdigestを署名してよいか」を決めます。OIDC claim、KMS key policy、署名サービスのoperation権限、release manifestへの書込権限を、採用環境でそれぞれ確認します。Tokenを短寿命にしても、すべてのartifactを署名できる権限なら対象のすり替えは残ります。

| 方式 | 選ぶ条件 | 確認する失敗経路 |
|---|---|---|
| Identityを使う短期鍵 | 対象のissuer・identity・発行時刻・検証材料をconsumerが扱える | 別workflow identity、必要な時刻や透明性証拠の欠落、信頼根拠の更新 |
| KMS/HSM等の管理鍵 | 鍵へのsign権限、鍵状態、鍵の交代、consumerの公開鍵配布を管理できる | 別jobや別releaseからのsign呼出し、失効鍵、広いkey policy |
| 自己管理鍵 | 保管・使用・交代・事故対応を実際に強制できる限定環境 | CI workspaceやlogへの鍵複製、共有鍵の長期利用、更新失敗 |

非exportable鍵やsign-only operationは有力な保護手段ですが、全方式の同一形式の必須値とはしません。どの方式でも、鍵やidentityの発行・使用・失効と、release対象の認可を別々に示します。

## 署名結果を利用者の条件で検証する

採用した署名形式を一つ選び、署名の対象、署名者を特定する材料、利用者が事前に管理する信頼根拠を明記します。Producer側でも完成したartifactと署名結果を、想定するconsumerの検証条件で照合します。自己署名した公開鍵をbundleから読み取り、そのまま信頼根拠にする確認は無意味です。

成果物への署名と来歴の検証は別です。検証器の設定で対象との照合を外さず、採用形式に必要な条件を確認します。製品固有の例と確認範囲は[署名資料の採否](../../../../sources/README.md#ref-artifact-signing-boundary-001)を参照してください。

## 必要な材料を取得できてから公開完了にする

Artifact digestから署名と必要な証明書・bundle等を発見でき、想定利用者の権限で取得・検証できることを確認します。Bundleが署名を含んでいても、公開先へ実際に置けたかは別です。採用profileが透明性ログや時刻証拠を要求するなら、その検証可能な証拠が欠けた結果を成功にしません。公開先の変更不能性と保持期間はartifactの利用期間に合わせ、可変URLの自己申告に頼りません。

公開を許可する判定では、`SIGNED_AND_AVAILABLE`、`REJECTED`、`ERROR`を区別します。不一致や未承認は`REJECTED`、署名器・検証器・状態情報・公開先の障害は`ERROR`です。どちらもreleaseを完了しません。再試行時は今回のexact digestと署名結果の対応を再確認し、古い成功receiptを使い回しません。一般ログにはdigest、署名者と方針の版、判断、公開先の識別子、時点だけを残し、認証情報や鍵を出しません。

`SIGNED_AND_AVAILABLE`は署名についての結果です。必要なprovenanceの配布、release SBOMの公開、成果物自体の公開など、採用先が要求する別の条件も揃えてからrelease全体を完了します。利用者側の受入れと実際の使用許可は、さらに別の判断です。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 承認後に成果物のbytesやdigestを変えても、前の承認で署名できないか。
- 可変tag、別release・別workload、期限切れの権限で署名できないか。
- 署名権限を持つjobが、未承認の別成果物まで署名できないか。
- 有効な署名でも、別の成果物へ付け替えたり、未承認のsignerを使ったりできないか。
- 必要な検証材料が欠ける、利用者が取得できない、署名器や公開先が止まる場合もrelease完了にしていないか。
- 判断記録やログへidentity token・秘密鍵・不要な署名本文を残していないか。

これらは診断・設計レビューの確認項目であり、live署名サービスや配布先で試した結果ではありません。

## フレームワークとの関係

- NIST SSDF 1.1 PS.2.1: 承認した成果物の正確な内容へ署名し、利用者が検証に必要な情報を得られるようにする部分を支えます。実際の鍵の保護、署名・公開、利用者による検証は別に確認します。

対象特性と根拠は[マッピング](../../../../mappings/frameworks.yaml)にあります。設計上の部分的な関係で、SSDFへの準拠や署名運用の完了を示しません。

## このコントロールの範囲

対象はproducer側の成果物署名と、その署名を利用者へ渡すまでです。Workload identityの発行は[CICD-006](../../cicd-security/psb-cicd-006-workload-federation-boundary/README.md)、build来歴の生成は[BUILD-003](../../build-security/psb-build-003-platform-provenance-generation/README.md)、利用者側の受入は[REL-001](../psb-rel-001-signature-provenance-verification/README.md)へ渡します。署名の成功だけでは成果物の無害性や来歴の正しさを示せません。

署名権限、形式、公開経路の選び方は[署名方式と権限](#対象の承認と署名権限を分ける)を参照してください。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料と採否](../../../../sources/README.md#ref-artifact-signing-boundary-001)、[移行記録](../../../../docs/MIGRATION_RELEASE.md#artifact-signing-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

工程間の受け渡しは[ビルドした成果物を署名・公開し、使用するまで](../../../../engineering/release-build-to-use.md)で確認できます。
