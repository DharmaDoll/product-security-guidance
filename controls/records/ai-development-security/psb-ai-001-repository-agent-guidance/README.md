# PSB-AI-001 Repository agent guidance

## このcontrolを一枚で理解する

Coding agentに「失敗したセキュリティテストを無効化して通すな」と教える指示ファイルは便利です。しかし同じファイルへ「今回だけ無効化してよい」を混ぜられたら、以後の作業を継続して誤らせます。本controlの問いは、**実際に読まれる指示を誰が変更でき、その指示が安全な作業を助けていると何で判断するか**です。

対象は開発端末・IDE・CLI・repository・CIのcoding agentに与えるrepository所有の指示です。悪意あるcontributor、未信頼PR、誤ったレビュー、評価の欠落を想定します。外部のSkill・MCP・pluginの採用は[AI-002](../psb-ai-002-agent-extension-dependency-governance/README.md)、読んだIssue等の間接注入は[AI-003](../psb-ai-003-development-content-injection-boundary/README.md)、ファイルや通信の実行時制限は[AI-004](../psb-ai-004-development-agent-runtime-boundary/README.md)が扱います。[製品自体のAI機能](../../../../docs/SECURITY_SCOPE.md)は対象外です。

## 必要なセキュリティ特性

| ID | 満たすべき状態 |
|---|---|
| DEV-GUIDE-1 | Agentごとに読み込む指示の場所・版・範囲を特定し、レビュー対象と実際の読み込みを照合する。 |
| DEV-GUIDE-2 | 指示の変更を別の責任者が意味までレビューし、agent自身や未信頼PRの自己承認を認めない。 |
| DEV-GUIDE-3 | 指示は管理方針、操作認可、scanner結果を上書きしない。文章で「許可」と書いても権限は増えない。 |
| DEV-GUIDE-4 | 同じ開発課題・初期状態・評価方法で指示の有無を比べ、危険な提案と作業の達成・過剰拒否を別に見る。 |
| DEV-GUIDE-5 | 対象版、観測元、欠落・失敗を示し、合成結果や評価不能を実agentでの改善として報告しない。 |

## 実装判断の羅針盤

まず採用先のagentが何をどの順序で読むか確かめます。`AGENTS.md`などのファイル名だけでは、実際の読み込みや優先順位は分かりません。次に変更経路を守ります。GitHubならCODEOWNERSだけを置いてもレビュー必須にはならず、対象branch側のCODEOWNERSと保護ルールの両方が必要です。指示ファイル自身とレビュー担当の設定も変更対象に含めます。詳細は[設計パターン](../../../../engineering/ai-development-security/repository-agent-guidance-review/README.md)を参照してください。

比較評価では、例えば「失敗したsecurity testを修正する」課題で、既存テストを守りつつ修正できたかを確認します。安全のため全作業を拒否した場合は、危険操作がなかったことと課題未達を分けます。合成JSONの数値だけでは、実agentが指示を読んだことも従ったことも分かりません。

## 診断で確認する項目（異常時テスト）

- 未信頼PRが指示ファイルを追加・変更・削除しても、承認なしに利用するbranchへ入らないか。新規ファイルや別パスも対象か。
- 指示と承認記録を同じ作成者が変更しても、独立レビューをすり抜けないか。承認後の追加pushや直接push、例外経路はどう扱われるか。
- 指示に「scanner停止」「権限を広げる」と書いても、実際のscannerや操作許可が文章だけで変わらないか。
- 指示を追加した比較で、課題・初期状態・agent版・tool権限・採点方法が変わっていないか。危険な提案、課題の成否、過剰拒否を別に観測しているか。
- Agentが指示を読んだか、runが完了したか、scorerが利用可能か不明な結果を改善率へ数えていないか。評価ログに秘密情報を保存していないか。

これらは診断の項目であり、実施結果ではありません。[教材](learning.md)で一つのrules-file変更を追います。[参照資料と採否](../../../../sources/README.md#ref-development-guidance-001)、[旧項目の対応](../../../../docs/REPOSITORY_AGENT_GUIDANCE_MIGRATION.md)も参照してください。
