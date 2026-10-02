# GitHub Actionsの権限をjobごとに絞る

Workflow全体を`permissions: {}`から始め、各jobが使う権限だけを追加します。同梱[permission-smoke.yml](permission-smoke.yml)は、sourceを読むjobへ`contents: read`、環境の開始確認をするjobへ`{}`を設定する小さな例です。手動起動だけで、公開・deploy・cloud認証を行いません。

対象はGitHub.com／GitHub Enterprise CloudのActions、hosted runner `ubuntu-24.04`、現在のjob権限とEnvironment設定です。製品仕様は**2026-09-27**に確認しました。Environmentの承認・branch制限等は契約とrepositoryの公開範囲で利用可否が変わるため、導入先で必要な機能を確認してください。GHESの対応版は未確認です。[設計pattern](../../README.md)と[control](../../../../../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)から、必要な操作と境界を先に判断できます。

## 手元のworkflowで変更する場所

Workflowの先頭を`permissions: {}`にし、**すべてのjob**で必要な権限を明示します。必要な項目を一つでも指定すると、未指定の項目は`none`になります。`GITHUB_TOKEN`そのものが消える設定ではありません。

| Jobの実際の処理 | 追加する候補 | 見直す点 |
|---|---|---|
| APIもcheckoutも使わない処理 | `permissions: {}` | 別途渡す認証情報やhost権限がないか |
| Repositoryのsourceをcheckout | `contents: read` | `persist-credentials: false`で、後続にGit認証を残さない |
| GitHub Releaseを作成 | `contents: write` | Release専用jobにし、必要な開始条件を保護する。Package・cloud権限を同時に足さない |
| OIDCでcloudへ認証 | `id-token: write`。Checkoutする場合は`contents: read`も追加 | 必要な交換jobだけへ付ける。Cloud側の条件は[CICD-006の実装](../../../workload-federation-boundary/implementations/github-aws/README.md)へ従う |

これは操作から設定を選ぶための例で、共通の許可一覧ではありません。使わない項目は追加しません。同じjobのActionやshellへ、そのjobの権限を共有してよいかを確認します。PAT、App token、cloud key、Environment secret、runnerのcredential・socket・内部通信は、`permissions`では制限できない別の経路です。

例えばテストとRelease作成を分けるなら、テストは読取り専用とし、公開jobだけへ`contents: write`を追加します。実行するコード、入力の信頼、branch・tag・イベント、Environmentの承認をそのjobへ結びます。Releaseの名前だけで対象を信頼せず、tagやsourceの変更を保護する必要があります。PRとの分離は[既存のGitHub例](../../../untrusted-pr-boundary/implementations/github-actions/README.md)を使い、同じ設定をここへ複製しません。

## 最短の導入・smoke test

以下は、許可された**使い捨てのGitHub repository**で行います。Default branchを`main`とし、少なくとも一つcommitがあり、Actionsと必要なEnvironment機能を利用できることが前提です。検証対象に本番secret・PAT・cloud key・self-hosted runnerを接続しません。

1. `Settings → Actions → General → Workflow permissions`で読取り中心の既定値を選びます。ActionsによるPR作成・承認が不要ならその設定も無効にします。組織・enterpriseの上位設定と、forkへのsecret・write配送も確認します。**既定値はjobの権限上限ではありません。**
2. **Workflowを入れる前に**`Settings → Environments`で`security-smoke`を作ります。利用可能な機能でrequired reviewerを設定し、`Prevent self-review`を有効にし、管理者のbypassを許さない設定にします。Deployment branches and tagsは`Selected branches and tags`から、branchの`main`だけを追加します。必要な制限を使えない場合はこの環境テストを未確認とし、同等の強制点を選び直します。
3. 本PJ側の実装ディレクトリを指定し、導入先repository rootで次を実行します。既存ファイルを上書きせず、差分をレビューしてdefault branchへ入れます。

```bash
JOB_AUTH_SOURCE='/absolute/path/to/product-security-guidance/engineering/cicd-security/purpose-bound-job-authority/implementations/github'
mkdir -p .github/workflows
cp -n "$JOB_AUTH_SOURCE/permission-smoke.yml" .github/workflows/workflow-authority-smoke.yml
git diff --no-index /dev/null .github/workflows/workflow-authority-smoke.yml
```

新規ファイルの差分がある時、`git diff --no-index`は終了値`1`です。導入の成功・拒否を判断するcommandではありません。WorkflowのEnvironment名と設定画面の名前を一致させます。名前の誤記や削除で無保護の環境が自動作成される経路を残さないため、workflow・設定変更のレビューも必要です。

4. `Actions → Workflow authority smoke → Run workflow`から`main`を選びます。`read-source`がsourceを取得し、commit IDを出すことと、job setupの`GITHUB_TOKEN Permissions`が`Contents: read`であることを確認します。`approved-marker`は承認前に待機し、`ENVIRONMENT_JOB_STARTED`が出ないことを確認します。必要な承認者が承認した後だけmarkerが出ることを確認します。Markerは本番処理の代わりで、tokenのwrite権限やcloud交換の確認ではありません。
5. 別のbranchで同じworkflowを手動起動します。`read-source`は実行できても、`approved-marker`はjob条件でskipされ、markerが出ないことを確認します。これはworkflow条件の確認で、Environmentのbranch制限を確認したことにはしません。

## 環境の拒否条件を別に確認する

同じ使い捨てrepositoryの検証branchで、`approved-marker`の`if`を一時的に`github.event_name == 'workflow_dispatch'`へ変えます。Environment名は`security-smoke`のままです。このbranchから手動起動し、Environment側のmain限定によってjob開始が拒否され、markerが出ないことを確認します。確認後は条件を戻し、検証branchを削除します。

承認を却下した場合にもmarkerが出ないこと、自分で起動したrunを自分で承認できないこと、設定したbypass拒否が有効なことを確認します。これらを試せない権限・契約・体制なら、その項目を未確認として残します。待機しているjobやAPIエラーを成功にしません。

環境名の誤記を調べる時も、この無権限markerだけで行います。期待する確認は「誤記しても自動で守られる」ではなく、**無保護環境の作成と開始が可能な場合を発見し、名称・変更保護を直すこと**です。既存の本番環境やsecretを使う確認へ置き換えないでください。

## 実jobへ戻す

確認できた配置を実jobへ適用し、そのjobが行う操作と権限の対応をレビューします。無権限markerへwriteやOIDCを付ける必要はありません。実際の公開・交換jobへは、その処理に必要な項目だけを別に追加します。必要な正常処理が成功し、不要な対象・文脈の操作が拒否されることを、採用先の許可されたテスト対象で確認します。このsmoke testだけで全scopeの拒否を証明したとはしません。

再利用workflowも呼出jobで権限を指定します。次は構造の断片で、参照するworkflowは採用先で用意します。

```yaml
jobs:
  reusable-check:
    permissions:
      contents: read
    uses: ./.github/workflows/reusable-check.yml
```

呼出先の`GITHUB_TOKEN`権限は呼出元より増やせませんが、呼出元が広く渡してよい理由にはなりません。必要なsecretだけを名前付きで渡し、不要な`secrets: inherit`を避けます。呼出元のjobに`environment`を足すことはできないため、必要なEnvironmentは呼出先の実jobで確認します。外部の参照固定は[CICD-001の実装](../../../reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)へ従います。

## 設定を読み取り専用で確認する

認証済みGitHub CLIを既に利用できる場合の補助です。CLI **2.95.0**の構文とREST API版**2026-03-10**の公式仕様を確認しています。GitHub.comの対象repositoryの設定を読む権限が必要で、fine-grained tokenなら`Administration: read`を使います。Jobの`GITHUB_TOKEN`へ管理権限を追加する例ではありません。

```bash
JOB_AUTH_REPO='OWNER/REPOSITORY'
gh api --method GET --hostname github.com -H 'X-GitHub-Api-Version: 2026-03-10' "/repos/$JOB_AUTH_REPO/actions/permissions/workflow" --jq '{default_workflow_permissions, can_approve_pull_request_reviews}'
```

期待する既定値は`default_workflow_permissions: "read"`と、PR承認が不要なら`can_approve_pull_request_reviews: false`です。このGETはEnvironment、実jobの付与、PAT・cloud権限、全workflowの最小性を取得しません。拒否・不足・古い確認結果を、現在の良好な設定へ読み替えないでください。組織の対象漏れは[SOURCE-006の手順](../../../../source-protection/organization-baseline-and-drift-review/implementations/github/README.md)へ渡します。

## 解除する

この例で追加したworkflowを削除し、検証用のrunが残っていればcancelします。追加したcheckを必須条件にした場合は、管理者が代替の検査を確認したうえで、そのcheckだけを外します。`security-smoke`が検証専用であることを確認してから、そのEnvironmentと検証branchを削除します。共有する環境や保護ルールは消しません。

実jobへの変更を戻す場合も、不要だった権限をまとめて復活させず、失敗した操作に必要な項目と対象を確認します。組織・repositoryの読取り中心の既定値は、この検証例の解除と独立して維持できます。

## 確認済みの範囲

本PJではYAMLの読込み、外部Actionの固定参照、shell構文、使い捨てローカルrepositoryへのcopyとsource確認を検査しました。GitHub上の設定・jobの実付与・承認待機・拒否・API取得・公開・cloud交換は未実行です。ローカルでGitのsourceを読めたことを、GitHubの権限が強制された証拠にはしません。

運用時は対象repository・revision・確認日、操作と権限、実設定、正常処理、拒否された文脈、未確認・障害・例外を残します。Token、secret、本番payloadは保存しません。Scannerを導入する場合も、形式検査と必要な操作のレビュー、providerの現在値を分けます。参照版・採否・製品の限界は[Sources](../../../../../sources/README.md#spec-github-workflow-authority)、具体化の判断は[移行記録](../../../../../docs/WORKFLOW_AUTHORITY_MIGRATION.md)にあります。
