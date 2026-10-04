# AI Development Security

開発者端末・IDE・CLI・repository・CIでAIを使う開発環境について、追加する指示やツール、渡す認証情報、実行時の権限を確認します。
製品自体のAI securityは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)の担当です。[対象範囲](../../../docs/SECURITY_SCOPE.md)で判断します。

| Control | 判断すること |
|---|---|
| [PSB-AI-001 Repository agent guidance](psb-ai-001-repository-agent-guidance/README.md) | 開発agentが読む指示の変更と、その効果を確認する |
| [PSB-AI-003 Development content injection boundary](psb-ai-003-development-content-injection-boundary/README.md) | 読んだ文書・Issue・tool出力を依頼や実行許可へ昇格させない |
| [PSB-AI-004 Development agent runtime boundary](psb-ai-004-development-agent-runtime-boundary/README.md) | 実効権限を外側の管理方針と現在の操作許可に収める |
| [PSB-AI-002 Agent extension dependency governance](psb-ai-002-agent-extension-dependency-governance/README.md) | どの拡張の、どの内容と権限を、いつまで利用してよいか |
| [PSB-AI-007 Development agent work budget](psb-ai-007-development-agent-work-budget/README.md) | 各操作が許可されても、作業全体の消費量が増え続ける前に止める |

AI-001の[repository指示のレビュー](../../../engineering/ai-development-security/repository-agent-guidance-review/README.md)、AI-003の[資料と指示の境界](../../../engineering/ai-development-security/untrusted-development-content-boundary/README.md)、AI-004の[操作認可](../../../engineering/ai-development-security/development-action-authorization/README.md)・[実行環境の隔離](../../../engineering/ai-development-security/development-runtime-isolation/README.md)を整理しました。実agentの比較、実行時の認可・隔離の製品別実装は未実施です。記録の存在から実装・導入を推定しません。

旧AI-005〜009の[選別結果](../../../docs/MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)では、操作の認可と結果をAI-004へつなぎました。AI-007は[作業予算の設計](../../../engineering/ai-development-security/development-work-budget-gate/README.md)と[Linux実行期限の例](../../../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)へ具体化しました。費用・呼び出しの実行前予約は未実装です。持続的context、agent間委譲、長時間agentの停止・復旧は採用する開発環境が決まるまで保留します。
