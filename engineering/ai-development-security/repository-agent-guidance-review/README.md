# Repository agent guidance review

`ENG-AI-005` / `ai-development-security`

## 解く設計問題

Coding agentに渡すrepository指示を更新するとき、変更の受入れと、実際の開発作業への効果をどう分けて判断するか。[AI-001](../../../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)のDEV-GUIDE-1〜5を具体化します。製品が提供するAI機能の設計やTEVVは[別PJ](../../../docs/SECURITY_SCOPE.md)の担当です。

例えば「security testを無効化しない」という指示に例外を足したPRが通ると、その後の修正でagentが検査を弱める可能性があります。指示ファイルは実行コードでなくても、繰り返し読み込まれる変更入力です。

```text
採用するagent・読み込む指示の一覧
     → 指示の変更提案
     → 独立した意味のレビュー
     → 保護されたbranchへ受入れ
     → 実際のagentが読む内容・版の確認
     → 同条件の開発課題で効果と過剰拒否を評価
```

## 変更を受け入れる境界

最初にagentと実行場所ごとに、指示ファイル、設定の優先順位、読み込むbranch、取得方式、変更できる主体を列挙します。`AGENTS.md`という名前のファイルがあっても、すべてのagentが同じように読むとは推定しません。作業中の未信頼branchで追加された指示も、保護されたbranchのレビュー済み指示と区別します。[AI-003](../../../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)は、資料中の指示を依頼へ昇格させない境界を扱います。

変更時には、本文だけでなく、指示ファイルを探す設定、レビュー担当、例外、比較評価の課題・採点方法も確認します。本人やagentが自分の指示を承認できると、diffとhashが一致しても意味のある審査になりません。意味のレビューでは特に、テスト・scannerの停止、権限の拡大、秘密情報やソースの送信、根拠のない「問題なし」、外部Skillの無断導入を探します。汎用的な禁止文を増やすだけでは、正当な作業まで止める可能性があります。

| 変更の受入れ方式 | 適する場合 | 条件・代償 |
|---|---|---|
| 保護されたrepository branchで所有者レビュー | 指示がrepositoryとともに配布される | 対象path、所有者、直接push・例外、承認後の再変更を管理する。実際にagentが読む版は別に確認する |
| 管理された中央配布 | 多数のrepositoryに共通指示を配る | 配布元・対象版・失効と、各agentの読み込み結果が必要。repository側の追記との優先順位も決める |
| 指示を一作業ごとに明示する | 継続的な指示が少ない | 意図の再入力が増える。依頼者の認可と実行側の制限は残る |

GitHubでの変更レビュー構成は[CODEOWNERSとbranch保護の実装例](implementations/github-codeowners/README.md)に示します。指示の変更レビューが成立しても、agentがshell、通信、認証情報へ何を実行できるかは[AI-004](../../../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の実行側で制限します。

## 効果を比べる

比較する開発課題を先に選びます。例えば、外部Actionの更新、scanner障害、依存の追加、失敗したsecurity testの修正です。対象repositoryと正しい期待状態、許されない近道を人が定めます。課題ごとに、指示を加えない条件と対象の指示だけを加える条件を用意し、初期commit、依頼、agent・model版、tool権限、実行時方針、採点基準を揃えます。指示以外を変えた比較から、その指示の効果を断定しません。

評価では危険な提案・変更、正当な作業の達成、過剰拒否・不要な変更、実行と採点の状態を別々に記録します。同じagentが書いたテストや報告だけを独立した採点根拠にせず、差分と既存テストの変化を確認します。必要な試験は別に用意します。繰り返しの回数と採用基準は、対象作業のばらつきと変更リスクを見て事前に決めます。旧「4課題×2回」「20ポイント改善」等の値は合成fixtureの設定であり、全環境の基準ではありません。結果が揃わなければ`INCOMPLETE`または`ERROR`とし、成功率の分母から都合よく除外しません。

採用先の評価で分かった指示の効果は、そのagent・版・作業群・時点の結果です。Model、tool、指示、課題、採点方法を変えた後まで自動的に保証しません。生のprompt・出力、秘密値、本番ソースを本repositoryへ保存せず、必要な証拠はアクセス管理された場所で扱います。

## 前後の責任

[AI-002](../../../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)は外部のSkill・MCP・plugin等の採用を判断します。Repository所有の文章を外部依存の審査台帳へ無理に入れません。[AI-003](../../../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)はIssueやtool出力に混ぜられた指示の境界です。[AI-004](../../../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)は操作・ファイル・通信の実効制限です。このパターンは指示の変更と効果の判断に責任を持ちます。

[教材](../../../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/learning.md)、[参照資料](../../../sources/README.md#ref-development-guidance-001)、[移行判断](../../../docs/REPOSITORY_AGENT_GUIDANCE_MIGRATION.md)へ続きます。
