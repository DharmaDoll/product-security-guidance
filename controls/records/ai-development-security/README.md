# AI Development Security

開発者端末・IDE・CLI・repository・CIでAIを使う開発環境について、追加する指示やツール、渡す認証情報、実行時の権限を確認します。
製品自体のAI securityは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)の担当です。[対象範囲](../../../docs/SECURITY_SCOPE.md)で判断します。

| Control | 判断すること |
|---|---|
| [PSB-AI-004 Development agent runtime boundary](psb-ai-004-development-agent-runtime-boundary/README.md) | 実効権限を外側の管理方針と現在の操作許可に収める |
| [PSB-AI-002 Agent extension dependency governance](psb-ai-002-agent-extension-dependency-governance/README.md) | どの拡張の、どの内容と権限を、いつまで利用してよいか |

AI-004のcontrol記録と[操作認可](../../../engineering/ai-development-security/development-action-authorization/README.md)・[実行環境の隔離](../../../engineering/ai-development-security/development-runtime-isolation/README.md)をガイダンス移行しました。製品別実装、prompt injection対策、開発用benchmark基盤は未移行です。記録の存在から実装・導入を推定しません。
