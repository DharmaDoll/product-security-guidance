# PSB-REL-005 Artifact signing generation

**承認した成果物そのものに、許可した主体だけが署名しているか。**

## なぜ必要か

例えば、正規の署名鍵を使っても、承認後に`latest`が指す先を変えれば別の成果物へ署名できます。署名できる権限と、今回どのbytesへ署名してよいかは別に決めます。

## 満たすべきこと

1. **署名対象を固定する。** 承認したreleaseと成果物のbytesまたはdigestを結び付け、署名器へ渡す実際の対象を再確認する（ART-SIGN-1）。File名や可変tagだけで判断しない。
2. **署名権限を限定する。** 署名できるworkload、操作、対象release、signer、期限を絞る（ART-SIGN-2）。鍵やidentityを保護・交代できるようにし、未信頼のbuild処理や一般の編集権限から分ける（ART-SIGN-3）。
3. **結果を検証して渡す。** 採用形式で正確な成果物に署名し、予定する利用者の信頼条件で結果を確認する（ART-SIGN-4）。署名と必要な検証材料を利用者が成果物から取得できるようにし（ART-SIGN-5）、署名・検証・公開の失敗ではreleaseを完了にしない（ART-SIGN-6）。対象、signer、判断結果を記録しつつ、tokenや秘密鍵を一般ログへ残さない（ART-SIGN-7）。

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

署名権限、形式、公開経路の選び方は[engineering](../../../../engineering/release-integrity/artifact-signing-boundary/README.md)を参照してください。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料と採否](../../../../sources/README.md#ref-artifact-signing-boundary-001)、[移行記録](../../../../docs/MIGRATION_RELEASE.md#artifact-signing-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
