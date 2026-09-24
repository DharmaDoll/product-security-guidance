# Dependency change review — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)

## シナリオ：見えていない変更を承認する

更新ボットが直接依存を一つ更新します。画面にはそのpackageだけが表示されますが、lockfileでは複数の推移依存が
追加・変更されていました。脆弱性情報の取得も途中で失敗しましたが、結果は「問題なし」と表示され、変更がmergeされます。

依存更新の判断には、現在のbaseとheadの完全な差分、その差分へ適用した方針、判断に使った情報の取得状態が必要です。
表示された一部だけを見た承認や、情報不足を0件へ変えた判定は、変更全体の承認ではありません。

## 同一性の確認と採用判断を分ける

Lockfileとhashは、buildがレビューした内容を使うための手掛かりです。ただしhash一致は、packageの既知脆弱性、
license、取得元、保守状態、悪意の有無を判断しません。一方、依存差分を詳しくレビューしても、通常buildが別のbytesを
使えば判断との接続が切れます。実際の入力との一致は[Dependency artifact identity](../psb-deps-003-dependency-artifact-identity/learning.md)が扱います。

## 古い判断を使い回さない

レビュー後にheadが変わった場合や、baseが進んだ場合は現在の差分を再評価します。結果には対象revisionと方針の版を
結び付けます。変更時のレビューと、後から公開される脆弱性を探す継続的な検査は時間軸が異なります。

## 振り返りで問うこと

- 直接依存だけでなく、追加・削除・変更された推移依存を確認できるか。
- Baseとhead、manifestとlockfile、判断結果が同じrevisionを指しているか。
- Advisoryやlicense等の情報が欠けたとき、0件ではなく確認不能として止めるか。
- 作成者やbotだけで、判定方針と必須merge条件を弱められないか。
- 例外はpackage、version、理由、所有者、期限を限定しているか。

この教材は[GitHub dependency review guidance](../../../../sources/README.md#ref-deps-002)と
[攻撃段階4→5](../../../../docs/ANALYSIS_LENSES.md)を使ったリポジトリ独自の解釈です。
組織のrulesetや継続的な脆弱性対応を導入済みとするものではありません。
