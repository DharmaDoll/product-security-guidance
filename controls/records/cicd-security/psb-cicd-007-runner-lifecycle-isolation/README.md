# PSB-CICD-007 Runner lifecycle isolation

**前のjobが残したものやhostの権限を、次のjobへ渡していないか。**

## なぜ必要か

例えば、前のjobが残したprocessが同じmachineで始まる公開jobの認証情報を読むことがあります。Runnerの登録を解除しても、hostや保存領域が残れば次のjobへの影響は消えません。

## 満たすべきこと

1. **実行先を限定する。** 未信頼jobを組織のself-hosted runnerへ割り当てず、使えるrepository・workflowを絞る（RUNNER-1）。承認済みのimageとrunner版を使い、更新時にjob由来の状態を引き継がない（RUNNER-3）。
2. **jobごとに新しい環境を使う。** 終わった実行環境を次のjobへ戻さず（RUNNER-2）、起動時に前jobのworkspace、process、host上の認証情報がないことを確認する（RUNNER-4）。不要なcloud metadata、host socket、管理・内部networkへの到達も止める（RUNNER-5）。
3. **管理権限と破棄を分けて確認する。** Runnerの登録権限を用途と期間へ限定し、jobから使わせない（RUNNER-6）。Jobとrunnerの世代に対応させ、登録解除だけでなくcompute、保存領域、processの破棄を確かめる（RUNNER-7）。調査用ログは破棄前に外へ保存する（RUNNER-8）。
4. **状態が不明な世代を再利用しない。** 作成・破棄・ログ配送の記録が欠ける、古い、部分的、失敗した場合は合格にせず、次のjobを割り当てない（RUNNER-9）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 未信頼PRや別repositoryから、限定した組織runnerへjobを割り当てられないか。
- 名前の変更、再登録、workspaceの削除だけで、前jobの環境やprocessを再利用していないか。
- 未承認imageや古い外部volume、不要なmetadata・host socket・管理networkへ到達できないか。
- Jobからrunner登録用の認証情報を読めないか。緊急時の管理経路が通常jobへ開いていないか。
- Job取消・異常終了や破棄失敗の後、同じ世代へ次のjobを割り当てていないか。ログ配送失敗を識別できるか。

これらは診断・設計レビューの確認項目です。試す場合は承認した使い捨て環境と無害なmarkerを使い、実認証情報を証拠へ保存しません。Markerが残らないことだけでは、全状態の消去を示せません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| GitHub「Secure use」 | 未信頼jobと特権runnerを分け、runner group・一回限りの登録・hostの到達先を確認する。 | 登録解除だけではmachineや保存領域の破棄を証明できない。 |
| OpenSSF OSPS Baseline 2026.02.19 OSPS-BR-01.03 | 未信頼jobから特権のCI資産・認証情報へ届かせない部分を支える。 | OSPSは一回限りrunnerや破棄方法を指定しない。 |
| MITRE ATT&CK Enterprise v19.1 T1552.005 | Jobからhostのcloud metadataへ到達させない設計が、認証情報の取得経路を部分的に狭める。 | Jobに意図して渡す認証情報や別の取得経路は対象外。 |

対象特性と残る範囲は[マッピング](../../../../mappings/frameworks.yaml)にあります。実runnerの破棄、通信拒否、規格への準拠を示しません。

## このコントロールの範囲

対象はrunnerの割当、起動時の状態、hostへの到達、登録権限、破棄、調査用ログです。Hosted runnerはproviderの保証範囲を、自組織のrunnerは実際の作成・破棄を確認します。外部cacheの再利用は[CICD-009](../psb-cicd-009-cache-trust-boundary/README.md)、未信頼PRの経路は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、job内のbuild隔離は[BUILD-001](../../build-security/psb-build-001-build-containment/README.md)へ渡します。ログの保存だけで異常を検知したことにはなりません。

Runnerの作成・破棄とGitHub固有の扱いは[engineering](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)を参照してください。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-cicd-014)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
