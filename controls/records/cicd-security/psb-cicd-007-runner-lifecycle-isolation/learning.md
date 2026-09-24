# Runner lifecycle isolation — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)

## シナリオ：新しいjobが前のjobを引き継ぐ

信頼できないPRのtestが、self-hosted runnerへ起動ファイルとbackground processを残します。
次のrelease jobは同じmachineへ割り当てられ、残ったprocessがrelease用の認証情報を読み取ります。
Job名やworkspaceが変わっても、compute、storage、processが残れば境界は新しくなっていません。

攻撃には、前のjobが変更できるstate、そのstateが残る経路、後のjobが持つ権限の三つが必要です。
一jobごとに新しいcomputeを割り当て、終了後に破棄し、前のprocessや書込領域を引き継がなければ、
この跨job経路を切れます。ただし、正規job内で悪意あるdependencyが動く問題は別に残ります。

## 登録名と実体を分ける

新しいrunner名や再登録は、新しいhostの証拠ではありません。確認したいのは、どのcomputeが割り当てられ、
起動時に何が存在し、終了後にprocess・memory・storage・credentialがどう破棄されたかです。
観測用markerが一つ見つからなくても、すべての残存経路を調べたことにはなりません。

External cacheはrunnerの外に残るため、runnerを破棄しても消えません。Cacheの保存者と利用者は
[Cache trust boundary](../psb-cicd-009-cache-trust-boundary/learning.md)で別に確認します。

## 振り返りで問うこと

- 一つのjobが終わった後、どのcompute、process、memory、storageが残るか。
- 信頼の異なるjobが同じhostや管理socketへ到達しないか。
- 破棄に失敗したrunnerが次のjobを受け取らないか。
- Runner imageを更新しても、外部volumeやcacheから古いstateを戻していないか。
- 破棄ログの存在を、実際に残存物がない証拠と取り違えていないか。

この教材は[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)と
[攻撃段階5→7](../../../../docs/ANALYSIS_LENSES.md)を使い、runnerの実体とjob境界を読み解くための
リポジトリ独自の解釈です。実環境のrunner破棄を確認した記録ではありません。
