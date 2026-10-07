# PSB-AI-004 Development agent runtime boundary

**開発agentが、許可されていないファイル・認証情報・通信先・操作に到達できないか。**

例えば、agentが未信頼のテストスクリプトを実行するとき、そのスクリプトに公開用tokenが渡れば、作業フォルダの書込みを制限していても外部への公開を止められません。Agentの提案や指示文とは別に、実行する側で権限と操作を制限します。

## 満たすべきこと

1. **到達できる範囲を狭める。** 管理方針はagentの外側で決め、作業ファイル、保護設定、認証情報、通信先を分ける。必要な隔離が使えない場合や迂回できる場合は、その実行を許可しない（DEV-RUNTIME-1〜3）。
2. **使う拡張と操作を確かめる。** 実際に読み込む拡張・tool・権限を現在の承認へ照合する。操作の名前だけでなく、対象と引数が起こす変更を判断する。重要操作は人が内容を確認して承認し、実行前に同じ依頼・対象・引数・期限か確かめる（DEV-RUNTIME-4〜6）。
3. **結果不明を安全扱いしない。** 承認の使い回し、確認用hookの漏れや故障を許可へ変えない。送信済みの外部操作は、結果が不明なまま自動再送しない。判断・実行結果・監査の欠落を区別し、古い正常結果で現在の状態を上書きしない（DEV-RUNTIME-7〜10）。

## 診断で確認する項目（異常時テスト）

- Agentや子プロセスが、作業に不要な認証情報、保護設定、管理用socket、通信先へ到達できないか。
- 承認した拡張が失効・変更されても、古い承認で次の呼び出しを続けられないか。拡張一覧の取得失敗を「拡張なし」と誤認していないか。
- 「読取り専用」と名乗るtoolが書込みや送信を行う場合、実際の効果に基づいて拒否できるか。
- 承認後に対象や引数を変える、承認を同時に使う、hookを通らず直接実行する経路がないか。
- 実行前の判定不能を拒否し、実行後の通信障害を結果不明として扱えるか。監査が届かない端末を「問題なし」にしていないか。

これらは確認項目であり、実際のagent製品で拒否を確認した結果ではありません。

## このコントロールの範囲

対象は開発者端末・IDE・CLI・開発用MCP・repository・CIで動くagentです。[製品自体のAI機能](../../../../docs/SECURITY_SCOPE.md)は扱いません。[AI-001](../psb-ai-001-repository-agent-guidance/README.md)はrepository指示の管理、[AI-002](../psb-ai-002-agent-extension-dependency-governance/README.md)は拡張の採用、[AI-003](../psb-ai-003-development-content-injection-boundary/README.md)は読んだ資料を依頼に昇格させない境界を扱います。AI-004は実行時の強制を受け持ちます。認証情報の発行・失効は[SOURCE-004](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)へ渡します。生成コードの正しさや、全端末の復旧完了までは保証しません。

隔離の選び方は[engineering: 実行環境](../../../../engineering/ai-development-security/development-runtime-isolation/README.md)、操作と承認の結び付けは[engineering: 操作認可](../../../../engineering/ai-development-security/development-action-authorization/README.md)を参照してください。Codex CLI固有の問いを含む[教材](learning.md)、10の特性と参照資料IDを残した[control.yaml](control.yaml)、資料の採否を示す[Sources](../../../../sources/README.md#ref-development-runtime-reconciliation-001)、旧項目の[移行記録](../../../../docs/MIGRATION_AI_DEVELOPMENT.md#ai-runtime-migration)へも辿れます。
