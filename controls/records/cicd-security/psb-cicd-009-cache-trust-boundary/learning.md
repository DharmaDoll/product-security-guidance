# Cache trust boundary — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)

## シナリオ：新しいrunnerへ古い攻撃が届く

信頼できないPRのtestが共有cacheへ改変したtoolを保存します。次のrelease jobは新しいVMで始まりますが、
そのcacheを復元してtoolを実行します。Runnerを毎回破棄しても、外部に保存したstateから高権限jobへ届く経路は残ります。

Cache keyが一致することは、内容が正しいことを意味しません。攻撃には、書き手がcacheを変更できること、
後のjobが同じentryを取得できること、その内容を信頼して実行することが必要です。

## 保存と利用の両方を見る

Cacheの判断では、keyだけでなく次を結び付けます。

- 誰がどのrevisionとjobから保存できるか。
- どのrepository、branch、OS、architecture、tool版、lockfileに使えるか。
- Consumerがcache内容を実行・公開する前に何を再検証するか。
- Exact keyが見つからないとき、どのprefixや古いentryへfallbackするか。
- Cache serviceが失敗したとき、完全性確認を省略せずclean installへ戻れるか。

同じhostに残るprocessやworkspaceはcacheとは保存場所と管理者が異なります。
[Runner lifecycle isolation](../psb-cicd-007-runner-lifecycle-isolation/learning.md)で別に確認します。

## 振り返りで問うこと

- 信頼できないjobが、より強い権限を持つjobのcacheを書けないか。
- 広いrestore prefixで別branch、別OS、別tool版のentryを受け入れないか。
- Cache hitによってhash照合、install、build等の必要な確認を飛ばしていないか。
- Cache削除や期限切れだけで、consumer側の再検証を不要としていないか。
- Cache障害やmetadata不足を、安全なmissと同じ意味にしていないか。

この教材は[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)と
[攻撃段階5→7→9](../../../../docs/ANALYSIS_LENSES.md)を使い、外部stateからconsumerへの受け渡しを
読み解くためのリポジトリ独自の解釈です。実環境のcache設定を確認した記録ではありません。
