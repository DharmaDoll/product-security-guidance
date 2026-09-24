# Authentication is not object authorization

## 正規利用者が攻撃者になる

利用者Aが自分の請求書画面を開き、APIの対象IDをBの請求書IDへ変えます。
この要求のログイン情報は正規です。認証は「誰か」を確定しますが、「この対象を読んでよいか」までは決めません。
IDが知られていても、AとBの関係をサーバーが確認すれば、Bの請求書を返す経路は成立しません。

別tenantにも同じuser IDが存在する場合、userだけの照合でも分離が壊れます。
対象、操作、主体、tenantを一緒に評価します。閲覧権限があっても編集権限があるとは限りません。

## 情報源を分ける

RequestのIDは「どれにアクセスしたいか」という未信頼の指定です。
認証層の主体情報とDB内のowner・tenantは、許可判断の根拠です。
Requestに`owner_id=A`と書いても、DBのB所有という事実を置き換えられないようにします。
同様に更新bodyを丸ごとDBへ渡すと、所有者やtenantを書き換える経路が生まれます。更新可能な項目を限定します。

署名・来歴が正規でも、アプリケーションの認可欠陥は残ります。
[Authentic is not acceptable](authentic-is-not-acceptable.md)のconsumer判断と、この対象への操作許可は別の保証です。

## 設計レビューで問うこと

単体取得だけでなく、list、検索、export、batch、非同期処理から同じ対象へ届かないか確認します。
Cacheへ許可済み結果を置く場合は、利用者・tenant・権限変更との関係も設計します。
拒否と未存在を同じ外向き応答にしても、timing等から存在が推測されない保証にはなりません。
認可DBが故障した場合は、情報を返さず、実装の障害として区別して扱います。

[OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)を設計入力とし、請求書シナリオはリポジトリ独自の教材です。
[REF-PORTFOLIO-001](../../sources/README.md#ref-portfolio-001)のapplication層を扱います。Supply-chainの12段階へ無理に割り当てません。

- [設計pattern](../../engineering/secure-design/object-access-boundary/README.md)
- [実装と拒否テスト](../../engineering/secure-design/object-access-boundary/implementations/python-sqlite/README.md)

対応するcontrolは未移行です。[全教材索引](README.md)で成果物の状態を確認できます。
