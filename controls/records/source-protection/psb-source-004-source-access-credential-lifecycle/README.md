# PSB-SOURCE-004: Source credential lifecycle

さらに具体的に学ぶ：[学習ノート](learning.md)

設計する：[Source credential lifecycle pattern](../../../../engineering/source-protection/source-access-credential-lifecycle/README.md)

## 問い

ソース管理基盤へアクセスする認証情報とセッションを、必要な主体、目的、リソース、操作、期間に限定し、
用途終了、異動、退職、端末紛失、漏えいが発生した際に、古い権限を確実に拒否できるか。

## できてはいけないこと

盗まれた認証情報、過剰な認証情報、所有者が不明な認証情報、不要になった認証情報が、
本来の用途を越えてソースコード、ワークフロー、リリース、組織情報へアクセスできる状態を残してはいけません。

## なぜ重要か

認証情報は単なる秘密文字列ではなく、ソース管理基盤が操作を許可する根拠です。
安全な場所へ保管していても権限が広すぎれば被害は拡大します。また、有効期間が短くても、
関連するセッションが残れば失効は完了していません。保管、権限、有効期間、棚卸し、失効、監査を、
一つのライフサイクルとして扱います。

## 横断分析での位置

| 分析軸 | 関係 | このコントロールが扱うこと | 次へ引き継ぐこと |
|---|---|---|---|
| プラットフォームとインフラストラクチャ | 直接 | ソース管理基盤が受け入れる権限の発行、範囲、期間、失効 | ソース変更の内容とレビュー、管理面の変更保証 |
| 運用 | 隣接 | 棚卸し、失効、監査による封じ込めの準備 | 影響範囲の特定、復旧、実環境の監視と証拠 |
| 攻撃段階1：開発端末と端末内の信頼境界 | 直接 | 端末から認証情報を盗まれても、到達できる権限と期間を狭める | 端末自体の防御と侵害検知 |
| 攻撃段階3：AI支援開発 | 隣接 | MCPやAIツールへ渡す認証情報の範囲を狭める | モデル出力を信頼せず、ツール認可をモデルの外側で強制する |
| 攻撃段階6：CI/CDのIDと管理面 | 直接 | 利用者の認証情報と、自動処理用の短命なIDを分ける | OIDCの信頼条件、管理面の変更、ランナーの隔離 |

この位置付けは[`REF-PORTFOLIO-001`](../../../../sources/README.md#ref-portfolio-001)の七つのレイヤーと、
[`LOCAL-SUPPLY-CHAIN-ATTACK-STAGES`](../../../../sources/README.md#local-supply-chain-attack-stages)の攻撃段階を
使った探索用の関係です。コントロールへの合格や組織への導入を示しません。全体像は
[横断分析の軸](../../../../docs/ANALYSIS_LENSES.md)を参照してください。

## 適用範囲

開発者または自動処理がソース管理基盤へ接続する際に使用する、OAuth認可、アクセストークン、PAT、
SSH認証鍵、アプリケーションID、ワークロードID、およびそれらから作られるセッションに適用します。

次は直接の対象ではありません。

- 開発端末全体のパッチ適用、EDR、ディスク暗号化。
- ソース管理基盤におけるメンバー、チーム、リポジトリ既定値の統制全般。
- 認証情報の漏えい後に行う、ソースコード、複製済みリポジトリ、成果物を横断したインシデント対応全般。
- AIエージェントやMCPツールが認証情報を取得した後の、ツール操作の認可。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `SRC-AUTH-1` | 各権限を、主体、目的、対象リソース、許可する操作、有効期限と明示的に結び付ける |
| `SRC-AUTH-2` | 認証情報の発行や機微な変更では、対象リスクに応じた強固な認証を要求する |
| `SRC-AUTH-3` | 自動処理では、開発者個人の再利用可能な認証情報ではなく、処理内容を限定したワークロードIDを使う |
| `SRC-AUTH-4` | 認証情報を保護された場所に保管し、必要な処理だけへ受け渡す |
| `SRC-AUTH-5` | 現在有効な認証情報を定期的に棚卸しし、ライフサイクル上の事象が発生したら、認証情報と関連セッションを失効させ、それらによるアクセスが拒否されることを確認する |
| `SRC-AUTH-6` | 発行、権限変更、利用、失効の記録を、所有者と対象リソースに結び付けて調査できる |

## 実装判断の羅針盤

1. 最初に「誰が、どのリソースへ、どの操作を行うか」を決め、認証情報の種類はその後で選ぶ。
2. 人が対話的に使う権限と、自動処理が使うIDを分ける。
3. 認証情報の名称ではなく、実際の対象リソース、権限、有効期間、受け渡し経路を評価する。
4. 自動失効だけに依存せず、退職、異動、紛失、漏えいを失効の契機にする。
5. 新しい認証情報の発行やファイルの削除を失効とみなさず、古い認証情報によるアクセスが拒否されることを確認する。
6. 監査ログを現在の認可状態の代わりにしない。現在有効な権限と過去の事象を別々に確認する。

製品固有の画面名や設定値は、コントロールに固定しません。GitHub向けの実装案は
[GitHub実装例](../../../../engineering/source-protection/source-access-credential-lifecycle/implementations/github/README.md)にあります。

## 判定例

| 観測した状態 | このコントロールでの判断 |
|---|---|
| トークンはキーチェーンにあるが、すべてのリポジトリへの書き込み権限を持つ | 不合格。安全な保管だけでは権限は狭くならない |
| きめ細かな権限を設定できるPAT（Fine-grained PAT）だが、所有者、対象リポジトリ、有効期限を確認していない | 合格を裏付けない |
| 自動処理が開発者個人のPATを使っている | 不合格候補。人とワークロードのライフサイクルを分離できない |
| 新しい認証情報へ切り替えたが、古い認証情報を失効させていない | 不合格。置き換えは失効ではない |
| 提供元のAPIから状態を取得できない | 安全とは判断できない。評価では`NOT_CHECKED`または`ERROR`とする |
| 適切に範囲を絞った認証情報でも、AIエージェントが危険な書き込みツールを呼び出せる | このコントロールに隣接する、実行時の認可に関する問題 |

## 保証しない範囲

このコントロールは、ソース管理基盤、IdP、組織管理者、認証済みの端末セッションが侵害されないことを
保証しません。正規の手順で既に複製されたソースコードや、流出済みのソースコードも、認証情報の失効では回収できません。

## 関連資料

- [学習ノート](learning.md)
- [Source credential lifecycle pattern](../../../../engineering/source-protection/source-access-credential-lifecycle/README.md)
- [Credential is delegated authority, not a string](../../../../docs/insights/credential-is-delegated-authority.md)
- [Security effects live at enforcement points](../../../../docs/insights/security-effects-live-at-enforcement-points.md)
- [パイロット内のマッピング](../../../../mappings/pilot.yaml)
- [フレームワーク対応関係](../../../../mappings/frameworks.yaml)
- [参照資料と仕様](../../../../sources/README.md)
- [横断分析の軸](../../../../docs/ANALYSIS_LENSES.md)
- [横断分析の機械可読マッピング](../../../../mappings/analysis-lenses.yaml)

## 参照仕様とマッピング

| 参照資料 | バージョン／ID | 関係 |
|---|---|---|
| GitHubセキュリティガイダンス | `github/docs@b17436d...`／`GHSC-SECURE-ACCOUNTS`、`GH-ADMIN-CREDENTIAL-TYPES`、`GH-ADMIN-SAML-IAM`、`GH-ADMIN-SCIM-ORGANIZATIONS` | GitHub実装を`supports` |
| MITRE ATT&CK | `v19.1`／`T1078`、`T1552.001` | 有効なアカウントの悪用と、ファイル内の認証情報露出を`mitigates` |
| NIST SSDF | `1.1 (SP 800-218, 2022)`／`PS.3.1` | ソースコード保護を`supports` |
| OpenSSF OSPS Baseline | `2026.02.19`／`OSPS-AC-01.01` | 機微な操作に対するMFAを`supports` |
| OWASP Agentic Top 10 | `2026`／`ASI03` | MCPなど、AIエージェントを介したアクセスに限り`mitigates` |

参照したコミット、セキュリティ特性への割り当て、根拠、レビュー状態は
[フレームワーク対応関係](../../../../mappings/frameworks.yaml)にあります。マッピングは、組織への導入、
完全な対応範囲、正式な準拠を示すものではありません。

## 一次資料

- [GitHubセキュリティガイダンスの参照資料記録](../../../../sources/README.md#spec-github-security-guidance)
- [REF-AI-004 GitHub MCPガイダンス](../../../../sources/README.md#ref-ai-004)
- [REF-USER-001 開発端末ハードニング資料](../../../../sources/README.md#ref-user-001)
- [REF-PORTFOLIO-001 プロダクトセキュリティ概観](../../../../sources/README.md#ref-portfolio-001)
- [サプライチェーン攻撃段階と代表経路](../../../../sources/README.md#local-supply-chain-attack-stages)
- [GitHub: Managing programmatic access to your organization](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization)
- [GitHub: Credential types](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types)
- [GitHub: Requiring two-factor authentication in your organization](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)
- [GitHub: Reviewing the audit log for your organization](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)
