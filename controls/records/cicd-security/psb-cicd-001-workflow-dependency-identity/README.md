# PSB-CICD-001 Workflow dependency identity

**CIで動く外部コードを、レビューした版に結び付けられるか。**

## なぜ必要か

例えば、Workflowに書いたActionの`v1`タグが別のcommitへ移ると、利用側の変更差分がなくてもCIで動くコードが変わります。そのjobがソースや認証情報に触れられるなら、配布元の変更がその権限へ届きます。

## 満たすべきこと

1. **直接呼ぶコードを固定する。** 外部Actionとreusable workflowを、出所と内容を確認したcommitへ結び付ける（WORKFLOW-REF-1）。直接使うcontainer Actionは内容のdigestへ結び付ける（WORKFLOW-REF-2）。タグやrelease名だけでは内容を固定できない。
2. **更新と追加取得を見直す。** 固定した参照を変えるときは、差分、更新先の出所・内容、jobの用途をレビューする（WORKFLOW-REF-3）。固定したコードが内部で別のscriptや依存を取得する場合、その範囲と残る可変性を別に確認する（WORKFLOW-REF-4）。
3. **検査できなければ受け入れない。** 必要な参照が検査対象へ入るようにし、入力を読めない、検査が失敗する、検査を省く場合は固定済みと扱わない。検査自体の変更や迂回にもレビューを求める（WORKFLOW-REF-5）。

## 配置と受け渡し

```text
CICD-001
正規の配布元・意図した版・変更内容を確認
  → commit / image digestへ固定したworkflow変更
  → 直接参照の検査 ＋ 固定コード内の追加取得review
  → 保護された受入経路
  → 用途に必要な権限だけで実行
```

検査は参照の形式、reviewは選ぶ内容と追加取得、受入ルールは検査・reviewを飛ばさないことを担当します。外部Actionの内側や同じrepositoryのActionを調べた記録と、呼出元の参照検査結果を分けます。更新PRには配布元、旧版と新版、commit permalink、用途、読んだ範囲、残る取得経路と対応を残します。

固定した版に後から追加された保護は自動で入らないため、更新PRでは用途に必要な修正が選んだcommitへ含まれることも確認します。例えばGitHubの2026年の`actions/checkout`保護は、古い固定SHAへは遡って適用されません。SHAの形式検査だけで修正済みと判定せず、[公式の適用条件と版](../../../../sources/README.md#ref-cicd-2026-pwn-request-review)を照合します。

## 方式を選ぶ

| 方式 | 向く条件 | 代償と確認点 |
|---|---|---|
| 小さな自社scriptへ置き換える | 必要処理が短く、外部Actionの機能を多く使っていない | 自社で保守する。scriptのdownloadやpackage取得を新しい抜け道にしない |
| 外部Actionを固定し、更新PRを作る | 配布元の機能・保守を使いたい | SHA変更だけで承認しない。追加取得、出所、権限に応じたreviewが残る |
| レビューしたforkを維持する | 必要機能があり、上流の可変取得をそのまま許容できない | 更新追従と修正責任を持つ。forkという名前だけで信頼しない |
| Provider policyとrepository検査を組み合わせる | 複数repositoryへ同じ条件を適用したい | 対象・迂回・上書きを確認する。Provider policyの対象外を検査で補う |

[GitHub / Python実装](../../../../engineering/implementations/python-workflow-refs/README.md)は直接参照の小さな検査とpinactによる修正手順を示します。検査の対象は明示したworkflowです。Composite Action、jobのcontainer・service、remote workflow内部、scriptの取得経路は別の確認へ残すため、全依存を固定するscannerとして選ばないでください。

## 強制点と失敗経路

手元の検査は早く気付くために使い、merge条件の検査は独立した受入経路へ接続します。同じPRでscript、依存lock、workflow、担当者設定まで無効化できるなら、緑表示は受入条件になりません。必要なreviewをbranch保護・ruleset等で要求し、対象branch、管理者の迂回、check名の衝突も確認します。PRコードを検査するjobの権限は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)へ従います。

検査障害や読めないworkflowは固定済みにせず止めます。正当なworkflowに外部参照がない場合は、その対象を読めたことと参照数ゼロを明示できます。入力が空の状態とは区別します。対応しない構文はエラーにし、別の検査方式か、レビューした構文変更を選びます。

直接参照が固定されていても、内部で可変取得が見つかった時はjobの用途・権限を確認します。高権限の処理へ渡す前に取得内容を固定・検証する、処理を分離する、方式を変更する、[期限付き例外](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)を選ぶ、という判断を残します。内部を取得できなかった場合も、その欠落をreview結果へ残します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 外部Actionやreusable workflowをタグ、branch、短いcommit参照へ戻しても受け入れられないか。
- Container Actionを変更可能なタグで指定しても、Git参照の検査成功だけで通らないか。
- 固定したコードが可変URLからscriptを取得するとき、直接参照の固定だけで全依存を確認済みと扱わないか。
- Workflowを壊す、対象を消す、検査を省く、検査scriptを書き換える場合に、未検査のまま受け入れられないか。

これらは確認項目であり、実際のCIやマージ条件で試した結果ではありません。

## フレームワークとの関係

外部Actionなどの参照を実際に動く内容へ結び付ける問いについて、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に個別の関係は登録していません。GitHubの公式仕様と固定版の資料を設計入力として使いますが、特定の規格への準拠や全ての追加取得の確認を主張しません。

## このコントロールの範囲

対象はWorkflowが呼ぶ外部Action、reusable workflow、直接のcontainer Actionと、その変更の受入です。同じrepository内のコードはソースの信頼に依存します。参照の固定はコードの無害性やjob権限の制限を示しません。依存変更の採用は[DEPS-004](../../dependency-security/psb-deps-004-dependency-change-review/README.md)、未信頼PRとの分離は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、jobの権限は[CICD-004](../psb-cicd-004-workflow-authority-minimization/README.md)へ渡します。

製品固有の参照形式は[実装例](../../../../engineering/implementations/python-workflow-refs/README.md)にあります。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-workflow-dependency-references)、旧項目との[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-dependency-migration)へも辿れます。

工程をまたぐ判断は[PRの検証からリリース用ビルド・公開への引き渡しまで](../../../../engineering/pull-request-to-release-build.md)で確認できます。
