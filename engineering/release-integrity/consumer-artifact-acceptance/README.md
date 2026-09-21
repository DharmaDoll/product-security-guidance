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

## 検証を置く場所と代償

| 場所 | 利点・残る境界 |
|---|---|
| Registryの登録時 | 多くの利用者へ一括適用できる。登録後のregistry侵害・再配布・使用直前の差替えは別 |
| Consumerの取得・使用時 | 利用者の期待値と実際のbytesを照合できる。Verifier配布、policy更新、全使用経路のgateが必要 |
| 継続monitor | 多数の成果物の変化を監視できる。通知だけでは使用を止めない。利用者の対応と結合が必要 |

期待値をproducerから提供してもらう場合も、認証した変更経路と利用者の承認を用意します。
新鍵、builder、repository、最低信頼条件を自動学習せず、変更レビューと適用期限を管理します。

## 実装で確認する拒否と障害

無害な試験成果物と試験鍵で、bytes差替え、不正署名、未承認署名者、正規署名だがwrong builder・source・parameter、
信頼signal欠落を拒否するか確認します。正規署名の想定外条件も必要であり、parse失敗だけでは代替できません。
Parser・crypto tool・証跡取得の障害を別に発生させ、使用gateが閉じ、違反と`ERROR`が区別されるか確認します。

固定公開鍵なら、鍵の配布・rotation・失効を管理します。Keylessならissuer・certificate identity・trust root・有効期間・
方式固有のtransparency証拠等を検証します。方式の違いを単一の`signature_valid`フラグへ隠しません。
Digest照合後も同じbytesを使い、可変tagの再解決や未検証pathへの切替を許可しません。

## 今回移植しない実装

旧実装はEd25519で来歴JSONのbytesへ署名する限定fixtureです。一般的なenvelope・keyless検証を実装するものではありません。
現行ツリーではpolicyが参照する公開鍵ファイルが欠け、OpenSSLの非ゼロ終了をすべて署名不正へ分類する処理もあります。
公開鍵を捏造して既存署名を通したり、fixtureの成功を組織導入に置き換えたりせず、独立実装の再レビューへ保留します。
実署名照合、失効・timestamp・transparency、使用gateは今回は未確認です。

- [Control](../../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)、[教材](../../../docs/learning/authentic-is-not-acceptable.md)
- [Build execution boundary](../../build-security/build-execution-boundary/README.md): 限定した実行権限から出力の受入判断へ引き継ぐ
- [仕様・採否](../../../sources/README.md#spec-consumer-artifact-verification)
