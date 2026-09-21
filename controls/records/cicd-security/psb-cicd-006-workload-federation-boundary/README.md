# PSB-CICD-006: Workload federation boundary

学ぶ：[学習ノート](learning.md) · 設計する：[Workload federation boundary](../../../../engineering/cicd-security/workload-federation-boundary/README.md)

## 問い

CIのworkloadがクラウド権限を取得する条件を、承認した主体・実行文脈・目的に限定し、
取得後の操作対象と有効期間も必要な範囲に絞れるか。

## できてはいけないこと

別repository、未承認のref、異なるEnvironmentのjobが、正規のissuerからtokenを取得しただけで
本番権限を得てはいけません。正しく認証したjobへ無関係なresourceの権限を渡したり、OIDC移行後も
旧長期keyによる迂回経路を残したりしてはいけません。

## 適用範囲と非適用

Issuer、token検証、交換先、受け入れるworkload文脈、token取得権限、交換後のrole・resource・session、
旧認証経路と現在の確認状態が対象です。主なdomainはCI/CD Security、クラウド側の設定とreleaseの権限へ接続します。
Package registryのTrusted Publishingは別の受け入れ先・操作であり、同じ導入境界として扱いません。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `FED-1` | 受け入れ先が承認したissuerとtokenの真正性・有効期間を検証する |
| `FED-2` | Audienceと安定したworkload identityを限定し、ref・Environment・workflow等の不足条件を別の強制点で補う |
| `FED-3` | Token取得と交換を保護されたjobに限定し、未信頼のコード・派生stateをそのjobへ昇格させない |
| `FED-4` | 期待するaccount・roleの必要操作とresourceだけを許可し、session期間を必要な範囲へ絞る |
| `FED-5` | 旧長期keyのconsumerを移行し、保管場所の削除だけでなく旧権限が使えないことを確認する |
| `FED-6` | 現在の設定・交換・拒否・旧key状態を確認できない場合、導入済みや合格にしない |

## 実装判断の羅針盤

まず受け入れ先で検証できるclaimsを確認します。Tokenにclaimがあることと、trust policyがそのclaimを
条件にしていることは別です。Environment名だけを一致させる方式では、branchや同じEnvironmentを使う
別workflowの許可を別途確認します。Repository名の再利用や移管を考慮し、安定したIDへ結び付けます。

認証条件と操作権限を別々にレビューします。短命なsessionでも、署名・公開・deployに使える期間中は被害が起こり得ます。
必要なbuild処理と交換jobを分け、渡されるartifactの同一性を確認します。ID確認の成功だけで権限の最小性を認定しません。

## 前後の境界と限界

攻撃段階6の権限取得を直接扱い、段階5の未信頼PR・workflow、段階7のrunner、段階9・10の公開・deployへ接続します。
七つのレイヤーではプラットフォームを主に扱い、外部依存、監査・復旧の運用、権限管理のガバナンスへつながります。
この対応は[横断分析](../../../../docs/ANALYSIS_LENSES.md)の探索用の関係です。

正規jobそのものの侵害、盗まれたtoken・sessionの有効期間内の悪用、issuer・cloud管理面の侵害は残ります。
Tokenの識別子があっても受け入れ先がsingle-useを強制するとは限りません。署名・来歴のあるartifactでも
内容が安全とは限らず、runner隔離、egress、検知、インシデント時の失効は別途必要です。

## 根拠をたどる

- [SPEC-WORKLOAD-FEDERATION](../../../../sources/README.md#spec-workload-federation)：GitHub・AWS・OIDC仕様
- [REF-CICD-009](../../../../sources/README.md#ref-cicd-009)：短命な認証情報でも残る悪用経路と採否
- [GitHub Actions / AWS実装例](../../../../engineering/cicd-security/workload-federation-boundary/implementations/github-aws/README.md)
- [Framework mappings](../../../../mappings/frameworks.yaml)：旧4関係を保持、特性割当は移行レビュー中
- [Metadata](control.yaml)
