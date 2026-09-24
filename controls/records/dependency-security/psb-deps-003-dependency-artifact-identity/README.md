# PSB-DEPS-003: Dependency artifact identity

学ぶ：[Dependency artifact identity](learning.md) · 設計する：[設計パターン](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)

## 問い

通常のbuildが、レビューしたmanifestとlockfileに対応する依存関係を使い、取得した外部ファイルの
bytesが承認したhashと一致することを、利用前に確認できるか。

## できてはいけないこと

Contributorや更新ボットがmanifestだけを変更した結果、CIがlockfileを暗黙に再生成して未レビューの
推移依存を採用してはいけません。Registry・mirror・cacheの侵害によって、同じ名前とversionの
別ファイルをbuildへ入れてはいけません。

## 適用範囲と非適用

Manifest、直接・推移依存のlock記録、通常installのコマンド、外部artifactのhash検証が対象です。
対象OS・architecture・optional依存の範囲を明示します。Local workspaceやVCS等は、選んだ方式で
同一性を保証できるか別に判断し、registry packageと同じ条件を満たすと推測しません。

取得元の正当性、packageの安全性、脆弱性、install scriptの許可はこのcontrolの直接の判定ではありません。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `DEP-ID-1` | Manifestとlockの対応を確認し、通常buildで再解決が必要な変更を拒否する |
| `DEP-ID-2` | 対象platformで使う直接・推移依存を、レビューしたexact versionと取得記録へ結び付ける |
| `DEP-ID-3` | 外部artifactに強いhashを要求し、利用するファイルとの不一致を拒否する |
| `DEP-ID-4` | 通常installと明示的な更新を分け、通常buildでlockを生成・書き換えない |
| `DEP-ID-5` | 入力欠落、未対応schema、runtime不在、検証失敗を合格にしない |

## 実装判断の羅針盤

Exact versionとhashは両方必要です。Versionは解決結果、hashは許可したbytesを識別します。
同じversionに複数platform用の配布ファイルがある場合、使用するファイルそれぞれのhashと適用範囲を管理します。
取得したファイルからhashを計算して同じbuildで自動承認するだけでは、事前のレビューへ結び付きません。

標準package managerのimmutable installと完全性検証を優先し、manifestの鮮度確認とlockの書換え禁止を
別々に確認します。単に「frozen」という名前があることや、lockfileが存在することを根拠にしません。
失敗時は更新経路へ戻って差分をレビューし、通常buildでlockを修復して続行しません。

## 境界と受け渡し

攻撃段階4で、承認済み依存から実際に取得するbytesまでを結び付け、段階7へ固定した入力を渡します。
悪意あるlock変更が承認され、悪意あるファイルがそのhashに一致する場合、このcontrolだけでは止まりません。
[Dependency change review](../psb-deps-004-dependency-change-review/README.md)が採用判断、
[Install execution policy](../psb-deps-002-install-execution-policy/README.md)が準備用コードの実行許可を担います。
その後のbuild、来歴、署名、SBOM、本番監視も別の責任です。

七つのレイヤーでは外部依存に直接対応し、プラットフォームの通常buildへ接続します。
[横断分析](../../../../docs/ANALYSIS_LENSES.md)は探索用の関係であり、導入済み状態の証明ではありません。

## 参照仕様とマッピング

- [SPEC-DEPENDENCY-LOCK-IDENTITY](../../../../sources/README.md#spec-dependency-lock-identity)：製品別仕様、採用・除外判断
- [Framework mappings](../../../../mappings/frameworks.yaml)：ATT&CK `v19.1 / T1195.001`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`、OSPS `2026.02.19 / OSPS-BR-05.01`。割当は移行レビュー中
- [Metadata](control.yaml)
