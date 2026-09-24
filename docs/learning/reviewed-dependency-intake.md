# Reviewed dependency intake — 学習ノート

## シナリオ：レビューは成功したのに別の内容が入る

更新ボットがweb frameworkのversionを更新します。推移依存のparserも変わりました。
レビュー担当者はparserの差分と公開済みadvisoryを調べ、採用可能と判断します。
ところがbuildでmutable installを使い、別の推移依存が選ばれます。あるいはcacheが同じversionの
別ファイルを返し、hashを照合せず使います。

採用判断が正しくても、実行する入力がその判断へ結び付いていなければ、未レビューの内容が入ります。
逆に悪意あるparserがlockとhashへ正しく記録されていたら、完全性検証は成功し得ます。
同一性の確認は、採用してよい理由にはなりません。

## 三つの問いをつなぐ

| 問い | 判断対象 | 主な責任 |
|---|---|---|
| 今回何が変わり、採用してよいか | Base→headの依存差分と、その時点の方針・根拠 | Dependency change review |
| Buildが承認した内容を使うか | Manifest→lock→直接・推移依存→取得bytes | Dependency artifact identity |
| 準備用コードを動かしてよいか | Hook、native build、source backendと実行環境の権限 | Install execution policy |

Dependency graphはpackageとその依存関係の一覧・つながりです。直接依存はprojectが明示して使うもの、
推移依存はそれらがさらに必要とするものです。Lockは選んだ解決結果を記録し、hashは配布ファイルのbytesを
識別します。複数platformの配布ファイルを一つのversionへ関連付ける場合も、許可したhashを区別します。

## 何が分かり、何が分からないか

| 観測 | 誤った解釈 | 次に問うこと |
|---|---|---|
| Hashが一致した | 安全なpackageである | そのhashを誰が、どの変更として承認したか |
| Advisoryがなかった | 悪意も脆弱性もない | データの対応範囲と取得成功を確認できたか。未知の問題が残るか |
| Actionが失敗した | Mergeも止まる | 実際のrulesetが現在のcheckを必須にしているか |
| Lockfileが変わらなかった | Manifestも最新である | 古いlockのまま使っていないか。鮮度検査は実行されたか |
| High advisoryが見つかった | 製品が必ず侵害される | Affected機能へ攻撃入力が届くか、CIのどの権限で実行するか |

Parserが最終artifactに入らず脆弱な処理も呼ばれないなら、そのadvisoryによる製品の被害経路は成立しない場合があります。
その調査と、検査失敗を無条件で許可することは別です。例外は対象version・advisory・理由・所有者・期限を限定します。

## 古い判断を使い回さない

レビュー後にheadが変われば再評価します。Baseが進んで比較対象が変わった場合も、現在のgraphとの対応を確認します。
判定結果にはrevisionと方針の識別情報を結び付け、通常buildは承認したlockを修復せず使います。
継続SCAは、変更がない状態で後から公開されるadvisoryを扱う別の時間軸です。

この教材は[REF-PORTFOLIO-001](../../sources/README.md#ref-portfolio-001)の外部依存・プラットフォーム・
PSIRT・ガバナンスを接続し、[攻撃段階4→5→7](../ANALYSIS_LENSES.md)の受け渡しを読み解くための
リポジトリ独自の解釈です。個別の製品仕様や導入済み状態は示しません。

方式は[設計パターン](../../engineering/dependency-security/reviewed-dependency-intake/README.md)、
根拠は[参照資料](../../sources/README.md#spec-dependency-lock-identity)へ進んでください。

対応する成果物：[PSB-DEPS-003](../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) · [PSB-DEPS-004](../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md) · [全教材索引](README.md)
