# 設計・実装

具体的な設定・スクリプト・導入手順を探す場合は、[実装例の一覧](implementations/README.md)から18件を概観できます。

## 何を設計したいですか

全体を先に見るなら、[開発から本番運用まで](developer-to-production.md)から始めます。個別の設計は、次の五つのテーマから選べます。

- [開発環境・ソースの保護](#engineering-topic-1)
- [開発AIエージェント](#engineering-topic-2)
- [依存・CI・ビルド・リリース](#engineering-topic-3)
- [本番環境・インフラ](#engineering-topic-4)
- [監視・調査・復旧](#engineering-topic-5)

複数の領域にまたがるガイドも、主な用途のところに掲載しています。

<a id="engineering-topic-1"></a>

### 開発環境・ソースの保護

| 読者の問い | 読むガイド |
|---|---|
| 開発権限・共有前の検査・漏えい対応・復旧をどうつなぐか | [開発アクセスから漏えい対応・復旧まで](developer-access-to-recovery.md) |
| 攻撃や誤操作で壊れたrepositoryから、どう開発を再開するか | [独立したバックアップと復旧](independent-repository-backup-and-restore.md) |
| レビュー画面では同じに見えるソースを、言語の解釈と照合するには | [Unicode source review](unicode-source-review.md) |

<a id="engineering-topic-2"></a>

### 開発AIエージェント

| 読者の問い | 読むガイド |
|---|---|
| 開発agentに何を任せ、どう停止・結果確認までつなぐか | [開発agentに作業を任せ、停止と結果確認まで行う](development-agent-task-to-stop.md) |
| 開発agentのファイル・認証情報・通信をどこまで制限するか | [実行環境の隔離](development-runtime-isolation.md) |
| 承認した変更だけを外部へ送り、結果不明をどう扱うか | [操作の承認と実行](development-action-authorization.md) |

<a id="engineering-topic-3"></a>

### 依存・CI・ビルド・リリース

| 読者の問い | 読むガイド |
|---|---|
| 依存プログラムが突然マルウェア化したら、どの対策を重ねて守るか | [七原則によるサプライチェーン防御](supply-chain-defense.md) |
| 依存の更新を審査し、承認した内容をビルドへ渡すには | [依存を追加・更新して、ビルドへ渡す](dependency-update-to-build.md) |
| 外部PRの検証から正規ビルド・公開までをどう分けるか | [PRからビルド・公開への引き渡し](pull-request-to-release-build.md) |
| CIの検査をマージ条件と結果表示へどうつなぐか | [検査・受入・結果公開](workflow-analysis-gate-and-reporting.md) |
| CIで何を再利用し、何を破棄するか | [cacheとrunnerの設計](ci-state-and-runner-lifecycle.md) |
| 承認したビルドの出力を、署名・公開してそのまま使うには | [ビルドから使用まで](release-build-to-use.md) |

<a id="engineering-topic-4"></a>

### 本番環境・インフラ

| 読者の問い | 読むガイド |
|---|---|
| 正規コンテナが侵害されても、横展開やhostの操作を抑えるには | [コンテナの実行から初動まで](container-deployment-to-response.md) |
| レビューしたインフラ変更と、適用後の実環境をそろえるには | [インフラ変更の承認から実環境の確認まで](infrastructure-plan-apply-and-drift.md) |

<a id="engineering-topic-5"></a>

### 監視・調査・復旧

| 読者の問い | 読むガイド |
|---|---|
| SBOMをどこで取得し、分析・稼働先の調査へつなぐか | [SBOMから脆弱性の影響調査へ](sbom-to-vulnerability-response.md) |
| 実行時の検知を正しい対象と担当者へ渡すには | [実行時の検知から初動対応まで](runtime-detection-to-triage.md) |
| 脆弱性報告を修正・通知まで進め、不正操作にも対応するには | [問題の発見から対応・再開まで](security-signal-to-response.md) |
| 攻撃の入口から内部操作まで、どの記録を集めて調べるか | [記録の収集・保護・検索](security-event-collection-and-investigation.md) |
| 検知ルールをどう試し、配備し、初動へつなげて改善するか | [Detection Engineering](detection-engineering-lifecycle.md) |
| 修正版を作るところから、旧成果物の停止までどう確認するか | [再ビルドから稼働成果物の置換まで](deployed-artifact-recovery.md) |

個別対策の必要性・条件・代表的な方式は[Control一覧](../controls/README.md)から読みます。教材は各Controlのlearning.mdから、製品固有の導入・確認・解除はガイドやControlが案内する実装例へ進んでください。独立Controlを持たないUnicodeの教材は、その技術ガイドから読めます。ガイドの存在は組織への導入証拠ではありません。

ガイド・設計資料はこのフォルダ直下、実装例は`implementations/<用途と技術>/`にまとめます。domainの分類はControlの索引へ残します。

旧domain別の配置は整理済みです。個別の認可方式は[DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)、Webアプリ共通の要件は[Secure Coding / ASVS](../controls/records/secure-coding/README.md)から読みます。構成変更と検証範囲は[移行台帳](../docs/MIGRATION.md#engineering-restructure)に残しています。

[マッピング](../mappings/README.md)は成果物間の関係であり導入の証拠ではありません。
現在地と次の主題は[進め方と移行計画](../docs/MIGRATION_PLAN.md#現在地と次の作業)を参照してください。
