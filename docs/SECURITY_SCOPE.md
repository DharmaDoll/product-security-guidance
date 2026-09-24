# Security scope

## AIを使う開発環境と、AIを備える製品

本PJのAI Development Securityは、AIを使ってソフトウェアを開発・レビュー・変更する環境を対象にします。
開発者端末に加えて、IDE・CLI、開発用MCP、リポジトリ連携、CIで動くcoding agentも含みます。
守る対象はソース、認証情報、開発・build環境、変更・公開・deployの権限です。

アプリケーション自体が提供するAI機能のセキュリティは、[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)へ委ねます。
本PJでは、該当するcontrolや教材を重複して構築しません。この分担は利用者の2026-09-20の指示に基づきます。
参照先に個別の対策が実装済みであることや、旧controlが移植済みであることを意味しません。

| 判断対象 | 本PJで扱う範囲 | ai-security-foundryへ委ねる範囲 |
|---|---|---|
| Agent・拡張 | Coding agentのSkill・MCP・plugin、指示、権限、更新・失効 | 製品が提供するAI agent・tool連携の設計と実行時保護 |
| Prompt injection | Repository文書、issue、tool出力が開発agentを介してソースや認証情報へ影響する経路 | 顧客入力、RAG、製品内toolを介したAI機能の悪用 |
| データ・通信 | 開発agentへのソース・秘密情報の受け渡し、外部送信、作業contextの取扱い | モデル・学習データ・RAG corpus、推論gateway、AI固有の入出力処理 |
| 評価 | 開発用の指示・拡張・操作認可の有効性を確かめる限定評価 | AI製品のTEVV、model評価、AI機能のrelease gate |
| 認可・運用 | 開発agentによる書込み、公開、deploy、委譲、停止を必要な範囲で扱う | 製品のmulti-agent構成、AI session・memory・推論基盤の保護 |

MCP、agent、promptという名称だけでは分類しません。「誰の作業を支援し、どの資産への権限を守るか」で決めます。
例えば、開発者がコードレビューに使うMCPは本PJ、製品のchatbotが顧客データを取得するMCPはai-security-foundryの範囲です。
両者に共通する知識は参照でつなぎ、AI製品全体の設計を開発環境のcontrolへ取り込みません。

## 一般的なProduct Securityは継続する

認証・認可、入力処理、秘密情報管理、依存関係、CI/CD、container・cloud・IaC、release、脆弱性対応は引き続き本PJの対象です。
AI機能を持つ製品にもこれらの一般的な対策は適用できます。AI製品固有の対策を別PJへ委ねることで、通常のApplication Securityや本番監視を除外するものではありません。

## 旧controlの移行判断

11 domainと既存IDを維持し、次の扱いを[移行計画](MIGRATION_PLAN.md)と候補一覧に適用します。

| 旧control | 扱い |
|---|---|
| PSB-AI-001〜004 | 開発用guidance・拡張・prompt injection・coding agent runtimeとして対象。AI-002・AI-004の記録は移行済み |
| PSB-AI-005〜009 | `scope-review-required`。Memory、操作結果、予算、委譲、停止・復旧から、開発環境に必要な部分だけを選ぶ。パッケージ全体の移行は予定しない |
| PSB-AI-010 | `out-of-scope`。AI application gatewayは別PJの担当 |
| PSB-AI-011 | `out-of-scope`。RAG corpus・retrievalは別PJの担当 |
| PSB-DEPS-005 | `out-of-scope`。モデル・データセットの供給経路は別PJの担当 |
| PSB-DETECT-002 | `out-of-scope`。AI製品のTEVV release gateは別PJの担当 |

`out-of-scope`は移行待ちではなく、本PJの移行対象からの除外です。`scope-review-required`は適用範囲の選別が済んでいない状態です。
旧52件は履歴上の棚卸し件数であり、全件を移す計画ではありません。現在の記録は27件ですが、旧件数との差をそのまま残作業件数にはしません。
旧文書・参照仕様は履歴と判断根拠として保持します。別PJのcoverageや完成度を、本PJの移行状況へ加算しません。
