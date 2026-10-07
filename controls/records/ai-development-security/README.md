# AI Development Security

開発者端末・IDE・CLI・repository・CIで使うagentについて、**何を読ませ、何を追加し、何を実行させるか**を確認します。製品自体のAI機能は[対象範囲の整理](../../../docs/SECURITY_SCOPE.md)に従い、ai-security-foundryへ委ねます。

| Control | 判断すること |
|---|---|
| [PSB-AI-001 Repository agent guidance](psb-ai-001-repository-agent-guidance/README.md) | Agentが読むrepository指示を管理し、その効果を確かめる |
| [PSB-AI-002 Agent extension dependency governance](psb-ai-002-agent-extension-dependency-governance/README.md) | 審査した拡張の内容と権限が、実際に使うものと一致するか |
| [PSB-AI-003 Development content injection boundary](psb-ai-003-development-content-injection-boundary/README.md) | 文書・Issue・tool出力に混じる指示を、依頼や実行許可にしない |
| [PSB-AI-004 Development agent runtime boundary](psb-ai-004-development-agent-runtime-boundary/README.md) | Agentが未許可のファイル・認証情報・通信先・操作に到達できないか |
| [PSB-AI-007 Development agent work budget](psb-ai-007-development-agent-work-budget/README.md) | 一作業の時間・費用・呼び出し回数を上限で止められるか |

方式は各controlからengineeringへ進めます。記載した条件が実際のagent製品や端末で強制されているかは、導入先で確かめる必要があります。旧AI項目の採否と保留理由は[移行判断](../../../docs/MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)にあります。
