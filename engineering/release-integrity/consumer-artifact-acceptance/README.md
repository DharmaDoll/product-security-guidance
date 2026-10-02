# ENG-REL-001: Consumer artifact acceptance

## 利用場面と推奨構造

取得した成果物を公開・install・deployへ渡す前に、利用者の期待値で受け入れる設計です。
検証する場所と、失敗時に使用を止める場所を選べるようにします。

```text
利用者の独立した承認 → 信頼根拠・期待値のpolicy
                              ↓
未信頼のartifact・来歴・署名 → 隔離して照合 → 同じdigestのbytes → 使用gate
                              ↓
                     違反／評価不能 → 使用停止・理由別の調査
```

受取処理に成果物のコードを実行させず、policyを成果物の書込権限から分離します。
認証した署名者とbuilderの組合せを確認し、build typeの意味に沿って外部parameterを照合します。
Unknown parameterは既定で拒否し、安全性を判断したものだけ許容します。

署名対象の種類も先に確認します。成果物への署名、ビルド来歴、SBOMなどの別の証明を混同せず、採用形式で必要な種類を検証します。SLSA Provenance v1なら`predicateType`も照合します。成果物署名を要求する場合は[Artifact signing boundary](../artifact-signing-boundary/README.md)から検証材料を受け取り、来歴の取得は[配布設計](../provenance-distribution-and-availability/README.md)へ接続します。

## 検証を置く場所と代償

| 場所 | 利点・残る境界 |
|---|---|
| Registryの登録時 | 多くの利用者へ一括適用できる。登録後のregistry侵害・再配布・使用直前の差替えは別 |
| Consumerの取得・使用時 | 利用者の期待値と実際のbytesを照合できる。Verifier配布、policy更新、全使用経路のgateが必要 |
| 継続monitor | 多数の成果物の変化を監視できる。通知だけでは使用を止めない。利用者の対応と結合が必要 |

期待値をproducerから提供してもらう場合も、認証した変更経路と利用者の承認を用意します。
新鍵、builder、repository、最低信頼条件を自動学習せず、変更レビューと適用期限を管理します。

## 実装で確認する拒否と障害

採用した検証器と使用経路で、[controlの診断項目](../../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md#failure-checks)を確認します。無害な試験成果物と試験鍵を使い、検証器の結果に加えて使用が止まったことを観測します。正規署名の想定外条件も必要であり、解析失敗だけでは代替できません。

固定公開鍵なら、鍵の配布・rotation・失効を管理します。Keylessならissuer・certificate identity・trust root・有効期間・
方式固有のtransparency証拠等を検証します。方式の違いを単一の`signature_valid`フラグへ隠しません。
Digest照合後も同じbytesを使い、可変tagの再解決や未検証pathへの切替を許可しません。

検証結果を別の処理へ渡す場合は、対象digest、使用したpolicy版と信頼根拠、判断と確認時点を結び付け、成果物側から結果を差し替えられないようにします。使用直前の再検証か、保護された結果と変更不能な対象の照合を選びます。前者は検証基盤の可用性、後者は結果の保護とpolicy変更時の再評価が必要です。

## 今回移植しない実装

旧実装はEd25519で来歴JSONのbytesへ署名する限定fixtureです。一般的なenvelope・keyless検証を実装するものではありません。
旧ツリーの移行レビューではpolicyが参照する公開鍵ファイルの欠落と、OpenSSLの非ゼロ終了をすべて署名不正へ分類する処理を記録しています。
今回の成果物は文書と診断項目で完了とし、旧fixtureは移植しません。採用する検証器・版、署名形式、信頼根拠、実際の使用経路が決まり、導入や拒否確認に役立つ場合だけ限定実装を検討します。
実署名照合、失効・timestamp・transparency、使用gateは今回は未確認です。

- [Control](../../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)、[教材](../../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/learning.md)
- [Build execution boundary](../../build-security/build-execution-boundary/README.md): 限定した実行権限から出力の受入判断へ引き継ぐ
- [仕様・採否](../../../sources/README.md#spec-consumer-artifact-verification)
