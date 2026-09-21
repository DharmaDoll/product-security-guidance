# pip実装例: Wheel-only dependency intake

## 対象と前提

承認済みindexから名前とexact versionで依存を取得し、source buildを必要としないPython環境向けです。
確認した公式文書はpip `26.2.1`表示版、確認日は`2026-09-16`です。
ローカルの挙動検査で使用した版はテスト出力に記録します。導入先はサポートされるPython・pipを
固定して再確認してください。この試作版はpip自体のインストールを行いません。

入力は直接・推移依存すべてのexact versionとレビュー済みSHA-256を含むrequirementsです。
この取得経路にlocal project、editable、VCS、直接指定のsource archiveを混ぜません。
requirements内の追加option・includeによるpolicyの上書きもレビュー対象です。

## 変更するもの

[`secure/requirements-policy.txt`](secure/requirements-policy.txt)の二つのoptionを、採用先の
保護されたrequirementsと実際のCI installコマンドへ反映します。既存の入力をレビューしてから使います。

```bash
python -m pip install --only-binary=:all: --require-hashes --no-cache-dir -r requirements.lock
```

このコマンドは採用先で実行する例です。`requirements.lock`はこの試作版に付属せず、採用先のgraphと
対象platformに合うwheel hashを持たせます。外部indexへの通信が発生します。
取得先の許可と実効設定、別installコマンドによる回避も別途確認します。

`--only-binary=:all:`は候補のsource distributionを除外し、`--require-hashes`は取得内容を入力のhashへ
結び付けます。両者は別の性質です。`--prefer-binary`はsource buildの拒否の代わりになりません。
[pip install reference](https://pip.pypa.io/en/stable/cli/pip_install/)

## ローカルで確認する

このディレクトリで次を実行します。

```bash
python3 -m unittest discover -s tests -v
```

無害なwheelとsource distributionを一時領域で作り、ネットワークなしでpipの実際の候補選択と
metadata準備を確認します。成功するwheel、拒否されるsdist、hash不一致を検査し、
比較用の制限なし実行では無害なbackendがmarkerを残して停止することを確認します。
比較用packageはテスト中だけ生成し、workflowや通常のinstallへ配置しません。

テストはpip `--dry-run`の取得・準備段階を対象にします。採用先での通常install、全入力の制限、
CI配線、host隔離を証明しません。pip不在・失敗・予期しない結果はテスト失敗です。

## 導入先で確認する

保護されたCIで実際に使うPython・pipの版、入力、command、設定の優先順位を確認します。
対応wheelを持つ依存が通常installできること、wheelがない候補が拒否され、source buildへ戻らないことを
無害な対象で確認します。未取得・未確認は`NOT_CHECKED`、収集・実行失敗は`ERROR`として残します。

## 限界

Wheel内のコードは後続のimport・testで実行できます。hashが一致しても内容の安全性を示しません。
Pythonのbuild isolationはbuild用依存を分ける仕組みで、OS権限のsandboxではありません。
source buildが必要なら、この経路の拒否を解除するのではなく、別の隔離buildとして設計します。
[Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/)

仕様の採否と他製品の候補は[参照資料記録](../../../../../sources/README.md#spec-install-execution-policy)、
方式は[pattern](../../README.md)を参照してください。
