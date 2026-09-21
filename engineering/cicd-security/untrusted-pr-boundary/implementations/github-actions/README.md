# GitHub Actions実装例: Untrusted PR boundary

[設計パターン](../../README.md) / [対応するコントロール](../../../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)

## この実装例が示すこと

PR作成者が変更できるコードを、書き込み権限やシークレットを持たない`pull_request`ワークフローで検証し、権限が必要な処理を
review／merge後の`push`から別のrunとして始める、保守的なGitHub Actions構成です。二つのrunの間で、
artifact、cache、output、workspaceを受け渡しません。

この例はGitHub上の設定を変更せず、導入済みであることも証明しません。設定例は
`engineering/.../implementations/`配下にあるため、自動的にワークフローとして有効にはなりません。

`contents: read`のジョブにも`GITHUB_TOKEN`は存在します。この例はトークンを一切なくすものではなく、
PRコードへ書き込み権限、配送されたシークレット、OIDC、永続資産、内部到達性を与えない構成です。

## 対象と参照版

- 対象: GitHub.comのGitHub Actions。
- 製品ガイダンスの基準版: `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24）。
- `actions/checkout`は、移行元でレビューされたfull commit SHAへ固定。
- GitHub Enterprise Serverや、基準版より後の仕様変更は採用時に再確認する。

## ファイル

| ファイル | 用途 | 取り扱い |
|---|---|---|
| [`secure/pr-validation.yml`](secure/pr-validation.yml) | PR由来のコードを無権限で検証する | 導入先の`.github/workflows/`へ移し、test commandとrunner境界をレビューする |
| [`secure/trusted-after-merge.yml`](secure/trusted-after-merge.yml) | review済みの`main`から新しいrunを始める | 必要な権限処理へ置き換え、job単位で最小権限を付与する |
| [`insecure/privileged-untrusted-pr.yml`](insecure/privileged-untrusted-pr.yml) | 境界を壊す構成をレビューで見分ける | **導入・有効化・コピー禁止** |

## 導入判断

### 1. 先に既存経路を調べる

全ワークフローについて、`pull_request`、`pull_request_target`、`workflow_run`、`issue_comment`、
reusable workflow、手動checkout、artifact、cache、outputを調べます。安全なファイルを追加しても、
既存の権限付きPR経路が残れば境界は成立しません。

### 2. PR検証を無権限にする

`secure/pr-validation.yml`を導入先のワークフローとして追加します。`make test`は対象プロジェクトの検証コマンドへ
置き換えられますが、PR作成者がそのコマンドや呼び出すファイルを変更できる前提で扱います。

- top-levelを`permissions: {}`とし、jobには`contents: read`だけを付与する。
- checkout後に認証情報を残さない。
- secret、OIDC、保護されたEnvironmentを参照しない。
- 既定例のGitHub-hosted runnerを、永続するself-hosted runnerへ安易に置き換えない。

### 3. 新しい信頼境界から権限処理を始める

`secure/trusted-after-merge.yml`は、保護された`main`への`push`から新しいrunを開始する境界だけを示します。
`echo`を実際の処理へ置き換える際に、必要なpermission、Environment、OIDC条件をそのjobへだけ付与します。
PR runのartifact、cache、output、workspaceを復元してはいけません。

### 4. 提供元の設定を合わせる

repository／organizationのActions token、fork approval、runner group、Environment、ruleset、required checkを確認します。
workflowファイルだけでは、これらの実効状態や実際のrunへ配送された権限を証明できません。

## 導入後に確認する状態

無害なfork PRと、そのPRをmergeした後のrunを使い、次を別々に記録します。

1. PR runが`pull_request`で起動し、意図したrevisionをcheckoutしている。
2. PR runにwrite permission、secret、OIDC、保護されたEnvironment、永続runner、内部networkがない。
3. PR runの状態を消費する権限付きworkflow、cache、artifact、outputがない。
4. merge後のrunが`main`のreview済みrevisionから新しく開始している。
5. provider設定、workflow inventory、runの一部を確認できない場合、結果を`NOT_CHECKED`または`ERROR`にしている。

静的解析はレビューを補助できますが、提供元設定と実runを置き換えません。実際のsecretを置いた流出試験や、
本番Environmentへの攻撃的な試験は行いません。

## この例を変更する場合

- metadata-onlyの`pull_request_target`を追加するなら、PR code、dependency、artifact、cacheを読み込まず、
  PR由来の文字列をshellや式へ直接展開しない専用workflowにする。
- run間でデータを渡すなら、schema、サイズ、完全性、producer、consumerでの解釈を固定する。
- private dependencyが必要なら、本番credentialを渡さず、読み取り専用mirrorまたは一時環境を検討する。
- third-party Actionを追加するならfull commit SHAへ固定し、そのActionが扱う入力とtokenをレビューする。

## 制限

この例は、branch／rulesetの強制、組織のfork policy、runnerの一回限りのライフサイクル、OIDCのcloud側trust、
cacheのprovenance、build sandbox、release integrityを実装しません。`pull_request_target`や`workflow_run`を
全面的に禁止する仕様でもなく、最初の導入で境界を見誤りにくくするための保守的な構成です。

## 参照資料

- [GitHub Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [GitHub Compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners)
- [REF-CICD-010 Preventing pwn requests](../../../../../sources/README.md#ref-cicd-010)
- [REF-CICD-005 GitHub Actions Best Practice 2025](../../../../../sources/README.md#ref-cicd-005)
- [GitHubセキュリティガイダンスの基準版](../../../../../sources/README.md#spec-github-security-guidance)
