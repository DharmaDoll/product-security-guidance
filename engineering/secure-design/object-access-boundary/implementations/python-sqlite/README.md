# Python / SQLite object access example

標準ライブラリだけで、実際のSQLite queryによるowner・tenant限定の読み書きを確認する限定例です。
HTTP serverや認証機構はありません。`Principal`は認証済みcontextを表す入力契約であり、requestから自由に構築してよいという意味ではありません。

`access.py`の`InvoiceService`が操作scopeを確認し、対象queryとUpdate自身にowner・tenant条件を含めます。
Update項目はdescriptionだけです。Owner移転やtenant変更を行う管理機能はこの例にありません。

本PJのrootから、標準ライブラリだけで動く使い捨てのSQLite DBを使って確認できます。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s engineering/secure-design/object-access-boundary/implementations/python-sqlite -p 'test_*.py' -v
```

Python 3.10以降の構文を使用します。確認した実行版は移行台帳へ記録します。
7テストで許可、他owner・tenant・未知ID・SQL文字列の拒否、scope不足、所有情報の更新項目拒否、
所有者変更後の拒否、DB障害の区別を確認します。外部ネットワーク、実データ、追加依存は使いません。

手元の別repositoryで試す場合は、まだ存在しない使い捨ての配置先を選びます。本PJのrootから次を実行します。

```sh
target=/path/to/disposable-repo
mkdir -p "$target/.security"
mkdir "$target/.security/object-access-demo"
cp engineering/secure-design/object-access-boundary/implementations/python-sqlite/access.py engineering/secure-design/object-access-boundary/implementations/python-sqlite/test_access.py "$target/.security/object-access-demo/"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s "$target/.security/object-access-demo" -p 'test_access.py' -v
```

解除はコピーした`object-access-demo`ディレクトリを削除します。実アプリへの採用では、認証層だけが`Principal`を作れる経路、既存のDB schemaと全読取り・変更経路を確認してから置き換えます。テストが通るだけではその接続を確認したことになりません。

DB障害は例外として伝え、呼出し層はデータを返さずサービス障害へ変換します。
`AccessDenied`は不許可・未存在を同じ外向き応答へ変換する契約です。HTTP状態・timing・ログの実装は未追加です。
ConnectionとDBへ直接アクセスする信頼済み基盤コードは迂回できるため、実システムでは呼出し経路とDB権限も確認します。
並行transaction、connection pool、auth contextの改ざん、list/export/batch/cacheは未検証です。

認可欠落の比較は「IDだけでSELECT／UPDATEするqueryなら他ownerの行も対象になる」と設計教材で扱い、
起動可能な無認可endpointは追加しません。

- [Control](../../../../../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)、[設計pattern](../../README.md)、[教材](../../../../../controls/records/secure-design/psb-design-001-object-access-authorization/learning.md)
