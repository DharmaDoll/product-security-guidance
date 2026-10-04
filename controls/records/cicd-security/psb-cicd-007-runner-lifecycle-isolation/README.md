# PSB-CICD-007: Runner lifecycle isolation

前のjobが残したprocessが、同じmachineで始まる次の公開jobの認証情報を読むことがあります。
このcontrolは、jobの割当から実行環境の破棄までを一つの世代として確認するものです。

学ぶ：[教材](learning.md) · 設計する：[CI state and runner lifecycle](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)

## 問い

各jobを承認したrunnerへ割り当て、前jobのファイル・process・host権限を持ち込まず、組織管理runnerの実行後に
実行環境と保存領域を破棄し、調査に必要な記録を外部へ残せるか。

## できてはいけないこと

悪意あるjobがファイルやプロセスを残して次のjobへ影響したり、クラウドのmetadata・host socket・管理networkから
本来渡されていない権限を得たりしてはいけません。登録解除だけでhost破棄を完了したと扱ってはいけません。

## 適用範囲と非適用

Jobの割当、runner group、image、起動状態、host境界、登録・管理権限、実行環境・保存領域の破棄、ログ保存が対象です。
Hosted runnerではproviderの保証範囲、自組織のrunnerでは実際の作成・破棄を分けて確認します。
Job内のbuild隔離、アプリケーション通信、runtime threat detectionは隣接するBuild Securityの責任です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `RUNNER-1` | 未信頼jobを組織のself-hosted資産へ割り当てず、group・repository・workflowを限定する |
| `RUNNER-2` | 一jobに一つの新しい実行環境を使い、終了した世代を再利用しない |
| `RUNNER-3` | 承認済みの現行image・runnerを使い、更新はレビューした置換として扱う |
| `RUNNER-4` | 起動時に前jobのworkspace・プロセス・host credentialがないことを確認する |
| `RUNNER-5` | Metadata、host socket、管理・内部networkへの不要なアクセスを拒否する |
| `RUNNER-6` | 登録権限を必要な対象・期間へ絞り、jobから持ち出させず、緊急時の対話型管理を別にする |
| `RUNNER-7` | Job・runner世代と対応する登録解除、実行環境・保存領域・processの破棄を確認する |
| `RUNNER-8` | 必要なログを破棄前に外部へ保存し、job・runner世代で照合できる |
| `RUNNER-9` | 未取得・古い・部分的な観測や失敗を合格にせず、安全性不明の世代を再利用しない |

## 新しい実行環境と破棄を確認する

組織資産への到達が不要なら、レビューしたhosted runnerを優先します。Self-hostedが必要なjobだけ
groupと実行文脈を絞り、一jobの登録と新しい実行環境を対応させます。GitHubのJIT登録は[設計ガイダンス](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md#githubの具体化と確認)で扱います。
Ephemeral登録はhostを消す操作ではありません。Workspace削除だけでも、残るprocess・disk・host設定を消したとは言えません。

無害なmarkerを二つのjobで確認する演習は残存stateの一例を観測できますが、全stateや物理消去を証明しません。
Providerの作成・破棄記録を世代で照合し、異常な世代を次のjobへ戻さない設計にします。
Jobが終了・取消された場合も、登録解除、実体の破棄、必要なログの保存は別に確認します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は、前jobの影響やhostの権限が境界を越えないか確認する項目です。設計レビューのチェックリストとして使えます。
試す場合は承認した使い捨て環境と無害なmarkerを使い、実認証情報やmetadataの内容は取得・保存しません。

- **RUNNER-1**：未信頼PRや別repository・workflowが、限定した組織runnerへjobを割り当てられないか。
- **RUNNER-2・4**：別のrunner名・再登録・workspace削除だけで、前jobと同じ実行環境や残存processを再利用しないか。
- **RUNNER-3**：承認していないimageや未対応runner版、古い外部volumeから起動しても、割当を続けないか。
- **RUNNER-5**：不要なmetadata、管理socket、内部networkへ、別の通信経路やIP形式から到達できないか。
- **RUNNER-6**：Jobから登録用の管理credentialを読めたり使い回せたりしないか。緊急接続の許可が通常のjobへ残らないか。
- **RUNNER-7・9**：Job取消・異常終了、登録解除だけの成功、破棄の失敗・観測不能があっても、その世代へ次のjobを割り当てないか。
- **RUNNER-8・9**：ログ配送を中断すると、外部保存の未完了を識別できるか。破棄済みの表示だけで調査記録も残ったと判断しないか。
- **RUNNER-9**：一つのmarkerがないことや、古い・別世代の破棄記録を、全残存経路の確認済みにしないか。

## 検知への受け渡しと限界

攻撃段階7のjob間・host境界を直接扱い、段階6の管理権限と段階12の調査・復旧へ接続します。
七レイヤーではプラットフォーム、運用、ガバナンスに関係します。
Job内で完結する窃取やartifact汚染はrunnerの破棄前に起こり得ます。
ログの保存は異常検知そのものではなく、検知にはprocess・file・networkの観測、センサー健全性、alert配送・対応を別に設計します。

外部に保存されたcacheは破棄の外に残るため[CICD-009](../psb-cicd-009-cache-trust-boundary/README.md)、PR由来の全経路は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、実行中のbuildの権限・通信は[BUILD-001](../../build-security/psb-build-001-build-containment/README.md)へ分けます。

- [教材](learning.md)
- [設計パターン](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)
- [REF-CICD-014と製品候補](../../../../sources/README.md#ref-cicd-014)
- [Mapping](../../../../mappings/frameworks.yaml)：GitHub `GHAS-REF-SECURE-USE`、OSPS `2026.02.19 / OSPS-BR-01.03`、ATT&CK `v19.1 / T1552.005`との部分的な設計関係。旧`PW.6.1`と`T1133`、GitHubの侵害時の影響解説は[移行台帳](../../../../docs/MIGRATION.md)に非継承理由を記録
