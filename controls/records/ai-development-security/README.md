# AI Development Security

開発者端末・IDE・CLI・repository・CIで使うagentについて、**何を読ませ、何を追加し、何を実行させ、いつ止めるか**を確認します。製品自体のAI機能は[対象範囲の整理](../../../docs/SECURITY_SCOPE.md)に従い、ai-security-foundryへ委ねます。

例えば、外部PRの修正をagentへ任せる場面を考えます。投稿者の説明を読み、必要なら拡張を使い、ソースを編集してテストします。その間に、開発者の別の鍵を使ったり、検査を勝手に削除したり、終わらない試行を続けたりさせないために、次の判断を分けます。

| Control | 判断すること | シナリオから読む教材 |
|---|---|---|
| [PSB-AI-001 Repository agent guidance](psb-ai-001-repository-agent-guidance/README.md) | チームの指示を誰が変更でき、実際にどの版が読まれるか | [指示ファイルの変更](psb-ai-001-repository-agent-guidance/learning.md) |
| [PSB-AI-002 Agent extension dependency governance](psb-ai-002-agent-extension-dependency-governance/README.md) | 追加するSkill・MCP・pluginの内容と権限が、審査したものと同じか | [承認した拡張の更新](psb-ai-002-agent-extension-dependency-governance/learning.md) |
| [PSB-AI-003 Development content injection boundary](psb-ai-003-development-content-injection-boundary/README.md) | 外部PR・Issueやツール出力の文章を、依頼や実行許可にしていないか | [外部のIssueやPRを読ませる](psb-ai-003-development-content-injection-boundary/learning.md) |
| [PSB-AI-004 Development agent runtime boundary](psb-ai-004-development-agent-runtime-boundary/README.md) | 不要な認証情報や通信先へ届かず、承認した対象・操作だけを実行できるか | [どこまで操作を任せるか](psb-ai-004-development-agent-runtime-boundary/learning.md) |
| [PSB-AI-007 Development agent work budget](psb-ai-007-development-agent-work-budget/README.md) | 同じ作業の再試行も含め、時間・費用・呼び出し回数を制限できるか | [テスト修正が終わらない](psb-ai-007-development-agent-work-budget/learning.md) |

指示をレビューするAI-001と、外部資料を作業指示にすり替えさせないAI-003は、扱う文章の役割が違います。どちらも、文章だけで実行権限を制限できるとは考えません。実行側の制限はAI-004、許可した作業を続けられる量はAI-007で判断します。

## 設計を選ぶとき

個別方式は各Controlへ統合しました。工程の接続は[開発agentに作業を任せ、停止と結果確認まで行う](../../../engineering/development-agent-task-to-stop.md)から読みます。隔離方式と操作承認には独立した設計上の選択があるため、次の二つを残します。

- [実行環境の隔離](../../../engineering/development-runtime-isolation.md)：agentや子プロセスが、どのファイル・認証情報・通信先へ届くか。
- [操作の承認と実行](../../../engineering/development-action-authorization.md)：届く範囲の中でも、今回の依頼で何を変更・送信してよいか。

開発端末での鍵の保管・受け渡しは[SOURCE-007](../source-protection/psb-source-007-developer-local-credential-storage/README.md)、CIで外部PRのコードを動かす条件は[CICD-005](../cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)も確認します。Agentの制限だけで、端末やCI全体の保護を済ませたことにはなりません。

記載した条件が実際のagent製品や端末で強制されているかは、導入先で確かめる必要があります。旧AI項目の採否と保留理由は[移行判断](../../../docs/MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)にあります。

[利用者提供の多層隔離・権限ペアリング資料](../../../sources/README.md#ref-user-agent-isolation-pairing-001)は、原文と本PJでの採否を分けて保存しています。主な反映先は[AI-004の実行環境設計](../../../engineering/development-runtime-isolation.md#credential-operation-pairing)です。
