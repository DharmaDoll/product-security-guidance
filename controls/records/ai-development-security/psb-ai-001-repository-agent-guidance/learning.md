# 指示ファイルを変えるPRが、その後の修正を変える

**対応するcontrol:** [PSB-AI-001 Repository agent guidance](README.md)。未信頼の資料からの注入は[AI-003](../psb-ai-003-development-content-injection-boundary/README.md)、操作の実行許可は[AI-004](../psb-ai-004-development-agent-runtime-boundary/README.md)へ続きます。

あるrepositoryでは、agentへ「失敗したsecurity testを消して通さない」と指示しています。外部のcontributorが別の修正に紛れて指示ファイルを変更し、「緊急修正ではテスト停止を許す」と足しました。後日、開発者がagentに失敗したテストの修正を頼むと、agentはその指示を読み、テストを止める提案をします。攻撃者は後日の依頼を直接送っていません。持続する指示を変えたことが効きました。

ここで区別するのは、**ファイルの同一性**、**変更の承認**、**実際の効果**です。Hashを計算すれば変更を見つけられますが、攻撃者が内容とhash記録を一緒に変えられるなら承認の代わりになりません。別の人がdiff全体と意味をレビューし、agentが読むbranchへ入る前に止める必要があります。また、レビュー済みの指示でもagentが読まない、従わない、過剰に拒否する可能性があります。

「指示に禁止と書いたから実行できない」は誤りです。文章は作業を導くもので、scanner、filesystem、通信、公開の強制点ではありません。「旧benchmarkが改善を示したから今のagentでも有効」も誤りです。旧結果は合成データの比較であり、現在のmodelやtoolの動作ではありません。

評価するときは、同じ初期状態から「指示なし」と「指示あり」を試し、同じ課題と評価基準を使います。危険な提案が減ったか、元の修正ができたか、不要に作業を断ったかを別々に見ます。採点者自身の失敗や未実行を安全な結果に数えません。最終判断にはagentの実行記録だけでなく、変更diff、テスト結果、人による意味の確認が必要です。

[設計パターン](../../../../engineering/ai-development-security/repository-agent-guidance-review/README.md)に、変更レビューと比較評価をどう結び付けるか示します。
