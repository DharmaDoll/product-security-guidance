# ENG-GOV-004: Deployed artifact rebuild and replacement

影響を受けた稼働成果物を置き換え、古い成果物が元の調査範囲で動いていないと確認するための設計です。満たすべきことは[GOV-005](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)、一部環境に旧イメージが残る場面は[教材](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md)を参照してください。

## 復旧の流れ

```text
影響する古いdigestと稼働範囲を特定する
  → 担当者・期限・対象環境を決める
  → 原因を再び取り込まないように再ビルドする
  → 新しいdigestを承認・公開し、各環境へ置く
  → 元の範囲を再確認し、古いdigestが動かないと確かめる
```

ビルド成功、新しいタグの公開、一つの環境への配布は、それぞれ途中の状態です。新しいdigestが使えることと古いdigestが使われていないことを別々に確認します。

## 設計時に決めること

| 判断 | 確認すること |
|---|---|
| どこを置き換えるか | 製品担当者の影響調査から、古いdigest、稼働環境、停止中の処理、切り戻し先を受け取る。依存が原因なら[GOV-001](../../../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)の結果を使う。タグ名だけで同一性を決めない |
| いつまでに行うか | 脆弱性なら[GOV-003](../../../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)の期限を引き継ぐ。一時使用の例外は[GOV-002](../../../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)で対象・期限を限定し、復旧済みとは扱わない |
| 何を再ビルドに使うか | 問題の原因に応じて、ソース、依存関係、キャッシュ、ビルド環境、署名に使う権限を見直す。同じ仕組みの再実行や別digestだけで安全と決めない。修正を主張するなら[GOV-008](../../../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md)の検証を受け取る |
| 新しい成果物をどう受け入れるか | レビューしたソース、ビルド、来歴、署名、SBOM、公開判断を同じ新しいdigestへ結ぶ。各環境で承認したdigestと実際に動くdigestを照合する |
| いつ復旧済みとするか | 元の調査範囲を新しい情報で再確認する。置換先では新digest、廃止先では停止と再起動経路を確かめ、対象環境で古いdigestが動かず切り戻しでも戻らないことを確認する |

来歴の生成は[BUILD-003](../../build-security/platform-owned-provenance-generation/README.md)、公開先の管理は[CONTAINER-002](../../container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)、利用時の受入は[CONTAINER-001](../../container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)などの隣接設計へつなぎます。これらが文書として存在することを、実環境で機能している証拠にはしません。

## 終了判断で見落としやすいこと

- 稼働一覧から消えた処理が、停止中なだけか、廃止されて再起動できない状態かを分ける。
- 配置の希望状態だけでなく、実際に動いているdigestと観測時刻を確認する。
- 別地域、切り戻し先、取得できなかった環境を、元の調査範囲から黙って外さない。
- 検知アラートが0件、収集処理が失敗、一部だけ取得、通知に失敗した状態を、旧digestが0件の証拠にしない。
- 対応中、期限超過、非該当、復旧済み、証拠不足を同じ「成功」表示へまとめない。

[controlの診断項目](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md#failure-checks)は机上演習にも使えます。実装はビルド基盤、レジストリ、デプロイ先の組合せが決まり、非本番で同じdigest・一部配布・観測失敗を安全に確かめられる場合にだけ検討します。共通の復旧判定スクリプトや架空の合格結果は置きません。旧実装の採否は[移行記録](../../../docs/MIGRATION_GOVERNANCE_OPERATIONS.md#deployed-artifact-recovery-migration)、資料の限界は[Sources](../../../sources/README.md#ref-deployed-artifact-recovery-001)にあります。実際のビルド・配布・稼働はこの文書では確認していません。
