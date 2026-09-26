# PSB-REL-004 Supplier SBOM 移行記録

## 結論

旧`PSB-REL-004`を[Supplier SBOM intake trust](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)へ移行しました。供給者から受け取ったSBOMを通常の部品台帳へ入れる前に、利用者側の期待値、出所と内容、対象製品・成果物、形式と欠落、隔離と評価不能、訂正・撤回、取込先を判断します。[設計パターン](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)と教材、診断観点を作りました。

旧実装の合成Ed25519 envelopeは移植していません。暗号計算とbytes照合は実際に行いますが、独自envelope、手書きの署名者状態、JSONで自己申告する台帳権限では、実際の供給者からの受入れを示せません。署名方式と供給者を選ばない段階で独自形式を標準経路にしない判断です。

旧envelopeの`signed_at`は署名対象に含まれる自己申告時刻であり、それだけで署名がその時刻に行われた証拠にはなりません。旧test用の`--as-of`とstatus snapshotも現在の失効状態を証明しません。時刻・失効の判断は、採用する方式の検証可能な証拠と信頼した状態sourceを選んでから実装します。

## 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/scripts/verify.py)
- [利用者提供のSBOM lifecycle資料](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)

## 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `SUP-001` 署名者の認証 | `SUP-INTAKE-1・2` | 利用者側の信頼根拠と出所確認を保持。Ed25519だけを全供給者の唯一方式にしない |
| `SUP-002` 製品と成果物の同一性 | `SUP-INTAKE-3` | 署名付きでも別製品を拒否する成果を保持。SBOMと実成果物のdigest関係を認証された情報で確かめる |
| `SUP-003` CycloneDX構造 | `SUP-INTAKE-4` | 対応形式・版と参照関係を検証。形式の成功を網羅性にしない |
| `SUP-004` 署名者の有効状態 | `SUP-INTAKE-2・6` | 時刻・失効・交代を採用方式ごとに評価。現在の期限だけで過去の署名を一律に決めない |
| `SUP-005` 隔離 | `SUP-INTAKE-5` | 不一致と評価不能を分け、どちらも通常取込を止める |
| `SUP-006` 取込権限 | `SUP-INTAKE-7` | 正確な取込先と必要な操作だけを許す。JSONの許可一覧では実権限を証明しない |
| `SUP-007` 証拠の最小化 | `SUP-INTAKE-7` | 判断に必要な値だけを残す。供給者の非公開inventoryをログへ複製しない |
| `SUP-008` 検証障害 | `SUP-INTAKE-5` | 暗号検証器・状態取得の失敗を受入成功にしない |

## 主題ごとの具体化判断

読者が今できるべき判断は、受渡し方式、利用者側の期待値、署名者または配送元の信頼根拠、成果物との結び方、通常台帳へ渡す条件の選択です。供給者と方式を選ばずに具体実装を置くと、旧fixtureと同じ独自envelopeを正解に見せます。そのため今回はcontrol、教材、pattern、診断観点、参照資料、mappingを必要な成果物とし、実装例は作りません。

実装を再開する条件は、供給者と対象製品・成果物、署名または認証済み配送方式、利用者側の信頼根拠、時刻・失効・訂正のsource、使い捨ての台帳取込先を具体的に選べることです。完了には、実際に検証したbytesの使用、正常な受入候補、別製品・改変・未知署名者の隔離、状態取得・検証器障害の`ERROR`、通常台帳への迂回拒否を観測できる必要があります。固定公開鍵だけの暗号テストを、供給者受入れの完了とはしません。

## 参照資料と境界

2026-09-25にCISAのSBOM consumption資料、CycloneDX 1.7、Sigstore bundleの公式文書、NIST SSDF 1.1を確認しました。CISA資料はSBOMの出所・完全性を配送方法も含めて確認し、不一致を取込前に解消する判断を支えます。署名は一つの方式であり、すべての供給者へ同じ方式を要求する根拠にはしません。採否と限界は[REF-SUPPLIER-SBOM-INTAKE-001](../sources/README.md#ref-supplier-sbom-intake-001)に保持します。

[REL-003](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)のCycloneDX限定実装は自組織のfinal artifactとbuild／post-build SBOMを結ぶものです。供給者から受け取った署名の身元や調達対象を判定する道具として再利用しません。[REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)の成果物使用判断とも別です。

## Framework mapping

NIST SSDF 1.1 `PW.4.1`を`SUP-INTAKE-1〜4・6`へ`supports / medium / design-reviewed`で部分割当します。第三者componentの出所情報を取得・維持し、採用リスクの評価へ渡す一部を支援します。供給者製品やcomponentの安全性、採用審査全体、準拠は主張しません。

旧`RV.1.1`は継承しません。潜在的な脆弱性情報の収集・調査は本controlの直接の成果ではなく、REL-003の分析やGOV-001の影響調査へ渡す仕事です。

## 完了範囲と残る作業

7特性のcontrol、教材、設計pattern、診断観点、参照資料、framework・成果物・横断mappingを追加しました。旧実装の暗号テストが成功していたことと、供給者の認証・失効・通常台帳での隔離が実証されたことを区別しています。実供給者、実署名・配送方式、状態source、台帳取込を使う実装と評価は未実施です。次の移行候補は旧`PSB-REL-005`のartifact signing generationです。
