# PSB-SOURCE-006: Source organization security posture

ソース管理サービスの組織で、共通方針が対象のリポジトリ・人・Appへ実際に適用され、後の変更や確認漏れにも気づけるかを問います。読者は組織の管理者、セキュリティ担当、CI担当です。守る資産は、ソースと開発経路へアクセス・変更できる権限、および複数リポジトリへ広がる共通設定です。

例えば、組織で秘密情報の検査を新規リポジトリの既定値にしていても、別組織から移管したリポジトリは適用対象から漏れることがあります。管理画面に方針が存在することと、対象すべてでその方針が効いていることは別です。

まず対象のリポジトリを一覧にし、それぞれに必要な設定が実際に効いているかを見ます。設定が一つの画面に表示されるだけでは、既存・移管済み・新規のすべてに適用されたとは判断しません。

## 適用範囲と直接の失敗

一つのソース管理組織と、必要なら上位のenterprise方針を対象にします。共通の認証・アクセス・repository作成・公開範囲・CI・セキュリティ機能について、組織が選んだ方針、適用対象、現在の状態、変更後の確認を扱います。

直接の失敗は、管理者権限の窃取や設定ミスで共通設定・付与済みの権限が変わり、対象漏れ、個別上書き、監視停止のために未承認のアクセスや実行権限が残ることです。確認用IDの権限不足、APIの部分取得、ログイン基盤（IdP）との連携障害も、状態を見誤る要因です。

## 満たすこと

| 特性 | 判断・確認すること |
|---|---|
| ORG-POSTURE-1 | 組織の固定した識別子、承認した方針の版、適用する対象を決める。Repository・member・team・外部協力者・App等の必要な一覧を、取得範囲と時点を付けて確認する |
| ORG-POSTURE-2 | 共通の認証条件、初期権限、作成・公開・fork・CIの方針と、それらを変更・迂回できる主体を管理する。上位方針、既定値、強制する制限を区別する |
| ORG-POSTURE-3 | 方針の存在と対象ごとの実適用を分ける。既存・新規・移管・再開したrepositoryについて、適用中、失敗、解除、個別上書き、対象外の理由を確認する |
| ORG-POSTURE-4 | 管理者、メンバー、チーム、外部協力者、Appに今ある権限を、責任者・用途・対象と照らす。ログイン基盤で無効にしたことと、ソース管理側の権限が消えたことを混同しない |
| ORG-POSTURE-5 | 重要な変更の記録と、定期的に取得した現在の状態を組み合わせて方針との差を確認する。イベントがないことや前回との差がないことだけで問題なしにしない |
| ORG-POSTURE-6 | 確認できた範囲、期限切れの確認、未確認、対象外、取得障害を区別する。部分取得・権限不足・通知経路の停止を良好な状態に変換しない |
| ORG-POSTURE-7 | 方針から外れた状態と取得・通知の障害を担当者へ渡し、期限、限定した例外、修正後の再確認を追跡する。変更や通知の受付だけで完了にしない |

設定の強制点はソース管理側、対象との照合はレビュー担当または収集・評価経路です。確認経路が壊れたときに、どの設定変更・権限追加・実行を保留するかは用途ごとに決めます。組織の状態が不明になったことを、すべての開発アクセスを自動停止する要件にはしません。

直接の判断根拠は[REF-SOURCE-ORGANIZATION-POSTURE-001](../../../../sources/README.md#ref-source-organization-posture-001)、GitHubの製品仕様は[SPEC-GITHUB-ORGANIZATION-POSTURE](../../../../sources/README.md#spec-github-organization-posture)です。Owner数、確認間隔、保持期間、許可する作成・fork・App権限は、組織の必要性に応じて決めます。

## 診断で確認する項目（異常時テスト）

以下は設計レビュー・診断で使う観点です。実施済みの結果ではありません。

| 試す状況 | 確認する結果 |
|---|---|
| 既定値を設定した後にrepositoryを作成・移管・再開する | 各経路の適用を別々に確認し、新規作成の成功から移管や既存対象へ一般化しない |
| Repository管理者が共通設定を変更する | 強制された項目では拒否され、許可された上書きは対象ごとの状態変化として検出される |
| 組織のtoken既定値は読取り専用だがworkflowはwriteを要求する | 既定値を権限の上限とみなさず、個別workflowの実効権限をCI担当へ渡す |
| 退職者、owner不明のteam・App、期限切れの外部協力者が残る | 組織のgrant照合から認証情報・IDの所有者へ渡す。GitHubの一覧だけで在籍や用途を判断しない |
| PAT・App・OAuthの組織方針を変える | 新しい発行・申請の制限と、既存のtoken・承認・installationの実効アクセスを別に確認する。方針変更だけで不要な認可の失効を完了にしない |
| 最初のpageだけ取得する、private対象が見えない、取得中に対象が変わる | 方針が適用すべき一覧と照合し、取得の不足や時点の不一致を未確認・障害として残す |
| 設定の取得に失敗するが前回は良好だった | 前回を現在の成功として再利用せず、どの対象・特性を確認できないか示す |
| Audit配送が止まる、検索条件から重要変更が漏れる | 現在状態の照合を残し、イベントの取得範囲・保持・配送を別に確認する |
| 通知が届かない、変更ticketが閉じる、例外が期限切れになる | 未対応の状態を担当者へ残し、再取得した実値と必要な拒否確認で修正を判断する |

## 隣接する成果物との分担

| 境界 | 詳細を持つ成果物 |
|---|---|
| 認証情報の保管と、ソース管理側の権限・失効 | 端末上の保管は[SOURCE-007](../psb-source-007-developer-local-credential-storage/README.md)、ソース管理側の権限・失効は[SOURCE-004](../psb-source-004-source-access-credential-lifecycle/README.md)。本controlは組織側に残る利用者・チーム・Appの権限を照合する |
| 秘密情報の検査と公開面の観測 | [SOURCE-002](../psb-source-002-secret-publication-boundary/README.md)・[SOURCE-003](../psb-source-003-public-source-exposure-triage/README.md)。本controlは選んだ検査設定の適用漏れを扱い、検出範囲や精査を定義しない |
| CIの外部参照、job権限、未信頼入力、cache、runner、workload identity | [CICD-001](../../cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)・[CICD-004](../../cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)と[CI/CDの一覧](../../cicd-security/README.md)。組織の設定だけでworkflowや実行環境を検証したことにしない |
| 削除制限、独立したbackup、復旧 | [SOURCE-005](../psb-source-005-repository-recovery-independence/README.md)。本controlの監視は復旧手段を提供しない |
| 例外とincident対応 | [GOV-002](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)・[GOV-001](../../governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)。設定差分だけで侵害を断定しない |

個別controlへの合格、組織全体の安全性、正式な準拠はこのcontrolから導きません。[教材](learning.md)から具体的な適用漏れを追い、[設計パターン](../../../../engineering/source-protection/organization-baseline-and-drift-review/README.md)で手作業と自動収集を選びます。[GitHub手順](../../../../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)は現在の設定を確認する入口です。旧10項目の採否は[移行判断](../../../../docs/MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)にあります。
