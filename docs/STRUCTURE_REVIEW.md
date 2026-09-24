# Structure review

この文書は構造レビューの結果と、その後の補修の記録です。現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を参照してください。

## 結論と範囲

2026-09-17時点で、Build、consumer、Application、Operationsの四種類について、
control・教材・pattern・実装を別の更新単位へ分ける構造を維持します。
ただし、これは執筆者による読み通し・構造検査であり、独立した利用者テストやセキュリティ監査ではありません。

初回レビューではcontrolを追加せず、12件の記録と11patternを入口で整理しました。その後GOV-001、GOV-002、DETECT-001、AI-002を追加しました。2026-09-20にAI-004の設計部分を先行移行し、その時点で17件の記録と17patternになりました。AI-004のcontrol記録を追加しました。操作認可に続き、開発用実行環境の隔離を設計資料へ分離しました。

## 四種類で確認した境界

| 主題 | 判断の正本 | 実装・検証の状態 | 残る境界 |
|---|---|---|---|
| [Build](../engineering/build-security/build-execution-boundary/README.md) | 実行コードへ渡す権限、外側の通信・隔離、観測 | ガイダンス。旧JSON計画検査は保留 | 実sandbox・通信拒否・sensorは未確認 |
| [Consumer](../engineering/release-integrity/consumer-artifact-acceptance/README.md) | 同一性・認証・利用者の期待値・使用gate | ガイダンス。旧crypto fixtureは公開鍵欠落等で保留 | 実署名・失効・使用gateは未確認 |
| [Application](../engineering/secure-design/object-access-boundary/README.md) | 主体・対象・操作・tenantを使う認可設計 | SQLite限定実装、7テスト | HTTP認証、全endpoint、並行処理は未確認。新規pilotでありcontrol移行ではない |
| [Operations](../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md) | 検知・観測障害・配送・対象・担当者・独立承認 | ガイダンス。旧synthetic adapterは保留 | Live sensor、通知、対応、PSIRT能力は未確認 |

教材は具体的なシナリオから誤解を解き、patternは方式・責任・代償を選ぶ材料とします。
同じ概念が現れても全文を統合せず、この役割分担と正本へのリンクを維持します。
今回、別の横断洞察は追加しません。既存の洞察と重なる「検証成功だけで安全とは言えない」を別名で水増ししないためです。

## 修正した不一致

- ファイルリンクが存在していてもSources内の短いID anchorが欠けていた6リンクを修正。
- Application・Operations・攻撃段階9／11の集約を最新成果物と一致させた。直接対応は文書が保証目標を扱う意味で、導入済みではない。
- Control・engineering索引を一つの一覧へ整理。CacheとRunner、Buildとconsumer、CI観測と本番監視を別の境界として維持。
- 初期三件のpilotと追加の構造検証を区別し、過去の「次に作業する」という案内を最新状態へ更新。

## 引き続き残す制限

初回検査: YAML parse、当時12件のID一意性とcontrol索引、ローカルMarkdownのファイル・見出しanchor、
`git diff --check`を確認。SQLiteの7テストも再実行して成功しました。
これらは構造と限定実装の確認であり、全本文の正確さや本番導入を保証する検査ではありません。

Sourcesに保留・取得失敗・mutable版の記録がある資料は、現在の仕様へ再確認済みと読み替えません。
Framework mappingは旧版・ID・関係を保持した移行レビュー中の関係です。新規Applicationのexact ASVS mappingは未追加です。
初回レビュー時は旧ツリーへの相対参照が独立化を妨げていました。2026-09-21に固定コミットへの外部参照へ変更し、[単独検査](REPOSITORY_CUTOVER.md)を追加しました。2026-09-22には本PJを正本とする公開先が確定しました。独立化の範囲と残る運用判断は[Repository cutover](REPOSITORY_CUTOVER.md)を参照してください。
全legacy実装の意味的レビュー、全参照仕様の現在の有効性、独立した読者による理解度確認は未完了です。

## 2026-09-20の横断補修

- DETECT-001の旧fixtureに関する根拠を`legacy_rationale`へ分け、現在のガイダンスとの関係と未検証範囲を記載。
- 候補一覧・横断分析の移行済み／未移行を更新。過去の作業順序は履歴と明記。
- GOV-002の設計上の接続先をDependencyの2件とDETECT-001の計3件へ統一。
- Scanner設計本文の日英混在を補修。これは全資料の文章校正完了を意味しない。
- [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)と教材を追加。AI-004の認可部分のみの再編集で、control全体・製品実装・framework mappingは未移行。

レビューは内部整合性を対象とし、外部仕様全体の現行性や実環境の導入は検証していません。新規資料で確認した外部資料の範囲はSourcesに記載します。

補修後の確認：YAML 20件の構文、control ID 16件の一意性、設計パターン16件、framework mapping 62件の旧版・ID・関係・confidenceの保持、property参照、ローカルMarkdownリンク761件のファイルと見出し、`git diff --check`を確認しました。コード・製品設定は変更していないため、実装テストや実環境の認可試験は実行していません。

## 追加移行と受け渡しのレビュー記録

[Security scope](SECURITY_SCOPE.md)により、AI-004は開発環境に限定します。製品自体のAI securityはai-security-foundryの担当であり、移行待ちとして補完しません。

追加batchで[PSB-GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)をガイダンス移行しました。
Runtimeの対象identityから、SBOM・build・artifact・稼働deploymentへ影響調査を渡す境界を再編集しました。
「該当なし」と「inventory不完全」、対応計画と実対応、PSIRTの組織能力を分けることが受入条件です。

端末隔離・認証情報・通信制限は[Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md)へ移行し、Source Protection・Build・runner・操作認可との責任分界を示しました。AI-004は[全26項目の対応表](AI_RUNTIME_MIGRATION.md)、10特性のcontrol記録、旧15件のframework関係を整理し、2026-09-21にAI-002との失効時の受け渡しを補修しました。

続いてSOURCE-001を[29項目の対応表](ENDPOINT_MIGRATION.md)へ棚卸しし、[Managed developer endpoint](../engineering/source-protection/managed-developer-endpoint/README.md)を追加しました。登録・現在の観測・業務アクセスを分け、11項目の設計を先行移行しています。端末管理範囲のcontrol記録と旧4件のframework関係の照合は、このレビュー時点で残っています。認証情報・実行隔離・公開防止を一つへ再集約しません。製品設定を移す場合のみ現行仕様と実際の拒否挙動を確認します。Domainを一つずつ全件移す方式へ戻しません。
この記録は追加の依存や実環境での操作を承認するものではありません。次作業の優先順位は移行計画で管理します。
