# PSB-SOURCE-003: Public source exposure triage

個人リポジトリのIssueに内部の接続先が貼られると、組織の既知リポジトリだけを調べても見つかりません。
このcontrolは、公開情報を探し、候補の意味を所有者が判断し、必要な対応へ渡すまでを扱います。
[教材：自社ドメインが見つかった後に何を確認するか](learning.md)から具体的な場面を読めます。

## 問い

セキュリティ担当者と情報の所有者が、自組織に関係するソースコードや開発上の会話を公開面から繰り返し探し、
観測できなかった状態を「候補なし」と区別し、新規・再出現した候補を判断と対応へ渡せるか。

## できてはいけないこと

意図しないソース、認証情報、内部の接続先、設定、組織固有情報が第三者から発見できる状態にあるのに、
検索範囲の欠落、収集処理の障害、期限切れの判断、重複抑制、通知失敗によって未対応のまま残してはいけません。

## 適用範囲

組織が観測を許可した識別子から探せる、公開リポジトリ、ソースファイル、commitに関連する公開情報、
Issue、Pull Request、Gistなどの開発上の公開面に適用します。ソース管理サービスの検索・API、
一般Webの検索索引、承認済みの外部監視サービスは観測手段の候補です。

次は直接の対象ではありません。

- 非公開リポジトリ、端末、社内ネットワークを探索すること。
- 第三者資産へのログイン、認証情報の有効性確認、能動的な通信検査、脆弱性悪用。
- 既知リポジトリのcommit前検査と受入拒否。
- 公開候補を脆弱性またはインシデントとして自動確定すること。
- 認証情報の失効、利用履歴の調査、公開コピーの削除、法務・広報判断を実行すること。
- 外部の攻撃対象全般の台帳照合、ポートスキャン、ドメイン乗っ取りの検査。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `PUBLIC-EXPOSURE-1` | 観測対象を、所有を確認した識別子、許可したサービス・公開面・検索条件、禁止する探索方法と結び付ける |
| `PUBLIC-EXPOSURE-2` | 観測ごとに検索条件または収集処理の版、対象の公開面、実行時刻、取得位置・範囲、サービスの上限、未観測範囲を追跡できる |
| `PUBLIC-EXPOSURE-3` | 一致した値と周辺の内容の収集・表示・保存・通知を必要最小限にし、認証情報や個人情報を新たな露出経路へ複製しない |
| `PUBLIC-EXPOSURE-4` | 公開場所と内容を識別し、候補の初出、継続、変更、判断期限切れ、是正後の再出現を区別する |
| `PUBLIC-EXPOSURE-5` | 候補の所有者、意図した公開か、影響する資産・認証情報、対応担当者、判断と期限を記録し、未判断を対応済みにしない |
| `PUBLIC-EXPOSURE-6` | 認証、検索回数の制限、ページ取得漏れ、応答の省略、タイムアウト、解析、状態更新、通知の失敗と古い観測を、正常に観測を完了した候補0件から区別する |

## 観測方法と対応を決める

1. 最初に「誰が何を所有し、どの公開面への検索を許可したか」を決める。検索語の多さから始めない。
2. 検索サービスが返した候補と、実際に観測できた範囲を同じ記録へ結び付ける。結果件数だけを証拠にしない。
3. 一致した本文をそのままチケット、チャット、ログへ複製せず、担当者が閲覧範囲を限定して原位置を確認できる参照を使う。
4. パスや表示名だけで同一候補とみなさず、サービス側の識別子と内容の変更から再判断できるようにする。
5. 「意図した公開」「誤検知」「是正済み」には所有者、理由、期限を持たせる。無期限の抑制にしない。
6. 認証情報が疑われる場合は、投稿の削除だけで閉じず、失効・セッション・利用履歴・派生権限の担当へ渡す。
7. 収集処理の異常と候補の発見を別に通知する。収集が止まった期間を候補なしとして扱わない。

既知のコミットやpushで認証情報が共有先へ届いたと分かっている場合、公開検索での再発見を対応開始条件にしません。このcontrolの検索対象は公開面であり、非公開リポジトリや受信側に届いた値の評価は[SOURCE-002](../psb-source-002-secret-publication-boundary/README.md)から所有者と[GOV-004](../../governance-operations/psb-gov-004-credential-exposure-containment/README.md)へ直接渡します。

[設計pattern](../../../../engineering/source-protection/public-exposure-observation-and-triage/README.md)で検索・状態管理・対応への引き渡しを選びます。
[GitHubの限定実装](../../../../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)は、少数の指標による検索と投稿単位の重複抑制を示します。
内容変更・再出現の再判断や所有者・理由・期限の記録は実装内で行わず、`PUBLIC-EXPOSURE-4`・`PUBLIC-EXPOSURE-5`全体を満たす例ではありません。採用先で補う責任を決めます。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は、公開情報の収集・判定・引き渡しで見落としてはいけない操作や異常の確認項目です。脆弱性診断や
設計レビューに利用できます。限定実装の代表テストとは範囲が異なり、全項目を実環境で確認した結果ではありません。

- **PUBLIC-EXPOSURE-1**：所有を確認していないドメイン、個人識別子、実際の認証情報、対象を限定しない検索語を送れるか。
- **PUBLIC-EXPOSURE-1・2**：公開情報だけを観測する処理に非公開リポジトリも読める認証情報を渡すと、検索範囲が変わってしまわないか。
- **PUBLIC-EXPOSURE-2・6**：取得上限、タイムアウト、`incomplete_results`、ページ取得漏れ、応答の省略を候補0件として受理しないか。
- **PUBLIC-EXPOSURE-3**：一致した周辺本文、メールの個人識別部分、token、認証ヘッダーがログ、成果物、状態ファイル、通知へ残らないか。
- **PUBLIC-EXPOSURE-4**：リポジトリ名やパスだけで重複をまとめ、内容変更・fork・mirror・再投稿を再判断しない状態にならないか。
- **PUBLIC-EXPOSURE-4・5**：意図した公開や誤検知という判断に所有者・理由・期限がなく、将来の変更も永久に抑制しないか。
- **PUBLIC-EXPOSURE-4・6**：検索から消えただけで是正済みにし、削除、非公開化、検索索引の変動、取得障害を区別できない状態にならないか。
- **PUBLIC-EXPOSURE-5・6**：状態更新または通知に失敗したのに取得位置を進め、次回の観測から候補が落ちないか。
- **PUBLIC-EXPOSURE-5**：認証情報の候補を投稿の削除だけで閉じ、古い権限の失効・拒否確認へ渡し忘れないか。
- **PUBLIC-EXPOSURE-1・4・6**：未レビューのリポジトリ変更で収集処理・検索条件・状態を書き換え、監視対象や抑制状態を隠せないか。

## 判定例

| 観測した状態 | このcontrolでの判断 |
|---|---|
| 検索が成功し、候補0件だが取得上限への到達を確認していない | 合格を裏付けない。観測範囲が不明 |
| 候補のURLと所有者だけをチケット化し、一致したtokenは原位置で限定確認する | 値の複製を抑えた精査記録になり得る |
| 同じパスの内容が変わったが、既知候補として通知を抑えた | 不合格候補。変更後の内容を再判断できない |
| 収集障害を別の通知として扱い、最後の成功時刻が見える | `PUBLIC-EXPOSURE-6`を支えるが、候補がない証明ではない |
| 公開した認証情報を削除し、失効・セッション拒否・利用履歴調査を対応記録へ渡した | このcontrolから対応担当への引き渡しが成立し得る |

## 保証しない範囲

検索サービスの索引は公開情報をすべて含むものではありません。削除済みの内容、過去のclone、cache、画像、
バイナリ、分割・難読化された値、検索されない公開面は残り得ます。
候補0件という件数だけでは、観測の完了は分かりません。正常完了と取得範囲を確認できた場合でも、
その範囲で候補が見つからなかったことを示すだけで、公開露出や過去の露出の不存在は保証しません。

## 関連資料

- [Public exposure observation and triage](../../../../engineering/source-protection/public-exposure-observation-and-triage/README.md)
- [GitHubの公開コード・Issue・PRを少数の指標で探す実装](../../../../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)
- [Secret publication boundary](../psb-source-002-secret-publication-boundary/README.md)
- [Source credential lifecycle](../psb-source-004-source-access-credential-lifecycle/README.md)
- [Credential exposure containment](../../governance-operations/psb-gov-004-credential-exposure-containment/README.md)
- [旧成果物との対応](../../../../docs/PUBLIC_EXPOSURE_MIGRATION.md)
- [参照資料と仕様](../../../../sources/README.md#ref-public-source-exposure-001)
- [横断分析の軸](../../../../docs/ANALYSIS_LENSES.md)

## Framework mapping

Enterprise ATT&CK v19.1の`T1593.003 Code Repositories`を、
`PUBLIC-EXPOSURE-1,2,4,5,6 / detects / medium / design-reviewed`として部分的に対応させます。
Public code repositoryから標的情報を探す攻撃経路に対し、本controlは同じ公開面で発見可能な露出候補を観測します。
攻撃者の検索行動そのものを検知する意味ではなく、public indexの完全性や実collectionを保証しません。

旧`T1552.001`、SSDF `RV.1.1`、OSPS `OSPS-BR-07.01`は対象成果との違いから非継承です。
版、旧関係、confidence、対象check、根拠、review日と判断理由は
[移行記録](../../../../docs/PUBLIC_EXPOSURE_MIGRATION.md#旧framework-mapping)に保持しています。
