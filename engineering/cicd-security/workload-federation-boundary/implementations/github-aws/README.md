# GitHub Actions / AWS実装例: Exact workload federation

## 対象と設定

GitHub.com、AWS標準partition、一つのrepository・production Environment・account・専用roleの例です。
確認日は`2026-09-16`。他provider、GitHub Enterprise Server、custom subjectは別profileとしてレビューします。

[`secure/role-trust-policy.json`](secure/role-trust-policy.json)は旧例のexact audience・immutable subjectを保持します。
Account `111122223333`、organization `example-org / 123456`、repository `secure-app / 987654`は架空の値です。
採用先の実IDと実際のsubjectへ置換し、AWS IAM roleのtrustへレビューした差分を反映します。
AWS IAM OIDC providerは`https://token.actions.githubusercontent.com`、audienceは`sts.amazonaws.com`とします。

Subject形式は対象repositoryの設定で確認し、作成日や名前だけから推測しません。
Immutable IDが入ってもEnvironment subjectだけではbranch・workflowを固定しません。
Production Environmentの許可branchを`main`へ限定し、reviewer・self-review・bypassの実効設定を確認します。
同じEnvironmentを使う別workflowからの取得もレビューします。
[GitHub OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)

## Workflowと操作権限

交換jobだけに`id-token: write`を与え、保護されたEnvironmentで交換します。
旧Actionの固定commitは`aws-actions/configure-aws-credentials@e6de054238d6b7531b4efff3b6587d9aade6a06c`。
Audience、role-to-assume、allowed-account-idsを明示し、旧profileのsession要求は900秒です。
この数値はAWS例の要求値であり、全providerの既定基準やsingle-useの保証ではありません。

Roleの操作権限はtrustと別に定義します。旧例の`s3:PutObject`と`releases/*`は一つのprefixへ限定した例ですが、
prefix内の全objectへ書ける権限です。すべてのdeployに十分・最小とは主張せず、必要な操作・resource・上書きの可否を
採用先でレビューします。IAM Access Analyzerの構文・policy検査と意味的な権限レビューを区別します。

## 実環境で確認する

この試作版は設定変更、token取得、AWS交換を実行していません。Adopterがsandboxで次を確認します。

| 境界 | 観測するもの |
|---|---|
| 認証・trust | Current provider・role trustと、正規contextの交換成功、wrong-audience・wrong-subjectの交換拒否 |
| 実行文脈 | Current Environment、許可branch・review・bypass、未許可refのjobが権限へ届かない結果 |
| Session・操作 | Account・role、要求と実際の有効期間、必要操作の許可と無関係なresourceへの拒否 |
| 旧key | Repository・Environment・organizationのconsumer inventory、provider側の無効化、旧keyが使えない結果 |

Identity確認には`aws sts get-caller-identity`を使えますが、roleの最小権限を証明しません。
拒否testは公開・deployを行わない構成で実施し、raw JWT、AWS access key、secret、session tokenを証拠へ保存しません。
未確認は`NOT_CHECKED`、取得・実行・収集失敗は`ERROR`、期待した境界に反する結果は`FAIL`。
JSON sampleの存在やsynthetic ledgerを実際のtoken検証・replay拒否の証拠にしません。

## 移行と限界

旧workflow・permissions policy・Terraform導入資料の参照仕様は[参照資料記録](../../../../../sources/README.md#spec-workload-federation)へ保持し、
今回はtrustの小さな例と導入判断を分離しました。CLI・Actionの導入は採用時にversion・integrityを確認します。
盗まれたsessionの有効期間内の悪用と、正規job内の悪意あるstepは残余リスクです。
旧keyのprovider失効・派生session確認は旧READMEより明確にした判断で、導入済みではありません。
[Pattern](../../README.md)へ戻ってrunner・公開・復旧との境界を確認してください。
