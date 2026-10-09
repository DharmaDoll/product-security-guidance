# ENG-DEPS-001: Dependency release cooldown

新しい依存版を、公開から一定期間は選ばないための設計です。何を満たすかは[DEPS-001](../../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)、公開直後の版を選ぶ場面は[教材](../../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/learning.md)を参照してください。

## 止める場所

```text
新しい依存版の候補
  → 名前・バージョン・取得元と公開時刻を確認
  → 待機期間を満たすか判定
      ├─ 未満・判定不能 → 採用を止める
      └─ 満たす       → 他のレビューへ進む
  → インストール・テスト・マージ
```

完全なCIでインストールした後に待機時間を調べても、そのCI上で動いたインストール用コードは止められません。判定は、依存が提供するコードの実行より前、かつマージより前に置きます。更新ボット、開発者、AIエージェント、ロックファイルの再生成など、版を新たに選ぶ経路を確認します。

## 設計時に決めること

| 判断 | 確認すること |
|---|---|
| 何を評価するか | パッケージ名、正確なバージョン、取得元レジストリを一組で扱う。PRの作成日やローカルファイルの時刻を公開時刻の代わりにしない |
| どの時刻を使うか | 承認した情報源の公開時刻と信頼できるUTC時刻を使う。情報がない、古い、読めない、取得に失敗した場合は通さない |
| どれだけ待つか | 更新の速さと公開直後の情報不足を考えて組織が決める。パイロットの168時間は旧設定を継いだ例であり、規格が求める値ではない |
| 誰が変更できるか | 依存を更新するPRが同じPR内で判定器や待機条件を弱められないようにする。別のクライアントや設定の上書きも確認する |
| 緊急時はどうするか | 対象の版を限定し、担当者、別の承認者、期限を記録する。通常条件は不合格のまま「例外付きで許可」と分ける。例外を将来の更新へ使い回さない |

## 強制方法を選ぶ

| 方法 | 向く場面と注意点 |
|---|---|
| パッケージ管理ツールで候補を除外 | 依存解決の時点で止められる。対応版、設定の優先順位、別クライアントからの迂回を確認する |
| 信頼できるCIの必須検査 | 複数のリポジトリに同じ判定を適用できる。インストール前に動かし、PRから判定器と方針を変更できないようにする |
| 管理されたレジストリプロキシ | 取得時の遮断・追跡は[DEPS-005](../../../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)で扱う。待機期間を強制する製品・設定でなければ、プロキシを通すだけでDEPS-001を満たしたことにはならない |
| 保護された手作業の確認 | 自動化できないときの運用手段。公開時刻、最短採用時刻、承認者を残し、自動的な拒否とは区別する |

[npmの実装例](implementations/npm/README.md)は導入・確認・解除まで示します。別のツールの仕様は[参照資料](../../../sources/README.md#ref-deps-004)から個別に確認してください。特定のツールが使えるからといって、他のツールにも同じ設定が効くとは限りません。

確認には[controlの診断項目](../../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md#failure-checks)を使います。待機時間を過ぎた版も、安全と証明されたわけではありません。取得物の同一性は[DEPS-003](../../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、インストール時の実行制御は[DEPS-002](../../../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)、例外の期限と承認は[GOV-002](../../../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へつなぎます。実際のCIや開発端末に導入した証拠は、この設計文書にはありません。
