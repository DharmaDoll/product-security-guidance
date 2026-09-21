# PSB-DEPS-004: Dependency change review

学ぶ：[Reviewed dependency intake](../../../../docs/learning/reviewed-dependency-intake.md) · 設計する：[設計パターン](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)

## 問い

今回の変更で追加・更新・削除される直接・推移依存を把握し、採用方針で拒否した変更と評価できない変更を、
マージ前に止められるか。

## できてはいけないこと

開発者、更新ボット、侵害されたcontributorが、長いlockfileの差分にある依存変更を見落とされたまま
build・製品へ取り込ませてはいけません。既知の脆弱性を含む変更が警告だけで通ったり、API・runnerの
失敗で評価されなかった変更が、必須検査の成功として扱われたりしてはいけません。

## 適用範囲と非適用

現在の変更のbaseとhead、対応する依存関係、変更されたpackage・version・利用範囲、判定方針、
その結果を使うmerge gateが対象です。依存が使われるOSやbuild条件と、比較機能の対応範囲を明示します。
既存の必須SCA検査が同じ差分・判定・merge拒否を提供するなら、重複したtoolは不要です。

未変更の依存への継続監視、取得artifactのhash検証、install時の実行抑止は別の責任です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `DEP-REVIEW-1` | 現在のbase・headに対する直接・推移依存の変更と利用範囲を、対応するmanifest・lockとともに表示する |
| `DEP-REVIEW-2` | 明示した方針で変更を評価し、拒否対象をwarning付きsuccessへ変換しない |
| `DEP-REVIEW-3` | 現在の変更の必須判定が成功しない限りmergeできず、failure、error、cancel、missingを許可にしない |

## 実装判断の羅針盤

まず差分の取得範囲、次に判定方針、最後にmergeの強制点を確認します。PRに差分が見えることと、
Actionが失敗することと、mergeが拒否されることは別々です。Headや対象baseが変わった場合は、
古い結果・承認を現在の変更の根拠にせず再評価します。

旧GitHub実装の基本方針は、変更依存のruntime・development・unknown scopeについて、既知high・criticalを
止めるものです。この基準を全環境の既定値にせず、利用経路、許容リスク、運用責任とともに決めます。
License、取得元、来歴、独立レビューを追加する場合は、根拠・観測範囲・判定を別に定義します。

## 境界と受け渡し

脆弱性が実害になるには、affected versionが実際に使われ、脆弱な処理へ攻撃入力や重要なCI資産から
到達する必要があります。Severityだけで侵害を断定せず、止めた後に文脈を調査します。
未公開の脆弱性、advisoryのない悪意あるpackage、侵害されたmaintainerの意図を、この基本判定では識別できません。
対応外のecosystemや不完全なデータは、空の安全な差分にせず未評価として扱います。

攻撃段階4の採用判断を段階5のmerge gateへ接続し、承認したgraphを
[Dependency artifact identity](../psb-deps-003-dependency-artifact-identity/README.md)へ渡します。
七つのレイヤーでは外部依存とプラットフォームに直接対応し、PSIRTのトリアージとガバナンスに接続します。
現在の変更が通っても、後日公開される脆弱性への継続対応やbuild・releaseの安全性は保証しません。

## 参照仕様とマッピング

- [REF-DEPS-002](../../../../sources/README.md#ref-deps-002)：旧参照資料と現行実装の範囲差、採否、製品仕様
- [GitHub実装例](../../../../engineering/dependency-security/reviewed-dependency-intake/implementations/github/README.md)
- [Framework mappings](../../../../mappings/frameworks.yaml)：OSPS `2026.02.19 / OSPS-VM-05.01..03`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`、ATT&CK `v19.1 / T1195.001`。移行レビュー中
- [Metadata](control.yaml)
