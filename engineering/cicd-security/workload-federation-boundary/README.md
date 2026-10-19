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

## ビルドしたものを公開ジョブへ渡すとき

レビュー後の変更をビルドし、その成果物を公開する場面を考えます。公開先の権限を取得できるからといって、ビルドと公開を同じ環境で動かす必要はありません。依存パッケージやビルド用スクリプトの実行には、公開用の権限を渡さない構成を選びます。

公開ジョブでは、管理された公開処理が、承認した成果物をデータとして送ります。成果物に含まれるスクリプトを実行したり、ビルド側が指定したコマンドや送信先をそのまま採用したりすると、ビルド側から公開権限を使う経路ができます。

| 渡すもの | 公開側で判断すること |
|---|---|
| 配布する成果物 | 対象の変更・生成元・digestと対応しているか。公開するものとして受け入れてよいか |
| 検査結果 | どの版を誰が検査したか。ビルド側の「成功」という自己申告だけで公開を決めていないか |
| 公開先や実行方法 | 保護された公開設定で決めているか。受け取ったファイルで勝手に変えられないか |

これは本PJでの設計判断です。OIDCは権限を取得する処理を限定しますが、渡された成果物の妥当性は判断しません。PR由来の状態を持ち込ませない条件は[CICD-005の設計](../untrusted-pr-boundary/README.md)、ビルドの実行制限は[Build execution boundary](../../build-security/build-execution-boundary/README.md)、成果物の受入判断は[Consumer artifact acceptance](../../release-integrity/consumer-artifact-acceptance/README.md)へつなぎます。Digestの一致だけで内容が安全だとは判断しません。

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
[Controlの診断項目](../../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md#failure-checks)で、交換前の拒否、交換後の操作、旧keyを分けて確認します。

短命な権限も正規jobの侵害で盗まれ得ます。Runner隔離・egress・検知、artifact検証、管理面の変更管理、
インシデント時の失効・復旧へ責任を渡します。
主なdomainはCI/CD Security。七レイヤーのプラットフォームと運用・ガバナンス、攻撃段階6と前後の受け渡しを確認します。

- [GitHub Actions / AWS実装例](implementations/github-aws/README.md)
- [Control](../../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)
- [Untrusted PR boundary](../untrusted-pr-boundary/README.md)：交換jobへ渡る状態の信頼判断
- [仕様・採否](../../../sources/README.md#spec-workload-federation)
