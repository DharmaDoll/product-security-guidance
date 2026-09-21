# ENG-CICD-002: Workload federation boundary

## 利用場面

CIからcloud・公開先の権限を取得する経路を、保存した長期keyから短命なworkload認証へ変えるときに使います。
読者はtokenの取得許可、交換条件、操作権限をどこへ配置するか判断できます。

## 推奨構成

```text
レビュー済みsource → 権限のないbuild → 固定したartifactと検証情報
  → 保護された交換jobでartifact・実行文脈を確認
  → 承認issuerのtoken → 受け入れ先の限定したtrust
  → 専用role・必要resource・短命session → 公開・deploy
```

交換jobは未信頼のbuild script、cache、workspaceを引き継いで実行しません。
受け入れ先の認証・認可を、tokenを求めるコードやその自己申告だけへ委ねません。

## 方式を選ぶ

| 方式 | 適用と代償 |
|---|---|
| Repository・refをsubjectで限定 | Branchを区別しやすい。workflowやEnvironmentの条件をどこで補うか確認する |
| Environmentをsubjectで限定 | 承認やdeploy条件へ接続できる。branch・別workflowの制限をEnvironmentやworkflow保護で補う |
| Custom subject・reusable workflow identity | より細かい条件を設計できる。issuerと受け入れ先の対応、切替時の旧trust削除を管理する |

Cloudに渡せるclaimsと、cloudが条件として検証するclaimsを区別します。
Token取得権限の縮小とrole操作権限の縮小も別々に行います。
旧keyの移行時にはconsumerを確認し、GitHub上の削除とprovider側の無効化・派生権限の扱いを照合します。

## 確認する状態と限界

成功する承認contextと、拒否されるaudience・subject・refのcontextを無害な操作で確認します。
Account・role identity確認の成功だけで、全許可操作の最小性を認定しません。
不完全な設定・inventory・交換結果は未確認として残します。

短命な権限も正規jobの侵害で盗まれ得ます。Runner隔離・egress・検知、artifact検証、管理面の変更管理、
インシデント時の失効・復旧へ責任を渡します。
主なdomainはCI/CD Security。七レイヤーのプラットフォームと運用・ガバナンス、攻撃段階6と前後の受け渡しを確認します。

- [GitHub Actions / AWS実装例](implementations/github-aws/README.md)
- [Control](../../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)
- [Untrusted PR boundary](../untrusted-pr-boundary/README.md)：交換jobへ渡る状態の信頼判断
- [仕様・採否](../../../sources/README.md#spec-workload-federation)
