# Python pattern scanner

スキャナー、Git hook、導入・検証・cleanup処理とテストの正本は、
[agent-control-plane の secret-checks Skill](https://github.com/DharmaDoll/agent-control-plane/tree/main/skills/secret-checks)へ移しました。
このディレクトリには実装の複製を残しません。

- [導入・診断・更新・切り戻し・解除・cleanup](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/references/installation.md)
- [Python版の検査範囲と制限](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/references/limitations.md)
- [実行テストと未確認範囲](https://github.com/DharmaDoll/agent-control-plane/blob/main/skills/secret-checks/evals/validation.md)

移管後の自動導入はLinux／WSL2、Git、Python 3.10以上を対象にし、既存hookや共有worktreeは先に診断します。
ローカルhookは省略でき、Gitleaks相当の検出やGitHub側の拒否を保証しません。
[設計上の選択条件](../../README.md)は引き続き本リポジトリで扱います。

移管元は本リポジトリのcommit `2b5e81df0eee973d4cc4fc493fe09d93d207ea0b`です。
過去の実装・検証記録はGit履歴から確認できます。移管先の公開は両リポジトリの変更を確認して行ってください。
