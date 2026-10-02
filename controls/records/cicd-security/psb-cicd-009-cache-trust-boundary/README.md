# PSB-CICD-009: Cache trust boundary

新しいrunnerでも、以前のjobが保存したtoolをcacheから戻して実行すれば、そのjobの影響を受けます。
このcontrolは、CIの再利用を高速化のための取得ファイルに絞り、保存者と利用時の確認を結び付けます。

学ぶ：[教材](learning.md) · 設計する：[CI state and runner lifecycle](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)

## 問い

CIが再利用するファイルを誰が保存し、誰が復元して使うかを追跡し、未信頼の内容が高権限の実行へ届く経路を切れるか。

## できてはいけないこと

PR作成者や侵害された保存処理が作ったファイルを、後続の公開・deploy・署名jobが検証せず実行してはいけません。
Cacheを読める利用者へ秘密情報を公開したり、別目的・別環境の復元結果を同じ依存内容として扱ったりしてはいけません。

## 適用範囲と非適用

依存の取得ファイルを再利用するdownload cacheの保存者・利用者、実効権限、key、保存path、復元結果、利用時の検証が対象です。
Setup Actionの自動cacheや独自clientも含め、全workflowを確認します。展開済みの依存環境やtoolの共有を、この取得cacheの許可へ含めません。
Runner自体の残存状態と、承認した成果物の配布は別の境界です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `CACHE-1` | 保存者をレビューした限定的な処理へ絞る |
| `CACHE-2` | 用途・形式の版・OS・architecture・runtime・欠落のないlock digestで取得対象を識別する |
| `CACHE-3` | 未信頼PRは復元だけを許可し、信頼済みの処理が使う範囲へ保存させない |
| `CACHE-4` | 秘密情報、展開済みの依存環境、tool、起動用ファイル、build出力をこの取得cacheへ入れない |
| `CACHE-5` | 完全一致でない結果・失敗・部分復元を採用せず、一致した場合も承認hashと依存関係を再確認する |
| `CACHE-6` | 権限付きrelease・deploy・署名jobはこのCI cacheを使わない |
| `CACHE-7` | 全保存者・利用者と現在の挙動を確認できなければ導入済みと判定しない |

## 何を再利用するか決める

まず利用者が何を実行し、どの権限へ届くかを確認します。次に保存者・内容・取得条件・実効アクセスを絞ります。
Keyは取得先を探す識別情報であり、内容の署名ではありません。保存者が信頼済みでも侵害される場合を考えます。
性能のために検証を省かず、cacheがない場合も同じhash付きinstallを行います。

GitHubのbranchごとの取得範囲、`cache-mode`、再利用workflowへの上限指定は[設計ガイダンス](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md#githubの具体化と確認)で確認します。
通常のPR用cacheを作っただけで、default branchのcacheも変更できたとは判断しません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は、再利用した内容が検証を迂回しないか確認する項目です。設計レビューに使えます。
試す場合は専用の使い捨てcacheと無害なファイルを使います。実施済みの結果ではありません。

- **CACHE-1・3**：未信頼PRや呼出先workflowが、信頼済み処理の取得範囲へ保存できないか。保存stepを省くだけでなく実効権限も確認する。
- **CACHE-2**：Lockの欠落、別OS・architecture・runtime・用途で、同じkeyを作り別内容を復元できないか。
- **CACHE-2・5**：完全一致がないとき、prefix一致や古い結果をそのまま実行せず、専用領域を初期化して正規の取得へ戻るか。
- **CACHE-4**：保存pathを広げたり自動cacheを使ったりすると、認証情報、展開済み環境、tool、起動ファイル、build出力が混ざらないか。
- **CACHE-5**：同じkeyで無害な改変ファイルを復元すると、利用前のhash照合が拒否するか。Hitを理由に照合や必要なinstallを飛ばさないか。
- **CACHE-5**：復元の中断・部分展開・障害があっても、残ったファイルを使わず同じ完全性確認を行うか。
- **CACHE-6**：公開・deploy・署名jobに、直接のcache操作だけでなくsetup Actionや呼出先経由の再利用が残っていないか。
- **CACHE-7**：保存拒否・処理省略が成功表示になる場合も実態を確認し、未取得・古い・部分的な観測を導入済みにしないか。

## 境界と根拠

攻撃段階5の保存済み状態を段階7・9・10の権限付き処理へ昇格させる経路を切ります。
高権限の利用者がなくても非特権jobの改ざんや停止は残り、復元archiveの展開前認証も別の問題です。
七レイヤーではプラットフォームに直接対応し、外部依存の同一性・運用の確認へ接続します。

取得内容の照合は[DEPS-003](../../dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、未信頼PRから権限処理への全経路は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、同じ実行環境に残る状態は[CICD-007](../psb-cicd-007-runner-lifecycle-isolation/README.md)へ接続します。

- [教材](learning.md)
- [設計パターンとGitHubガイダンス](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)
- [Cache仕様と採否](../../../../sources/README.md#spec-ci-cache-boundary)
- [Mapping](../../../../mappings/frameworks.yaml)：SITF `1.0.0@d1d1536 / T-C007`、GitHub固定registry、OSPS `2026.02.19 / OSPS-BR-01.03`。割当は移行レビュー中
