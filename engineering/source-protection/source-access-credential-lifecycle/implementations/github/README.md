# GitHub実装例: Source credential lifecycle

パターン：[Source credential lifecycle](../../README.md)

コントロール：[PSB-SOURCE-004](../../../../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)

## 位置付け

移行パイロットです。旧プロジェクトのGitHub向けガイダンスを再構成したもので、採用時にはGitHubの契約プラン、
API、画面、IdP構成を公式文書で再確認してください。サンプルやこの文書の存在は、導入済みであることの証拠ではありません。

## 参照資料から採用した判断

| 参照資料 | この実装例で採用した判断 | この資料だけでは判断しないこと |
|---|---|---|
| GitHubセキュリティガイダンス | 認証方式、認証情報の種類、組織ポリシー、棚卸しと監査の確認箇所 | 実際の組織設定が安全か、現在も同じ画面・APIか |
| `REF-AI-004` | OAuthの優先、PATを使う場合の範囲、子プロセスへの受け渡し、読み取り専用のツール公開 | IDEが秘密情報を安全に保存するか、ツール呼び出しが認可されているか |
| `REF-PORTFOLIO-001` | モデル出力を認可判断にせず、MCPのツール認可を認証情報の範囲とは別に強制する | GitHub固有の設定値や、AIセキュリティ全体への対応 |
| サプライチェーン攻撃段階 | 開発端末、AIツール、ソース管理、CI/CDのIDを一つの攻撃経路として確認する | 前後すべての段階をこの実装例が保護するという主張 |

採否と版の正本は[参照資料と仕様](../../../../../sources/README.md)、段階間の関係は
[横断分析の軸](../../../../../docs/ANALYSIS_LENSES.md)にあります。

## 対象

- GitHub.comまたはGitHub Enterprise Cloudの組織とリポジトリ。
- OAuth認可、fine-grained personal access token、personal access token (classic)、SSH認証鍵、GitHub App。
- 開発者によるアクセス、リポジトリの自動処理、GitHubへ接続する開発ツール。

## 先に決めること

| 決めること | 主な担当 |
|---|---|
| 対象組織、リポジトリ、事業上重要な操作 | プロダクト所有者 |
| 利用者認証、SSO、入社・異動・退職 | 組織管理者、IdP管理者 |
| PAT、OAuth App、GitHub Appの方針 | 組織管理者、セキュリティ担当者 |
| 自動処理のIDと利用プロセス | リポジトリ管理者、プラットフォーム担当者 |
| 端末上の保管場所とツールへの受け渡し | 端末管理者、開発者 |
| レビュー周期、失効の目標時間、インシデント対応への引き継ぎ | セキュリティ担当者、インシデント対応担当者 |

## 推奨する導入順序

### 1. 現在の権限を棚卸しする

認証情報の値は収集せず、種類、伏せ字にした識別子、所有者、目的、対象リポジトリ、権限、
作成日時、最終利用日時、有効期限、レビュー状態を記録します。APIや画面から取得できない範囲は、未確認として残します。

### 2. 利用者認証を強化する

組織の認証方針をIdPと連携し、ソースへのアクセスや認証情報の変更時に、リスクに応じたMFAを要求します。
設定変更前に、メンバーと外部コラボレーターへの影響、復旧担当者、再登録手順を確認します。

### 3. プログラムからのアクセスを制限する

- Classic PATを通常経路にしない。
- Fine-grained PATが必要なら、所有者、対象リポジトリ、権限、有効期限をレビューする。
- OAuth AppとGitHub Appを組織管理者のレビュー対象にする。
- Appのインストールごとに、対象リポジトリと権限を確認する。

### 4. 自動処理から利用者の認証情報を除く

開発者のPATやOAuthトークンを使用するボット／CIを、GitHub Appのインストールトークンなど、
短命な専用IDへ移します。利用プロセスの移行後、古い認証情報を明示的に失効させます。

### 5. 保管と受け渡しを分ける

PATやトークンを、シェルの設定ファイル、dotenvファイル、GitのリモートURL、リポジトリ、
IDEのJSON設定へ直接保存しません。承認したキーチェーンまたはシークレット管理サービスから、
必要なプロセスだけへ短時間受け渡します。

### 6. 期待する許可と拒否を確認する

本番環境から分離したテスト用リポジトリとテスト用IDで、次を確認します。

- 許可した読み取りまたは書き込みだけが成功する。
- 付与していない操作が、副作用なしで拒否される。
- 対象として選んでいないリポジトリへのアクセスが拒否される。
- テスト用認証情報を失効させた後、同じ操作が拒否される。

タイムアウト、APIの失敗、権限不足によって試験できない状態は、拒否に成功したとは扱いません。

### 7. レビューと失効を運用する

退職、異動、端末紛失、漏えい、所有者不在、用途終了、長期未使用を契機にします。
代替の認証情報の発行、ファイル削除、自然な期限切れだけで完了とせず、古い権限が拒否されるまで確認します。

## GitHubへ接続する開発ツール

ツールがOAuthを安全に利用できる場合は、利用者が管理するPATを日常的に作らない構成を優先します。
PATによる代替が避けられない場合は、ツール専用、選択したリポジトリ、読み取りに必要な権限、
有限の有効期限に限定し、親IDEや関係のない子プロセスへ値を広げません。

認証情報の範囲だけでツール操作を認可しません。書き込みや影響の大きい操作は、
別の実行時認可の境界で制御します。

## 失敗時の扱い

- 認証方針の変更で利用者がアクセスできなくなった場合、安全要件を満たす方法で再登録する。
- Appの権限が不足した場合、必要な操作だけを追加し、全リポジトリや広い書き込み権限へ戻さない。
- 証拠となる情報を取得できない場合、安全と推測せず、評価では未確認またはエラーとする。
- 緊急アクセスは、主体、対象リソース、操作、期限、別の承認者を限定する。

## 公式資料

- [特定のコミットで固定したGitHubセキュリティガイダンスの参照資料記録](../../../../../sources/README.md#spec-github-security-guidance)
- [REF-AI-004 GitHub MCPの参照資料記録](../../../../../sources/README.md#ref-ai-004)
- [GitHub credential types](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types)
- [Managing programmatic access to your organization](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization)
- [Setting a personal access token policy for your organization](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization)
- [OAuth App access restrictions](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions)
- [Limiting OAuth App and GitHub App requests and installations](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/limiting-oauth-app-and-github-app-access-requests-and-installations)
- [Reviewing GitHub Apps installed in your organization](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/reviewing-github-apps-installed-in-your-organization)
- [Requiring two-factor authentication in your organization](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)
- [Reviewing the audit log for your organization](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)
- [Setting up the GitHub MCP Server](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server)
- [Pinned GitHub MCP README](https://github.com/github/github-mcp-server/blob/3778a41476e31a072430cfee7c5d31c5f72def60/README.md)
- [Pinned GitHub MCP policies and governance](https://github.com/github/github-mcp-server/blob/3778a41476e31a072430cfee7c5d31c5f72def60/docs/policies-and-governance.md)
- [REF-PORTFOLIO-001の参照資料記録](../../../../../sources/README.md#ref-portfolio-001)
- [サプライチェーン攻撃段階と代表経路](../../../../../sources/README.md#local-supply-chain-attack-stages)
