# CI/CD Security

変更内容を検証する処理と、リポジトリ、クラウド、リリース環境へ影響を与えられる処理を、同じ信頼境界へ置かないようにします。

| コントロール | 問うこと | できてはいけないこと |
|---|---|---|
| [PSB-CICD-005 Untrusted PR boundary](psb-cicd-005-untrusted-pr-boundary/README.md) | コントリビューターが変更できるコードや状態を、権限を持つ処理から分離できるか | 未信頼のコード、成果物、キャッシュ、出力が、書き込み権限、秘密情報、OIDC、保護された環境、永続ランナーを利用できる |
| [PSB-CICD-006 Workload federation boundary](psb-cicd-006-workload-federation-boundary/README.md) | 承認workloadだけへ必要なcloud権限を必要期間だけ渡せるか | 正規tokenであれば別contextや過大な操作権限まで許可される |
| [PSB-CICD-007 Runner lifecycle isolation](psb-cicd-007-runner-lifecycle-isolation/README.md) | jobの状態や権限を次のjobへ残さず、実行資産を破棄できるか | 登録だけ消したhostや共有storageが後続jobへ再利用される |
| [PSB-CICD-009 Cache trust boundary](psb-cicd-009-cache-trust-boundary/README.md) | 低信頼のwriterが作ったstateを権限を持つconsumerへ渡していないか | key一致だけで復元内容を承認済みと判断する |

## 読み進め方

[Runner教材](psb-cicd-007-runner-lifecycle-isolation/learning.md)、[Cache教材](psb-cicd-009-cache-trust-boundary/learning.md)と
[CI state and runner lifecycle pattern](../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)で、再利用するcacheと破棄するhostを分けて設計します。

Cloudへ接続する場合は[Workload federation boundary](psb-cicd-006-workload-federation-boundary/README.md)と
[学習ノート](psb-cicd-006-workload-federation-boundary/learning.md)で、未信頼PR分離後も残る交換条件・操作権限を確認します。

1. コントロール記録で、未信頼の状態と権限を分けるためのセキュリティ特性を確認する。
2. [学習ノート](psb-cicd-005-untrusted-pr-boundary/learning.md)で、pwn requestが成立する条件と、イベント名だけでは安全性を判断できない理由を理解する。
3. [Untrusted PR boundary pattern](../../../engineering/cicd-security/untrusted-pr-boundary/README.md)で、producerとconsumerの信頼関係を設計する。
4. GitHub Actionsを利用する場合に限り、[実装例](../../../engineering/cicd-security/untrusted-pr-boundary/implementations/github-actions/README.md)を読む。
5. [横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で、ソース変更、依存関係、CIのID、ランナー、リリースへ残る責任を確認する。
