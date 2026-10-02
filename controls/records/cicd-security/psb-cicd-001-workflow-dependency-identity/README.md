# PSB-CICD-001: Workflow dependency identity

Workflowを変更していないのに、昨日と違う外部コードがCIで動く。たとえばActionの`v1`タグが別のcommitへ移ると、利用側のレビューに差分が出ないまま実行内容が変わります。CIを管理する開発者とレビュー担当者が、**選んだ外部コードを、レビューした版へ結び付けられるか**を判断するcontrolです。

## 守るものと失敗の条件

守るものはCIの実行内容、そこで扱う非公開source・credential、生成物と検査結果です。配布元の管理権限を奪った攻撃者、悪意ある配布者、タグの付け替え事故が原因になります。変更可能な参照が実際に実行され、そのjobの情報・権限や結果を利用できると、配布元の変更が利用側の実行権限へ届きます。

対象はworkflowが呼ぶ外部Action、外部reusable workflow、直接のcontainer Actionと、その変更を受け入れる経路です。同じrepositoryの参照は取得したsourceの信頼に依存し、外部参照の固定とは別に確認します。

## 満たすべきこと

| 特性 | 確認すること |
|---|---|
| WORKFLOW-REF-1 | 外部Actionと外部reusable workflowを、配布元と内容を確認した変更不能なcommitへ結ぶ。名前やrelease名だけで版を決めない |
| WORKFLOW-REF-2 | 直接のcontainer Actionを内容のdigestへ結ぶ。Gitのcommit固定でcontainerの取得先まで固定したと扱わない |
| WORKFLOW-REF-3 | 固定参照の変更を差分としてレビューする。更新先の出所・変更内容・jobの用途を確認し、脆弱な版へ固定したまま放置しない |
| WORKFLOW-REF-4 | 固定したコードの内側で取得・実行する依存を、確認した範囲と未確認範囲へ分ける。直接参照の検査結果から、この確認結果を推測しない |
| WORKFLOW-REF-5 | 変更の受入前に、必要な参照が検査対象へ入っていることを確認する。読めない入力・検査障害・未確認を「固定済み」に変えず、検査自体の変更と迂回にもレビューを要求する |

参照仕様と本PJの解釈は[Sources](../../../../sources/README.md#spec-workflow-dependency-references)へ記録します。製品固有の40桁SHA、`docker://`、検査の終了値は[実装例](../../../../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)を参照してください。

## 診断で確認する項目（異常時テスト）

以下はレビューや診断で使う項目です。実際の確認結果は別に残します。

| 試す条件 | できてはいけないこと・期待する扱い | 観測する場所 |
|---|---|---|
| タグ・branch・短いcommit参照へ変更する | 必要な外部参照が受入条件を通る | 変更差分、検査結果、merge条件 |
| 外部reusable workflowだけタグへ戻す | Actionの固定policyだけで全参照を確認済みにする | 呼出job、検査対象、provider設定 |
| container Actionを同名タグへ戻す | 内容が変更可能でもGit参照の検査成功で受け入れる | container参照、検査結果 |
| SHAは固定するが、内側で可変URLからscriptを取得する | 直接参照の成功を依存全体の安全性とする | 固定commitのsource、追加取得のreview |
| YAMLを壊す、入力を消す、検査を省略する | 未検査を成功としてmergeできる | error、対象一覧、required checkと迂回権限 |
| PR内で検査scriptやworkflowも書き換える | 無効化した検査の緑表示だけで受け入れる | 保護したreview経路、実際の受入ルール |

## 隣接するcontrolとの分担

固定はコードの無害性、全依存の固定、jobの権限削減を保証しません。[DEPS-004](../../dependency-security/psb-deps-004-dependency-change-review/README.md)は依存変更の採用判断、[DEPS-001](../../dependency-security/psb-deps-001-dependency-release-cooldown/README.md)は公開後の観測期間を扱います。[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)は未信頼PRと権限付き処理、[CICD-006](../psb-cicd-006-workload-federation-boundary/README.md)はcloud権限の発行条件を扱います。

[SOURCE-006](../../source-protection/psb-source-006-source-organization-security-posture/README.md)へ渡すのは、選んだ方針と必要対象・適用確認です。Jobに渡す権限と開始条件は[CICD-004](../psb-cicd-004-workflow-authority-minimization/README.md)へ渡します。[教材](learning.md)から固定後に残る取得経路を追い、[設計pattern](../../../../engineering/cicd-security/reviewed-workflow-dependency-binding/README.md)で検査の配置と更新方式を選べます。旧項目との関係は[移行判断](../../../../docs/WORKFLOW_DEPENDENCY_MIGRATION.md)にあります。
