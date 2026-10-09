# PSB-SOURCE-006 Source organization security posture

**ソース管理の共通設定は、必要なリポジトリと利用者に実際に効いているか。**

## なぜ必要か

例えば、新規リポジトリには秘密情報の検査を既定で有効にしていても、他の組織から移管したリポジトリには適用されていないことがあります。管理画面に方針が存在するだけでは、対象すべてが守られているとは分かりません。

## 満たすべきこと

1. **対象と方針を決める。** 組織内のリポジトリ、人、チーム、外部協力者、Appを把握し、認証、アクセス、作成・公開、CI、検査機能について必要な設定を決める（ORG-POSTURE-1〜2）。既定値と、変更を拒否する強制設定を区別する。
2. **現在の適用を確かめる。** 既存・新規・移管・再開したリポジトリを対象ごとに調べ、設定の適用漏れ、個別の上書き、不要な権限を見つける（ORG-POSTURE-3〜4）。ログイン基盤で人を無効にしたことを、ソース管理側の権限が消えた証拠にしない。
3. **変更と確認漏れを追う。** 変更記録と現在の状態を照合し、対象の不足、古い結果、取得・通知の障害を「問題なし」にしない。差分や障害は期限・限定した例外とともに担当者へ渡し、修正後の実際の状態を再確認する（ORG-POSTURE-5〜7）。

## 診断で確認する項目（異常時テスト）

- 新規作成だけでなく、既存・移管・再開したリポジトリにも共通設定が効いているか。個別の上書きや解除に気付けるか。
- 設定の既定値を権限の上限と誤認していないか。管理者やAppが変更・迂回できる範囲を把握しているか。
- 退職者や用途不明のチーム・App・外部協力者の権限、方針変更前からあるtokenや承認が残っていないか。
- 一覧の一部しか取得できない、確認用IDに権限がない、監査や通知が止まった場合に、全件確認済みとしていないか。
- 通知や修正ticketを閉じただけで完了とせず、対象の設定と権限を読み直しているか。

これらは確認項目であり、実際の組織設定や拒否を確かめた結果ではありません。

## フレームワークとの関係

組織設定が各リポジトリへ実際に効くかという問いについて、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に個別の関係は登録していません。GitHubの公式設定資料は具体的な判断材料ですが、設定画面を確認しただけで規格への準拠や全対象への適用を主張しません。

## このコントロールの範囲

対象は、ソース管理組織が選んだ共通方針と、リポジトリ・利用者・Appごとの実際の状態です。確認できない範囲を良好としませんが、収集の障害だけで全開発アクセスを自動停止する要件でもありません。組織設定の確認は、秘密情報の検出[SOURCE-002](../psb-source-002-secret-publication-boundary/README.md)、ソース管理用の認証情報の失効[SOURCE-004](../psb-source-004-source-access-credential-lifecycle/README.md)、CIの実際のjob権限[CICD-004](../../cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)を代替しません。

手作業と自動収集の選び方は[engineering](../../../../engineering/source-protection/organization-baseline-and-drift-review/README.md)、GitHubで現在の設定を読む方法は[手順](../../../../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)を参照してください。[教材](learning.md)、７つの特性と参照資料IDを残した[control.yaml](control.yaml)、資料の採否を示す[Sources](../../../../sources/README.md#ref-source-organization-posture-001)、旧項目の[移行記録](../../../../docs/MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)へも辿れます。
