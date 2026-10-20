# Git hooks and Gitleaks

Gitleaks adapter、固定設定、Git hook、導入・検証・cleanup処理とテストの正本は、
[agent-control-plane の secret-checks Skill](https://github.com/DharmaDoll/agent-control-plane/tree/main/skills/secret-checks)へ移しました。
Gitleaks本体は外部製品の公式配布物を使い、このリポジトリにはbinaryも実装の複製も置きません。

- [固定版Gitleaksの取得・照合と選択条件](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/references/gitleaks.md)
- [導入・診断・更新・切り戻し・解除・cleanup](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/references/installation.md)
- [実行テストと未確認範囲](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/evals/validation.md)

送信対象から到達する履歴を検査するため、対応形式と規模の上限があります。
ローカルhookの有効化と、GitHub側のpush protectionは別の確認です。
[設計上の選択条件](../../README.md)は引き続き本リポジトリで扱います。

<a id="参考自前のgit受信先"></a>

## 参考：自前のGit受信先

移管したadapterには隔離テスト用の`pre-receive`モードが残っています。
[移管先の説明](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/references/gitleaks.md#receiving-side-reference)を参照してください。
自前の受信先を設計する際の参考であり、GitHub.comへ配置する手順ではありません。

移管元は本リポジトリのcommit `2b5e81df0eee973d4cc4fc493fe09d93d207ea0b`です。
過去の実装・検証記録はGit履歴から確認できます。移管先の公開は両リポジトリの変更を確認して行ってください。
