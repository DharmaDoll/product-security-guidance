# PSB-SOURCE-005 Repository recovery independence

**リポジトリを失っても、別に守ったデータから必要な開発を再開できるか。**

## なぜ必要か

例えば、盗まれた管理者セッションでリポジトリを削除されたとき、同じ権限でバックアップも消せるならコピーは復旧手段になりません。Gitの履歴だけ戻しても、製品に必要なLFSファイルや設定がなければ開発を再開できません。

## 満たすべきこと

1. **戻すものを決める。** 製品の責任者が、必要なリポジトリ・履歴・関連データ・設定、担当者、許容できるデータ損失と復旧時間を決める（RECOVERY-1）。
2. **破壊から復旧手段を分ける。** ソースの削除や履歴書換えを制限し、ソース管理者やバックアップ取得担当の権限だけでは、保管した過去の世代を消せないようにする。復旧用IDと鍵も使える状態に保つ（RECOVERY-2〜4）。取得の失敗や古い世代を現在の成功と扱わない。
3. **実際に戻して確かめる。** 不正変更の経緯から使う世代を選び、隔離した場所へ復元する。履歴・必要なデータ・アクセス制限を確認し、修正やビルドを再開できるか確かめる（RECOVERY-5〜6）。Gitの整合性が通っても、侵害後の内容なら復旧成功にしない。

## 診断で確認する項目（異常時テスト）

- ソースを削除・移管・書換えできる人が、過去の保管世代や保持期間まで変更できないか。復旧用IDや鍵が使えないコピーを復旧可能と扱っていないか。
- 取得失敗、対象の追加・移管、許容期間を超えた古い世代を、復旧可能な最新のコピーとして扱っていないか。
- 必要なタグ・LFS実体・設定が欠けても、Gitの検査やファイル数だけで成功としていないか。
- 不正変更後に取得した世代を、ハッシュが合うという理由で採用していないか。正しい時点を選べなければ判断を保留できるか。
- 元のソース管理サービスが使えない状態で取り出し、隔離先から修正やビルドを再開できるか。

これらは確認項目であり、実際の保管先や製品の開発再開を試した結果ではありません。

## フレームワークとの関係

独立した復旧用コピーと開発再開について、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に個別の関係は登録していません。復旧の資料は参照していますが、このControlだけで特定規格の復旧要件全体を満たすとは扱いません。資料の役割と限界は[Sources](../../../../sources/README.md)からたどれます。

## このコントロールの範囲

対象は、製品の修正・再構築・調査に必要なリポジトリと関連データです。GitのコピーだけでIssues、Packages、権限、Secrets、製品の稼働データまで戻るとは扱いません。認証情報の失効は[SOURCE-004](../psb-source-004-source-access-credential-lifecycle/README.md)、配布済み成果物の置換は[GOV-005](../../governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)の判断です。

保管先の権限、世代の選び方、復元の確認は[engineering](../../../../engineering/source-protection/independent-repository-backup-and-restore/README.md)を参照してください。[Git mirror例](../../../../engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror/README.md)はローカルの履歴復元に限ります。[教材](learning.md)、６つの特性と参照資料IDを残した[control.yaml](control.yaml)、資料の採否を示す[Sources](../../../../sources/README.md#ref-repository-recovery-001)、旧項目の[移行記録](../../../../docs/MIGRATION_SOURCE_PROTECTION.md#repository-recovery-migration)へも辿れます。
