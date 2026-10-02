# GitHub実装例: Dependency change review

PRで変わる依存をGitHubのデータから比較し、既知のhigh・criticalな脆弱性を含む変更を失敗にする例です。
通常のPR作成・更新でActionが動きます。PRのコードをcheckout・installせずに判定し、その結果をmerge条件へ接続します。

## 対象と変更箇所

GitHub.comの対象repositoryでDependency graphと対応manifest・lockを使う場合の例です。
Plan・ecosystem・推移依存の対応範囲は採用先で確認します。確認日は`2026-09-16`、
参照したActionは`a1d282b36b6f3519aa1f3fc636f609c47dddb294`です。
このActionのREADMEが示すruntimeはNode.js 24、最低Actions Runner版は`2.327.1`です。
GitHub-hosted runnerでの実行可否を採用時に確認します。

[`secure/dependency-review.yml`](secure/dependency-review.yml)をレビューし、採用先の
`.github/workflows/dependency-review.yml`へ既存設定との差分を反映します。

この例はPR内容をcheckout・buildせず、read-onlyのActionで差分を判定します。PR実行先はGitHub-hosted runnerです。
APIへの外部通信が発生し、Dependency graphの提供と対象manifestの対応が前提です。

## 手元のリポジトリから導入する

次は既存workflowがない場合の配置例です。`source_dir`と`target`を絶対pathへ置き換えてください。
同じ名前の既存workflowがあれば、上書きせず差分を統合します。

```bash
source_dir="/absolute/path/to/product-security-guidance/engineering/dependency-security/reviewed-dependency-intake/implementations/github"
target="/absolute/path/to/target-repository"

(
  set -eu
  git -C "$target" rev-parse --show-toplevel
  test ! -e "$target/.github/workflows/dependency-review.yml"
  mkdir -p "$target/.github/workflows"
  cp "$source_dir/secure/dependency-review.yml" "$target/.github/workflows/dependency-review.yml"
)
```

途中で失敗すればcopyを止めます。差分をレビューしてGitHubへ反映した後、下のsmoke testで実行と対象差分を確認します。
対象branchの有効な保護ルールへ、job名`Dependency Review`を必須検査として登録します。取得範囲と未評価の扱いも確認してから採用します。
Workflowの配置だけではmerge拒否は有効になりません。Head・base更新時の再評価、検査の出所、workflow・判定方針の変更レビューとbypassも設定・確認対象です。

## 方針とデータ不足の扱い

旧実装の`high`以上、runtime・development・unknown scope、`warn-only: false`を保持しています。
LicenseとScorecardは判定に含めません。Snapshotはdependency submissionで提供する依存関係の記録です。
固定Actionの[`getComparison`](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/src/main.ts#L33-L62)は、snapshotの警告が残る場合に再試行しますが、期限後は取得できた比較結果で判定を続けます。
この例の120秒は待機期限であり、期限後の未評価を自動的に失敗へ変える設定ではありません。
[固定Actionの仕様](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/README.md#configuration)

GitHubの必須検査は`skipped`・`neutral`を受け入れる場合もあります。成功表示だけで必要な評価が終わったとは判断しません。
対象manifestのデータが揃うことを確認し、警告や対象外が残る採用先では、独立した必須レビューや対応する検査で未評価を止めます。
その判断まで接続できない場合、このworkflowだけを[DEPS-004](../../../../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)全体を満たすmerge gateとして採用しません。
[GitHubの必須検査の仕様](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)

## 使い捨てリポジトリでのsmoke test

無害なlock更新のPRを作り、base/headの直接・推移依存差分を実ファイルと照合します。
拒否対象のない変更でjobが成功することも確認します。
既知highを記録した更新は依存をinstall・実行せず、判定失敗とmerge拒否を確認します。
取消・検査欠落・job省略の状態でも必要な評価なしでmergeできないこと、head更新後に古い結果を使わないことを確認します。
データ準備の警告が待機期限後に残る場合と、対応外の入力で差分が取得されない場合も、別の必須判断で止まるか確認します。
Branch更新と運用設定のbypassも確認範囲に含めます。

確認できない対象・結果は`NOT_CHECKED`、API・runner・収集の失敗は`ERROR`であり、合格にはしません。
この試作版では実際のGitHub設定変更やPR作成を行っていません。ローカルの文字列検査を導入証拠にしません。

2026-09-27は上の配置手順をローカルの使い捨てGitで試し、copyの一致と、既存workflow・repository不在時に止まることを確認しました。
固定Actionのsource・配布コードも読みましたが、上の実GitHubでのsmoke testを実施した結果ではありません。

## 解除する

置き換える必須判定がある場合は、先に対象branchへ接続します。
この例の必須検査設定を見直してから、追加したworkflowを削除、または既存workflowへ統合した差分を戻します。
単にworkflowを消すと、必須検査が欠落してmergeできない状態になり得ます。

## 限界と参照資料

このworkflowはhash、origin、license、来歴、独立した人のレビュー、未知の悪意を自動判定しません。
通常buildで承認したlockとbytesを使うことも、別の実装で確認します。
[GitHub dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)

[REF-DEPS-002](../../../../../sources/README.md#ref-deps-002)には、参照資料一覧の追加提案と
今回の基本実装の範囲差を残しています。設計方式は[pattern](../../README.md)を参照してください。
[DEPS-004の教材](../../../../../controls/records/dependency-security/psb-deps-004-dependency-change-review/learning.md)から、表示・判定・merge拒否を分ける理由を読めます。
