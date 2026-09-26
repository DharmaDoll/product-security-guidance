# PSB-CODE-005: Unicode source review

学ぶ：[同じに見えるコードが違う意味になる](learning.md) · 設計する：[Unicode source review](../../../../engineering/secure-coding/unicode-source-review/README.md) · 試す：[Pythonの限定実装](../../../../engineering/secure-coding/unicode-source-review/implementations/python/README.md)

## 問い

レビュー担当者は、画面に見えたコードと、言語処理系が読む文字・識別子の違いを、変更の受入前に見つけられるか。

## できてはいけないこと

たとえばコメント中の双方向制御文字によって行の見た目が変わり、レビュー担当者が「無害なコメント」と思った変更を、そのまま受け入れてはいけません。見た目が似た別の識別子や、処理系が正規化して同じ名前とみなす綴りも、気付かないまま通常の変更として扱ってはいけません。

## 適用範囲と境界

レビュー対象のソース、表示・差分表示、言語の字句解釈、受入判定が対象です。文字列やコメントには正当な多言語テキストが入ります。すべての非ASCII文字を禁止することは、このcontrolの要件ではありません。採用する言語、表示環境、識別子の命名規則に合わせて、どの文字を見せ、警告し、拒否するかを決めます。

[SOURCE-002](../../source-protection/psb-source-002-secret-publication-boundary/README.md)は秘密情報の混入を防ぎ、[DETECT-001](../../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)は検査結果の信頼性を扱います。本controlはソース文字と解釈の食い違いに絞ります。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `UNICODE-SOURCE-1` | 対象言語、path、revisionを決め、レビューで文字の実体と字句構造を確認できる |
| `UNICODE-SOURCE-2` | 双方向・不可視文字の扱いを文脈に応じて決め、見た目を偽る使い方を受入前に見つける |
| `UNICODE-SOURCE-3` | 元の識別子の綴りと処理系の解釈を比べ、紛らわしい別名・正規化差分を見落とさない |
| `UNICODE-SOURCE-4` | 採用した検査を、レビューするrevisionの受入経路で実行し、投稿者が設定変更や別経路で無言に迂回できない |
| `UNICODE-SOURCE-5` | 対象漏れ、文字コード・構文の不正、検査障害は「問題なし」にせず、調査に必要な位置・分類・code pointだけを出す |

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- コメントや文字列に双方向制御文字を入れて行を並べ替えて見せても、その文字の存在を確認できるか。
- 不可視文字で異なる文字列や識別子を同じに見せた変更を、差分表示だけで見落とさないか。
- 別scriptの似た文字を使う識別子、正規化で綴りが変わる識別子を、採用した言語と命名方針で評価できるか。
- 多言語の通常テキストを含む変更を、根拠のない一律の非ASCII禁止で妨げていないか。
- 検査pathから外れたファイル、symlink、読めない文字コード、構文エラー、tool障害を成功として報告しないか。
- 投稿者がCI定義、検査script、例外設定を同じ変更で書き換えた時に、受入側の方針が静かに弱くならないか。

これは設計・診断の確認項目です。各言語やrepositoryで受入拒否を確認した記録ではありません。

## このcontrolが保証しないこと

Unicodeの全ての紛らわしさ、すべてのフォントやreview UIの表示、悪意あるコードの全検出、アプリケーションの認可・入力処理の安全性は保証しません。Python実装は特定の厳格なprofileの例であり、UTS #39／#55への完全準拠を主張しません。

## 根拠と関係

- [Unicode Source Code Handling](../../../../sources/README.md#spec-unicode-source-handling-2)
- [Unicode Security Mechanisms](../../../../sources/README.md#spec-unicode-security-mechanisms)
- [移行記録](../../../../docs/UNICODE_SOURCE_MIGRATION.md)
