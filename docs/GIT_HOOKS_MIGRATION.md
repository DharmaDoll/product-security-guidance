# Git hooks migration reconciliation

2026-09-23、旧PSB-SOURCE-002を[Secret publication boundary](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)と
[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/control.yaml)と
[README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md)です。

## 13項目の配置

旧IDはGHK-001〜012とGHK-014です。欠番を埋めず、元の13項目を追跡します。
以下は設計への移行と隣接責任の整理であり、旧実装の動作検証ではありません。

| 旧check | 主題 | 配置・採否 |
|---|---|---|
| GHK-001 | hookの所有・レビュー | SECRET-3。Repository配置と中央配布を選択肢にし、実際に実行する版を管理 |
| GHK-002 | 外部hookパス | SECRET-3。絶対・共有パスを一律拒否する旧方式は普遍化せず、配布元・変更権限・実効設定を確認 |
| GHK-003 | credential helper・remote内の値 | 隣接：SOURCE-004の保管境界。Git製品設定の移植は保留 |
| GHK-004 | safe.directory | 隣接：SOURCE-001の端末権限。Git所有権チェックの製品設定は保留し、hooks管理だけで保証しない |
| GHK-005 | 署名とpush範囲 | 分割：push範囲はSECRET-1。署名・identityの設定は保留し、内容の検査と分離 |
| GHK-006 | 機密形式の拒否 | SECRET-1・2。拡張子だけで機密性を判断せず、内容・検査不能範囲と組み合わせる |
| GHK-007 | 検出と非表示 | SECRET-2・6。旧ルール一覧と検出率を現在の保証には移さない |
| GHK-008 | サイズ上限 | SECRET-1・4。検査の上限を超えた場合の拒否・別経路を定め、旧5 MiBを一律要件にしない |
| GHK-009 | staged内容 | SECRET-2。作業ツリーとの違いを診断で確認する項目へ |
| GHK-010 | commit message | SECRET-2。内容とメタデータを別に検査 |
| GHK-011 | push履歴 | SECRET-1・2。導入履歴を確認。pre-push自体も省略できるためSECRET-5へ接続 |
| GHK-012 | 検査障害 | SECRET-4。失敗・未検査を検出なしにしない |
| GHK-014 | Gitleaks併用 | SECRET-3・4・6の設計へ。製品wrapper・image取得・実行は保留し、複数エンジンを必須にしない |

受信側の独立した判断SECRET-5と限定した除外SECRET-7は、旧READMEの限界と今回確認した仕様から具体化した本PJの設計です。
[端末管理のDEH-004・005](ENDPOINT_MIGRATION.md)から、このcontrolへローカル検査とサーバー側検査の責任を接続します。
公開済み情報の探索・回収、署名、全機密データの分類は統合しません。

## 旧4件のframework関係

| 旧関係 | 今回の扱い |
|---|---|
| ATT&CK v19.1 / T1552.001 / mitigates / medium | ファイル内認証情報の取得と誤公開の接点はあるが、端末からの窃取全体への防御とは異なる。旧関係は履歴に保持し、保管を分離した新特性への割当は保留 |
| SSDF 1.1 / PS.3.1 / supports / medium | releaseの保存に関する原文と、旧source保護全般という根拠が不一致。継承しない。SOURCE-001の[照合結果](ENDPOINT_MIGRATION.md#旧実装とframework-mapping)を参照 |
| OSPS 2026.02.19 / OSPS-BR-07.01 / supports / high | 2026-09-23に公式本文を確認。SECRET-1・2・4・5への部分的な設計関係として採用。旧highは履歴に残し、現行のconfidenceはmedium。全機密データや迂回経路の防御・適合性を証明しない |
| CISA Version 2 / CISA-PSBP-PP-08 / mitigates / medium | このIDは旧registryによるローカルID。公式PDFを今回取得できず、新特性への割当は保留。旧版・根拠・対象checkを削除しない |

### 原記録

次の旧記録は現在のマッピングではありません。現行の関係は[frameworks.yaml](../mappings/frameworks.yaml)で管理します。

```yaml
legacy_mappings:
- framework: mitre-attack
  version: v19.1
  id: T1552.001
  relationship: mitigates
  confidence: medium
  rationale: ローカルでのsecretおよび機密ファイル検査はファイル内credentialの誤公開を減らすが、回避可能でpatternにも限界がある。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-003
  - GHK-007
  - GHK-009
  - GHK-010
  - GHK-011
  - GHK-014
- framework: nist-ssdf
  version: 1.1 (SP 800-218, 2022)
  id: PS.3.1
  relationship: supports
  confidence: medium
  rationale: レビューで保護されたrepository-owned hooksとローカルのcredentialおよびidentity保護は、source codeと開発環境の保護を支援する。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-001
  - GHK-002
  - GHK-003
  - GHK-004
  - GHK-005
  - GHK-006
  - GHK-007
  - GHK-008
  - GHK-009
  - GHK-010
  - GHK-011
  - GHK-014
- framework: openssf-osps-baseline
  version: 2026.02.19
  id: OSPS-BR-07.01
  relationship: supports
  confidence: high
  rationale: Repositoryへcommitされる前にsecret patternと機密ファイルを検出・拒否し、unencrypted sensitive dataの意図しない保存防止を支援する。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-006
  - GHK-007
  - GHK-009
  - GHK-010
  - GHK-011
  - GHK-014
- framework: cisa-product-security-bad-practices
  version: 2 (January 2025)
  id: CISA-PSBP-PP-08
  relationship: mitigates
  confidence: medium
  rationale: Commit前にhardcoded credentialとsecret patternを検出・拒否してsource codeへの混入を減らすが、pattern外のsecretやhook
    bypassまでは防止できない。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-007
  - GHK-009
  - GHK-010
  - GHK-011
```

## 実装・検証の扱い

旧installer、Docker版Gitleaks wrapper、設定は移植していません。
既存hooksを自動上書きしない判断と切り戻し時の注意は、[新しい代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)の明示的な導入手順へ反映しました。
Gitleaks 8.30.1の組込み検出を採用し、独自PythonはGit objectと拒否判断の接続に限定しました。
旧Gitleaks版・container digest、旧独自ルール、5 MiB等をGitleaks実装の推奨設定として引き継いでいません。
検出・迂回・履歴・検査障害・値の非表示は、controlの診断で確認する項目として整理しました。
一時worktreeとbare repositoryだけで23件の実装テストを実施しました。本PJ自身や実環境のhooks有効化、
外部への検出用文字列の送信、組織の実環境診断は実施していません。
参照版・採否・取得できなかった資料は[Sources](../sources/README.md#ref-secret-publication-001)へ記録します。

2026-09-23追記：具体化判断により、[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しました。
旧実装をそのまま復元せず、検出は固定したGitleaksへ、独自コードはGitとの接続へ責任を分けています。
範囲と完了状態の正本は[実装計画](MIGRATION_PLAN.md#source-002の具体実装計画)です。

2026-09-25追記：旧`scan-sensitive.py`の正規表現、機密file名、staged内容、commit message、push履歴、
matched valueを表示しない判定を、[Python pattern scanner](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)へ再編集しました。
外部toolなしで仕組みを読み、軽い組織固有ruleを試すための第二実装です。新規remote refはremote-tracking refを信頼せず、local tipから到達する履歴を検査するよう変更しました。
ローカルhookだけで受信側のSECRET-5を満たさず、Gitleaksと検出同等でもありません。旧installer、Docker wrapper、巨大なfixture inventoryは移していません。
12 ruleの無効canary、near miss、値の非表示、staged内容、削除後もpush履歴に残る値、Gitによるhook起動を7 testで確認しました。
これは限定したimplementationの挙動であり、本PJや利用者のrepositoryへの導入証拠ではありません。
