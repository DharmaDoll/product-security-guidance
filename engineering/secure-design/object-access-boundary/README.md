# ENG-DESIGN-001: Object access boundary

## 一つの請求書から設計する

利用者Aは自分の請求書を閲覧・編集できます。しかし、リクエストのinvoice IDを利用者Bのものへ変えたときも、
ログイン済みという理由だけでデータを返すAPIなら、Bの情報を読み書きできてしまいます。
攻撃者は正規利用者でもあり得ます。ランダムなIDは探索を難しくしますが、既に知っているIDへのアクセスを認可するものではありません。

読者は、認証・対象特定・操作許可・実際の読み書きをどこに置くか判断できるようになります。
主なdomainはSecure Design、実装はSecure Codingの教材です。既存controlの移行ではなく、新規の限定pilotです。

## このpilotのアクセスモデル

| 主体と対象 | Read | Update |
|---|---|---|
| 同tenantのowner、必要な操作scopeあり | 許可 | 許可 |
| 同tenantの別利用者 | 拒否 | 拒否 |
| 別tenantのownerと同じuser ID | 拒否 | 拒否 |
| 認証主体なし／scope不足 | 拒否 | 拒否 |

Tenantは所属する組織・顧客の分離単位です。この例にadmin、共有請求書、代理アクセスはありません。
それらが必要になったら、新しい関係・操作と拒否条件を先に定義します。

## 強制点

```text
未信頼のID・更新内容       認証層が確定したuser・tenant・scope
           ↓                              ↓
     Serviceの操作許可 → DBのtenant・owner付き条件 → Read／Update
           ↓
     不許可・未存在は同じ外向き応答、DB障害は別の評価不能
```

Subjectのuser・tenant・scopeは認証層から渡し、request bodyや未検証headerから組み立てません。
対象のowner・tenantはDBに保存した値を根拠にします。Updateの許可条件を実際の書込queryにも含め、
一度読み取った後に無条件で更新する構造を避けます。List、export、batch、background jobも同じ認可設計の対象です。

## 方式の選択と代償

Owner限定ならDB条件とservice層を組み合わせる小さな設計で始められます。
共有・代理・期間限定権限が必要なら、関係や属性を管理する方式を検討します。Roleだけで個々の対象へのアクセスを決めないようにします。
DBのrow-level securityも候補ですが、session context、connection pool、管理者の迂回、service層との責任分界の確認が必要です。
UIで非表示にするだけの制限は、APIへの直接要求を止めません。

## 検証する判断と残る境界

他owner・他tenant・scope不足・主体なし・未知IDのRead／Updateを拒否し、拒否したUpdateでDBが変わらないことを確認します。
Ownerやtenantを書き換える更新項目も拒否します。IDにSQL構文が含まれても、値として処理されることを確認します。
例外が起きたときに別の無認可queryへ切り替えないようにします。

このpilotはHTTP認証、token検証、session失効、CSRF、cache、全endpoint、並行した権限変更、監査配送を実装していません。
実システムの導入確認と小さな関数の拒否テストを混同しません。

- [Python / SQLite実装](implementations/python-sqlite/README.md)
- [教材](../../../docs/learning/authentication-is-not-object-authorization.md)
- [参照資料と採否](../../../sources/README.md#ref-application-authorization-001)
- [Portfolio review](../../../docs/PORTFOLIO_MIGRATION_REVIEW.md): アプリケーション内の悪用経路は供給経路だけで分類しない
