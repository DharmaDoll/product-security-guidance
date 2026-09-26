# GitHub indicator watch

`IMPL-GITHUB-PUBLIC-INDICATOR-WATCH`。公開コード、Issue、PRに自社ドメイン名または指定したメールアドレスが現れた**候補**を探す、Python 3.10向けの小さな実装です。通常の流れは「少数の指標で検索 → URLを人が精査 → 確認した候補だけWebhookへ通知」です。同じ公開ファイル・Issue・PRに複数の指標が当たっても候補をまとめ、通知済みの候補は再通知しません。

これは[PSB-SOURCE-003](../../../../../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)の限定実装です。公開サービスの台帳照合を行う[DETECT-003](../../../../../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)とは対象が異なります。検索結果だけで情報漏えい、脆弱性、サービスの稼働を確定しません。

## 手元のリポジトリへ入れる

Python 3.10以降と、**公開リポジトリだけにアクセスできる専用GitHub認証情報**を用意します。実装ディレクトリを、利用するリポジトリのたとえば`.security/github-indicator-watch/`へコピーします。`config.example.json`を`config.json`へコピーし、所有を確認したドメイン名または精査したいメールアドレスを1〜5件設定します。`config.json`と`state.json`は付属の`.gitignore`で除外します。

```bash
cd .security/github-indicator-watch
cp config.example.json config.json
# config.json の example.invalid を自組織の指標に変更する
# 秘密管理の仕組みから GITHUB_TOKEN を環境変数へ渡す
python3 watch.py scan --config config.json --state state.json
python3 watch.py list --state state.json
```

検索は指標ごとに公開コード・Issue・PRを各1回ずつ、最大100件の先頭結果だけ取得します。たとえば指標2件なら最大6回の検索です。`scan`は新候補のID・指標ID・公開URLを表示します。検索結果の本文やメール値は状態ファイルや通常出力へ保存しません。`state.json`は候補の再通知を抑えるために保持してください。定期実行する場合も、一つの状態ファイルに対してジョブを一つだけ起動します。

各URLをブラウザで開き、指標の**正確な記載**、公開意図、所有者、必要な対応を確認します。通知すると決めた候補だけ、表示されたIDを指定します。Webhookの受信側は下記JSONを受け取れるものを用意してください。

```bash
# 通知先が認証を要する場合だけ WEBHOOK_TOKEN を秘密管理の仕組みから渡す
python3 watch.py notify --state state.json --id <候補ID> --webhook-url https://your-receiver.example/alerts
```

Webhookには`id`、`source`、`indicator_ids`、`surface`、`url`だけを送ります。認証情報や検索本文は送りません。正常応答を受けた後に`notified`を保存し、再実行時には同じ候補を送りません。送信先が受信した直後に接続が切れた場合は受領が不明なので、再試行で重複する可能性があります。受信側でも`id`を重複排除キーにしてください。

## 安全なsmoke test

```bash
python3 -m unittest -v test_watch.py
```

テストはローカルの模擬GitHub APIとWebhookだけを使います。指標2件が同じ公開候補に当たると1件になること、精査前には通知しないこと、通知済み候補を再送しないこと、検索不完全時に状態を更新しないこと、先頭100件を超えた場合に部分結果と知らせることを確認します。実GitHub検索や組織の通知経路の動作確認ではありません。実際の対象で試す場合は、無害な公開テスト記載を用意し、ブラウザで確認したIDだけをテスト用Webhookへ通知してください。

## 解除と制限

解除するときは定期ジョブを停止し、使ったGitHub認証情報を失効させます。状態ファイルには公開URLと精査履歴が残るため、保持方針を確認してから移動・削除します。状態ファイルを失うと、過去候補が再び新規として表示されます。

GitHubのREST Code SearchはGitHubの画面上の新しいCode Searchとは異なる旧検索構文で、記号を無視する場合があります。`example.com`やメールアドレスの**完全一致をAPI結果だけで証明しない**ため、人がURLで確認してから通知します。公開コードは既定ブランチなどインデックス対象に限られ、Issue・PRはタイトルと本文に絞っています。コメント、Gist、削除済みの内容、外部Web、全てのforkや過去履歴は調べません。先頭100件を超えると`PARTIAL`と終了コード`2`を返します。認証失敗、検索の不完全結果、状態破損も`ERROR`で終了コード`2`とし、正常な候補0件へ変換しません。`PARTIAL`時は取得した候補を残すので、指標を絞って再実行してください。

同じ公開ファイルはrepository IDとpath、Issue・PRはGitHub object IDで重複排除します。内容変更だけでは再通知しない限定方式です。是正後の再出現や期限付き判断まで必要なら、[上位pattern](../../README.md)の状態設計を追加してください。通知先の運用と実際の対応は、このコードの外にあります。

[GitHub公式資料の採否](../../../../../sources/README.md#ref-public-source-exposure-001)と[具体化判断](../../../../../docs/PUBLIC_EXPOSURE_MIGRATION.md)を参照してください。
