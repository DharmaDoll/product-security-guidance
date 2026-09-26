# PSB-REL-005: Artifact signing generation

学ぶ：[署名が正しくても、署名した対象が違う](learning.md) · 設計する：[Artifact signing boundary](../../../../engineering/release-integrity/artifact-signing-boundary/README.md)

## 問い

リリース担当者は、承認した成果物そのものに、許可した主体だけが署名したことを確かめ、署名を利用者へ渡せるまでリリースを完了させないか。

## できてはいけないこと

正規の署名鍵を使えても、`latest`が後から指す別の成果物、承認時と異なるbytes、別リリースの成果物へ署名してはいけません。署名権限を持つだけで、どの成果物にも署名してよいことにはなりません。署名の生成、検証、必要な公開に失敗したリリースを、署名済みとして配布してはいけません。

## 適用範囲と非適用

Build後に確定したrelease artifact、署名要求、署名権限と鍵、署名結果、利用者へ渡す検証材料、リリース完了判定が対象です。ファイルとOCI imageでは署名対象と配布方式が異なるため、対象と形式を採用時に明記します。

[CICD-006](../../cicd-security/psb-cicd-006-workload-federation-boundary/README.md)はworkload identityの発行、[BUILD-003](../../build-security/psb-build-003-platform-provenance-generation/README.md)はbuild来歴の生成を扱います。本controlは成果物への署名を作るproducer側の境界です。[REL-001](../psb-rel-001-signature-provenance-verification/README.md)がconsumerの期待値と照合し、[REL-002](../psb-rel-002-provenance-distribution-availability/README.md)はprovenanceの配布を扱います。署名の公開は本controlの責任として残し、provenance配布済みから推定しません。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `ART-SIGN-1` | 承認したreleaseと変更不能なartifact bytesまたはdigestを決め、署名器へ渡す実際の対象と再照合する。ファイル名や可変tagだけを同一性にしない |
| `ART-SIGN-2` | 署名操作を対象workload、signer、releaseへ限定し、短い有効期間と再利用範囲を採用方式に応じて強制する。job内の自己申告だけで権限を証明しない |
| `ART-SIGN-3` | 鍵またはidentityの保管、許可操作、状態、交代を管理する。未信頼のbuild処理や一般的な編集権限から署名権限を分離する |
| `ART-SIGN-4` | 採用した形式でexact artifactへ署名し、予定するconsumerの信頼根拠・署名者条件で結果を検証する。暗号署名の成功だけで対象の正当性を決めない |
| `ART-SIGN-5` | 署名と必要な検証材料をexact artifactから取得できるよう公開し、採用profileが要求する時刻・透明性などの証拠も揃える。保存したという自己申告を公開完了にしない |
| `ART-SIGN-6` | 署名・検証・必要な公開の失敗や評価不能をrelease gateで止める。暗黙のunsigned fallbackを設けない |
| `ART-SIGN-7` | 対象digest、signer、policy版、判断、公開先と確認時点を記録し、token・秘密鍵・不要な署名本文を一般ログへ複製しない |

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 承認後にartifactのbytesやOCI digestを差し替えても、前の承認で署名できないか。
- 可変tag、別releaseのrequest、別workloadの資格情報、期限切れの権限を使って署名できないか。
- 署名権限を持つjobが、未承認の別成果物まで署名できる経路がないか。
- 使用停止した鍵、予期しない署名者、別の信頼根拠で生成した署名をrelease成功にしないか。
- 署名は有効でも、別のartifactへbundleや署名を付け替えたとき拒否できるか。
- 採用profileで必要な証拠が欠ける、署名公開先から取得できない、公開対象が変わる場合にreleaseを止めるか。
- 署名器、検証器、状態取得、公開先の停止やtimeoutを成功または「署名不要」へ変えないか。
- 一般ログや判断記録へidentity token、秘密鍵、過剰な署名・証明書本文を残さないか。

これらは設計・診断の確認項目です。live署名サービスや配布先で拒否を確認した結果ではありません。

## このcontrolが直接保証しないこと

正規の権限を持つ侵害されたrelease担当者が悪意ある成果物に署名しないこと、成果物の無害性、build provenanceの真実性、consumerが期待する署名者として受け入れることは保証しません。特定のKMS、HSM、Sigstore、透明性ログやSLSA Build levelの採用も意味しません。

## 根拠と関係

- [REF-ARTIFACT-SIGNING-BOUNDARY-001](../../../../sources/README.md#ref-artifact-signing-boundary-001)
- [移行記録](../../../../docs/ARTIFACT_SIGNING_MIGRATION.md)
- [成果物マッピング](../../../../mappings/pilot.yaml)
- [Frameworkマッピング](../../../../mappings/frameworks.yaml)
