# PSB-CICD-007: Runner lifecycle isolation

## 問い

各jobを承認したrunnerへ割り当て、前jobのstate・host権限を持ち込まず、組織管理runnerの実行後に
compute・storageを破棄し、調査に必要な記録を外部へ残せるか。

## できてはいけないこと

悪意あるjobがファイルやプロセスを残して次のjobへ影響したり、metadata・host socket・管理networkから
本来渡されていない権限を得たりしてはいけません。登録解除だけでhost破棄を完了したと扱ってはいけません。

## 適用範囲と非適用

Job routing、runner group、image、起動状態、host境界、登録・管理権限、compute・storage破棄、ログ保存が対象です。
Hosted runnerではproviderの保証範囲、自組織のrunnerでは実際のprovision・teardownを分けて確認します。
Job内のbuild隔離、アプリケーション通信、runtime threat detectionは隣接するBuild Securityの責任です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `RUNNER-1` | 未信頼jobを組織のself-hosted資産へ割り当てず、group・repository・workflowを限定する |
| `RUNNER-2` | 一jobに一つの新しいcompute世代を使い、終了した世代をpoolへ戻さない |
| `RUNNER-3` | 承認済みの現行image・runnerを使い、更新はレビューした置換として扱う |
| `RUNNER-4` | 起動時に前jobのworkspace・プロセス・host credentialがないことを確認する |
| `RUNNER-5` | Metadata、host socket、管理・内部networkへの不要なアクセスを拒否する |
| `RUNNER-6` | JIT登録権限を使い回さず、通常の対話型管理とbreak-glassを分ける |
| `RUNNER-7` | Job・runner世代と対応する登録解除、compute・storage・process破棄を確認する |
| `RUNNER-8` | 必要なログを破棄前に外部へ保存し、job・runner世代で照合できる |
| `RUNNER-9` | 未取得・古い・部分的な観測や失敗を合格にせず、安全性不明の世代を再利用しない |

## 実装判断の羅針盤

組織資産への到達が不要なら、レビューしたhosted runnerを優先します。Self-hostedが必要なjobだけ
groupと実行文脈を絞り、JIT登録と一jobの新しいcomputeを対応させます。
Ephemeral登録はhostを消す操作ではありません。Workspace削除だけでも、残るprocess・disk・host設定を消したとは言えません。

無害なmarkerを二つのjobで確認する演習は残存stateの一例を観測できますが、全stateや物理消去を証明しません。
Providerの生成・破棄イベントを世代で照合し、異常な世代を次のjobへ戻さない設計にします。

## 検知への受け渡しと限界

攻撃段階7の跨job・host境界を直接扱い、段階6の管理権限と段階12の調査・復旧へ接続します。
七レイヤーではプラットフォーム、運用、ガバナンスに関係します。
Job内で完結する窃取やartifact汚染はrunnerの破棄前に起こり得ます。
ログの保存は異常検知そのものではなく、検知にはprocess・file・networkの観測、センサー健全性、alert配送・対応を別に設計します。

- [共有教材](../../../../docs/learning/ci-state-and-runner-lifecycle.md)
- [設計パターン](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)
- [REF-CICD-014と製品候補](../../../../sources/README.md#ref-cicd-014)
- [Mapping](../../../../mappings/frameworks.yaml)：GitHub固定registry、SSDF `1.1 / PW.6.1`、OSPS `2026.02.19 / OSPS-BR-01.03`、ATT&CK `v19.1 / T1552.005・T1133`。割当は移行レビュー中
