# Repository agent guidanceの移行判断

旧[`PSB-AI-001`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/repository-owned-ai-security-guidance/control.yaml)を、開発agentが読むrepository所有の指示と、その開発作業への影響に絞りました。固定した移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。製品が顧客へ提供するAI機能の設計、RAG、AI製品のTEVVは[ai-security-foundryとの分担](SECURITY_SCOPE.md)に従い対象外です。

| 旧項目 | 残す判断と移行先 |
|---|---|
| AIG-001 | [DEV-GUIDE-1〜2](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)：実際に読む指示の場所・版と変更の独立レビュー。4ファイル・単一bundle digestを普遍要件にしない |
| AIG-002 | DEV-GUIDE-2〜3：指示に保護策を弱める意味を混ぜない。Hashと自己申告のsemantic reviewを承認の代わりにしない。実行時の拒否は[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) |
| AIG-003〜005 | DEV-GUIDE-4：同条件で指示の効果を比較し、安全上の逸脱、作業の達成、過剰拒否を分ける。旧4課題×2回、改善20ポイント、false block 15%等はfixture固有の値 |
| AIG-006〜007 | DEV-GUIDE-5：run・scorer・証拠の不足とlive未実施を成功へ変えない。生の秘密・prompt・出力を公開repositoryへ置かない |

旧`secure/benchmark/`の初期状態hashは実repositoryのsnapshotではなく合成識別子です。`guided-results.json`と`baseline-results.json`はagentを起動せずに用意した結果で、旧verifierはその整合と集計を検査します。62.50%→93.75%という値は、現在のagentや指示の効果ではありません。旧CodeGuard profileもrepository所有の例であり、外部製品の動作や利用中の設定を示しません。旧実験prompt、結果JSON、verifierは本PJの実装・評価へコピーしません。

必要な成果物は[control](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)、control配下の教材、[設計パターン](../engineering/ai-development-security/repository-agent-guidance-review/README.md)、診断観点、技術経路が明確な[GitHubの変更レビュー例](../engineering/ai-development-security/repository-agent-guidance-review/implementations/github-codeowners/README.md)です。GitHub例はCODEOWNERSとbranch保護の接続を示しますが、レビュー担当者・保護branch・bypass・実GitHubの拒否結果は未設定・未確認です。したがって具体実装の設計はあり、採用先での動作確認は残作業です。開発agent比較の実装はagent・版、作業群、実行権限、観測元を選んだ時に限定して作ります。

旧framework mappingのATLAS `AML.T0081`、`AML.CS0041`、Agentic Top 10 `ASI04`は、変更の脅威との関連を示しますが、今回のGitHub設定や実agent効果の確認ではありません。旧`detects`・`mitigates`の確度をそのまま継承せず、新しいframework mappingは追加しません。版と採否は[参照資料](../sources/README.md#ref-development-guidance-001)に保持します。

旧資料ID `REF-AI-001`のClaude Code固有部分は製品採用時の参考にとどめ、`REF-AI-002`の一般的なagent guidanceは開発環境に当たる部分だけ新しい資料記録へ統合しました。旧IDを新しい成果物の別名として残しません。
