# ENG-CICD-005: Purpose-bound job authority

必要な処理を、必要な権限と承認条件へ結び付けます。CI設計者が、**jobを分ける場所、認証情報を渡す場所、開始を制限する場所**を選ぶpatternです。対応する要件は[PSB-CICD-004](../../../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)です。

## 操作から構成を決める

最初にjobごとに、操作する対象、必要なAPIや通信、取得・実行するコード、認証情報と権限を書き出します。不要な権限を減らし、残した権限をどのコードへ共有するかを決めます。

```text
権限を持たない検証・build
  → 内容と信頼を確認した受け渡し
  → 承認したrevision・イベント・環境の開始条件
  → 必要なjobだけへ限定したtoken・secret・発行許可
  → 対象を限定した公開・deploy等の操作
```

Job内のstep名やsecretの引数指定だけで、実行状態を隔離したとは扱いません。分けたjob間のartifact・cache・outputも、実行コードへ昇格させる前に確認します。[Untrusted PR boundary](../untrusted-pr-boundary/README.md)がこの受け渡しを所有します。

## 選択肢と代償

| 構成 | 向く条件と代償 |
|---|---|
| Jobの権限を明示して必要項目だけ追加 | 同じ信頼・用途の処理をまとめたい。Job内の全コードが持つ操作範囲を確認する |
| Build・report・release・cloud交換を分ける | 操作や扱う情報、信頼度が違う。実行時間と受け渡しの設計が増えるが、権限の共有を切りやすい |
| 共通workflowへ処理を委譲する | 同じ用途の設定を一か所で保守したい。呼出元の権限・secret、固定した呼出先、内部の環境とさらに先の委譲を確認する |
| 別repository・別runnerで公開する | 権限や管理主体を強く分けたい。独立した入力確認、認証、更新・運用責任が必要になる |

分割数を増やすこと自体は成果ではありません。不要な共有を切り、必要な入力と操作だけを渡せる構成を選びます。実行中のhost・network権限は[CI state and runner lifecycle](../ci-state-and-runner-lifecycle/README.md)と[Build execution boundary](../../build-security/build-execution-boundary/README.md)へ戻します。

## 強制点を分ける

| 判断 | 強制する場所・確認先 |
|---|---|
| 標準tokenでできる操作 | Providerのtoken権限とjob設定。追加PAT・App・cloud権限を同じ制限とみなさない |
| Secretを渡す対象 | Secret管理とjobへの配送。共有状態の書換え経路も確認する |
| Tokenを発行してよいjob | Jobの発行許可。交換先の対象・操作は[Workload federation boundary](../workload-federation-boundary/README.md)で制限する |
| 実行を開始できる条件 | 保護されたsourceの変更経路、イベント、環境・承認、迂回権限。名前だけを条件にしない |
| 設定の変更を受け入れる条件 | Workflow・呼出元・共通workflow・環境設定のレビューと変更管理。検査を消しても通る経路を残さない |

組織の既定値は初期条件で、すべてのjobの最大権限とは限りません。[Organization baseline and drift review](../../source-protection/organization-baseline-and-drift-review/README.md)へ必要な方針と対象を渡し、実行側で付与された権限も確認します。

## 失敗時の判断

正当な処理が権限不足で失敗したら、失敗した操作・対象・必要な権限を調べます。原因不明のまま全権限や共通PATへ置き換えません。必要な追加は用途と対象を示す変更としてレビューします。

検査が成功しても、不要な権限の最小性や現在のprovider設定を自動では証明できません。設定一覧、必要な処理の成功、禁止した文脈の拒否、未確認・障害を分けます。環境の誤記・削除、承認の迂回、委譲先の変更は、それぞれ実値と実行条件を見直します。

[GitHubの設定・smoke test例](implementations/github/README.md)では、読取り専用のsource確認と、権限を付けずに環境の待機・拒否を確認する方式を選びます。SaaSの設定を合成JSONで良好と判定するscriptは作りません。Source、secret、権限、保護branch・環境を選ぶレビューが必要な主題であり、記述量やscannerの検出数で完了にしません。

主にplatform and infrastructure、攻撃段階5・6のjob権限と開始条件を扱います。段階2の変更保護を受け、段階7の実行隔離、段階9・10の限定した公開・deploy、段階12の失効・調査へ渡します。参照仕様・採否は[Sources](../../../sources/README.md#spec-github-workflow-authority)、旧項目と実装の扱いは[移行判断](../../../docs/WORKFLOW_AUTHORITY_MIGRATION.md)にあります。
