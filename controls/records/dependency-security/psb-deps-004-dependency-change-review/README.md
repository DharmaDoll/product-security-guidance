# PSB-DEPS-004: Dependency change review

直接依存を一つ更新したつもりでも、その先の依存も変わることがあります。
このcontrolは、今回の変更を判断する範囲と、その判断がmergeを止める条件を結び付けます。

学ぶ：[Dependency change review](learning.md) · 設計する：[設計パターン](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)

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
| `DEP-REVIEW-3` | 現在の変更を評価し終えた必須判定がない限りmergeできず、失敗・取消・検査欠落・未評価を許可にしない |

## 比較・判定・merge条件を決める

まず差分の取得範囲、次に判定方針、最後にmergeの強制点を確認します。PRに差分が見えることと、
Actionが失敗することと、mergeが拒否されることは別々です。Headや対象baseが変わった場合は、
古い結果・承認を現在の変更の根拠にせず再評価します。

Jobの成功表示から、必要な評価が終わったと推測しません。データ不足や処理の省略が成功扱いになる方式なら、
別の必須判定で未評価を止める必要があります。判定方針と必須条件の変更自体も独立したレビューへ結び付けます。

旧GitHub実装の基本方針は、変更依存のruntime・development・unknown scopeについて、既知high・criticalを
止めるものです。この基準を全環境の既定値にせず、利用経路、許容リスク、運用責任とともに決めます。
License、取得元、来歴、独立レビューを追加する場合は、根拠・観測範囲・判定を別に定義します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は、拒否した変更や評価できない変更がmergeされないか確認する項目です。診断・設計レビューに使えます。
依存を実行する必要はありません。項目を記載しただけで、実際のmerge拒否を確認済みとは扱いません。

- **DEP-REVIEW-1**：直接依存は変えずに推移依存を追加・更新・削除しても、現在の差分へ表示されるか。
- **DEP-REVIEW-1・3**：Head更新やbaseの進行後、古い比較結果・承認だけで現在の変更をmergeできないか。
- **DEP-REVIEW-1**：対応外のmanifest、必要なデータの未取得、部分取得を、依存変更なしとして扱わないか。
- **DEP-REVIEW-2**：拒否対象を追加したとき、警告だけの成功や別の利用範囲への分類で判定を通らないか。
- **DEP-REVIEW-1・3**：データ準備の待機期限後も不足が残る場合、成功表示だけでmergeを許可しないか。
- **DEP-REVIEW-3**：失敗、取消、検査欠落、処理の省略を試すと、必要な評価なしでmergeできないか。
- **DEP-REVIEW-2・3**：同じ変更で判定方針・必須条件を弱めたり、別の処理が同じ検査名の成功を出したりして、承認を迂回できないか。

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
- [Framework mappings](../../../../mappings/frameworks.yaml)：OSPS `2026.02.19 / OSPS-VM-05.03`の既知脆弱性gateと、SSDF `1.1 / PW.4.1`の部品採用レビューに限る部分的な設計関係。旧`OSPS-VM-05.01・05.02`とATT&CK `T1195.001`は[移行台帳](../../../../docs/MIGRATION.md)に非継承理由を記録
- [Metadata](control.yaml)
