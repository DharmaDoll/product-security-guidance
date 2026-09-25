# The reviewed plan is not always the change that runs

## シナリオ

Application teamはTerraformの変更をpull requestへ出しました。CIはplanを表示し、暗号化とprivate networkのpolicy checkも通過しました。Reviewerはその表示を見て承認します。

Merge後のapply jobは保存したplanを使わず、設定から新しいplanを作りました。その間にremote moduleのversion解決とproduction variableが変わり、providerがapply時に決めるpublic endpointもpolicy inputではunknownでした。Apply jobは広いcloud権限を持っていたため、そのまま作成できました。

後日、運用者はconsoleから一時的にnetworkを公開しました。Drift checkはTerraform stateにある一部resourceだけを古いcredentialで取得し、権限不足を「差分なし」と表示しました。Pull requestのplan checkは成功していましたが、reviewした変更、実行した変更、現在の状態は一致していませんでした。

## どこで境界が切れたか

この流れには少なくとも五つの異なる対象があります。

1. 人がreviewしたsourceと依存・入力
2. Toolが解決した実行計画
3. Policyが評価した入力と判断
4. Apply identityがproviderへ実行した操作
5. Providerに現在存在するresourceと設定

同じpull requestやrun IDが付いていても、内容が自動的に同じになるわけではありません。各境界で、前の対象と次の対象を結ぶidentityと、結べなかった時の停止が必要です。

## 用語

- **Desired state**：Source、module、入力、policy等で表した期待状態。実resourceの現在状態とは分ける。
- **Speculative plan**：変更のpreviewに使うplan。後でそのままapplyする意図を持つ保存planとは役割が異なる。
- **Saved executable plan**：後からapplyへ渡せるplan artifact。設定、入力、planned value等を含み得るため機微情報として扱う。
- **Unknown value**：Plan時点では確定せず、apply時にprovider等が決める値。`null`や「存在しない」と同じではない。
- **Drift**：承認済みのdesired state、IaC state、provider上の実resourceの間にある差。正当な緊急変更、侵害、collector failureを同じ原因として扱わない。
- **Golden Path**：安全な既定値、標準module、workflowを使いやすい入口として提供する設計。利用した事実だけで実効状態を証明しない。

## 悪用・失敗経路を分解する

1. Contributorまたは侵害されたdependencyがsource、module、provider、variable、policyのどれかを変える。
2. Review対象とは異なる入力でplanが解決される。
3. Policyはcreateの一部だけを見る、unknownをallowする、または失敗をcleanにする。
4. Approvalが表示用planやcommitにだけ付き、実行可能planへ結び付かない。
5. Apply jobが再planし、広いidentityで別targetまたは追加操作を実行する。
6. Console、API、別toolによる変更がCIの外で行われる。
7. Drift観測のscope・権限・freshnessが不足し、現在状態の差を見落とす。
8. 自動修正が影響を判断せず実行され、availabilityや調査証拠を損なう。

## よくある誤解

### 「承認済みmoduleを使えば安全」

Moduleは安全な既定値と狭いinterfaceを提供できます。一方で、version解決、override、provider default、組合せ、resource固有要件、moduleを通らない変更経路は別に確認します。

### 「`.terraform.lock.hcl`がmoduleとproviderを全部固定する」

Terraformのdependency lock fileが現在追跡するのはproviderです。Remote moduleはexact version constraint等を別に設計します。Lock fileがあっても、最初に選んだproviderの信頼判断やmodule sourceの内容まで自動的に保証しません。

### 「Plan policyがpassしたのでapply後も安全」

Plan時にunknownな値、providerが決める値、別経路の変更、apply後のdriftは残ります。Plan policyが判断できる範囲を示し、最終強制点と実状態の観測へ渡します。

### 「Apply前にもう一度planすれば新しい状態へ追随できる」

新しいplanは必要な場合がありますが、その時は新しいreview対象です。以前のplanをreviewして得た承認を、別の再planへそのまま使いません。

### 「Driftがあれば自動的に元へ戻せばよい」

差分には正当なincident対応、外部serviceの変更、import漏れ、collector errorも含まれます。削除、遮断、key変更等は復旧不能や証拠消失を起こすため、新しい変更として影響とrollbackを判断します。

## 判断基準

- Reviewしたsource、module、provider、variable、policy、targetは何で識別するか。
- Policyはどのresource actionと値を見て、unknown・未対応・errorをどう区別するか。
- Reviewerの判断をどの保存planへ結び付け、誰が差替えできないようにするか。
- Apply identityはどのtargetでどの操作だけを、どの期間実行できるか。
- Console、API、別tool、emergency pathをどこで拒否または観測するか。
- Provider上の全対象resourceと収集healthを何で確認し、未管理・未取得・staleをどう示すか。
- Driftや例外を誰がいつまでに判断し、どの修正を自動化してよいか。

次に[control](README.md)で必要な特性を確認し、[pattern](../../../../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)で実装へ落とす境界を選びます。
