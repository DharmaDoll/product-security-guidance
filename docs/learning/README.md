# 学習資料

学習資料は、一つの具体的なシナリオから攻撃経路、誤解、判断基準を理解するための教材です。
受講者、理解度、受講履歴はこのリポジトリで記録しません。

このページを教材とcontrol・patternの対応関係の正本にします。Controlは満たすべき成果、patternはその成果を実現する
設計上の選択肢を示します。複数controlで使う教材は複製せず、関係する行から同じ教材へリンクします。

## 全教材索引

| Domain | 教材 | 主に理解すること | 対応するcontrol | 対応するpattern |
|---|---|---|---|---|
| AI Development Security | [Reviewing an agent extension](reviewing-an-agent-extension.md) | 拡張の内容・権限・読み込み・失効 | [PSB-AI-002](../../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) | [Agent extension admission](../../engineering/ai-development-security/agent-extension-admission/README.md) |
| AI Development Security | [Approval is bound to an action](approval-is-bound-to-an-action.md) | 承認対象、実行対象、再利用、結果不明 | [PSB-AI-004](../../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) | [Development action authorization](../../engineering/ai-development-security/development-action-authorization/README.md) |
| Source Protection | [Managed is not currently trusted](managed-is-not-currently-trusted.md) | 端末の登録、現在の観測、アクセス判断 | [PSB-SOURCE-001](../../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | [Managed developer endpoint](../../engineering/source-protection/managed-developer-endpoint/README.md) |
| Source Protection | [Source credential lifecycle](../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/learning.md) | Credentialを秘密文字列ではなく権限として扱う | [PSB-SOURCE-004](../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | [Source credential lifecycle](../../engineering/source-protection/source-access-credential-lifecycle/README.md) |
| Dependency Security | [Dependency release cooldown](../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/learning.md) | 待機期間が提供する観測時間 | [PSB-DEPS-001](../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | [Dependency release cooldown](../../engineering/dependency-security/dependency-release-cooldown/README.md) |
| Dependency Security | [Install execution policy](../../controls/records/dependency-security/psb-deps-002-install-execution-policy/learning.md) | 取得・準備用コード実行・利用の違い | [PSB-DEPS-002](../../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md) | [Install execution policy](../../engineering/dependency-security/install-execution-policy/README.md) |
| Dependency Security | [Reviewed dependency intake](reviewed-dependency-intake.md) | 採用判断、artifact同一性、実行許可の接続 | [PSB-DEPS-003](../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、[PSB-DEPS-004](../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md) | [Reviewed dependency intake](../../engineering/dependency-security/reviewed-dependency-intake/README.md) |
| CI/CD Security | [Untrusted PR boundary](../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/learning.md) | 未信頼producer、派生状態、権限付きconsumer | [PSB-CICD-005](../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | [Untrusted PR boundary](../../engineering/cicd-security/untrusted-pr-boundary/README.md) |
| CI/CD Security | [Workload federation boundary](../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/learning.md) | Token認証、workload認可、交換後の権限 | [PSB-CICD-006](../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) | [Workload federation boundary](../../engineering/cicd-security/workload-federation-boundary/README.md) |
| CI/CD Security | [CI state and runner lifecycle](ci-state-and-runner-lifecycle.md) | 外部cacheとrunner残存stateの違い | [PSB-CICD-007](../../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、[PSB-CICD-009](../../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) | [CI state and runner lifecycle](../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md) |
| Build Security | [Build code is not build authority](build-code-is-not-build-authority.md) | Build対象コードと実行環境の権限 | [PSB-BUILD-001](../../controls/records/build-security/psb-build-001-build-containment/README.md) | [Build execution boundary](../../engineering/build-security/build-execution-boundary/README.md) |
| Release Integrity | [Authentic is not acceptable](authentic-is-not-acceptable.md) | 署名の真正性とconsumerの受入判断 | [PSB-REL-001](../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) | [Consumer artifact acceptance](../../engineering/release-integrity/consumer-artifact-acceptance/README.md) |
| Detection / Verification | [Zero findings is a scoped observation](zero-findings-is-a-scoped-observation.md) | Clean、finding、error、coverage | [PSB-DETECT-001](../../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) | [Scanner acquisition and evidence boundary](../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md) |
| Container / Cloud / IaC Security | [No events is not no incident](no-events-is-not-no-incident.md) | 検知なしと観測・配送不能の違い | [PSB-CONTAINER-004](../../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) | [Runtime detection to triage](../../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md) |
| Governance / Operations | [Impact is an evidence chain](impact-is-an-evidence-chain.md) | Component、build、artifact、deploymentの証拠連鎖 | [PSB-GOV-001](../../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) | [Incident impact and response planning](../../engineering/governance-operations/incident-impact-and-response-planning/README.md) |
| Governance / Operations | [An exception is a decision, not a PASS](an-exception-is-not-a-pass.md) | Control failureと期限付きrisk acceptance | [PSB-GOV-002](../../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) | [Security exception decision boundary](../../engineering/governance-operations/security-exception-decision-boundary/README.md) |
| Secure Design / Coding | [Authentication is not object authorization](authentication-is-not-object-authorization.md) | 正規利用者に対する対象・操作・tenant認可 | Control未移行 | [Object access boundary](../../engineering/secure-design/object-access-boundary/README.md) |

## 辿り方

1. 教材でシナリオと誤解を読む。
2. 対応するcontrolで、成立すべきセキュリティ特性と保証しない範囲を確認する。
3. 対応するpatternで、方式、強制点、トレードオフ、失敗経路を比較する。
4. Pattern配下にimplementationがある場合だけ、製品固有の設定・コード・確認方法へ進む。

「Control未移行」は、教材とpatternが先行する新規pilotです。教材の存在をcontrolへの対応済み状態へ読み替えません。

## 教材に残す内容

- 主体、データ、操作が分かる一つのシナリオ。
- 攻撃者に可能なこと、信頼境界、悪用経路。
- 初めて出る用語。
- セキュリティ不変条件と強制点。
- 合格・不合格、隣接する特性、保証しない範囲の判断基準。
- よくある誤解と、設計レビューで使える問い。

空の教材やcontrol本文の複製は作りません。攻撃段階と前後の受け渡しは
[横断分析](../ANALYSIS_LENSES.md)で確認してください。
