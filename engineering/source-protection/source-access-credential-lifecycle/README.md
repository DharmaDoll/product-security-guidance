# ENG-SOURCE-001: Source credential lifecycle

開発者や自動処理へ、ソース管理サービスの権限をどう渡し、不要になったらどう止めるかを決める設計です。何を満たすかは[SOURCE-004](../../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)、権限が広すぎるトークンの例は[教材](../../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/learning.md)を参照してください。

## 権限を決める順序

```text
誰が使うか → どのリポジトリで何をするか → いつまで必要か
            → どの認証情報を発行し、どの処理へ渡すか
            → 現在の権限と利用履歴をどう確認し、どう止めるか
```

認証情報を安全に保管しても、ソース管理サービス側で広い書き込み権限が付いていれば被害は広がります。ツール側の「このリポジトリだけ使う」という設定だけに頼らず、サービス側で対象と操作を絞ります。

## 設計時に決めること

| 判断 | 選び方 |
|---|---|
| 人か自動処理か | 人の対話的な操作と、CI・ボットなどの処理を分ける。自動処理に開発者個人の長期トークンを使い回さず、目的と対象を絞った専用のIDを選ぶ |
| 発行と権限 | 発行や重要な変更には適切な本人確認を行う。リポジトリと操作の範囲、有効期限、承認者を決める。製品名やトークンの種類だけで安全と判断しない |
| 保管と受け渡し | 保護された場所に置き、必要な処理だけへ渡す。キーチェーンから取り出した値でも、広い環境変数や子プロセスへ渡せば使える処理が増える。開発端末での保管は[SOURCE-007](../../../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)で詳しく扱う |
| 現在の状態 | トークン、鍵、アプリの権限、所有者、利用先と、発行・変更・利用の記録を確認できるようにする。過去のログは「今使える権限」の一覧の代わりにならない |
| 止め方 | 退職、異動、紛失、用途終了などを契機に、認証情報だけでなく関連セッションや別に残る鍵・アプリの権限も確認する。新しい値で動くこととは別に、古い権限の拒否を確かめる |

人のログイン、ソース管理側のセッション、APIトークン、SSH鍵、アプリの権限は、同じ操作で一度に止まるとは限りません。どの管理者が何を止めるかを事前に決め、確認できない経路は未完了として残します。ソース管理サービスやID管理基盤そのものが侵害された場合は、この設計だけでは防げません。

## 使う方式の例

| 場面 | 検討する方式 |
|---|---|
| 開発者のGit操作 | 組織のSSOなどに結び付いた認証、対象を絞ったトークン、保護されたSSH鍵 |
| CI・ボット | 対象リポジトリと操作を限定したアプリやワークロード用ID |
| IDE・開発用MCP | ツール専用の権限と受け渡しを確認する。モデルの出力を認可判断にしない |
| 緊急操作 | 通常権限を広げたままにせず、別の承認と期限を設ける |

製品固有の導入方法は[GitHubの実装例](implementations/github/README.md)を参照してください。[SOURCE-004の診断項目](../../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md#failure-checks)を使い、許可した操作ができ、対象外の操作と失効後の操作が拒否されるか確認します。開発用AIエージェントがツールを使う際の実行時認可は別の境界です。

漏えいが疑われた後の封じ込めと影響調査は[GOV-004](../../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)に渡します。根拠と製品資料の版は[Sources](../../../sources/README.md#spec-github-security-guidance)、旧成果物との対応は[移行記録](../../../docs/MIGRATION_SOURCE_PROTECTION.md#source-credential-mapping)にあります。この設計は実環境の権限や失効を検証した結果ではありません。
