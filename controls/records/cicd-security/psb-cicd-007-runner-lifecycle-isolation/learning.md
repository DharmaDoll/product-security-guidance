# Runner lifecycle isolation — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)

## シナリオ：新しいjobが前のjobを引き継ぐ

信頼できないPRのテストが、自組織のrunner（self-hosted runner）へ起動ファイルとbackground processを残します。
次のrelease jobは同じmachineへ割り当てられ、残ったprocessが公開用の認証情報を読み取ります。
Job名やworkspaceが変わっても、実行環境・保存領域・processが残れば境界は新しくなっていません。

攻撃には、前のjobが変更できるstate、そのstateが残る経路、後のjobが持つ権限の三つが必要です。
一jobごとに新しい実行環境を割り当て、終了後に破棄し、前のprocessや書込領域を引き継がなければ、
このjob間の経路を切れます。ただし、正規job内で悪意ある依存コードが動く問題は別に残ります。

## 登録名と実体を分ける

新しいrunner名や再登録は、新しいhostの証拠ではありません。ここでいう世代は、jobへ割り当てた実行環境の実体を区別するための識別です。
確認したいのは、どの実体が割り当てられ、起動時に何が存在し、終了後にprocess・memory・保存領域・credentialがどう処理されたかです。
観測用markerが一つ見つからなくても、すべての残存経路を調べたことにはなりません。

GitHubのephemeral登録は一job後にrunnerの登録を解除します。Hostを消す処理は利用者側で別に用意します。
JIT（just-in-time）登録も、一job用の登録と実行環境の作成・破棄を結び付ける方式であり、登録成功だけで新しい実体ができたとは判断しません。
製品の事実と本PJの採用判断は[runner資料の記録](../../../../sources/README.md#ref-cicd-014)へ分けています。

## Jobが取消された後も破棄を追う

Jobが終わった表示、runner一覧から消えたこと、実行環境・保存領域の破棄は別の状態です。
取消や異常終了でも同じ世代を追い、破棄の失敗・観測不能を記録し、次のjobへ戻しません。
破棄をjob自身の後片付けだけへ任せると、悪意あるjobや異常終了がその処理を妨げるため、外側の管理処理で確認します。

調査ログは外へ保存します。配送の失敗を見えなくしてrunnerを残し続けたり、破棄したからログも保存済みと扱ったりせず、
再利用を止めた状態で隔離・破棄と記録不足を別に扱います。

External cacheはrunnerの外に残るため、runnerを破棄しても消えません。Cacheの保存者と利用者は
[Cache trust boundary](../psb-cicd-009-cache-trust-boundary/learning.md)で別に確認します。

## 振り返りで問うこと

- 一つのjobが終わった後、どの実行環境、process、memory、保存領域が残るか。
- 信頼の異なるjobが同じhostや管理socketへ到達しないか。
- 破棄に失敗したrunnerが次のjobを受け取らないか。
- Runner imageを更新しても、外部volumeやcacheから古いstateを戻していないか。
- 破棄ログの存在を、実際に残存物がない証拠と取り違えていないか。

この教材は[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)と
[攻撃段階5→7](../../../../docs/ANALYSIS_LENSES.md)を使い、runnerの実体とjob境界を読み解くための
リポジトリ独自の解釈です。実環境のrunner破棄を確認した記録ではありません。

診断項目は[control](README.md#failure-checks)、割当・ログ保存・破棄を結ぶ方式は[設計pattern](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)へ進めます。
PRから権限を使う経路は[Untrusted PR boundary](../psb-cicd-005-untrusted-pr-boundary/learning.md)、実行中の権限・通信は[Build containment](../../build-security/psb-build-001-build-containment/learning.md)で確認します。
