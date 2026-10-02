# PSB-DEPS-003: Dependency artifact identity

依存の更新を承認しても、通常buildがlockfileを作り直すと、レビューしていない推移依存が入ることがあります。
このcontrolは、承認した依存関係と実際に使うファイルを一致させるためのものです。

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

## 固定する入力と照合方法を決める

Exact versionとhashは両方必要です。Versionは解決結果、hashは許可したbytesを識別します。
同じversionに複数platform用の配布ファイルがある場合、使用するファイルそれぞれのhashと適用範囲を管理します。
取得したファイルからhashを計算して同じbuildで自動承認するだけでは、事前のレビューへ結び付きません。

標準package managerのimmutable installと完全性検証を優先し、manifestの鮮度確認とlockの書換え禁止を
別々に確認します。単に「frozen」という名前があることや、lockfileが存在することを根拠にしません。
失敗時は更新経路へ戻って差分をレビューし、通常buildでlockを修復して続行しません。

既に展開した依存環境を再利用する場合も、名前とversionが同じという理由だけで検証済みにしません。
その状態を承認済みの入力へ結び付けて確認できないなら、新しい環境で照合し直します。取得時のhash検査は、後から書き換えられた展開済みファイルの保証にはなりません。

[既存pip例](../../../../engineering/dependency-security/install-execution-policy/implementations/pip/README.md)は、wheelの選択とhash不一致の拒否を示す限定例です。
Manifestとの対応、全推移依存、対象platform全体を確認する例ではありません。必要な方式は[設計pattern](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)で選びます。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は、レビューしていない依存を通常buildへ入れないか確認する項目です。製品に応じた手順で確認し、
チェックリストの記載を実施済みの結果とは扱いません。

- **DEP-ID-1・4**：Manifestだけを変えた状態で、古いlockを使う、またはlockを自動修復してbuildを続けられないか。
- **DEP-ID-2**：推移依存、別OS・architecture、optional依存が固定対象から漏れ、実行時に再解決されないか。
- **DEP-ID-3**：同じ名前とversionで別のファイルを返したとき、mirror・cache経由でも利用前に不一致を拒否するか。
- **DEP-ID-2・3**：展開済みの依存環境を差し替えて再利用すると、名前とversionだけで検証済みとして通らないか。
- **DEP-ID-3・5**：hashのない依存や対応外の取得形式を混ぜても、検証済みという結果にならないか。
- **DEP-ID-4**：通常buildや後続コマンドがlockを生成・書き換え、レビューとの差分を隠していないか。
- **DEP-ID-5**：入力欠落、不正な形式、ツール不在、取得・検証失敗のとき、照合を省略して続行しないか。

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
- [Framework mappings](../../../../mappings/frameworks.yaml)：ATT&CK `v19.1 / T1195.001`の未レビュー依存・取得物差し替え経路と、NIST SSDF `1.1 / PW.4.4`の部品完全性確認に限る部分的な設計関係。旧`PW.4.1`とOSPS `BR-05.01`は[非継承](../../../../docs/MIGRATION.md)とした。悪意ある内容の検知、SSDFやOSPSへの準拠、実際のbuildでの強制を意味しない
- [Metadata](control.yaml)
