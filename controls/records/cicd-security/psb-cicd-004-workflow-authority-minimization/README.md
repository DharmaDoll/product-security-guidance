# PSB-CICD-004 Workflow authority minimization

**各jobは、必要な操作だけができる権限で動いているか。**

## なぜ必要か

例えば、テストだけをするjobに公開権限まで付いていると、そのjobで動くActionや依存が侵害されたとき、テスト結果だけでなく公開物も変えられます。権限の種類に加え、どの変更・イベントからそのjobを起動できるかも確認します。

## 満たすべきこと

1. **jobごとの権限を明示する。** 広い既定権限を暗黙に受け取らず、操作・対象・用途に必要な権限だけを渡す（JOB-AUTH-1・2）。信頼度や用途が違う処理を同じjobへまとめると、渡した権限を互いに使えることを考慮する。
2. **実際に使える権限を数える。** 標準tokenだけでなく、PAT、Appやcloudの認証情報、秘密情報、host・networkへの到達を確認する（JOB-AUTH-3）。OIDCなどのtoken発行は必要な交換jobへ限定し、交換先の許可条件とは分けて判断する（JOB-AUTH-4）。再利用workflowへ渡す権限と秘密情報、その先への委譲も確認する（JOB-AUTH-6）。
3. **開始条件と実適用を確かめる。** 強い権限を使うjobのrevision、イベント、承認条件を実際の保護設定へ結び付ける（JOB-AUTH-5）。対象jobの現在の付与と、必要な処理の成功・不要な操作の拒否を別々に確認し、取得失敗や古い設定を合格にしない（JOB-AUTH-7）。

## 操作から構成を決める

最初にjobごとに、操作する対象、必要なAPIや通信、取得・実行するコード、認証情報と権限を書き出します。不要な権限を減らし、残した権限をどのコードへ共有するかを決めます。

```text
CICD-004
権限を持たない検証・build
  → 内容と信頼を確認した受け渡し
  → 承認したrevision・イベント・環境の開始条件
  → 必要なjobだけへ限定したtoken・secret・発行許可
  → 対象を限定した公開・deploy等の操作
```

Job内のstep名やsecretの引数指定だけで、実行状態を隔離したとは扱いません。分けたjob間のartifact・cache・outputも、実行コードへ昇格させる前に確認します。[Untrusted PR boundary](../psb-cicd-005-untrusted-pr-boundary/README.md)がこの受け渡しを所有します。

## 選択肢と代償

| 構成 | 向く条件と代償 |
|---|---|
| Jobの権限を明示して必要項目だけ追加 | 同じ信頼・用途の処理をまとめたい。Job内の全コードが持つ操作範囲を確認する |
| Build・report・release・cloud交換を分ける | 操作や扱う情報、信頼度が違う。実行時間と受け渡しの設計が増えるが、権限の共有を切りやすい |
| 共通workflowへ処理を委譲する | 同じ用途の設定を一か所で保守したい。呼出元の権限・secret、固定した呼出先、内部の環境とさらに先の委譲を確認する |
| 別repository・別runnerで公開する | 権限や管理主体を強く分けたい。独立した入力確認、認証、更新・運用責任が必要になる |

分割数を増やすこと自体は成果ではありません。不要な共有を切り、必要な入力と操作だけを渡せる構成を選びます。実行中のhost・network権限は[CI state and runner lifecycle](../../../../engineering/ci-state-and-runner-lifecycle.md)と[Build execution boundary](../../build-security/psb-build-001-build-containment/README.md)へ戻します。

## 強制点を分ける

| 判断 | 強制する場所・確認先 |
|---|---|
| 標準tokenでできる操作 | Providerのtoken権限とjob設定。追加PAT・App・cloud権限を同じ制限とみなさない |
| Secretを渡す対象 | Secret管理とjobへの配送。共有状態の書換え経路も確認する |
| Tokenを発行してよいjob | Jobの発行許可。交換先の対象・操作は[Workload federation boundary](../psb-cicd-006-workload-federation-boundary/README.md)で制限する |
| 実行を開始できる条件 | 保護されたsourceの変更経路、イベント、環境・承認、迂回権限。名前だけを条件にしない |
| 設定の変更を受け入れる条件 | Workflow・呼出元・共通workflow・環境設定のレビューと変更管理。検査を消しても通る経路を残さない |

組織の既定値は初期条件で、すべてのjobの最大権限とは限りません。[Organization baseline and drift review](../../source-protection/psb-source-006-source-organization-security-posture/README.md)へ必要な方針と対象を渡し、実行側で付与された権限も確認します。

## 失敗時の判断

正当な処理が権限不足で失敗したら、失敗した操作・対象・必要な権限を調べます。原因不明のまま全権限や共通PATへ置き換えません。必要な追加は用途と対象を示す変更としてレビューします。

検査が成功しても、不要な権限の最小性や現在のprovider設定を自動では証明できません。設定一覧、必要な処理の成功、禁止した文脈の拒否、未確認・障害を分けます。環境の誤記・削除、承認の迂回、委譲先の変更は、それぞれ実値と実行条件を見直します。

[GitHubの設定・smoke test例](../../../../engineering/implementations/github-job-authority/README.md)では、読取り専用のsource確認と、権限を付けずに環境の待機・拒否を確認する方式を選びます。SaaSの設定を合成JSONで良好と判定するscriptは作りません。Source、secret、権限、保護branch・環境を選ぶレビューが必要な主題であり、記述量やscannerの検出数で完了にしません。

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

[GitHub実装例](../../../../engineering/implementations/github-job-authority/README.md)は限定した設定と確認手順を示します。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、[GitHub仕様](../../../../sources/README.md#spec-github-workflow-authority)、[本PJの解釈](../../../../sources/README.md#ref-workflow-authority-001)、旧項目との[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-authority-migration)へも辿れます。

工程をまたぐ判断は[PRの検証からリリース用ビルド・公開への引き渡しまで](../../../../engineering/pull-request-to-release-build.md)で確認できます。
