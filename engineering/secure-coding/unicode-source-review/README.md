# Unicode source review

対象：[PSB-CODE-005](../../../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md) · 試す：[Pythonの限定実装](implementations/python/README.md)

レビュー画面と処理系が同じソースを違って見せる時、どこで気付けるようにするかを設計します。たとえばPythonの`pаyload`（2文字目だけキリル文字）は別の名前でも、フォントによって`payload`に見えます。投稿者、表示器、処理系、受入側を別の主体として扱います。

## 強制点を置く

まずレビュー対象のrevision、言語、pathを定めます。レビューUIやeditorでは不可視文字・双方向の影響を見せ、字句構造に沿う表示を選びます。静的検査は元のソースを読み、言語のtokenと元の綴りを照合します。受入側のCIで同じrevisionを検査する場合、検査script・対象path・例外方針を投稿者が変更できるかを確認します。ローカルhookは早いfeedbackですが、投稿者の端末にあるため最終的な受入条件にはなりません。

## 選択肢と代償

| 方式 | 向く状況 | 限界 |
|---|---|---|
| Editor／review UIで字句構造と不可視文字を表示 | 多言語のコメント・文字列・識別子を使う | 全員の表示環境と差分経路に適用する必要がある |
| 言語に合わせた検査と命名profile | 受入時に機械的な拒否を置きたい | 言語の字句規則、source encoding、生成物、例外を管理する必要がある |
| ASCII識別子など狭いprofile | 識別子に多言語名を必要としないPython等のプロジェクト | 正当な多言語識別子を拒否する。文字列・コメントも一律禁止する理由にはならない |

識別子のconfusable判定はUnicode UTS #39／#55を参照して設計できます。ただしscriptの混在だけを拒否しても、単一scriptの紛らわしい名前を見落とします。PythonのNFKC判定も、その言語の意味に基づく限定策です。他言語へ同じ規則を移しません。

## 失敗経路と確認

- 見える差分だけを審査し、元のcode pointを表示しない。
- ソースをテキストとして読む検査が、実際のsource encodingや字句規則と食い違う。
- 構文エラーや対象ゼロ件を`PASS`にする。
- PRが検査scriptやCI設定を変更し、同じPRでその弱い検査を合格させる。
- 厳格な拒否条件をすべての言語と多言語テキストへ一律に適用する。

診断に使う具体的な入力と観点は[control](../../../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md#failure-checks)に置きます。[Python例](implementations/python/README.md)は実ファイルを読む局所的な検出を実装します。Protected CI設定とreview UI表示は採用先で接続・確認します。

## 根拠

- [Unicode Source Code Handling](../../../sources/README.md#spec-unicode-source-handling-2)
- [Pythonの字句規則](../../../sources/README.md#spec-python-source-lexical-3-10)
- [移行記録](../../../docs/UNICODE_SOURCE_MIGRATION.md)
