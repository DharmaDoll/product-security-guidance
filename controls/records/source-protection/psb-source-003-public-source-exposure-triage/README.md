# PSB-SOURCE-003: Public source exposure triage

**公開された場所に、自社の情報が出ていないか。出ていたら、公開してよい情報かを確かめ、必要な対応につなげられるか。**

## なぜ必要か

たとえば、第三者の公開リポジトリのIssueに社内システムの接続先が貼られても、自社のリポジトリの検査だけでは見つかりません。このコントロールは、公開コードや投稿にある自社の情報を探し、見つけた後の判断につなげるものです。

## 満たすべきこと

1. **探す。** 自社のドメインやメールアドレスなど、使用を認めた手がかりで公開コード・Issue・Pull Requestなどを調べる。どこまで調べられたかを分かるようにし、検索が失敗した場合を「見つからなかった」と扱わない。
2. **確かめる。** 見つけた情報が自社のものか、公開してよいものか、第三者が知ると何ができるかを所有者と判断する。同じ投稿でも内容が変われば確認し直す。
3. **渡す。** 対応が必要なら担当者へ知らせ、判断と対応の状況を追えるようにする。通知や記録に失敗した候補を放置せず、認証情報などの値を不要に複製しない。

公開検索は、既に分かっている漏えいへの対応を待たせる理由にはなりません。認証情報が共有先へ届いたと分かっている場合は、[SOURCE-002](../psb-source-002-secret-publication-boundary/README.md)から所有者と[GOV-004](../../governance-operations/psb-gov-004-credential-exposure-containment/README.md)へ直接渡します。顧客データなどは[SOURCE-008](../psb-source-008-sensitive-data-repository-admission/README.md)からデータの所有者と情報漏えい対応担当へ渡します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 検索が途中で失敗したり、結果が件数の上限で切れたりしても、「該当なし」と報告していないか。
- 同じ投稿に新しい情報が加わったとき、以前の「確認済み」で見逃していないか。
- 発見した情報を担当者へ渡せなかったとき、対応済みとして閉じていないか。通知に認証情報の値を載せていないか。
- 認証情報の投稿を削除しただけで、失効などの対応を担当者へ渡し忘れていないか。

ここに書いたのは確認項目であり、実際に診断した結果ではありません。

## フレームワークとの関係

- MITRE ATT&CK Enterprise v19.1 T1593.003: 公開コードリポジトリから自社情報が見つかる経路を観測する、部分的な検出関係です。攻撃者が実際に検索したことを検知するものではなく、公開面を網羅した証明にもなりません。

このControlと技法の関係は[マッピング](../../../../mappings/frameworks.yaml)に記録しています。公開検索や精査の実施結果は含みません。

## このコントロールの範囲

対象は、公開されたコードや開発上の投稿から自社の情報を探し、内容を確認して対応へ渡すところまでです。非公開リポジトリや端末の検査、認証情報の失効、公開情報の削除は別の作業です。検索で0件でも、公開情報がどこにも存在しない証明にはなりません。

具体的な場面は[教材](learning.md)、検索範囲・重複・通知・失敗時の設計は[engineering](../../../../engineering/source-protection/public-exposure-observation-and-triage/README.md)、GitHubの公開コード・Issue・PRを探す方法は[実装例](../../../../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)を参照してください。6つの特性と参照資料IDは[control.yaml](control.yaml)、参照した資料の採否は[Sources](../../../../sources/README.md#ref-public-source-exposure-001)、フレームワークとの関係は[マッピング](../../../../mappings/frameworks.yaml)、旧成果物との対応は[移行記録](../../../../docs/MIGRATION_SOURCE_PROTECTION.md#public-exposure-migration)にあります。
