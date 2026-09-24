# CI state and runner lifecycle — 学習ノート

## シナリオ：新しいrunnerなのに古い攻撃が届く

PRのtestが悪意ある依存を実行し、共有stateへ改変したtoolを残します。
次のrelease jobは新しいVMを使いますが、そのstateをcacheから復元して実行します。
Runnerを破棄してもcacheから高権限jobへ届く経路は残ります。

逆にcacheを使わなくても、同じself-hosted machineを繰り返し使い、前jobの起動ファイル・プロセスが残ると
後続jobへ影響できます。この二つは保存場所と制御主体が違います。

| 残るstate | 問うこと | 主な責任 |
|---|---|---|
| 外部cache | 誰が保存し、誰が何として復元して使うか | Cache trust boundary |
| Runnerのcompute・storage・process | 何が起動時に存在し、終了後に何を破棄したか | Runner lifecycle isolation |
| Artifact・release | 承認した出力と公開する内容が同じか | Release Integrityへ受け渡す |
| 外部ログ | 何を観測でき、センサー・配送が稼働しているか | Runtime検知・運用へ受け渡す |

Stateは前の処理から残るファイル・プロセス・情報です。Producerはそれを作る側、consumerは利用する側です。
Runtime検知は実行中の振る舞いを観測して異常を知らせる仕組みで、stateの破棄と同じではありません。

## 攻撃が成立する条件

攻撃者が変更できるstate、後続への復元・残存経路、そのstateを実行・信頼するconsumerの接続が必要です。
Consumerが署名・公開権限を持つなら、その権限に応じた汚染や不正操作へ届きます。
低信頼stateを高権限jobが使わず、新しいcomputeでも前jobを引き継がなければ、これらの跨job経路は成立しません。
正規job内で悪意あるdependencyが動く経路は別に残ります。

## 誤解を解く

Keyのexact hitは内容が正しいという意味ではありません。新しい登録名は新しいhostを意味しません。
Tokenがread-onlyでもhost metadataやsocketへ届けば別の権限を使えます。
二jobのmarkerが見つからなくても、すべての永続化経路を調べたことにはなりません。
破棄後にログが残っても、異常を検知しalertを届けた証明にはなりません。

レビューでは、writer・reader・pathと、job・compute世代・破棄イベント・外部ログを別の流れとして説明してください。
Cache障害からclean installへ戻る場合も、hash検証を省かないことを確認します。

これは[REF-PORTFOLIO-001](../../sources/README.md#ref-portfolio-001)からプラットフォームと運用の受け渡しを
確認し、[攻撃段階5→7→9・12](../ANALYSIS_LENSES.md)を追うリポジトリ独自の教材です。
[Pattern](../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)で方式を選んでください。

対応する成果物：[PSB-CICD-007](../../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) · [PSB-CICD-009](../../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) · [全教材索引](README.md)
