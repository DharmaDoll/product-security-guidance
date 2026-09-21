# Workload federation boundary — 学習ノート

## シナリオ：正しいtokenを別のjobが使う

CIの長期AWS keyを廃止し、GitHubのOIDC tokenからroleを引き受ける方式に変えました。
Trust policyが組織内の全repositoryを許可すると、侵害された小さなtest repositoryからも本番roleへ届く可能性があります。
Issuerの認証が正しくても、どのworkloadへ権限を渡すかが広すぎるためです。

Repositoryを一つに限定した後も、同じproduction Environmentを使う別workflowからtokenを取得できれば、
意図したdeploy workflowだけの許可にはなりません。さらに許可したdeploy jobのstepが侵害されれば、
そのstepは短命sessionの期間内に権限を使えます。被害範囲はroleが操作できるresourceに依存します。

## 用語を操作へ結び付ける

Issuerはtokenの発行者、audienceはtokenの受け入れ先を識別する値、subjectは権限を求める主体を示す値です。
Claimsはtokenに入る属性で、受け入れ先が検証して初めて認証・認可の判断に使えます。
Federationは、外部issuerの証明を受け入れ先の一時的な権限へ交換する仕組みです。

```text
どのコードがtokenを求められるか
  → issuerは誰か、tokenは真正・有効か
  → このaudience・subject・実行文脈を許すか
  → どのaccount・role・resourceを何秒使えるか
```

前の判定が正しくても、後の判定が広ければ被害は残ります。

## 直感と実際の境界

| 直感 | 確認すること |
|---|---|
| OIDCならcredentialが盗まれない | Tokenと交換後sessionもcredentialであり、実行中のstepから漏れる可能性がある |
| Environmentがproductionならmainだけ | Subjectにbranch条件が含まれるか。含まれなければEnvironment側でrefを制限する |
| Repository IDを固定したのでworkflowも固定 | 同じrepositoryで同じcontextを使える別workflowはないか |
| JTIがあるのでreplayできない | 受け入れ先にsingle-useの強制があるか。ない保証をtest用ledgerで補わない |
| get-caller-identityが成功したのでleast privilege | 正しいaccount・roleの確認と、許可操作の必要性は別 |
| Secretから旧keyを消したので移行完了 | Provider側で旧key・派生sessionが使えないか、残るconsumerがないか |

別workloadのtokenがtrustを満たさず交換前に拒否されれば、そこから本番roleを得る経路は成立しません。
ただし正規workloadが侵害される経路は別です。短命化は悪用可能な時間を狭め、操作権限の限定は影響範囲を狭めます。

## レビューで使う問い

「どこでtoken取得を許し、どこで交換を拒否し、どこで操作を制限するか」を説明してください。
Workflow変更、Environment policy変更、role trust変更がその説明を変えるか確認します。
実際のwrong-subject・wrong-audience拒否と、想定したjobの成功を別々に観測します。

この教材は[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)を使い、
プラットフォームの認証を運用・ガバナンスへ接続するリポジトリ独自の解釈です。
[攻撃段階5→6→7→9・10](../../../../docs/ANALYSIS_LENSES.md)では、
未信頼状態、権限取得、runner、公開・deployの責任を分けて読みます。
方式は[pattern](../../../../engineering/cicd-security/workload-federation-boundary/README.md)、仕様は[参照資料](../../../../sources/README.md#spec-workload-federation)へ進んでください。
