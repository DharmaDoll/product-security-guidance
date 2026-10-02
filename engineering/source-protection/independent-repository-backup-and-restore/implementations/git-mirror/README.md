# Git mirrorで履歴を保管し、別の場所へ戻す

Gitのブランチ・タグとその履歴をコピーし、元のリポジトリを使わず、新しい場所へ復元する例です。取得時のref一覧と照合するので、必要なタグが欠けた復元や、名前は同じでも指すobjectが違う復元を成功にしません。

Gitの標準コマンドを使います。手元のrepositoryへ設定を追加する必要はありません。[設計パターン](../../README.md)のうち、Gitの取得・照合・復元だけを具体化します。

## 対象と準備

- 確認環境：Linux、Git 2.47.2、Bash 5.2.37、Python 3.10.4（smoke testだけに使用）。Gitコマンドの参照版は2.47.0で、この版のmirror・local cloneの説明を採用しています。
- コピー元：読取り権限のある、必要な全履歴とrefを持つrepository。手元の完全なrepository、またはHTTPSのGit URLを指定します。作業用cloneの未commitファイルは対象外です。
- コピー先・復元先：新しいディレクトリ。手元で試す場合もソースと別の場所を選びます。
- 取得時の一覧を比較できるよう、試す間はブランチ・タグの変更を止めます。認証情報をURLやこの例のログへ埋め込まないでください。

確認した版は実装の再現条件であり、Gitの運用版を固定する推奨ではありません。[直接の資料と限界](../../../../../sources/README.md#ref-repository-recovery-001)を参照してください。

## 任意のリポジトリで試す最短手順

以下はBashで実行します。`source_location`と`backup_parent`を手元の場所へ置き換えます。全体を同じshellで実行し、エラーが出た世代は成功扱いにしません。

### 1. 新しい保管場所を用意する

```bash
set -euo pipefail
umask 077
source_location='/absolute/path/to/your-repository'
# HTTPSの場合：https://github.com/EXAMPLE/REPOSITORY.git
backup_parent='/absolute/path/to/backup-area'
mkdir -p "$backup_parent"
generation=$(mktemp -d "$backup_parent/git-generation.XXXXXX")
```

ここでは手元の別ディレクトリへコピーします。運用では独立した保管先に世代全体を保管し、保持と読取り権限を確認します。ディレクトリを分けただけでは、同じ利用者による削除を防げません。

### 2. ref一覧を採り、mirrorを作る

```bash
git ls-remote --refs -- "$source_location" 'refs/heads/*' 'refs/tags/*' \
  | LC_ALL=C sort > "$generation/expected.refs"
test -s "$generation/expected.refs"
git clone --mirror --origin origin --no-local --no-hardlinks --reject-shallow --template= \
  -- "$source_location" "$generation/repository.git"
git -C "$generation/repository.git" fsck --full
git -C "$generation/repository.git" for-each-ref \
  --format='%(objectname)%09%(refname)' refs/heads refs/tags \
  | LC_ALL=C sort > "$generation/copied.refs"
diff -u "$generation/expected.refs" "$generation/copied.refs"
```

`--mirror`でrefを写し、`--no-local`でローカル元にもGitの転送経路を使います。`--no-hardlinks`も明示し、元のobjectファイルと共有するコピーを避けます。`--shared`や`--reference`は使いません。`--reject-shallow`で浅い履歴を拒否し、`--template=`でtemplateからhookを追加しません。

必要なrefが取得前から消えていれば、この一覧だけでは気づけません。製品の復旧対象として決めたブランチ・タグも確認します。例えば`main`が必要な場合は次を実行します。保守ブランチとリリースタグも必要対象に合わせて同様に確認します。

```bash
git -C "$generation/repository.git" show-ref --verify refs/heads/main
```

### 3. コピー元との接続を外して保管する

```bash
git -C "$generation/repository.git" config --remove-section remote.origin
```

接続設定を外し、後の`remote update`で保管世代を更新する経路をなくします。これは権限上の保持lockではありません。`expected.refs`を含む世代全体を保持対象にし、取得元の固定ID、取得日時、製品の必要対象との照合結果も運用記録へ残します。バックアップ自身から作り直した一覧を復旧の期待値にしません。

### 4. 新しい隔離先へ戻して照合する

```bash
restore_parent='/absolute/path/to/disposable-restore-area'
mkdir -p "$restore_parent"
restore_area=$(mktemp -d "$restore_parent/git-restore.XXXXXX")
restore_target="$restore_area/repository.git"
git clone --mirror --origin origin --no-local --no-hardlinks --reject-shallow --template= \
  -- "$generation/repository.git" "$restore_target"
git -C "$restore_target" config --remove-section remote.origin
git -C "$restore_target" fsck --full
git -C "$restore_target" for-each-ref \
  --format='%(objectname)%09%(refname)' refs/heads refs/tags \
  | LC_ALL=C sort > "$restore_area/restored.refs"
diff -u "$generation/expected.refs" "$restore_area/restored.refs"
```

`fsck`と`diff`がともに終了コード0なら、記録したブランチ・タグとGit objectを照合できました。Mirrorは作業ファイルをcheckoutしないbare repositoryです。Workflow、build、checkout filter、submoduleの追加取得はこの手順では起動しません。既存の本番repositoryへpushする手順も含みません。

`expected.refs`はコピー元から取得した一覧です。攻撃者が取得前に内容を書き換えていれば、その内容と一覧が一致しても検出できません。採用する世代は、変更の経緯、承認済みの変更記録、別に保管した期待値と照合して選びます。判断できない場合は復旧成功とせず、疑わしい世代を調査用に残します。

ここから必要な外部データ・設定を戻し、隔離した実行環境で修正やbuildを確認する判断は[pattern](../../README.md#復旧の判断を三段階に分ける)へ戻ります。

## 簡単なテスト方法

本PJのrootで実行できます。

```bash
make test-repository-recovery
```

またはこのフォルダを手元へコピーし、GitとPythonだけで実行します。

```bash
python3 -m unittest discover -s /absolute/path/to/git-mirror -p 'test_*.py' -v
```

テストは使い捨てrepositoryを作り、実際のGitコマンドで次の七経路を観測します。Network接続や本番repositoryの変更は行いません。

| 経路 | 観測する結果 |
|---|---|
| 元repositoryが元の場所からなくなる | 保管したobjectだけでmain・保守ブランチ・annotated tagを復元し、過去版の内容を読める |
| 復元先のタグが欠ける | `fsck`成功でもref照合が不一致になる |
| タグ名は同じでobjectが変わる | ref数が同じでも照合が不一致になる |
| 保管objectが破損する | Gitの整合性確認が失敗する |
| 復元先に既存repositoryがある | Cloneが失敗し、既存ファイルを保持する |
| コピー元がshallow repository | Cloneが失敗する |
| ref一覧の取得後にタグが増える | 取得時点の差を照合で検出する |

## 解除と制限

元repositoryには設定を加えません。練習後は表示した`generation`と`restore_area`の場所を確認し、その練習用ディレクトリだけを削除できます。運用の保管世代は保持方針に従い、練習用コピーと同じ手順で廃棄しません。

この例はGitのブランチ・タグの照合に限定します。Notes等の他refをmirrorが写しても、テストの確認対象は増えません。LFS実体、submoduleの別repository、reflog、未commit変更、GitHubの設定・Issues・PR・Packages・Secrets等は確認しません。Partial cloneや外部object storeへの依存がある環境も未検証です。

この例は世代の真正性、取得前の不正変更、cloudの保持・鍵・account分離、RPO・RTO、通知、製品の開発再開を証明しません。実データに対する削除拒否や復旧確認は[controlの診断観点](../../../../../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md#診断で確認する項目異常時テスト)へ戻して評価します。
