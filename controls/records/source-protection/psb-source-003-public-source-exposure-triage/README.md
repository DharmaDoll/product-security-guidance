# PSB-SOURCE-003: Public source exposure triage

設計する：[Public exposure observation and triage](../../../../engineering/source-protection/public-exposure-observation-and-triage/README.md)

## 問い

自組織に関係するsource codeと開発上の会話が公開面へ現れていないかを反復して観測し、
観測できなかった状態を「候補なし」と区別し、新規・再出現した候補を所有者の判断と対応へ渡せるか。

## できてはいけないこと

意図しないsource、credential、内部endpoint、設定、組織固有情報が第三者から発見できる状態にあるのに、
検索範囲の欠落、collector障害、期限切れの判断、重複抑制、通知失敗によって未対応のまま残してはいけません。

## 起点となるシナリオ

開発者が個人repositoryのIssueへ内部endpointを貼り、後で本文を編集しました。既知repositoryだけを検査する運用は
この投稿を観測できません。検索結果から一度消えたことを是正完了と扱うと、別のforkやGistへ再投稿された場合も
既知扱いで通知されません。Credentialらしい値が含まれる場合、投稿の削除だけを行って失効を忘れる危険もあります。

このcontrolは、外部から発見できる候補の観測、状態管理、triage、対応先への引渡しを扱います。
公開を事前に拒否する境界や、credential漏えい後の封じ込めそのものは別の責任です。

## 適用範囲

組織が観測を許可した識別子から探せる、public repository、source file、commitに関連する公開情報、
Issue、Pull Request、Gistなどの開発上の公開面に適用します。Source hosting providerの検索、provider API、
一般Web index、承認済みの外部監視serviceは観測手段の候補です。

次は直接の対象ではありません。

- Private repository、端末、社内networkを探索すること。
- 第三者資産へのlogin、credential validation、active probing、脆弱性悪用。
- 既知repositoryのcommit前検査と受入拒否。
- 公開候補を脆弱性またはincidentとして自動確定すること。
- Credentialの失効、利用履歴の調査、公開copyの削除、法務・広報判断を実行すること。
- 外部attack surface全般のinventory、port scan、domain takeover検査。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `PUBLIC-EXPOSURE-1` | 観測対象を、所有を確認した識別子、許可したprovider・surface・query、禁止する探索方法と結び付ける |
| `PUBLIC-EXPOSURE-2` | 観測ごとにqueryまたはcollectorの版、対象surface、実行時刻、cursor・範囲、provider上限、未観測範囲を追跡できる |
| `PUBLIC-EXPOSURE-3` | Matchした値と周辺contentの収集・表示・保存・通知を必要最小限にし、credentialや個人情報を新たな露出経路へ複製しない |
| `PUBLIC-EXPOSURE-4` | Candidateを安定したoccurrenceへ結び付け、初出、継続、変更、判断期限切れ、是正後の再出現を区別する |
| `PUBLIC-EXPOSURE-5` | Candidateの所有者、意図した公開か、影響する資産・credential、必要なresponse owner、判断と期限を記録し、未判断を閉じない |
| `PUBLIC-EXPOSURE-6` | 認証、rate limit、pagination、truncation、timeout、parse、state更新、通知の失敗とstaleな観測を、完了した0件から区別する |

## 実装判断の羅針盤

1. 最初に「誰が何を所有し、どの公開面への検索を許可したか」を決める。検索語の多さから始めない。
2. Providerが返した候補と、実際に観測できた範囲を同じ記録へ結び付ける。結果件数だけを証拠にしない。
3. Match本文をそのままticket、chat、logへ複製せず、担当者がアクセス制御された原位置で確認できる参照を使う。
4. Pathや表示名だけで同一候補とみなさず、provider objectと内容の変更を再判断できるoccurrenceを使う。
5. 「意図した公開」「false positive」「是正済み」には所有者、理由、期限を持たせる。無期限の抑制にしない。
6. Credentialが疑われる場合は、content削除だけで閉じず、失効・session・利用履歴・派生権限の担当へ渡す。
7. 観測のhealthとfindingを別に通知する。Collectorが止まった期間をcandidateなしとして扱わない。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は、公開情報の収集・判定・引き渡しで見落としてはいけない操作や異常の確認項目です。脆弱性診断や
設計レビューに利用できます。項目を記載しただけであり、本PJがテストを実行したことを意味しません。

- 所有を確認していないdomain、個人識別子、実credential値、対象を限定しないgeneric queryを送れる。
- Public-onlyの攻撃者視点を評価する処理がprivate repositoryを読めるidentityを使い、結果の意味を変える。
- Search result cap、timeout、`incomplete_results`、pagination欠落、truncated contentを0件として受理する。
- Match snippet、email local part、token、authorization headerがlog、artifact、state、通知へ残る。
- Repository名やpathだけで重複を潰し、内容変更・fork・mirror・再投稿を再判断しない。
- `accepted-public`や`false-positive`にowner・reason・expiryがなく、将来の変更も永久に抑制する。
- Searchから消えたことだけで`remediated`にし、削除、非公開化、index変動、取得障害を区別しない。
- State更新または通知に失敗したのにcursorを進め、次回の観測対象から候補が落ちる。
- Credential候補に対しcontent削除だけを行い、old authorityの拒否確認へ渡さない。
- Collector、query、stateを未信頼のrepository変更が書き換えられ、監視対象や抑制状態を隠せる。

## 判定例

| 観測した状態 | このcontrolでの判断 |
|---|---|
| Provider検索が成功し、候補0件だがresult上限への到達を確認していない | 合格を裏付けない。Coverageが不明 |
| Candidate URLと所有者だけをticket化し、matched tokenは原位置で限定確認する | 値の複製を抑えたtriage evidenceになり得る |
| 同じpathのcontent identityが変わったが、既知findingとして通知を抑えた | 不合格候補。変更後のoccurrenceを再判断できない |
| Provider障害を別のhealth alertとして通知し、最後の成功時刻が見える | `PUBLIC-EXPOSURE-6`を支えるが、候補がない証明ではない |
| 公開credentialを削除し、失効・session拒否・利用履歴調査を別のresponse記録へ渡した | このcontrolからresponseへのhandoffが成立し得る |

## 保証しない範囲

検索providerとindexは公開情報の完全な写像ではありません。削除済みcontent、過去clone、cache、screenshot、画像、
binary、分割・難読化された値、providerがindexしないsurfaceは残り得ます。0 findingsは、宣言した範囲の観測が
完了したことだけを示し、公開露出が存在しないことや、過去に存在しなかったことを保証しません。

## 関連資料

- [Public exposure observation and triage](../../../../engineering/source-protection/public-exposure-observation-and-triage/README.md)
- [GitHubの公開コード・Issue・PRを少数の指標で探す実装](../../../../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)
- [Secret publication boundary](../psb-source-002-secret-publication-boundary/README.md)
- [Source credential lifecycle](../psb-source-004-source-access-credential-lifecycle/README.md)
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
