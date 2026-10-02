# ENG-DEPS-003: Reviewed dependency intake

## 利用場面

依存更新をレビューしているのに、buildが同じ内容を使うか分からないときに使います。
読者は採用判断、入力の固定、取得時の照合をどこへ配置するか選べるようになります。
[同一性の教材](../../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/learning.md)と[更新レビューの教材](../../../controls/records/dependency-security/psb-deps-004-dependency-change-review/learning.md)から、それぞれの問いを読めます。

## 推奨構成

```text
明示的な依存更新 → manifest・lockの変更
  → 現在のbase/headで直接・推移依存を比較
  → 方針・根拠で判定 → 必須merge gate
  → 承認したrevision・manifest・lock
  → 通常build: manifestとの対応確認・lock書換え禁止
  → 準備コードの実行方針を適用した取得・準備とhash照合
  → 後続実行の隔離 → build・release → 継続的な脆弱性対応
```

更新の作成者は入力を変えられますが、その変更の評価方針や承認結果まで自己申告で決める構造にしません。
Merge後の通常buildが再解決すると、前段のレビューとの対応が切れます。

## 三つの判断を渡す

| 判断 | 次へ渡すもの | その判断だけでは分からないこと |
|---|---|---|
| 更新を採用するか（DEPS-004） | 対象revision・依存差分・判定方針と承認 | 通常buildが同じファイルを使うか |
| 承認した内容と一致するか（DEPS-003） | 対象環境の固定入力と、利用するファイルの照合結果 | その内容を実行してよいか |
| 準備用コードを動かすか（DEPS-002） | 実行不要という方針、または対象を絞った実行許可 | 許可した処理や後続のテストが持つ権限の妥当性 |

実行方針は取得・準備の前に置きます。依存管理ツールがパッケージ情報を集める段階で準備コードを起動する場合もあるためです。
配置の詳細は[Install execution policy](../install-execution-policy/README.md)へ分けます。

## 方式と代償

| 方式 | 利用場面 | 失敗経路・代償 |
|---|---|---|
| Native lockとimmutable install | 対応package managerで通常buildを再現する | Local source、optional依存、platform差を別に確認する。書換え禁止だけで鮮度を保証しない |
| Exact versionと全依存hash付き入力 | 配布ファイルを明示できる環境 | Platform別hashと推移依存の保守が必要。Manifestとの対応を生成・更新経路で管理する |
| Providerのdependency diffと必須gate | Providerのmanifest・graph対応を確認できる環境 | 部分的なデータやsnapshotの遅延を空の安全な差分にしない |
| 既存SCAを変更差分へ結び付ける | Native reviewを使えない環境 | Base/head比較、scanner・DBの失敗処理、必須merge条件を別に実装する |

Graph・hashの固定と、既知脆弱性・license・取得元・来歴の採用判断を一つの結果へ丸めません。
どの入力に何の方針を適用したかを記録し、追加の判断を有効化したときは対応範囲を明示します。

展開済みの依存環境を再利用する場合は、その内容が承認した入力と対応することも確認します。
取得ファイルのcacheと、後で実行する展開済み環境を同じ検査対象にしません。既存状態を検証できない採用先では、新しい環境を選びます。

## 確認する境界

通常installではmanifest drift、推移依存の差し替え、hash欠落、runtime不在を無害な対象で確認します。
Merge gateでは、差分の完全性と拒否対象の判定を確認した後、失敗・取消・検査欠落が実際にmergeを止めるか確認します。
データ準備の待機期限や処理の省略が成功表示になる方式では、必要な評価が完了したかを別に確認し、未評価を必須判断で止めます。
リポジトリ内のサンプル成功と、組織の導入判定は別です。

## 関連する成果物

- [Dependency artifact identity](../../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)
- [Dependency change review](../../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)
- [Install execution policy](../install-execution-policy/README.md)：実行許可の責任
- [既存pip実装例](../install-execution-policy/implementations/pip/README.md)：限定したwheel取得とhash拒否の観測。Manifest鮮度や完全graphの証明は含まない
- [GitHub review実装例](implementations/github/README.md)
- [仕様と採否](../../../sources/README.md#spec-dependency-lock-identity)
- [横断分析](../../../docs/ANALYSIS_LENSES.md)：段階4・5から7、release、PSIRTへの受け渡し
