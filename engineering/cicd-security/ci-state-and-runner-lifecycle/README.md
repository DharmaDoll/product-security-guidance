# ENG-CICD-003: CI state and runner lifecycle

## 利用場面と推奨構成

高速化のための再利用と、jobの信頼境界を両立させる設計に使います。
読者は再利用するデータと破棄する資産、実行時検知へ残す責任を選べるようになります。
[Cacheの教材](../../../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/learning.md)と[runnerの教材](../../../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/learning.md)で、それぞれの攻撃経路を追えます。

```text
承認済みimage → 限定したjob dispatch → 新しいcompute世代
  → 限定したdownload cacheを復元 → 独立したartifact hash照合
  → 権限を絞って実行 → 固定したartifactを別のconsumerへ渡す
  → 外部へログ保存 → 登録解除・computeとstorage破棄 → 世代を照合
```

高権限consumerはこのCI cacheを使わず、認証・検証したartifactやclean inputから始めます。
外部cache、runnerのworkspace、artifactの受け渡しを一つの信頼済みstateとして扱いません。

## 三つの境界を分ける

| 判断 | 主なcontrol | 別に残る判断 |
|---|---|---|
| PRで変えられる内容を、権限処理へ渡してよいか | [CICD-005](../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 個々の保存場所やrunnerの実体が隔離されているか |
| 保存・復元する取得ファイルを、誰が作り、何を照合するか | CICD-009 | 同じhostのprocess・volumeが残っていないか |
| 次のjobに新しい実行環境を渡し、前の世代を破棄したか | CICD-007 | 外部cacheや成果物から未信頼の内容を戻していないか |

新しいrunnerを作っても、外部cacheの信頼は変わりません。Cacheを使わなくても、同じhostに残るprocessは消えません。
Job実行中の権限・通信は[Build containment](../../../controls/records/build-security/psb-build-001-build-containment/README.md)へ渡します。

## 選択肢と代償

| 選択 | 代償・確認する境界 |
|---|---|
| Cacheを使わない | ダウンロードとbuild時間が増える。Runner残存stateは別に対処する |
| 非特権jobのdownload cacheだけ再利用 | 全graphのhash確認とpath分類が必要。秘密情報と実行済み環境を混ぜない |
| Hosted runnerを使う | Providerのimage・生成・破棄・隔離の保証範囲を確認する |
| 組織のJIT one-job runnerを使う | Provisioner、group、network、ログ配送、破棄の実装・確認責任が増える |

Cache miss、部分復元、障害では限定したpathを初期化してcleanな取得へ戻し、同じ検証を行います。
初期化対象は採用先で解決・確認した専用pathだけです。Cacheの可用性低下と、依存完全性の検証失敗は別の結果です。
失敗した復元の残存ファイルや、以前の展開済み環境を再利用しません。取得ファイルの照合条件は[DEPS-003](../../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)で確認します。

## GitHubの具体化と確認

Cacheのkeyはpurpose・schema・platform・runtime・lock digestで識別し、exactでない復元を採用しません。
旧profileはprotected mainへのpushだけが保存する方式です。2026-09-27に確認したGitHub.comの仕様では、
`cache-mode: read`は復元だけ、`none`は復元・保存とも許可しません。使う場合はjobの実効値を確認します。
Workflowの値はjob側で上書きできます。再利用workflowには呼出元のjobから明示的な上限を渡し、save stepを削除しただけで保存権限がなくなったと判断しません。

通常の`pull_request`で保存するcacheはmerge refの範囲です。Default branchの後続runが復元するcacheとは区別します。
一方、default branchで動く低信頼イベントに明示的な書込みmodeを与えると、既定の読取り制限を外すため、その内容を誰が変更できるかを再評価します。
保存が拒否・省略されてもjobが失敗するとは限りません。実効mode、操作ログ、保存先を照合します。
製品仕様の出典と採否は[資料記録](../../../sources/README.md#spec-ci-cache-boundary)を参照してください。

無害なPRとmain runで実際の保存scopeと復元結果を確認します。Exact hit・lock変更・破損時にも
hash付きinstallが行われ、秘密情報やinstalled treeをpathに含めないことを確認します。
ここでの成果は方式と確認項目を選ぶガイダンスです。旧workflow・provisionerは一括移植していません。製品固有の例は、採用するruntime・Actionの版、実効挙動と導入時の不足を確認し、効果を説明できる場合に選びます。

Runnerはgroup・repository・workflowを限定し、一jobごとのprovision・dispatch・登録解除・破棄を世代で照合します。
二つのjobの無害なmarkerと、providerイベント、responseを保存しないmetadata・socket・network拒否確認を併用します。
Provider固有のprovisioner・破棄はこのpatternでは実装していません。Live未確認は`NOT_CHECKED`、収集失敗は`ERROR`です。

## 取消・破棄失敗とログ不足を扱う

割当、起動、終了・取消、登録解除、外部ログ保存、実体の破棄を、job IDとrunner世代で追跡します。
終了したjob自身の後片付けだけに頼らず、外側の管理処理で破棄を確認し、失敗・観測不能の世代を再利用しません。
ログ配送が失敗しても、危険な環境を共有poolへ戻したり、記録を待つために動かし続けたりしません。隔離・破棄と調査記録不足を別の状態として扱います。

GitHubのephemeral登録は一job後の登録解除を行いますが、hostの破棄は利用者側の処理です。
Hosted runnerの保証範囲と、自組織の作成・破棄・volume管理・ログ配送の責任を同じ証拠で代用しません。
ここで必要なのは採用先の方式と診断項目の選択です。Provider未選定のprovisionerや合成テストは追加しません。

## 検知の判断を別に残す

Runtime観測にはprocess・file・networkのどの行動を検知したいかを先に定めます。
Job内からsensorを止められるか、イベント欠落を検出できるか、ログが破棄前に外部へ届くか、
alertが所有者へ届き対応されるかを別に確認します。
センサーの導入候補は[REF-BUILD-001](../../../sources/README.md#ref-build-001)へ残し、採用済みや検知完了とは扱いません。

主なdomainはCI/CD Security。Job内のbuild containmentはBuild Security、artifact・deploy・本番runtime・復旧は
Release Integrity、Container / Cloud / IaC Security、Governance / Operationsへ接続します。

- [Cache control](../../../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md)
- [Runner control](../../../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)
- [Runner lifecycle教材](../../../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/learning.md)
- [Cache trust教材](../../../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/learning.md)
- [Cache仕様](../../../sources/README.md#spec-ci-cache-boundary)、[runner仕様と採否](../../../sources/README.md#ref-cicd-014)
