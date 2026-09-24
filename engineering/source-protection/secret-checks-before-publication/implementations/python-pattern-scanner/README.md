# Python pattern scanner

Python標準ライブラリだけで動く、小さなsecret pattern scannerです。Gitのstaged内容、commit message、
pushで追加する履歴を検査し、見つけた値そのものを表示せずにGit操作を止めます。

旧`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の`scan-sensitive.py`を、
単独で読んで試せるimplementationとして再編集しました。

対象はPOSIX shellを使えるLinuxまたはmacOS上のローカルGit repositoryです。Git 2.47.2と
Python 3.10.4で確認しています。Pythonの外部packageは使いません。Windows Git Bashは未確認です。

## まず試す

安全なファイルは終了値`0`で通過します。

```sh
tmp_file=$(mktemp)
printf '%s\n' 'hello' >"$tmp_file"
python3 scan_sensitive.py --file "$tmp_file" --label example.txt
rm "$tmp_file"
```

無効な検出用文字列を作ると、終了値`1`で拒否します。値は出力されません。

```sh
tmp_file=$(mktemp)
python3 -c 'print("api_" + "key=" + "x" * 16)' >"$tmp_file"
python3 scan_sensitive.py --file "$tmp_file" --label example.txt
scan_status=$?
rm "$tmp_file"
test "$scan_status" -eq 1
```

## Gitでの動き

| Hook | 検査するもの |
|---|---|
| `pre-commit` | `git add`済みの追加・変更・renameファイル |
| `commit-msg` | コミットメッセージ |
| `pre-push` | Pushで追加するcommitのメッセージと、そのcommitで追加・変更・renameされたファイル |

通常の`git commit`では`pre-commit`と`commit-msg`、`git push`では`pre-push`がGitから起動されます。
検出時はGit操作を終了値`1`で止めます。Gitまたは入力を検査できない場合は終了値`2`で止めます。

## 手元のrepositoryへ導入する

次の例はscanner一式を対象repositoryの`.git`配下へcopyし、対象repositoryのローカル設定だけを変更します。
`source_dir`と`target`を自分の絶対pathへ置き換えてください。

```sh
source_dir="/absolute/path/to/product-security-guidance/engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner"
target="/absolute/path/to/target-repository"

git -C "$target" rev-parse --show-toplevel
git -C "$target" config --show-origin --get-all core.hooksPath || true
default_hooks=$(git -C "$target" rev-parse --git-path hooks)
find "$default_hooks" -maxdepth 1 -type f ! -name '*.sample' -print
```

`core.hooksPath`の確認または`find`で既存設定・hookが表示された場合は、ここで止めます。既存hookを上書きせず、
既存の処理からこのscannerを呼ぶか、hook managerへ組み込んでください。呼出し順と終了値も確認します。

何も表示されなかった場合は、次の手順で導入できます。

```sh
(
  set -eu
  git_dir=$(git -C "$target" rev-parse --absolute-git-dir)
  bundle="$git_dir/product-security-guidance/python-pattern-scanner"

  test ! -e "$bundle"
  mkdir -p "$bundle/hooks"
  cp "$source_dir/scan_sensitive.py" "$bundle/"
  cp "$source_dir/hooks/"* "$bundle/hooks/"
  chmod 755 "$bundle/scan_sensitive.py" "$bundle/hooks/"*
  git -C "$target" config --local core.hooksPath "$bundle/hooks"
  git -C "$target" config --show-origin --get core.hooksPath
)
```

最後のコマンドが対象repositoryの`.git/config`と、copy先の`hooks`を表示すれば設定されています。
copyした一式はcommit対象になりません。scannerを更新するときは、差分をレビューしてから同じ場所へcopyし直します。

### Git hookを簡単に試す

次のsmoke testは、導入したhookを使い捨てrepositoryから実際に起動します。安全なcommitが成功し、
未発行で無効なcanaryを含むcommitが拒否されれば`PASS`を表示します。対象repositoryのindexや履歴は変更しません。

```sh
(
  set -eu
  git_dir=$(git -C "$target" rev-parse --absolute-git-dir)
  bundle="$git_dir/product-security-guidance/python-pattern-scanner"
  test -x "$bundle/hooks/pre-commit"

  smoke_repo=$(mktemp -d)
  trap 'rm -rf "$smoke_repo"' EXIT HUP INT TERM

  git -C "$smoke_repo" init -q
  git -C "$smoke_repo" config user.name 'Secret scanner smoke test'
  git -C "$smoke_repo" config user.email 'scanner@example.invalid'
  git -C "$smoke_repo" config core.hooksPath "$bundle/hooks"

  printf '%s\n' 'safe content' >"$smoke_repo/example.txt"
  git -C "$smoke_repo" add example.txt
  git -C "$smoke_repo" commit -q -m 'safe smoke test'

  python3 -c 'print("api_" + "key=" + "x" * 16)' >"$smoke_repo/canary.txt"
  git -C "$smoke_repo" add canary.txt
  if git -C "$smoke_repo" commit -q -m 'blocked smoke test'; then
    printf '%s\n' 'FAIL: inert canary was committed' >&2
    exit 1
  fi
  printf '%s\n' 'PASS: safe commit accepted; inert canary rejected'
)
```

これはhookの接続と代表的な拒否を確かめるテストです。全ルールは、元のimplementation directoryで次を実行して確認できます。

```sh
python3 -m unittest discover -s "$source_dir" -p 'test_*.py' -v
```

### 解除する

導入時に既存の`core.hooksPath`がなかったことと、現在値がこのimplementationを指すことを確認してから解除します。

```sh
(
  set -eu
  git_dir=$(git -C "$target" rev-parse --absolute-git-dir)
  bundle="$git_dir/product-security-guidance/python-pattern-scanner"

  test "$(git -C "$target" config --local --get core.hooksPath)" = "$bundle/hooks"
  git -C "$target" config --local --unset core.hooksPath
  rm -rf "$bundle"
)
```

既存hookへ手作業で統合した場合は、統合時の差分を戻します。このimplementationをcopyしただけでは、
本PJ自身や他のrepositoryでhookは有効になりません。

## 検出するもの

代表的なprivate key header、GitHub token、AWS access key、AWS secret key、Google API key、JWT、
Bearer token、Slack webhook、npm registry credential、PyPI token、一般的なcredential代入を正規表現で検査します。

`.env`、private key、keystore、archive、binary、database等の代表的な名前・拡張子も拒否します。
`.env.example`、`.env.sample`、`.env.template`は名前では拒否しませんが、内容は検査します。
1ファイルが5 MiBを超える場合とNULを含む場合は、検査できたことにせず拒否します。

終了値は、`0`が検出なし、`1`がfinding、`2`がGitや入力のエラーです。

## Gitleaks版との使い分け

このscannerは、正規表現とGit hookのつながりを読みやすく示し、組織固有の軽いルールを試すための例です。
[Git hooks and Gitleaks](../git-gitleaks/README.md)は、固定したGitleaks、Git objectの全到達範囲、
受信側`pre-receive`、未対応形式や検査器異常の厳しい拒否を扱います。

Python版はローカルhookだけなので`--no-verify`で省略できます。受信側の独立した拒否、Web UI・API・bot等の
書込経路、未知・符号化・分割されたsecret、全履歴の完全な走査を保証しません。Gitleaksと同等の検出範囲も主張しません。
ファイル名とcommit位置は出力するため、それ自体を機微情報にしない運用も必要です。

## 実装テストの範囲

テストは12種類の代表的な無効canary、近似した安全入力、値の非表示、staged内容と作業ツリーの違い、
最新treeから削除されたpush履歴、Gitによるhookの起動とcommit拒否を確認します。本物の認証情報や
外部repositoryは使いません。

- [設計pattern](../../README.md)
- [Control](../../../../../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)
- [移行記録](../../../../../docs/GIT_HOOKS_MIGRATION.md)
