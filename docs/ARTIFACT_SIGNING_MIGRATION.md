# PSB-REL-005 Artifact signing generation 移行記録

## 結論

旧`PSB-REL-005`を[Artifact signing generation](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)へ移行しました。署名対象の確定、対象の承認と署名権限、鍵の管理、署名結果の検証、公開完了、release gateを分けました。[教材](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/learning.md)、[設計pattern](../engineering/release-integrity/artifact-signing-boundary/README.md)、診断観点を追加しました。

旧verifierはOpenSSLでEd25519署名を検証し、artifactの実bytesをhashしていたため、その部分の観測価値はあります。しかし旧`generate_fixture_bundle.py`はlocal fileのprivate keyで署名し、KMS/HSM、鍵の非export性、公開先の変更不能性、透明性ログの包含、release gateの状態をJSONへ書いていました。旧verifierの`PASS`はその主張をlive providerで確認していません。独自statementと合成receiptを新しいrelease signing実装として移植しません。

## 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/scripts/verify.py)
- [旧fixture generator](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/scripts/generate_fixture_bundle.py)

## 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `ASG-001` exact release artifact | `ART-SIGN-1` | 実bytes/digestの固定を保持。Git tag・full revisionを全artifactへ一律要求しない |
| `ASG-002` short-lived authorization | `ART-SIGN-2` | 対象と操作を限定。固定5分、nonce形式、OIDC audienceを全方式の普遍要件にしない |
| `ASG-003` signer state | `ART-SIGN-3` | 鍵・identityの保護と状態確認を保持。非exportable KMS/HSM/keylessという固定列挙は方式の選択肢にする |
| `ASG-004` signed statement | `ART-SIGN-1・4` | 対象と承認の結合を保持。独自statement envelopeを標準としない。自己申告の署名時刻をtrusted timestampとしない |
| `ASG-005` signature validity | `ART-SIGN-4` | 採用形式とconsumer信頼根拠で実暗号検証する。Ed25519と固定公開鍵digestは限定profileの選択 |
| `ASG-006` publication / transparency | `ART-SIGN-5` | exact artifactから署名を取得できることを保持。HTTPS、透明性ログ、公開形式は選択したprofileに従う |
| `ASG-007` release gate | `ART-SIGN-6` | 必要な署名・検証・公開が揃わないreleaseを止める。fixtureの`BLOCK`値を実gateの証拠にしない |
| `ASG-008` minimal evidence / errors | `ART-SIGN-6・7` | 秘密情報を複製せず、評価不能を成功にしない |

## 主題ごとの具体化判断

今回必要な成果物は、provider-neutralなcontrol、教材、実装判断に使うpattern、診断観点、参照資料、mappingです。具体実装は作りません。署名対象をfileとOCI manifestのどちらにするか、signer、release承認の強制点、公開先、consumerの信頼条件が未選定だからです。旧local cryptographyだけを移してもsigner custody、対象認可、公開、release gateは実証できません。

実装を再開する条件と完了条件は[pattern](../engineering/release-integrity/artifact-signing-boundary/README.md#具体化判断)へ記載しました。Sigstore/Cosignの公式`sign-blob`/`verify-blob`は採用候補として明記し、特定方式への実装済み・導入済みという主張はしません。

## 参照資料とmapping

旧`REF-REL-003`は[新しい役割別記録](../sources/README.md#ref-artifact-signing-boundary-001)へ再編集しました。2026-09-26にSigstoreのblob署名、検証、binary取得・検証の公式文書とNIST SSDF 1.1 `PS.2.1`を確認しました。Cosign固有のbundle、certificate identity、透明性証拠を、全方式に必須のフィールドへ変換しません。

NIST SSDF 1.1 `PS.2.1`は署名を含むsoftware integrity verification informationを取得者へ提供する課題です。`ART-SIGN-4・5・6`を`supports / medium / design-reviewed`で部分割当します。旧`high` confidenceは実公開が未確認のため継承しません。旧OpenSSF `OSPS-BR-06.01`、`OSPS-AC-04.01`、ATT&CK `T1553.002`は、今回その正確な版と要件本文で再照合していないため新しいmappingへ継承しません。脅威との関連をframework準拠や防御完了とは扱いません。[SLSA Build Track Basics 1.2](https://slsa.dev/spec/v1.2/build-track-basics)を2026-09-26に再確認し、Build L2が署名を要求する対象はprovenanceであって、独立したartifact signing要件ではないため、本controlをSLSA Build levelへ割り当てません。

## 完了範囲と残る作業

7特性のcontrol、教材、pattern、診断観点、参照資料、framework・成果物・横断mappingを追加しました。実signer、key policy、署名・公開・取得、gateの拒否は未実施です。次の移行候補は旧`PSB-BUILD-002`のHosted consistent buildとし、builderの承認、一貫したbuild定義、利用者が変更できる範囲を選別します。
