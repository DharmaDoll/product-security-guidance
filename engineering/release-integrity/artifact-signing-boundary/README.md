# ENG-REL-005: Artifact signing boundary

## 利用場面と推奨構造

Build後の成果物へ署名を付けるproducer向けです。署名は正しいbytesと正しい権限が出会って初めて意味を持ちます。release jobが署名器を呼べることだけを合格条件にしません。

```text
review済みrelease決定 ──> artifact family / release ID / exact digest / signer policy
                               |                         |
build後のartifact bytes ──> digestを計算・固定 ──> 対象一致の認可
                                                    |
                                      限定されたsignerで署名
                                                    |
                                consumer条件で検証・公開先から取得
                                                    |
                                      全て揃ったときreleaseを完了
```

## 1. 署名対象を確定する

承認者が判断したrelease IDと成果物を、署名要求の前にdigestで固定します。署名器には、承認記録にあるdigestと、実際に署名するbytesまたはOCI manifestから計算したdigestが一致することを強制できる場所を設けます。署名後に別のファイルを同名で置く、registry tagを動かす、bundleを別digestに添付する経路も確認します。Source revisionやbuild IDは追跡に役立ちますが、署名したbytesとの関係を別に検証しなければ同一性の代わりにはなりません。

## 2. 対象の承認と署名権限を分ける

Workload federationは「誰が署名サービスへ接続できるか」を決めます。署名対象の承認は「今回どのdigestを署名してよいか」を決めます。OIDC claim、KMS key policy、署名サービスのoperation権限、release manifestへの書込権限を、採用環境でそれぞれ確認します。Tokenを短寿命にしても、すべてのartifactを署名できる権限なら対象のすり替えは残ります。

| 方式 | 選ぶ条件 | 確認する失敗経路 |
|---|---|---|
| Identityを使う短期鍵 | 対象のissuer・identity・発行時刻・検証材料をconsumerが扱える | 別workflow identity、必要な時刻や透明性証拠の欠落、信頼根拠の更新 |
| KMS/HSM等の管理鍵 | 鍵へのsign権限、鍵状態、鍵の交代、consumerの公開鍵配布を管理できる | 別jobや別releaseからのsign呼出し、失効鍵、広いkey policy |
| 自己管理鍵 | 保管・使用・交代・事故対応を実際に強制できる限定環境 | CI workspaceやlogへの鍵複製、共有鍵の長期利用、更新失敗 |

非exportable鍵やsign-only operationは有力な保護手段ですが、全方式の同一形式の必須値とはしません。どの方式でも、鍵やidentityの発行・使用・失効と、release対象の認可を別々に示します。

## 3. 署名結果を利用者の条件で検証する

採用した署名形式を一つ選び、署名の対象、署名者を特定する材料、利用者が事前に管理する信頼根拠を明記します。Producer側でも完成したartifactと署名結果を、想定するconsumerの検証条件で照合します。自己署名した公開鍵をbundleから読み取り、そのまま信頼根拠にする確認は無意味です。

Sigstore/Cosignで通常のfileを選ぶなら、公式文書の`cosign sign-blob <file> --bundle ...`が具体的な出発点です。検証では同じfileとbundleを`cosign verify-blob`へ渡し、keylessなら期待するcertificate identityとOIDC issuerを指定します。OCI imageではfileと異なり、immutable digestとregistry上のsignature relationを選びます。Cosign binary自身の取得・検証もrelease経路の一部です。これらのコマンドだけでrelease承認、signer権限、公開、gateは成立しません。

## 4. 公開完了を確かめてからreleaseを開く

Artifact digestから署名と必要な証明書・bundle等を発見でき、想定利用者の権限で取得・検証できることを確認します。Bundleが署名を含んでいても、公開先へ実際に置けたかは別です。採用profileが透明性ログや時刻証拠を要求するなら、その検証可能な証拠が欠けた結果を成功にしません。公開先の変更不能性と保持期間はartifactの利用期間に合わせ、可変URLの自己申告に頼りません。

Release gateは`SIGNED_AND_AVAILABLE`、`REJECTED`、`ERROR`を区別します。不一致や未承認は`REJECTED`、署名器・検証器・状態情報・公開先の障害は`ERROR`です。どちらもreleaseを完了しません。再試行時は今回のexact digestと署名結果の対応を再確認し、古い成功receiptを使い回しません。一般ログにはdigest、signerとpolicy版、判断、公開先識別子、時点だけを残し、credentialや鍵を出しません。

## 典型的な失敗経路

- 承認したtagの先を署名直前に更新し、正規の鍵で別bytesへ署名する。
- KMS鍵は持ち出せないが、侵害されたjobが任意のdigestを署名できる。
- 正しい署名とbundleを別artifactのreleaseへ付け替える。
- 署名job成功だけでreleaseを進め、bundle公開失敗やconsumer取得不能を見逃す。
- JSONに`immutable`、`included`、`active`と記したfixtureを、実storage、透明性ログ、鍵状態の証拠と誤認する。

## 具体化判断

旧実装のOpenSSL Ed25519検証は署名とbytesの対応を実値で確認します。一方、独自statement形式と自己申告のsigner・publication・transparency・gate状態を、実運用の完成形として移す価値はありません。本移行ではcontrol、教材、pattern、診断観点を完成させ、実装例は保留します。

実装時は一つのartifact形式、署名方式、signerまたはkey provider、release承認の正本、公開先、consumerの信頼条件、使い捨てのrelease先を選びます。対象versionとclient binaryを固定し、導入・解除手順を付けます。正常署名だけでなく、別digest・別identity・停止したsigner・公開失敗・consumer取得不能がreleaseを止めることを実値で観測できたときに、限定名の実装例として追加します。単にlocal keyで署名して検証する例を、release signing全体の実装完了とはしません。

## このpatternの境界

[REL-005](../../../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)の`ART-SIGN-1〜7`を、対象確定、認可、鍵管理、署名、公開、gate、証拠へ配置します。[CICD-006](../../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)がworkload認証、[BUILD-003](../../../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)が来歴生成、[REL-001](../../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)がconsumer受入、[GOV-004](../../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)が漏えい時の旧権限停止を扱います。

## 根拠

- [REF-ARTIFACT-SIGNING-BOUNDARY-001](../../../sources/README.md#ref-artifact-signing-boundary-001)
- [移行記録](../../../docs/ARTIFACT_SIGNING_MIGRATION.md)
