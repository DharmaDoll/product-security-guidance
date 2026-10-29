# 実装例の一覧

特定の技術で対策を導入し、動作を確認して、必要なら解除するための具体例です。コードだけでなく、GitHubの設定手順なども含みます。使いたいものだけを選びます。

## Control・設計ガイドとの関係

- [Control](../../controls/README.md)：何を満たす必要があるか、なぜ必要か。
- [設計ガイド](../README.md)：対策をどう組み合わせ、工程間の抜けをどう防ぐか。
- 実装例：その設計の一部分を、特定の製品・言語でどう導入・確認・解除するか。

一つのガイドに実装例が複数あっても、実装例がなくても構いません。実装例だけでControl全体を満たすわけではありません。下表から各READMEを開くと、対象版、前提、導入・確認・解除方法と制限を読めます。関連Controlと根拠は各READMEまたは関連ガイドからたどれます。

## 用途から選ぶ

| したいこと | 実装例 | 提供するもの | 関連する設計ガイド |
|---|---|---|---|
| 公開直後のnpm依存を採用するまで待つ | [npm-release-cooldown](npm-release-cooldown/README.md) | 設定ファイル・導入手順 | [依存の変更からビルドへ](../dependency-update-to-build.md) |
| pipのソースビルドを止め、hashを照合する | [pip-install-policy](pip-install-policy/README.md) | 設定・ローカルテスト | [依存の変更からビルドへ](../dependency-update-to-build.md) |
| PRの依存差分を審査する | [github-dependency-review](github-dependency-review/README.md) | workflow・導入手順 | [依存の変更からビルドへ](../dependency-update-to-build.md) |
| GitHub tokenの範囲と失効を確かめる | [github-credential-lifecycle](github-credential-lifecycle/README.md) | 設定・確認の手順 | [開発アクセスと復旧](../developer-access-to-recovery.md) |
| 組織の共通設定と適用漏れを調べる | [github-organization-review](github-organization-review/README.md) | 設定・確認の手順 | [開発アクセスと復旧](../developer-access-to-recovery.md) |
| 公開GitHubで自社ドメイン・メールを探し通知する | [github-indicator-watch](github-indicator-watch/README.md) | Pythonスクリプト・テスト | [開発アクセスと復旧](../developer-access-to-recovery.md) |
| Gitの履歴を別の場所に保管し復旧する | [git-mirror-recovery](git-mirror-recovery/README.md) | 操作手順・ローカルテスト | [独立したバックアップと復旧](../independent-repository-backup-and-restore.md) |
| 開発agentの指示ファイル変更をレビューへ回す | [github-agent-guidance-review](github-agent-guidance-review/README.md) | CODEOWNERS例・設定手順 | [開発agentの作業と停止](../development-agent-task-to-stop.md) |
| 開発agentの実行時間と停止を確認する | [linux-agent-deadline](linux-agent-deadline/README.md) | Linux操作手順・テスト | [開発agentの作業と停止](../development-agent-task-to-stop.md) |
| workflowの外部参照が固定されているか調べる | [python-workflow-refs](python-workflow-refs/README.md) | Pythonスクリプト・workflow・テスト | [PRからビルド・公開へ](../pull-request-to-release-build.md) |
| jobごとの権限と承認を絞る | [github-job-authority](github-job-authority/README.md) | workflow・設定手順 | [PRからビルド・公開へ](../pull-request-to-release-build.md) |
| 外部PRの検証と権限を使う処理を分ける | [github-untrusted-pr](github-untrusted-pr/README.md) | workflow・確認手順 | [PRからビルド・公開へ](../pull-request-to-release-build.md) |
| GitHubの実行主体をAWSの一時権限へ結び付ける | [github-aws-federation](github-aws-federation/README.md) | IAM設定例・確認手順 | [PRからビルド・公開へ](../pull-request-to-release-build.md) |
| CycloneDX SBOMと指定した成果物の対応を確認する | [cyclonedx-artifact-binding](cyclonedx-artifact-binding/README.md) | Python検証器・サンプル・テスト | [SBOMから影響調査へ](../sbom-to-vulnerability-response.md) |
| Podの過大な権限を起動前に拒否する | [kubernetes-psa-cel](kubernetes-psa-cel/README.md) | Kubernetes設定・確認スクリプト | [コンテナの実行から初動へ](../container-deployment-to-response.md) |
| Pod間の通信を必要な経路へ絞る | [kubernetes-networkpolicy](kubernetes-networkpolicy/README.md) | Kubernetes設定・確認スクリプト | [コンテナの実行から初動へ](../container-deployment-to-response.md) |
| Podの資源消費に上限を設ける | [kubernetes-resourcequota-cel](kubernetes-resourcequota-cel/README.md) | Kubernetes設定・確認スクリプト | [コンテナの実行から初動へ](../container-deployment-to-response.md) |
| Pythonソースの見た目と解釈の違いを調べる | [python-unicode-source-review](python-unicode-source-review/README.md) | Python検査器・テスト | [Unicode source review](../unicode-source-review.md) |

## ファイルを分ける基準

説明や短い比較例はREADMEへ書きます。コピーして使う設定、実行するスクリプト、テストが直接読む入力はファイルとして残します。本文とファイルに同じ設定の正本を二つ作りません。

通常のファイルは各実装例の直下に置き、`secure/`という名前だけの階層は作りません。`tests/`や`fixtures/`などは役割がある場合だけ使います。危険な比較例は導入用ファイルと分け、説明で十分ならREADME内に置きます。

ローカルのテスト成功と、GitHub・AWS・Kubernetesなどでの実適用は別です。確認済みの範囲は各READMEを参照してください。特に実環境へ変更を加える確認スクリプトは、前提と解除方法を読んでから使い捨ての対象で実行します。
