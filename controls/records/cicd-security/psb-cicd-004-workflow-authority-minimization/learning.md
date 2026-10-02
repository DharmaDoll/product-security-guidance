# read-onlyのテストjobから、なぜ公開物を書き換えられるのか

対象は[PSB-CICD-004 Workflow authority minimization](README.md)、設計の行き先は[Purpose-bound job authority](../../../../engineering/cicd-security/purpose-bound-job-authority/README.md)です。

## テストと公開を一つにしたチーム

あるチームは、コードのcheckout、依存のinstall、テスト、release作成を一つのjobへ入れています。Release作成に必要な書込み権限を付けると、同じjobで動くActionやshellも、そのjobのtoken権限を使える状態になります。依存の実行コードが侵害されれば、本来テストするコードが公開処理の権限へ届きます。

対策としてテストjobを`contents: read`へ変えたものの、release用PATをそのjobへ渡したままだったとします。PATは別の認証情報です。`GITHUB_TOKEN`がread-onlyでも、PATで許される操作は残ります。読み取り専用という表示が、job全体の書込み不能を意味するわけではありません。

## 権限を「何ができるか」で読む

GitHub Actionsの`permissions`は、そのjobの`GITHUB_TOKEN`の操作範囲とOIDC tokenの発行許可を指定します。Workflow全体の`permissions: {}`から始め、各jobへ必要な項目を追加すると、何のために増やしたかが見えます。ただしtokenの存在自体や、PAT・App・cloud key、runnerに保存したcredentialを消す設定ではありません。

例えば「sourceを取得する」は`contents: read`、「GitHub Releaseを作る」は`contents: write`という異なる操作です。前者へ後者の権限をまとめて渡す必要はありません。失敗したAPIを調べず`write-all`へ広げると、元の処理とは無関係な権限まで増えます。

OIDCの`id-token: write`はrepositoryの書込みではなく、tokenを求める許可です。交換先が受け入れればcloud権限へつながるので、不要なテストjobには渡しません。発行できることと、交換先でどこへ何ができるかは[CICD-006](../psb-cicd-006-workload-federation-boundary/learning.md)で別に追います。

## Jobを分けた後にも残る問い

テストと公開を別jobへ分けても、公開jobがテスト側のscript・cache・workspaceをそのまま実行すれば、未信頼側が公開処理を操作する経路が残ります。処理の分割と、渡す状態の判断を一緒に行います。その詳細は[CICD-005の教材](../psb-cicd-005-untrusted-pr-boundary/learning.md)へ渡します。

Stepの`env`へsecretを限定するのは不要な配送を減らしますが、同じjob内の信頼度が違うコードを隔離する壁にはなりません。先に動いたコードが共有ファイルや後続処理を変更できる条件があれば、後のsecret利用へ影響できます。重要な分割はstepの名前ではなく、実行状態と権限の共有を切れる場所で行います。

## 「mainだから」「環境名があるから」の落とし穴

`main`への条件は実行対象を絞りますが、mainへ誰でも書けるなら承認済みとは言えません。Branchの変更経路、必要なレビュー、管理者の迂回を確認します。

GitHubでは、存在しないEnvironment名をworkflowへ書くと、新しい環境が作られることがあります。名前を`release`と書いただけでは承認待ちになりません。先に環境を作り、承認者、許すbranch・tag、自分の実行への承認、管理者の迂回を設定してから、その**同じ名前**を参照します。

再利用workflowでも、呼出先は渡された`GITHUB_TOKEN`権限を増やせませんが、呼出元が広く渡してよい理由にはなりません。必要な権限とsecretを呼出元で絞り、呼出先のjobと環境も確認します。

最終的な判断は、「処理に必要な操作」「実際に届く認証情報と環境」「その処理を開始できる条件」の三つを合わせて行います。[GitHub実装例](../../../../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)で無権限・読取り専用のjobと環境の待機・拒否を確認できる手順へ戻り、[Sources](../../../../sources/README.md#spec-github-workflow-authority)から製品仕様の確認日と限界をたどれます。
