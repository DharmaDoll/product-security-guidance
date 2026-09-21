# Untrusted PR boundary — 学習ノート

[コントロール記録](README.md)

## この文書の目的

pwn requestを特定のGitHub Actionsイベント名の問題として暗記せず、未信頼のproducer、状態を受け取るconsumer、
consumerが持つ権限の組み合わせとして理解するための教材です。

## 1. 具体的なシナリオ

公開リポジトリは、外部コントリビューターのPRへ自動的にテスト結果をコメントしようとしています。
ワークフローは書き込み権限を得るために`pull_request_target`で起動し、PRのheadをcheckoutしてから
リポジトリ内のテストscriptを実行します。ジョブにはコメント用tokenのほか、保護されたEnvironment、
組織内self-hosted runner、内部パッケージレジストリへの到達性があります。

攻撃者はテストスクリプトを変更したPRを送ります。その変更が実際に読み込まれて実行されると、スクリプトは
トークンを目的外に利用し、ランナー上のファイルを読み、内部サービスへ接続できます。

checkoutなどの保護がPRコードの読み込みを止める場合、この経路は成立しません。ただし、手動fetch、別のAction、
成果物、キャッシュから読み込む経路もあるため、一つの保護機能だけで信頼境界の確認を終えないようにします。

```text
PR作成者がtest scriptを変更
  -> 権限を持つイベントがPRのheadをcheckout
  -> 変更されたscriptを実行
  -> token／secret／runner／内部networkへ到達
  -> repository変更、情報流出、永続化、後続処理の汚染
```

イベント名だけが原因ではありません。実害には次の三条件が必要です。

1. 攻撃者が変更できるコードまたは実行可能な状態が、実際に処理される。
2. その処理または後続consumerが、価値のある権限、資産、到達性を持つ。
3. コードがAPI操作、外部通信、永続化、または後続stateの汚染によって権限を利用できる。

三つ目までつながらない場合、ここで説明する最大の被害は成立しません。ただし将来の権限追加で経路が
完成しないよう、未信頼の実行と権限を構造的に分離します。

## 2. 用語

- **未信頼の状態**: PR作成者が直接または間接に変更できるコード、依存関係、入力、artifact、cache、output。
- **producer**: 状態を作る処理。PRジョブだけでなく、依存関係の解決やcache保存も含む。
- **consumer**: その状態を読み、展開し、解釈し、または実行する処理。
- **権限**: tokenだけでなく、secret、OIDC、Environment、runner上の資産、内部network、信頼される後続stateを含む。
- **信頼判断**: どのrevisionと入力を、どの権限で処理してよいかを新たに決めること。単なる実行承認とは異なる。

## 3. 境界を越える経路

### 同じジョブで越える

未信頼コードをcheckoutしてからシークレットを参照する、書き込み可能なトークンを残す、OIDCを発行できるようにする経路です。
`persist-credentials: false`はcheckoutが残す認証情報を減らしますが、job自体に別の権限があれば十分ではありません。

### 別の実行へ状態を持ち上げる

未信頼ジョブが作ったartifact、cache、outputを権限ジョブが実行または過度に信頼する経路です。
ワークフローを二つに分けても、実行可能状態をそのまま運べば信頼境界にはなりません。

### runnerを介して越える

再利用するself-hosted runnerへファイルやprocessを残す、ローカルcredentialを読む、内部networkへ接続する経路です。
`GITHUB_TOKEN`がread-onlyでも、runnerが持つ権限は消えません。

## 4. セキュリティ不変条件

```text
未信頼の変更を実行する境界
  = 価値のある権限を持たない
  + 権限処理へ実行可能状態を残さない

権限を必要とする境界
  = 新しく信頼したrevisionから開始
  + 未信頼runの実行可能状態を継承しない
```

データだけを渡す必要がある場合は、producerの識別、完全性、厳密な形式、許可する用途を検証し、
shell、テンプレート、コード、依存関係として解釈されないことを確認します。

## 5. よくある誤解

### 「`pull_request_target`は常に危険」

イベント自体ではなく、権限のある文脈がPR由来のコードや状態を読み込むことが問題です。PR本文を
検証済みのデータとして扱い、限定した権限でラベルだけを操作する処理は設計できます。ただし、後から
checkoutやscript実行が追加される変更も保護する必要があります。

### 「一度、メンテナーが承認すればコードは信頼済み」

承認は実行を許可しますが、状態のproducerを変えません。承認後のPR更新、依存関係、artifact、cacheまで
自動的に信頼済みになるわけではありません。

### 「最初のジョブがread-onlyなら後続も安全」

後続の権限ジョブが、最初のジョブの成果物やcacheを実行すれば攻撃経路は残ります。各consumerまで追跡します。

### 「workflowファイルを見れば導入を証明できる」

fork設定、実効permission、secret、Environment、runner group、実際のrevisionは提供元側の状態です。
取得できない場合は`PASS`にしません。

## 6. 設計レビューで使う問い

1. PR作成者が直接・間接に変更できるものは何か。
2. その状態を読むすべてのjob、workflow、cache、artifact、script、serviceは何か。
3. 各consumerが持つtoken、secret、OIDC、Environment、runner資産、network到達性は何か。
4. 権限処理は、どのrevisionと入力を新しく信頼したのか。
5. 実行可能状態がrunをまたいでいないか。データだけなら、どこで何を検証するか。
6. 確認できていないworkflowや提供元設定を、どの状態で記録するか。

## 7. 攻撃連鎖の前後

このノートが詳しく扱うのは[サプライチェーン攻撃の第5段階](../../../../docs/ANALYSIS_LENSES.md#サプライチェーン攻撃の12段階)です。
第2段階のソース変更と第4段階の依存関係を入力として受け取り、第6段階のCI/CD ID、第7段階のランナー、
第9段階のリリースへ、信頼境界を壊さず引き継ぐ必要があります。

## 参照資料

- [REF-CICD-010 Preventing pwn requests](../../../../sources/README.md#ref-cicd-010)
- [REF-CICD-005 GitHub Actions Best Practice 2025](../../../../sources/README.md#ref-cicd-005)
- [GitHubセキュリティガイダンスの基準版](../../../../sources/README.md#spec-github-security-guidance)
- [REF-PORTFOLIO-001 プロダクトセキュリティ概観](../../../../sources/README.md#ref-portfolio-001)
- [サプライチェーン攻撃段階と代表経路](../../../../sources/README.md#local-supply-chain-attack-stages)
