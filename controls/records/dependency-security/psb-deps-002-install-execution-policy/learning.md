# Install execution policy — 学習ノート

## シナリオ：testが始まる前に権限を使われる

開発者が画像処理ライブラリを更新します。公開から十分な時間が経ち、レビューしたlockfileのhashとも一致しています。
CIがinstallを開始すると、推移依存の準備用スクリプトが実行されます。そのCIにpackage公開用tokenがあれば、
スクリプトはtestの開始前にその権限を使える可能性があります。

攻撃者に必要なのは、その依存内容への影響力、install時の実行経路、実行環境から使える資産の接続です。
外部コードを起動しない取得経路では、このinstall時の攻撃は成立しません。起動しても公開用権限がなければ、
そのtokenを使う経路は成立しません。ただし、書き込めるworkspaceや内部サービス等の影響は別途残ります。

## 取得、準備、利用を分ける

Lifecycle scriptは、package managerがinstall等のイベントに合わせて起動するパッケージ側の処理です。
Native buildは、対象環境用のコードをコンパイルする準備処理です。Pythonのbuild backendは、
source distributionからmetadataやwheelを生成するコードです。metadataを読むつもりでもbackendが動く場合があります。

```text
パッケージを選ぶ → bytesを取得・照合 → 準備用コードを実行 → import・test → build・release
                                        ↑ この主題の実行許可
```

取得する許可は、公開者のコードを実行する許可と同じではありません。hashはレビューしたbytesとの一致を示し、
実行の必要性や内容の善良さは示しません。

## よくある誤解

| 直感 | 確認すべきこと |
|---|---|
| 「test jobにはsecretがないから安全」 | checkoutの認証情報、hostの権限、内部到達性、後続jobへ渡すstateも確認する |
| 「Pythonのbuild isolationなら隔離されている」 | ビルド用依存を分ける環境であり、OS・network・認証情報のsandboxではない |
| 「wheelなら安全」 | source build経路は減るが、wheel内のコードは後でimport・testされる |
| 「一度trustしたpackageなら更新してよい」 | 承認がどのversion・digestまで有効か確認する |
| 「失敗したので全許可を有効にする」 | 必要な処理を特定し、対象の許可と実行権限を限定する |

## レビューで問うこと

新しい依存を追加するとき、どの処理がいつ外部コードを起動するかを説明してください。
実行不要なら停止できるか。必要なら、どのversionを誰が承認し、実行環境から何へアクセスできるか。
更新や別コマンドで許可が広がらないか。拒否後のfallbackが同じコードを起動しないか。

この教材は[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)を使い、
取得側の判断をプラットフォーム権限・例外管理へ接続しています。
[攻撃段階4→7](../../../../docs/ANALYSIS_LENSES.md)に焦点を当て、後続の実行・成果物・本番監視を別の責任として残します。

方式を選ぶには[設計パターン](../../../../engineering/dependency-security/install-execution-policy/README.md)、
Pythonで具体化するには[pip実装例](../../../../engineering/dependency-security/install-execution-policy/implementations/pip/README.md)、
仕様と採否には[参照資料記録](../../../../sources/README.md#spec-install-execution-policy)を参照してください。
