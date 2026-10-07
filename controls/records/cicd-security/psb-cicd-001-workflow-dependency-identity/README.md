# PSB-CICD-001 Workflow dependency identity

**CIで動く外部コードを、レビューした版に結び付けられるか。**

例えば、Workflowに書いたActionの`v1`タグが別のcommitへ移ると、利用側の変更差分がなくてもCIで動くコードが変わります。そのjobがソースや認証情報に触れられるなら、配布元の変更がその権限へ届きます。

## 満たすべきこと

1. **直接呼ぶコードを固定する。** 外部Actionとreusable workflowを、出所と内容を確認したcommitへ結び付ける（WORKFLOW-REF-1）。直接使うcontainer Actionは内容のdigestへ結び付ける（WORKFLOW-REF-2）。タグやrelease名だけでは内容を固定できない。
2. **更新と追加取得を見直す。** 固定した参照を変えるときは、差分、更新先の出所・内容、jobの用途をレビューする（WORKFLOW-REF-3）。固定したコードが内部で別のscriptや依存を取得する場合、その範囲と残る可変性を別に確認する（WORKFLOW-REF-4）。
3. **検査できなければ受け入れない。** 必要な参照が検査対象へ入るようにし、入力を読めない、検査が失敗する、検査を省く場合は固定済みと扱わない。検査自体の変更や迂回にもレビューを求める（WORKFLOW-REF-5）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 外部Actionやreusable workflowをタグ、branch、短いcommit参照へ戻しても受け入れられないか。
- Container Actionを変更可能なタグで指定しても、Git参照の検査成功だけで通らないか。
- 固定したコードが可変URLからscriptを取得するとき、直接参照の固定だけで全依存を確認済みと扱わないか。
- Workflowを壊す、対象を消す、検査を省く、検査scriptを書き換える場合に、未検査のまま受け入れられないか。

これらは確認項目であり、実際のCIやマージ条件で試した結果ではありません。

## このコントロールの範囲

対象はWorkflowが呼ぶ外部Action、reusable workflow、直接のcontainer Actionと、その変更の受入です。同じrepository内のコードはソースの信頼に依存します。参照の固定はコードの無害性やjob権限の制限を示しません。依存変更の採用は[DEPS-004](../../dependency-security/psb-deps-004-dependency-change-review/README.md)、未信頼PRとの分離は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、jobの権限は[CICD-004](../psb-cicd-004-workflow-authority-minimization/README.md)へ渡します。

固定方法と更新・検査の置き方は[engineering](../../../../engineering/cicd-security/reviewed-workflow-dependency-binding/README.md)で選びます。製品固有の参照形式は[実装例](../../../../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)にあります。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-workflow-dependency-references)、旧項目との[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-dependency-migration)へも辿れます。
