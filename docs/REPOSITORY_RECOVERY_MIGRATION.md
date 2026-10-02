# Repository recovery independenceの移行判断

旧[PSB-SOURCE-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/control.yaml)を、重要なソースの破壊権限、独立した保管世代、実際の復旧と開発再開へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-26です。

| 旧項目 | 行き先・採否 |
|---|---|
| RDR-001 | [RECOVERY-1](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)：製品の必要対象、固定ID、owner、RPO・RTO。GitHubの数値IDと全page取得は製品固有の選択であり、全providerの要件にしない |
| RDR-002 | RECOVERY-2と[設計pattern](../engineering/source-protection/independent-repository-backup-and-restore/README.md)：repository削除・移管とref保護、制限の変更・bypassを分ける。GitHubの設定を全providerへコピーしない |
| RDR-003 | RECOVERY-3〜4：保管世代を破壊できる権限、鍵と復旧用ID、保持、取得の鮮度。別accountやObject Lock COMPLIANCEという製品選択を唯一の実現方法にしない |
| RDR-006 | RECOVERY-5〜6：隔離した実復元、ref・内容・外部データの照合、設定、修正・build、開発再開までの時間。旧四半期を全組織の確認間隔にしない |

旧controlにRDR-004〜005は存在しません。欠番を補完しません。旧[secure runbook](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/secure/README.md)の一律checklistは、そのまま正本にせず、選ぶ対象・権限・復元方法・確認結果を説明する設計へ分けました。組織の導入状況は移行しません。

## 具体化判断と旧テストの扱い

必要な成果物はcontrol、control配下の教材、設計pattern、診断観点です。Gitの取得と復元は技術経路が明確なため、[Git mirror実装例](../engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror/README.md)も完成条件に含めました。独自のbackupサービスやJSON判定器は作らず、Git標準コマンドによる最短手順、smoke test、解除方法を示します。

旧[tests/test.sh](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/tests/test.sh)は実際に使い捨てrepositoryを作り、mirror、元の削除、branches・tagsのpush、ref照合、不完全復元の検出を確認します。合成JSONの自己申告ではなく、この実観測の価値を移しました。

新しい例は、新世代へのmirror取得と新しいbare repositoryへの復元に限定します。ローカル元とのobject共有を避け、annotated tagのobject IDも照合し、元の接続設定を外します。練習用の元repositoryは削除せず別名へ移し、元の場所への依存がないことを確認します。七件の実Gitテストは元の不在、タグ欠落、同名タグの指す先変更、object破損、既存復元先、shallow source、取得中のref変更を観測します。

実装から設計へ戻した判断は、`fsck`成功と必要対象の充足は別、ref名だけでは不足、取得中の変更を成功にしない、更新用mirrorと保持世代を分ける、コピー元との接続を残さない、という点です。取得時のref一覧も取得前から消えた対象を知らないため、製品の必要対象との照合を別に残しました。

2026-09-30の読み合わせでは、攻撃者が内容を書き換えた後に取得した世代も、`fsck`と取得時のref一覧との比較に成功し得ることを明示しました。採用する世代は変更経緯と独立した判断材料から選び、判断できなければ復旧成功にしません。NIST SP 800-61 Rev.3の復旧用資産・復元後の資産を確認する考え方を[Sources](../sources/README.md#ref-repository-recovery-001)へ追加しました。Git例の七テストは整合性と復元経路の確認であり、侵害前の世代を識別する試験ではありません。

この限定例の完了は組織への導入や開発再開の確認ではありません。Live GitHubの拒否、独立したcloud account・鍵・保持lock、LFS、metadata、設定復元、製品の修正・build、RPO・RTO、通知は未確認です。Provider・保管先・必要データ・復元先・許可された確認方法が選べたときに、対応する実装・評価へ戻ります。

## 参照と旧framework関係

直接の資料は[REF-REPOSITORY-RECOVERY-001](../sources/README.md#ref-repository-recovery-001)、Git実装の仕様は[REF-GIT-MIRROR-RECOVERY-001](../sources/README.md#ref-git-mirror-recovery-001)へ分けました。GitHubのarchive取得とrestore対応を同一視せず、Object Lockの保護対象versionとdelete marker、保持modeの迂回権限を区別します。旧資料の固定確認間隔、保持mode、provider内の削除後復元への依存を共通要件へ移しません。

旧framework mappingはSITF `1.0.0@d1d1536 / T-V009`の`mitigates / high`、MITRE ATT&CK `v19.1 / T1485`の`mitigates / medium`でした。旧日付は2026-08-25で、前者はRDR-001・002・003・006、後者はRDR-002・003・006へ割り当てられていました。攻撃行動との概念上の関係は残りますが、今回その固定版の本文との項目別再照合は行っていないため新しいframework mappingへ継承しません。ローカルGit復元の成功から、組織の大量削除対策や導入済みを主張しません。Framework mappingは116件のままです。
