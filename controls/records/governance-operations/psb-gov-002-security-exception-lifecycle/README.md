# PSB-GOV-002 Security exception lifecycle

## このcontrolを一枚で理解する

| 項目 | 内容 |
|---|---|
| セキュリティ上の問題 | 例外が広すぎる、自己承認される、期限後も残る、または評価不能でも利用されると、意図した範囲を超えてsecurity gateが無効になる。 |
| 誰から、または何から守るか | 納期圧力による過大なscope、悪意ある回避、承認者の誤認、台帳の欠落・改ざん、失効処理や評価処理の障害から守る。 |
| 何が対象か | Control固有の失敗に対して発行する例外decision、その対象、責任者、risk、代替策、承認、期限、失効状態。 |
| 何をするか | Exact scope、独立した役割、期限、是正先を持つversioned decisionとして記録し、使用時に状態を再評価する。 |
| 成功状態 | 有効・失効間近・期限切れ・不正・評価不能を区別でき、期限切れや評価不能は元のsecurity failureを解除しない。 |
| 対象外・残余リスク | 例外の妥当性は元controlのrisk判断を代替しない。Ticket、時刻、policy engine、audit log、実環境の強制は組織側で確認する。 |

## 問いと境界

「誰が、どのcontrolのどの失敗を、どの対象について、なぜ、いつまで受け入れたか」を、例外を使用する時点で説明できるか。
共通化するのは例外のlifecycleです。脆弱性の悪用可能性、dependency採用、scanner findingの重大性など、例外を認めてよいかというcontrol固有の判断は共通policyへ移しません。

## 必要なセキュリティ特性

| ID | 満たすべき状態 |
|---|---|
| EXCEPTION-1 | 一つの既知control property、exact target、environmentへscopeを限定し、wildcardで他対象へ拡張しない |
| EXCEPTION-2 | Owner、risk reviewer、approverを追跡可能な異なる主体として記録する |
| EXCEPTION-3 | 理由、受け入れるrisk、代替策、承認decision、是正作業を相互に追跡できる |
| EXCEPTION-4 | 作成時刻より後の上限付き期限を持ち、信頼できる評価時刻から失効を自動判定する |
| EXCEPTION-5 | 使用する例外集合の完全性、鮮度、改変有無を確認し、一部だけの台帳を正本としない |
| EXCEPTION-6 | Credential、source code、production payloadを複製せず、安全な参照だけを証拠へ残す |
| EXCEPTION-7 | Consumerはversioned interfaceを使い、control固有のrisk・enforcement semanticsを維持する |
| EXCEPTION-8 | `ACTIVE`、`EXPIRING`、`EXPIRED`、`INVALID`、`ERROR`を区別し、後三者は元の拒否を解除しない |

## 実装判断の羅針盤

例外はcontrolを`PASS`へ書き換える仕組みではなく、失敗を残したまま限定的なrisk acceptanceを関連付ける別decisionです。
実際のgateには、例外IDと対象IDが同じ語彙で届く必要があります。台帳だけ正確でも、consumerがbranch名やpackage名を曖昧に再解釈すればscopeは広がります。

期間上限は一律30日とは限りません。Risk class、露出、代替策、是正能力に応じて組織が定めます。
延長は既存期限の編集ではなく、現在の状況を再評価した新しい承認として扱います。緊急対応でも、事後に広い恒久例外へ変換しません。

## 設計上の接続先

現時点では[Dependency release cooldown](../../dependency-security/psb-deps-001-dependency-release-cooldown/README.md)の`DEP-AGE-6`と、
[Install execution policy](../../dependency-security/psb-deps-002-install-execution-policy/README.md)の限定実行判断、
[Scanner evidence trust boundary](../../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)の`SCAN-6`、
[Secret publication boundary](../../source-protection/psb-source-002-secret-publication-boundary/README.md)の`SECRET-7`を接続しています。いずれも設計上の関係であり、実環境の接続確認ではありません。
Cooldownは待機期間前の特定バージョンの採用、Install execution policyは特定の取得物に含まれる準備用コードの実行について、それぞれのリスク判断を残します。
Scanner側には検出ルール・対象・取得物・検出結果の識別情報と、一時的に許容する理由を残します。検査の停止やデータ取得失敗は例外で解除しません。
公開境界では対象repository・送信先・ref・commit・path・ruleを限定し、秘密値を申請へ貼らず、元の検出結果を残します。変更後の内容や検査不能な履歴への流用は認めません。
機械可読な対象identityと禁止範囲は[exception consumer mapping](../../../../mappings/exception-consumers.yaml)が正本です。
「例外」という語を含むだけのエラー処理やデータ受渡しはrisk acceptanceではないため、consumerへ登録しません。

## 関連資料

- [教材: An exception is a decision, not a PASS](learning.md)
- [設計pattern: Security exception decision boundary](../../../../engineering/governance-operations/security-exception-decision-boundary/README.md)
- [参照仕様と採否](../../../../sources/README.md#ref-security-exception-lifecycle-001)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [Exception consumer mapping](../../../../mappings/exception-consumers.yaml)

旧YAML verifierとfixtureは実装候補として保留しました。この移行はticket system、policy engine、信頼時刻、実環境のgateを検証していません。
