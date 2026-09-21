# Security effects live at enforcement points

## 洞察

セキュリティ成果物の価値は、その成果物が存在することではなく、保護対象への操作を実際に変える
強制点に接続されることで生まれます。

```text
ガイダンス／ポリシー／設定／判断
                    |
                    v
             強制点
                    |
          許可／拒否／制限／停止
                    |
                    v
             保護対象の操作
```

## 二つの具体例

認証情報ポリシーのJSONに「PATは短命」と書いても、ソース管理基盤上の権限や有効期限は変わりません。
効果が生まれるのは、サービス提供側やIdPによる認証、リポジトリ権限、有効期限、失効が、
実際の要求へ強制されたときです。

`.npmrc`のサンプルに最低待機時間を書いても、開発者、更新ボット、CIが別の設定を使えば、
公開直後のリリースは採用されます。効果が生まれるのは、実際の依存関係解決処理または信頼できるCIが、
依存パッケージのコードを実行する前に候補を止めるときです。

## 設計レビューへの応用

1. 守りたい操作を動詞で書く。例：ソースコードを変更する、パッケージのバージョンを選択する。
2. 最終的に操作を実行する構成要素を特定する。
3. 許可／拒否を決める権限主体と、判断に使う情報の信頼元を特定する。
4. 代替経路、例外経路、管理者経路、キャッシュされた判断を追う。
5. 成果物そのもののテストと、実環境の強制点を確認するテストを区別する。

[横断分析の軸](../ANALYSIS_LENSES.md)を使う場合は、攻撃段階ごとに強制点を一つずつ確認します。
前段の`PASS`を後段へそのまま持ち込まず、どの識別子と判断を渡し、次の構成要素がどこで再度
許可または拒否するのかを明示します。

## よくある誤用

- ポリシー用リポジトリにファイルがあるため、導入済みと判断する。
- サンプル検証器の`PASS`を、本番設定も`PASS`である根拠として扱う。
- スキャナーの実行失敗を、指摘なしとして扱う。
- ガイダンス中心のコントロールを無理にテスト用データへ落とし込み、実際の境界を観測しない。

## 限界

強制点が存在しても、ポリシーの意味、ID、対象リソースの解決が誤っていれば、安全とは限りません。
この洞察は「どこを見るか」を示すもので、個別コントロールの正しい判断を定義するものではありません。

## 関連資料

- [PSB-SOURCE-004](../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)
- [PSB-DEPS-001](../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)
- [Source credential lifecycle pattern](../../engineering/source-protection/source-access-credential-lifecycle/README.md)
- [Dependency release cooldown pattern](../../engineering/dependency-security/dependency-release-cooldown/README.md)
