# PSB-CICD-009: Cache trust boundary

## 問い

CIが再利用するstateを誰が保存し、誰が復元して使うかを追跡し、低信頼のstateが高権限の実行へ届く経路を切れるか。

## できてはいけないこと

PR作成者や侵害されたproducerが保存したファイルを、後続の公開・deploy・署名jobが検証せず実行してはいけません。
Cacheを読めるcontributorへ秘密情報を公開したり、別目的・別platformの復元結果を同じ依存内容として扱ったりしてはいけません。

## 適用範囲と非適用

Cache writer・reader、実効権限、key、path、restore結果、利用時の独立検証、全workflowのinventoryが対象です。
Setup Actionの自動cacheやcustom clientも含めます。Runner自体の残存stateと、承認artifactの配布は別の境界です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `CACHE-1` | 保存者をレビュー済みの限定したproducerへ絞る |
| `CACHE-2` | Purpose・schema・OS・architecture・runtime・非空のlock digestでlookupを識別する |
| `CACHE-3` | 未信頼PRはrestore-onlyとし、信頼済みconsumerへ届くnamespaceへ保存させない |
| `CACHE-4` | 秘密情報、installed tree、tool、起動用state、build outputをこのdownload cacheへ入れない |
| `CACHE-5` | 非exact・失敗・部分復元を捨て、exact hitでも承認hashと依存整合性を再検証する |
| `CACHE-6` | 権限付きrelease・deploy・署名jobはこのCI cacheを使わない |
| `CACHE-7` | 全writer・consumerと現在の挙動を確認できなければ導入済みと判定しない |

## 実装判断の羅針盤

まずreaderが何を実行し、どの権限へ届くかを確認します。次にwriter・内容・lookup・実効アクセスを絞ります。
Keyはlookupの識別情報であり、内容の署名ではありません。保存者が信頼済みでも侵害される場合を考えます。
性能のために検証を省かず、cacheがない場合も同じhash付きinstallを行います。

旧GitHub例はprotected mainへのpushだけがdownload cacheを保存する方式です。
現在の`cache-mode`による制限も確認し、event名だけやsave stepの条件だけで実効権限を推測しません。
PRが通常作るmerge-ref cacheとdefault-branch cacheは同じscopeではなく、PRがcacheを作っただけで
default branchが汚染されたとは断定しません。

## 境界と根拠

攻撃段階5の永続stateを段階7・9・10の権限付きconsumerへ昇格させる経路を切ります。
高権限consumerがなくても非特権jobの改ざんや停止は残り、復元archiveの展開前認証も別の問題です。
七レイヤーではプラットフォームに直接対応し、外部依存の同一性・運用の確認へ接続します。

- [共有教材](../../../../docs/learning/ci-state-and-runner-lifecycle.md)
- [設計パターンとGitHubガイダンス](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)
- [Cache仕様と採否](../../../../sources/README.md#spec-ci-cache-boundary)
- [Mapping](../../../../mappings/frameworks.yaml)：SITF `1.0.0@d1d1536 / T-C007`、GitHub固定registry、OSPS `2026.02.19 / OSPS-BR-01.03`。割当は移行レビュー中
