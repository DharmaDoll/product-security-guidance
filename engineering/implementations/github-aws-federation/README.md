# GitHub Actions / AWS実装例: Exact workload federation

## 対象と設定

GitHub.com、AWS標準partition、一つのrepository・production Environment・account・専用roleの例です。
資料照合日は`2026-10-15`。他provider、GitHub Enterprise Server、custom subjectは別profileとしてレビューします。

[`role-trust-policy.json`](role-trust-policy.json)は旧例のexact audience・immutable subjectを保持します。
Account `111122223333`、organization `example-org / 123456`、repository `secure-app / 987654`は架空の値です。
採用先の実IDと実際のsubjectへ置換し、AWS IAM roleのtrustへレビューした差分を反映します。
AWS IAM OIDC providerは`https://token.actions.githubusercontent.com`、audienceは`sts.amazonaws.com`とします。

Subject形式は対象repositoryの設定で確認し、作成日や名前だけから推測しません。
Immutable IDが入ってもEnvironment subjectだけではbranch・workflowを固定しません。
Production Environmentでは選択したbranchの`main`だけを許可し、reviewer・self-review・bypassの実効設定を確認します。保護branchがない状態で「Protected branches only」を選ぶと、全branchが対象になります。必要な承認機能が契約プランと公開範囲で使えることも導入前に確認します。
同じEnvironmentを使う別workflowからの取得もレビューします。
[GitHub OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)

## 最短導入と解除

1. 使い捨てのGitHub repositoryと専用のAWS roleを用意し、現在のrole trustと操作権限を保存する。共有OIDC providerの設定は変更しない。
2. GitHub jobで使うEnvironmentと実際のOIDC subject形式を確認する。`role-trust-policy.json`の架空のaccount・repository ID、subjectを採用先の値へ置き換え、差分をレビューして専用roleのtrustへ反映する。
3. Environmentの許可branchとreviewerを設定し、交換するjobだけへ`id-token: write`と専用roleを指定する。最初の確認jobでは公開や配布を行わない。
4. 正規のjobで`aws sts get-caller-identity`のaccount・roleを確認し、未許可のbranch・subjectからは交換できないことを確認する。操作権限の確認は次節の別項目として行う。

解除するときは、追加したjobのOIDC権限とrole指定を外し、保存したtrustを戻します。試験のために作った専用roleは利用者がいないことを確認してから廃止します。共有OIDC providerや既存のroleは削除しません。旧keyを止めた移行の場合、その再有効化をこの例の自動的な切り戻し手順には含めず、必要な権限と漏えいリスクを別に判断します。

## Workflowと操作権限

交換jobだけに`id-token: write`を与え、保護されたEnvironmentで交換します。
Actionは`aws-actions/configure-aws-credentials@e6de054238d6b7531b4efff3b6587d9aade6a06c`へ固定します。2026-10-15に`v6.2.3`タグとの一致と、このcommitの`action.yml`の入力定義を確認しました。Action全体の安全性や実行結果を確認したものではありません。
Audience、role-to-assume、allowed-account-idsを明示し、旧profileのsession要求は900秒です。
この数値はAWS例の要求値であり、全providerの既定基準やsingle-useの保証ではありません。

認証の確認jobへ実際のビルド・公開を追加する前に、[ビルドから公開への受け渡し](../../pull-request-to-release-build.md#artifact-handoff)を確認します。交換成功は、PR由来のファイルや依存スクリプトをその権限で実行してよいという判断ではありません。

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

### 拒否された場所を分けて記録する

| 試す条件 | 確認する結果 |
|---|---|
| 許可していないbranchから同じEnvironmentを使う | GitHub側でjobが進めないこと。この結果だけではAWSのtrustによる拒否は未確認 |
| 検証用の別Environmentから対象roleへ交換する | 実際のsubjectがtrustと異なることと、AWS側の交換拒否。対象roleのtrustを緩めて試さない |
| 同じEnvironmentを使う別workflow | このtrustだけでは区別しない。許可するworkflowの変更管理や、必要ならsubject設計を別途見直す |
| 通信障害やActionの起動失敗 | 認証条件による拒否と数えず、実行失敗として原因を確認する |

試験は一度に一条件だけ変え、対象のrun・検証用role・期待した拒否箇所と実際の結果を残します。raw JWTや認証情報は残しません。正常な交換を確認できないまま失敗ケースだけを並べても、制限が効いた証拠にはなりません。

解除でtrustを戻す作業と、既に発行したsessionの停止も別です。緊急停止が必要な場合は、[認証情報の漏えい対応](../../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)で対象roleの停止手段を確認します。

## 移行と限界

旧workflow・permissions policy・Terraform導入資料の参照仕様は[参照資料記録](../../../sources/README.md#spec-workload-federation)へ保持し、
今回はtrustの小さな例と導入判断を分離しました。CLI・Actionの導入は採用時にversion・integrityを確認します。
盗まれたsessionの有効期間内の悪用と、正規job内の悪意あるstepは残余リスクです。
旧keyのprovider失効・派生session確認は旧READMEより明確にした判断で、導入済みではありません。
[CICD-006の方式](../../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)へ戻ってrunner・公開・復旧との境界を確認してください。
