# PSB-DEPS-002: Install execution policy

学ぶ：[学習ノート](learning.md) · 設計する：[Install execution policy](../../../../engineering/dependency-security/install-execution-policy/README.md)

## 問い

依存パッケージを取得・準備するとき、公開者が提供したスクリプトやbuild backendの実行を、
必要性を確認した対象だけに限定できるか。

## できてはいけないこと

悪意ある公開者や侵害された保守担当者が、依存パッケージのインストールを入口に、開発端末・CIの
認証情報、ソース、内部サービスへアクセスしてはいけません。インストールを成功させるための全許可が、
新しいバージョンや推移依存まで無条件に実行可能にしてはいけません。

## 適用範囲と非適用

依存パッケージのlifecycle script、native build、source distributionのbuild backendを起動する経路が対象です。
直接依存だけでなく推移依存、自動更新、開発端末、CI、別のinstallコマンドも確認します。

インストール後のimport、test、compiler plugin、アプリケーション実行の安全性は別の境界です。
実行不要なパッケージだけを使う環境にも適用でき、その場合は許可リストを空にできます。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `DEP-EXEC-1` | install時に外部提供のコードを実行する経路を特定し、未承認の実行を既定で拒否する |
| `DEP-EXEC-2` | 実行を許可する場合、対象パッケージ・バージョン・取得内容と必要性を特定し、別の担当者がレビューする |
| `DEP-EXEC-3` | CLI、環境変数、設定の優先順位、別コマンド、source buildへのfallbackで拒否を回避させない |
| `DEP-EXEC-4` | 設定欠落、未対応版、解析失敗、挙動を確認できない状態を、実行許可や合格に変えない |

## 実装判断の羅針盤

まず「そのコードを実行しなくても必要な機能を得られるか」を確認します。実行不要なら停止し、
必要なら実行許可と実行環境の権限を別々に決めます。package managerの標準機能を優先しますが、
名前だけのtrustや全許可を、対象バージョンの独立レビューの代わりにはしません。

| 状況 | 判断 |
|---|---|
| scriptやsource buildが不要 | 実行を全面停止し、拒否による失敗をfallbackで回避しない |
| 特定のnative buildが必要 | 対象を絞って許可し、認証情報と通信を制限した使い捨て環境で実行する |
| 製品の許可機能が名前だけを指定する | version・digestを別の保護された入力に結び付ける。将来の更新まで承認したと解釈しない |
| 未承認scriptがskipされてinstallは成功する | 必要機能が欠ける可能性も確認する。成功終了だけで採用判断を完了しない |

実行例外の所有者、理由、期限は例外管理と接続します。通常の実行許可を無期限の包括例外にしません。

例外のscope・承認・期限・失効状態は[Security exception lifecycle](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へ接続します。
Install execution policy側には、exact package・version・artifact digest・実行pathが必要か、どのcontainmentで実行を許すかという判断を残します。
例外が有効でも`DEP-EXEC-1`のdefault denyを`PASS`へ変更せず、別artifactやglobalなinstall script有効化には使いません。関係の正本は[exception consumer mapping](../../../../mappings/exception-consumers.yaml)です。

## 前後の受け渡しと残余境界

Cooldownは観測時間、lockfile・hashは採用内容の同一性、このcontrolはinstall時の実行許可を扱います。
古く、hashが一致するパッケージでも、悪意あるscriptは存在し得ます。

七つのレイヤーでは外部依存とサプライチェーンを直接扱い、プラットフォームの実行権限とガバナンスに接続します。
攻撃段階4の取得・準備から段階7の実行へ渡る箇所で、未承認コードを起動する経路を切ります。
許可したbuildと、その後のimport・testの隔離、runnerの破棄、成果物・本番の安全性は保証しません。

## 根拠をたどる

- [製品仕様と採否](../../../../sources/README.md#spec-install-execution-policy)
- [REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)と[攻撃段階の分析](../../../../docs/ANALYSIS_LENSES.md)：横断分析の入力
- [framework mapping](../../../../mappings/frameworks.yaml)：ATT&CK `v19.1 / T1195.001`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`。移行レビュー中であり、準拠や導入済み状態を意味しない
- [control metadata](control.yaml)
