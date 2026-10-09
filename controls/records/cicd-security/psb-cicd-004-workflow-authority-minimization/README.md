# PSB-CICD-004 Workflow authority minimization

**各jobは、必要な操作だけができる権限で動いているか。**

## なぜ必要か

例えば、テストだけをするjobに公開権限まで付いていると、そのjobで動くActionや依存が侵害されたとき、テスト結果だけでなく公開物も変えられます。権限の種類に加え、どの変更・イベントからそのjobを起動できるかも確認します。

## 満たすべきこと

1. **jobごとの権限を明示する。** 広い既定権限を暗黙に受け取らず、操作・対象・用途に必要な権限だけを渡す（JOB-AUTH-1・2）。信頼度や用途が違う処理を同じjobへまとめると、渡した権限を互いに使えることを考慮する。
2. **実際に使える権限を数える。** 標準tokenだけでなく、PAT、Appやcloudの認証情報、秘密情報、host・networkへの到達を確認する（JOB-AUTH-3）。OIDCなどのtoken発行は必要な交換jobへ限定し、交換先の許可条件とは分けて判断する（JOB-AUTH-4）。再利用workflowへ渡す権限と秘密情報、その先への委譲も確認する（JOB-AUTH-6）。
3. **開始条件と実適用を確かめる。** 強い権限を使うjobのrevision、イベント、承認条件を実際の保護設定へ結び付ける（JOB-AUTH-5）。対象jobの現在の付与と、必要な処理の成功・不要な操作の拒否を別々に確認し、取得失敗や古い設定を合格にしない（JOB-AUTH-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Jobの権限指定を消したとき、広い既定権限が復活しないか。
- 標準tokenがread-onlyでも、追加のPAT、App、cloud keyで書込みや公開ができないか。
- Secretを使うstepの前に動く未信頼コードが、共有状態を介して後続処理へ影響できないか。
- 未承認revisionや別イベントから、権限付きjobやtoken交換を起動できないか。
- 再利用workflowへ全secretや広い権限を渡していないか。設定取得の失敗を、最小権限の証拠にしていないか。

これらは診断・レビューの確認項目であり、実際のjobで試した結果ではありません。

## フレームワークとの関係

Jobに実際に渡る権限と、許す操作の対応について、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に個別の関係は登録していません。CICD-006などにある権限関連の関係を、このControlの全jobへ自動で継承しません。

## このコントロールの範囲

対象はjobへ渡す権限と、そのjobを起動できる条件です。外部コードの版は[CICD-001](../psb-cicd-001-workflow-dependency-identity/README.md)、未信頼PRの分離は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、cloud側のtoken交換条件と操作権限は[CICD-006](../psb-cicd-006-workload-federation-boundary/README.md)へ渡します。追加認証情報の発行・失効は[SOURCE-004](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)が扱います。

Jobの分け方と権限の渡し方は[engineering](../../../../engineering/cicd-security/purpose-bound-job-authority/README.md)を参照してください。[GitHub実装例](../../../../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)は限定した設定と確認手順を示します。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、[GitHub仕様](../../../../sources/README.md#spec-github-workflow-authority)、[本PJの解釈](../../../../sources/README.md#ref-workflow-authority-001)、旧項目との[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-authority-migration)へも辿れます。
