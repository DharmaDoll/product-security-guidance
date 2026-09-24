# Container registry publication boundary移行記録

旧`PSB-CONTAINER-002`の7 checkを、[control](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)の`REGISTRY-1..7`と
[pattern](../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

Transport、repository／action authority、short-lived publisher、release immutability、audit、lifecycle、evidence healthはregistryがartifactを保管・配布する境界として保持しました。
Build、signing、provenance、scanning、consumer verification、admission、runtimeは隣接成果物へ分離しています。

旧policy・identity・operation・audit・inventory JSON、Python verifier、testsは非移植です。Synthetic recordの整合はlive registryの実効権限、mutation拒否、collector完全性、replica・cacheを証明しません。問題のある操作や異常は確認項目として保持しました。

## 具体化判断

Exact endpoint、repository／action scope、digest immutability、audit、lifecycleという技術構造はpatternへ具体化しました。
Provider、edition、API、identity、event schema、retentionが未選定なので実装例は作りません。選定後にlive APIと無害な拒否試験を行えるadapterを追加します。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SP 800-190 `4.2.1` | `REG-001 / mitigates / high` | `REGISTRY-1 / supports / medium / design-reviewed`。Exact endpointと保護通信の設計関係。Live transportは未確認 |
| NIST SP 800-190 `4.2.2` | `REG-006 / mitigates / high` | `REGISTRY-6,7 / supports / medium / design-reviewed`。Stale state、deadline、deployability、evidence healthとの部分関係 |
| NIST SP 800-190 `4.2.3` | `REG-002..005 / mitigates / high` | `REGISTRY-2..5,7 / supports / medium / design-reviewed`。Authn／authz、publisher identity、mutation protection、auditとの設計関係 |

NIST本文は特定providerの短命federation、state名、期限、tag protection APIを規定しません。これらは旧controlと攻撃経路を再評価したrepository interpretationです。NIST SP 800-190全体の対応や組織導入を主張しません。
