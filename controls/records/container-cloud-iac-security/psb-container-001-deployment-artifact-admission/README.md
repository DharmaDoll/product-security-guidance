# PSB-CONTAINER-001 Deployment artifact admission

**実行する成果物をすべて確認し、現在の受入条件に合わなければ起動を止められるか。**

## なぜ必要か

例えば、main imageだけを確認しても、init containerやsidecarが未確認なら別のコードを起動できます。Tag、過去の「合格」表示、deployerが付けた`verified: true`だけで使用を許可してはいけません。

## 満たすべきこと

1. **実行するものを漏らさない。** Main、init、sidecar、ephemeralなど全artifactをrepositoryとdigestで特定する（ARTIFACT-ADMIT-1）。複数platformのimage indexを使う場合は、実行先が選ぶmanifestとの対応も追う。
2. **利用者の受入判断と結び付ける。** 署名、来歴、builder、source、入力などについて、利用者が現在採用する条件で判断した結果を、正確なdigestと対象環境へ結び付ける（ARTIFACT-ADMIT-2）。Mutationやtagの再解決後、実行へ渡す最終状態にも判断を適用する（ARTIFACT-ADMIT-3）。
3. **別経路と失敗を通さない。** 作成・更新・rollback・controller・直接作成など、実行物を変えられる全経路に同じ強制を適用する（ARTIFACT-ADMIT-4）。Artifactや判断材料を取得・評価できない場合は通常の起動を止める（ARTIFACT-ADMIT-5）。許可した結果は対象artifact群、環境、policy版、判断時刻へ結び付け、変更・失効・再評価を管理する（ARTIFACT-ADMIT-6）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Tagだけの参照や、別repository・別digest・別環境用の証拠を使って起動できないか。
- Image indexの確認結果を、対応が不明な別platformのmanifestへ流用できないか。
- Init、sidecar、ephemeral、debug用のartifactや、更新・rollback・直接作成の経路が検査を迂回しないか。
- Mutation後の差替え、評価後のtag解決変更、古い許可結果の再利用を許さないか。
- Registry、evidence、policy、評価器の欠落・timeout・部分失敗を、通常の許可へ変えていないか。
- 使用停止と決めたdigestを、古い許可結果、別tag、cacheから再投入できないか。

これらは診断・設計レビューの確認項目であり、実際のclusterでの拒否結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L2「Consumer validates authenticity」 | 実際に使う成果物を、利用者自身の期待値と照合してから許可する段階へつなぐ。 | 検証の中身はREL-001。受入実装とSLSA levelは未確認。 |
| SLSA Build provenance v1.2 | 来歴に記された成果物と、起動するdigestを同じ対象へ結び付ける。 | 来歴の取得・暗号検証はここでは行わない。 |
| NIST SP 800-190 §4.1.5 | 信頼する成果物の正確な同一性を起動前に確認する部分を支える。 | Registry管理、保守、実際の署名検証は別。 |
| NIST SP 800-190 §4.4.5 | 起動前の受入条件と、誰が何を許可したかの記録を支える。 | 配備権限や全ての不正起動経路は扱えない。 |

4件の対象特性と限界は[マッピング](../../../../mappings/frameworks.yaml)にあります。いずれも部分的な設計・受け渡しの関係で、実際の起動拒否や規格への準拠を示しません。

## このコントロールの範囲

対象はdeployment requestから実行へ渡す最終状態と、その受入を強制する全経路です。Registryでの公開と保持は[CONTAINER-002](../psb-container-002-container-registry-publication-boundary/README.md)、利用者の受入条件は[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)、実行後の観測は[CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。許可した成果物の無害性や、runtimeで同じbytesが動いたことまでは示しません。

Consumer verifierとadmissionのつなぎ方、判断結果の再利用、障害時の挙動は[engineering](../../../../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)で選びます。旧offline JSON verifierはliveのAPI経路やmutation後の状態を示さないため移植していません。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-deployment-artifact-admission-001)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#deployment-artifact-admission-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
