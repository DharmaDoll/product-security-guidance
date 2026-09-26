# Python 3.10: Unicode source check

これはPythonの`.py`ファイルを読み、レビューで見落としやすい文字を報告する小さな実装例です。対象コードは実行しません。双方向・不可視文字の限定リストをソース全体で検査し、識別子はASCIIだけを許すprofileで確認します。日本語などの通常の文字列・コメントは通します。

対象はPython 3.10.4で確認しました。標準ライブラリだけで動きます。`0`は対象ファイル全件を読んだ上で検出なし、`1`は検出、`2`は読めない・解析できない・対象ゼロ件などの評価不能です。どちらの非ゼロも受入を止めます。出力はpath、行・列、code point、分類に限定し、ソース行は出しません。

## 手元のrepositoryへ入れる

1. このPJのrootから、次のように[script](check_unicode_source.py)を対象repositoryへコピーする。`/path/to/target-repo`は実際のpathへ置き換える。

   ```sh
   mkdir -p /path/to/target-repo/.security
   cp engineering/secure-coding/unicode-source-review/implementations/python/check_unicode_source.py /path/to/target-repo/.security/check_unicode_source.py
   ```

2. 対象repositoryのrootで、レビュー対象のPython source pathを明示して実行する。例：`python3 .security/check_unicode_source.py src tests`。`src`や`tests`が存在しなければ、実際の対象pathへ置き換える。Script自体の変更もレビューする。
3. 受入条件にする場合は、protected CIでレビュー対象のrevisionに対して同じコマンドを走らせる。検査script、対象path、CI workflowを投稿者が同じ変更で弱められないように、受入側の承認・保護を設定する。ローカルhookは任意の早期feedbackにとどめる。

この例は対象path以下の`.py`を再帰的に読むため、生成物やvendor codeを含めるかは導入時に決めます。選んだpathの外は検査しません。Symlinkの`.py`とsymlink directoryは、対象漏れを避けるため評価不能にします。

## 安全なsmoke test

対象repositoryとは別の使い捨てdirectoryで試せます。悪用コードの実行はありません。

```sh
tmpdir=$(mktemp -d)
printf 'message = "日本語"\n' > "$tmpdir/example.py"
python3 .security/check_unicode_source.py "$tmpdir"
python3 -c 'from pathlib import Path; import sys; Path(sys.argv[1]).write_text("# " + chr(0x202E) + " hidden\n", encoding="utf-8")' "$tmpdir/example.py"
python3 .security/check_unicode_source.py "$tmpdir"
rm -r "$tmpdir"
```

最初は`PASS`・終了コード`0`、次は`U+202E bidi-control`・終了コード`1`です。さらに`python3 -m unittest discover -s .security -p 'test_check_unicode_source.py'`で同梱[test](test_check_unicode_source.py)を走らせられます。Testを使う場合はscriptと一緒にコピーしてください。

## 解除と限界

導入を解除する時は、CIの必須checkと呼出しを見直し、コピーしたscriptを削除します。独立した別の検査が必要な場合、先にその受入条件を接続します。

この実装の拒否リストとASCII識別子は一つのproject policyです。Unicodeの全不可視文字、confusable全般、review UIの表示、すべてのsource encoding、別言語の字句規則は扱いません。`tokenize.detect_encoding`でUTF-8以外の宣言を止め、UTF-8 bytesを読み、Python parserとtokenizerで識別子を確認します。BOMも拒否対象です。解析エラーを検出なしへ変換しません。検査自体の改変、CIの迂回、対象pathの選び違いは、導入先の受入経路で別に確かめます。

設計判断：[pattern](../../README.md) · 仕様：[Python字句規則](../../../../../sources/README.md#spec-python-source-lexical-3-10) · [移行記録](../../../../../docs/UNICODE_SOURCE_MIGRATION.md)
