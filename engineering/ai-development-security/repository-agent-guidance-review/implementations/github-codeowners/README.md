# GitHubの指示ファイル変更レビュー

この構成は、GitHub.comの保護されたbranchへcoding agent用の指示ファイルを入れる前に、指定した所有者のレビューを要求する例です。`CODEOWNERS`だけではmergeを止められません。Branch protectionまたはrulesetで、PRとcode ownerの承認を必須にします。GitHub公開文書を2026-09-26に確認しました。実GitHubでの有効化・拒否試験は本PJではまだ行っていません。

## 対象と変更箇所

- 対象: GitHub.comのrepository、保護するbase branch、そこで実際に使うagent指示ファイル。GitHub Enterprise Serverや他ホストの挙動は対象外です。
- 追加するファイル: base branchの`.github/CODEOWNERS`。このディレクトリの[例](CODEOWNERS.example)から、存在する指示pathだけを選び、`@REVIEWER`を書込み権限のある実在アカウントへ置き換えます。追加の指示ファイルや指示を読み込む設定も所有対象へ足します。
- GitHub側の変更: 対象branchに「PR必須」「code ownerレビュー必須」を有効化。承認後の変更に再レビューを要求し、直接push・bypassを許す主体を確認します。設定する権限がない場合はrepository管理者が行います。

GitHubの[CODEOWNERS仕様](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)では、PRのbase branch側にファイルが必要で、所有者には書込み権限が必要です。複数所有者を一行に書いた場合は誰か一人の承認で足ります。独立した承認者が必要なら、そのアカウントの選択と権限も運用で確認します。[Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)と[ruleset](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)はbypassや承認後の更新に選択肢があるため、画面に「有効」と表示されるだけで経路全体を判定しません。

## 使い捨てrepositoryでの最短確認

1. 自分が管理する使い捨てGitHub repositoryを作り、base branchに無害な`AGENTS.md`と、所有者を実在する別アカウントへ置き換えた`.github/CODEOWNERS`を入れます。指示本文に秘密情報を入れません。
2. Repositoryの`Settings → Rules → Rulesets`からbase branchを対象とする有効なbranch rulesetを作り、「Require a pull request before merging」と「Require review from Code Owners」を選びます。承認後の新しいpushで再承認が必要になる設定も選びます。通常作業者・bot・管理者のbypass一覧を記録します。既存のbranch protectionを使う場合も同じ効果の項目を設定します。
3. 所有者以外の作業者から、`AGENTS.md`に無害な一行を足すPRを出します。所有者の承認前にmergeできず、承認後にmerge可能になることをGitHub上で確認します。この時点ではまだmergeしません。
4. 承認後、同じPRへもう一行足します。再レビューが必要かを確認します。再承認後にmergeします。可能なら直接pushやbypass主体からの更新も、想定した制限と一致するか確かめます。設定や権限の制約で試せない経路は`NOT_CHECKED`とします。
5. `.github/CODEOWNERS`自身の変更PRでも同じ所有者の承認を要求するか確認します。使い捨てrepositoryで一覧にない仮の指示pathを追加し、code ownerレビューの対象にならない失敗を観測します。そのpathをCODEOWNERSへ加えた後、対象になることを再確認します。

期待するのは、対象ファイルの未承認変更が保護branchへ入らないことです。指示の意味が安全か、agentがその版を実際に読むか、指示がagentの挙動を改善するかは、この設定の効果ではありません。これらは[設計パターン](../../README.md)に従って別に確認します。

## 解除と限界

使い捨てrepositoryでは、試験後に設定したbranch保護と例示のCODEOWNERSを解除し、repositoryを管理者の手順で片付けます。既存repositoryで外す場合は、レビューが不要になる影響を確認してから管理者が変更します。

この例はGitHub UIの設定手順とCODEOWNERSの対象pathを示すもので、実際の強制結果は未観測です。`@REVIEWER`のままでは有効な構成になりません。Base branchにCODEOWNERSがない、所有者に書込み権限がない、指示ファイルが一覧にない、保護ルールにbypassがある場合は、主張する拒否経路が成立しない可能性があります。実際に読んだ指示と操作権限の検査も別です。[Control](../../../../../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)へ戻って判断します。
