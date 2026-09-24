# ENG-CICD-003: CI state and runner lifecycle

## 利用場面と推奨構成

高速化のための再利用と、jobの信頼境界を両立させる設計に使います。
読者は再利用するデータと破棄する資産、実行時検知へ残す責任を選べるようになります。

```text
承認済みimage → 限定したjob dispatch → 新しいcompute世代
  → 限定したdownload cacheを復元 → 独立したartifact hash照合
  → 権限を絞って実行 → 固定したartifactを別のconsumerへ渡す
  → 外部へログ保存 → 登録解除・computeとstorage破棄 → 世代を照合
```

高権限consumerはこのCI cacheを使わず、認証・検証したartifactやclean inputから始めます。
外部cache、runnerのworkspace、artifactの受け渡しを一つの信頼済みstateとして扱いません。

## 選択肢と代償

| 選択 | 代償・確認する境界 |
|---|---|
| Cacheを使わない | ダウンロードとbuild時間が増える。Runner残存stateは別に対処する |
| 非特権jobのdownload cacheだけ再利用 | 全graphのhash確認とpath分類が必要。秘密情報と実行済み環境を混ぜない |
| Hosted runnerを使う | Providerのimage・生成・破棄・隔離の保証範囲を確認する |
| 組織のJIT one-job runnerを使う | Provisioner、group、network、ログ配送、破棄の実装・確認責任が増える |

Cache miss、部分復元、障害では限定したpathを初期化してcleanな取得へ戻し、同じ検証を行います。
初期化対象は採用先で解決・確認した専用pathだけです。Cacheの可用性低下と、依存完全性の検証失敗は別の結果です。

## GitHubの具体化と確認

Cacheのkeyはpurpose・schema・platform・runtime・lock digestで識別し、exactでない復元を採用しません。
旧profileはprotected mainへのpushだけが保存する方式です。現在の`cache-mode`ではPR等のconsumerを`read`、
権限付きjobを`none`へ限定する方式も検討します。対応範囲と実効値は採用先で確認します。
Reusable workflowのcaller側にも明示的な上限を設定する設計を検討し、save stepを削除しただけで
jobが保存権限を持たないと解釈しません。

無害なPRとmain runで実際の保存scopeと復元結果を確認します。Exact hit・lock変更・破損時にも
hash付きinstallが行われ、秘密情報やinstalled treeをpathに含めないことを確認します。
旧workflowは全面移植せず、採用するruntime・Actionの版と実効挙動を確認してから独立実装にします。

Runnerはgroup・repository・workflowを限定し、一jobごとのprovision・dispatch・登録解除・破棄を世代で照合します。
二つのjobの無害なmarkerと、providerイベント、responseを保存しないmetadata・socket・network拒否確認を併用します。
Provider固有のprovisioner・破棄はこのpatternでは実装していません。Live未確認は`NOT_CHECKED`、収集失敗は`ERROR`です。

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
