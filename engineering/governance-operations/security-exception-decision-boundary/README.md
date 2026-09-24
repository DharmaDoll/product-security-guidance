# Security exception decision boundary

`ENG-GOV-002` / `governance-operations`

## 解く設計問題

複数のsecurity controlが、弱い独自の除外形式を増やさずに、限定されたrisk acceptanceを同じlifecycleで利用できるようにします。

```text
control failure + exact enforcement target
  → control ownerによるrisk分析
  → independent review / approval
  → immutable exception decision + expiry
  → consumerが使用時にscope・状態を評価
  → allow-with-exception または元のdenyを維持
```

## 責任の分離

共通serviceはidentity、役割分離、期間、状態、証拠の完全性を所有します。各controlは何が失敗したか、対象identity、許容できる代替策、例外時にも禁止する操作を所有します。
Gateは例外の存在だけを問い合わせず、control propertyとexact targetを渡し、対応したdecisionだけを受け取ります。

## 設計選択

| 方式 | 利点 | 主な失敗 |
|---|---|---|
| Repository内decision | Review履歴をsourceと一緒に管理しやすい | Merge権限と承認権限が同じ、信頼時刻や即時失効が弱い |
| Ticket / GRC system | Role、期限、監査を集中管理できる | GateとのID変換、API停止、部分取得をfail-openにしやすい |
| Policy service | 使用時に一貫して評価しやすい | 高可用性と認証が必要で、全risk判断を中央へ押し込む危険がある |

方式を組み合わせる場合は、どれが承認の正本で、どれがcacheかを明示します。Digestだけでは同じ主体によるdecisionとmanifestの同時改変を防げないため、独立した監査・署名・保護された履歴を検討します。

## Lifecycleと失敗経路

作成、承認、有効化、失効間近、失効、取消、再申請を別状態にします。延長は元decisionの履歴を消さない新規decisionとします。
Self approval、wildcard scope、対象ID変換の曖昧さ、過去時刻の指定、stale cache、欠けたpagination、secretを含む自由記述、`ERROR`からallowへの変換を負のシナリオとして確認します。

評価は実際のgateで、期限切れ・取消・backend停止・未知versionが元の拒否を解除しないことを確認します。サンプル台帳の検査だけで組織への導入済みとは判定しません。

設計上の接続先は[Dependency release cooldown](../../dependency-security/dependency-release-cooldown/README.md)、
[Install execution policy](../../dependency-security/install-execution-policy/README.md)、
[Scanner acquisition and evidence boundary](../../detection-verification/scanner-acquisition-and-evidence-boundary/README.md)です。実環境での接続は未確認です。
共通serviceへ渡すidentity、元の失敗、control側に残す判断、例外でも禁止する操作は[consumer mapping](../../../mappings/exception-consumers.yaml)で確認できます。

[Control](../../../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)、[教材](../../../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/learning.md)、[Sources](../../../sources/README.md#ref-security-exception-lifecycle-001)を参照してください。
