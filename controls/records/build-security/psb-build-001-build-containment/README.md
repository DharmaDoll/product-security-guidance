# PSB-BUILD-001: Build containment

## 問い

ビルドするコードが悪意を持っていても、ソースの読み取りと限定した出力の生成を超えて、秘密情報、host、管理面、deploy権限へ届かないようにできるか。

## できてはいけないこと

依存パッケージやビルドスクリプトが、同じ実行環境にある認証情報やruntime socketを使って、リポジトリを書き換えたり本番を操作したりしてはいけません。
通信制限の宣言やイベント件数ゼロを、実際の拒否やセンサー正常稼働の証拠にしてはいけません。

## 適用範囲と非適用

ソース・依存・plugin・testを実行するビルド環境、その実効権限、ファイルシステム、通信、観測、出力の受け渡しが対象です。
Runnerの割当・破棄は[Runner lifecycle isolation](../../cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、
取得した依存の同一性は[Dependency artifact identity](../../dependency-security/psb-deps-003-dependency-artifact-identity/README.md)が扱います。
来歴生成、署名、consumerの受入、本番監視は別の保証境界です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `BUILD-1` | 実行コードから秘密情報、token発行能力、管理面の書込権限を除く。取得に認証が必要なら、別の取得境界で入力を用意する |
| `BUILD-2` | Buildとdeployを別の権限境界に置き、固定した成果物だけを受け渡す。受取側は内容と期待値を独立して判断する |
| `BUILD-3` | 通信を既定で拒否し、必要な宛先だけを外側の強制点で許可する。Proxy、DNS、redirect、metadata等の迂回も確認する |
| `BUILD-4` | 一時的な非root環境、読み取り専用root、専用の書込領域を使い、host socketや管理サービスへ届かせない |
| `BUILD-5` | Process・networkを観測し、センサーと配送の健全性を別に確認する。異常の通知・調査先を決める |
| `BUILD-6` | 設定欠落、収集失敗、部分的・古い観測を適合と判定しない。出力の昇格を停止し、未確認と異常を区別する |

## 実装判断の羅針盤

Build jobは信頼済みrevisionで始まっても、依存やtestのコードを実行します。読み取り専用tokenでも読み取れる非公開資産があるため、
「writeがない」だけで被害がないとは判断しません。取得と実行を分け、実行環境へ渡す入力・権限を減らします。

通信先のallowlistは内容の安全性も送信内容の適切さも保証しません。必要なら入力取得後はネットワークを閉じます。
Read-only rootでもビルド用の書込領域は必要です。出力を後続jobの設定・起動コードとして解釈すると、権限分離を越える経路が残ります。

## 保証しない範囲

Sandboxや許可先の侵害、成果物自体の悪意、共有kernel・platform管理面の欠陥は残ります。
隔離と観測を定めるだけでSLSA Build L3を達成したとは扱いません。
旧JSON計画検査は実行時の強制を証明しないため、今回は移植していません。

- [学習ノート](learning.md)
- [Build execution boundary pattern](../../../../engineering/build-security/build-execution-boundary/README.md)
- [仕様・採否](../../../../sources/README.md#spec-build-containment)、[sensor候補](../../../../sources/README.md#ref-build-001)
- [Framework mapping](../../../../mappings/frameworks.yaml): 旧版・ID・関係を保持。新しい特性への割当はレビュー中
