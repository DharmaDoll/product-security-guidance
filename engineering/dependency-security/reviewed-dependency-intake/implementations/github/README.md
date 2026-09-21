# GitHub実装例: Dependency change review

## 対象と変更箇所

GitHub.comの対象repositoryでDependency graphと対応manifest・lockを使う場合の例です。
Plan・ecosystem・推移依存の対応範囲は採用先で確認します。確認日は`2026-09-16`、
参照したActionは`a1d282b36b6f3519aa1f3fc636f609c47dddb294`です。
このActionのREADMEが示すruntimeはNode.js 24、最低Actions Runner版は`2.327.1`です。
GitHub-hosted runnerでの実行可否を採用時に確認します。

[`secure/dependency-review.yml`](secure/dependency-review.yml)をレビューし、採用先の
`.github/workflows/dependency-review.yml`へ既存設定との差分を反映します。
Active rulesetで対象branchへのmergeに`Dependency Review`の成功を要求します。
Workflowの配置だけではmerge拒否を有効にしたことになりません。

この例はPR内容をcheckout・buildせず、read-onlyのActionで差分を判定します。PR実行先はGitHub-hosted runnerです。
APIへの外部通信が発生し、Dependency graphの提供と対象manifestの対応が前提です。

## 方針と確認方法

旧実装の`high`以上、runtime・development・unknown scope、`warn-only: false`を保持しています。
LicenseとScorecardは判定に含めません。Snapshot warningのretryは最大120秒であり、不完全な結果の採用許可ではありません。
[固定Actionの仕様](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/README.md#configuration)

Sandbox repositoryで無害なlock更新を作り、base/headの直接・推移依存差分を実ファイルと照合します。
既知highを記録した更新は依存をinstall・実行せず、判定失敗とmerge拒否を確認します。
取消・検査欠落の状態でもmergeできないこと、head更新後に古い結果を使わないことを確認します。
Branch更新と運用設定のbypassも確認範囲に含めます。

確認できない対象・結果は`NOT_CHECKED`、API・runner・収集の失敗は`ERROR`であり、合格にはしません。
この試作版では実際のGitHub設定変更やPR作成を行っていません。ローカルの文字列検査を導入証拠にしません。

## 限界と参照資料

このworkflowはhash、origin、license、来歴、独立した人のレビュー、未知の悪意を自動判定しません。
通常buildで承認したlockとbytesを使うことも、別の実装で確認します。
[GitHub dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)

[REF-DEPS-002](../../../../../sources/README.md#ref-deps-002)には、参照資料一覧の追加提案と
今回の基本実装の範囲差を残しています。設計方式は[pattern](../../README.md)を参照してください。
