# PSB-AI-004 Development agent runtime boundary

**開発agentが、許可されていないファイル・認証情報・通信先・操作に到達できないか。**

## なぜ必要か

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

## フレームワークとの関係

現行マッピングの11件は、開発agentの実行時に**到達できる資産と操作を制限する**部分に限ります。

| 参照先 | このControlとの関係 | 主な限界 |
| --- | --- | --- |
| MITRE ATLAS 2026.05 AML.T0053 | Toolの種類・操作・引数を限定し、tool経由の権限悪用を狭める。 | 全tool経路と外部サービス権限は未確認。 |
| MITRE ATLAS 2026.05 AML.T0086 | 接続先と送る情報を実行側で確認し、tool経由の漏えいを狭める。 | 正規toolでの送信内容や全経路は未確認。 |
| MITRE ATLAS 2026.05 AML.T0098 | 認証情報へ届くファイルとtoolを絞り、認証情報の収集を狭める。 | 外部の文書庫・メールなどの保存先は未確認。 |
| OWASP Agentic Top 10 2026 ASI02 | 正規toolの操作と引数を限定し、重要操作を独立して承認する。 | Toolの連鎖や実際の拒否は未確認。 |
| OWASP Agentic Top 10 2026 ASI03 | Agentが継承する認証情報と権限を絞り、操作を依頼者へ結び付ける。 | 独立したagent identityや下流サービスの認可は対象外。 |
| OWASP Agentic Top 10 2026 ASI04 | 実行時に読み込む拡張・toolを現在の承認へ照合する。 | 採用前の審査はAI-002。Remote側の変化も未確認。 |
| OWASP Agentic Top 10 2026 ASI05 | 隔離と操作認可で、意図しないcode実行の影響を狭める。 | 意図して動かすbuild/testコードや隔離突破への保証はない。 |
| OWASP AISVS 1.0 C9.3.1 | Tool・pluginの権限と到達先を隔離する設計に関係する。 | 実際に最小権限で動くことは未確認。 |
| OWASP AISVS 1.0 C9.2.1 | 重要操作の人による承認を、実行する対象・引数へ結び付ける。 | 承認画面と実行前拒否の実動作は未確認。 |
| OWASP AISVS 1.0 C9.5.1 | Toolの操作と引数を独立した実行時方針へ照合する。 | 全toolの引数値を実際に拒否できるか未確認。 |
| OWASP AISVS 1.0 C10.1.2 | 未承認MCP serverを実行時に使わせない設計に関係する。 | Server一覧の照合と拒否は未確認。 |

対応する特性と資料の版は[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)にあります。すべて部分的な設計関係です。製品AIの実行環境、実際の拒否、規格への準拠を示しません。

## このコントロールの範囲

対象は開発者端末・IDE・CLI・開発用MCP・repository・CIで動くagentです。[製品自体のAI機能](../../../../docs/SECURITY_SCOPE.md)は扱いません。[AI-001](../psb-ai-001-repository-agent-guidance/README.md)はrepository指示の管理、[AI-002](../psb-ai-002-agent-extension-dependency-governance/README.md)は拡張の採用、[AI-003](../psb-ai-003-development-content-injection-boundary/README.md)は読んだ資料を依頼に昇格させない境界を扱います。AI-004は実行時の強制を受け持ちます。認証情報の発行・失効は[SOURCE-004](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)へ渡します。生成コードの正しさや、全端末の復旧完了までは保証しません。

隔離の選び方は[engineering: 実行環境](../../../../engineering/ai-development-security/development-runtime-isolation/README.md)、操作と承認の結び付けは[engineering: 操作認可](../../../../engineering/ai-development-security/development-action-authorization/README.md)を参照してください。Codex CLI固有の問いを含む[教材](learning.md)、10の特性と参照資料IDを残した[control.yaml](control.yaml)、資料の採否を示す[Sources](../../../../sources/README.md#ref-development-runtime-reconciliation-001)、旧項目の[移行記録](../../../../docs/MIGRATION_AI_DEVELOPMENT.md#ai-runtime-migration)へも辿れます。
