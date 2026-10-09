# PSB-CODE-005: Unicode source review

**レビュー画面に見えるコードと、言語処理系が読む文字の違いに気付けるか。**

## なぜ必要か

たとえばコメント内の双方向制御文字でコードの表示順が変わると、レビュー担当者は実際とは違う内容を承認するかもしれません。見えない文字や、似ていて別の識別子も同じ問題を起こします。

## 満たすべきこと

- 対象の言語、ファイル、revisionを決め、実際の文字と処理系が読む構造を確認できるようにする。
- 双方向制御文字、不可視文字、表示だけで改行に見える文字を、言語と文脈に応じて評価し、紛らわしい変更を受入前に見つける。
- 識別子の元の綴りと処理系による解釈を比べ、見た目が似た別名や正規化による違いを見落とさない。
- 採用した検査を、レビューしたrevisionの受入時に適用する。投稿者が検査設定を変えたり、別経路で通したりしても、無言で迂回できないようにする。
- 対象漏れ、文字コード・構文の不正、検査の失敗を「問題なし」にしない。調査に必要な位置、分類、code pointを示す。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- コメントや文字列の双方向制御文字、不可視文字、表示だけで改行に見える文字を見落とさないか。
- 似た別文字や正規化によって識別子の意味が変わる場合、採用した言語・命名方針で評価できるか。
- 検査対象外のファイル、読めない文字コード、構文エラー、検査ツールの障害を成功として報告しないか。
- 投稿者が同じ変更で検査設定を弱めたとき、受入側が気付けるか。

これは設計レビューや診断で使う項目であり、各repositoryで試験した記録ではありません。

## フレームワークとの関係

現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)には、このControlへの個別の対応関係を登録していません。Unicode仕様は文字の表示・解釈を調べる直接の資料ですが、仕様への準拠やASVSの特定要件をここから主張しません。参照した仕様と採否は[Sources](../../../../sources/README.md#spec-unicode-source-handling-2)から確認できます。

## このコントロールの範囲

対象はソースの表示と解釈の食い違いです。通常の多言語テキストもあるため、非ASCII文字の一律禁止は求めません。すべてのフォントやreview UI、悪意あるコード全般の検出も保証しません。[Pythonの限定実装](../../../../engineering/secure-coding/unicode-source-review/implementations/python/README.md)は一つの設定例で、Unicode仕様への完全準拠を示すものではありません。秘密情報の混入は[SOURCE-002](../../source-protection/psb-source-002-secret-publication-boundary/README.md)が扱います。

[教材](learning.md) · [設計パターン](../../../../engineering/secure-coding/unicode-source-review/README.md) · [Unicode Source Code Handling](../../../../sources/README.md#spec-unicode-source-handling-2) · [Unicode Security Mechanisms](../../../../sources/README.md#spec-unicode-security-mechanisms) · [移行記録](../../../../docs/UNICODE_SOURCE_MIGRATION.md)
