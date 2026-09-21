# Untrusted PR boundary

対応するコントロール：[PSB-CICD-005](../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)

実装例：[GitHub Actions](implementations/github-actions/README.md)

## 解く設計問題

外部コントリビューターや低信頼の利用者が変更できるコードをCIで検証しながら、そのコードに
リポジトリ、クラウド、リリース環境、永続ランナーの権限を渡さないようにします。単にジョブを分けるのではなく、
未信頼の実行が作った状態を、権限を持つconsumerへ昇格させないことも含みます。

## 基本構成

```text
未信頼の変更
    |
    v
隔離された検証 ──> 受動的な結果
  - 書き込み権限なし
  - secret／OIDCなし
  - 永続資産／内部networkなし
  - 権限処理へ実行可能状態を渡さない
                           review／mergeによる新しい信頼判断
                                         |
                                         v
                               信頼済みrevisionから新規実行
                                 - 目的に必要な権限だけ
                                 - 未信頼runの状態を継承しない
```

「受動的な結果」は、statusや厳密に検証した構造化データなど、後続処理がコードとして実行しない情報です。
圧縮されたworkspace、script、生成された設定、依存関係、cacheは、別のrunへ移しても未信頼のままです。

## 設計手順

### 1. 状態とconsumerを列挙する

PRのheadだけでなく、テスト、build script、lockfile、Action入力、手動fetch、submodule、生成物、cache key、
artifact、job output、再利用ワークフローへの入力を調べます。それぞれについて、誰が変更できるか、どこで
解釈または実行されるかを記録します。

### 2. 権限を到達性として捉える

token permissionだけでなく、配送されるsecret、OIDC発行、Environment、runner上のcredentialやsocket、
内部network、後続のtrusted consumerが受け入れるstateを確認します。権限の名称ではなく、攻撃者が
実際に何を操作できるかで評価します。

### 3. 未信頼の実行から権限を外す

可能なら一回限りの管理されたrunnerを使い、read-only以外のtoken、secret、OIDC、保護されたEnvironment、
内部networkを与えません。PR作成者が変更できるコマンドを実行する以上、そのジョブ内での任意コード実行を
前提に境界を設計します。

### 4. 権限処理を新しく開始する

review済みのrevisionを信頼の起点にし、別のworkspaceで処理を始めます。未信頼runのcheckout、cache、artifact、
output、依存関係を暗黙に引き継ぎません。権限は権限処理の目的に必要な範囲だけで付与します。

### 5. データだけを渡す例外を設計する

runをまたぐ必要がある場合は、データのproducer、署名または完全性、schema、サイズ、文字集合、許可する値、
consumerでの用途を決めます。shell文字列、template、HTML、path、式、コードとして再解釈される経路を確認します。

## 選択肢

| 選択肢 | 適する場面 | 主な代償と注意点 |
|---|---|---|
| PRでは無権限の検証だけを行い、権限処理はmerge後に始める | 最初に安全な境界を作る場合 | pre-mergeの統合試験が減る。rollbackやmerge queueが必要になる場合がある |
| metadata-onlyの権限ワークフローを分ける | label、comment、triageなど、PRコードを実行しない操作 | 文字列のcommand injection、将来のcheckout追加、過剰なpermissionを防ぐ必要がある |
| 隔離された一時環境で統合試験を行う | private dependencyや外部serviceを使う試験 | 環境作成、network分離、資格情報の用途制限、破棄を別に保証する必要がある |
| 厳密に検証した受動的な結果だけを後続処理へ渡す | coverage値や検査statusなどを権限処理が表示する | artifact全体を信頼せず、producerと形式とconsumerの解釈を固定する必要がある |

## セキュリティ特性の配置

| 特性 | 主な強制点 |
|---|---|
| `PR-BOUNDARY-1` | workflow inventory、producer／consumerのdata-flow review |
| `PR-BOUNDARY-2` | job permission、secret delivery、OIDC、Environment policy |
| `PR-BOUNDARY-3` | runner group、ephemeral lifecycle、network policy、workspace破棄 |
| `PR-BOUNDARY-4` | cache namespace、artifact consumer、workflow trigger、reusable workflow境界 |
| `PR-BOUNDARY-5` | branch／ruleset、review、trusted revision、fresh workspace |
| `PR-BOUNDARY-6` | provider設定とlive runを含む評価、`PASS`／`FAIL`／`NOT_CHECKED`／`ERROR`の分離 |

## 失敗しやすい設計

- event名だけで信頼を決め、手動checkoutや外部scriptによるcode loadingを見落とす。
- 未信頼ジョブのtokenだけをread-onlyにし、self-hosted runnerや内部networkを権限として数えない。
- `workflow_run`や別ワークフローへ移せば安全と考え、artifactやcacheを実行する。
- actor名、author association、label、過去の承認を、更新後も有効な信頼判断として使う。
- workflowファイルの静的検査結果を、fork設定や実効permissionの導入証拠にする。

## 運用上のトレードオフ

強い分離は、外部コントリビューター向けの試験範囲を狭め、CI時間と隔離環境の費用を増やすことがあります。
不足する試験を権限の再付与だけで解決せず、mock、読み取り専用mirror、一時環境、merge queue、post-merge検証、
迅速なrollbackを組み合わせます。例外は対象workflow、権限、runner、期限、所有者を限定します。

## 確認方法

設計レビューでは、全PR関連workflowのproducer／consumer図を作り、権限へ至る経路がないことを確認します。
導入確認では、提供元のtoken／fork／Environment／runner設定と、無害なfork PRの実runを観測します。
設定やrunを取得できない場合は`NOT_CHECKED`または`ERROR`であり、設計例の存在だけで`PASS`にはしません。

## 参照資料

- [REF-CICD-010 Preventing pwn requests](../../../sources/README.md#ref-cicd-010)
- [REF-CICD-005 GitHub Actions Best Practice 2025](../../../sources/README.md#ref-cicd-005)
- [GitHubセキュリティガイダンスの基準版](../../../sources/README.md#spec-github-security-guidance)
- [サプライチェーン攻撃段階と代表経路](../../../sources/README.md#local-supply-chain-attack-stages)
