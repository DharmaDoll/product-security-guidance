# ENG-SOURCE-004: Public exposure observation and triage

対応するコントロール：[PSB-SOURCE-003](../../../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)

対象読者はProduct Security、AppSec、source hosting管理者、incident response担当者です。
公開面の検索を単発のdork collectionにせず、観測範囲、candidate state、triage、response handoffを
一つの運用経路として設計します。

## 攻撃が成立する条件

外部の攻撃者は組織のrepository一覧を知らなくても、domain、email suffix、endpoint、製品名などから
公開codeや開発上の会話を探せます。防御側が既知repositoryだけを検査している場合、個人repository、fork、mirror、
Gist、Issue、Pull Request、外部indexにあるcopyが観測範囲から外れます。

観測serviceが候補を返しても、ownerが決まらず、match値をchatへ複製し、通知失敗を記録せず、
content削除だけでcredentialを有効なまま残せば、security outcomeは成立しません。

## 設計する経路

```text
所有を確認したindicatorと許可したsurface
  -> provider別のquery・collector
  -> coverageとhealthを伴う観測
  -> 値を最小化したcandidate
  -> occurrence stateと再出現判定
  -> ownerによるtriage
  -> content owner / credential owner / incident response / platform owner
```

各矢印は別の失敗点です。Collectorの成功を通知成功や対応完了へ読み替えません。

## 最初に決めること

| 判断 | 決める内容 | 決めないまま進んだ場合 |
|---|---|---|
| Ownership | Domain、repository namespace、製品名などを誰が所有確認するか | 第三者情報を過剰収集し、対象範囲を説明できない |
| Observation scope | Provider、public surface、query、時刻範囲、cursor、手動確認 | 0件の意味と未観測範囲が分からない |
| Data handling | Match本文を誰がどこで見られ、何をstate・ticket・通知へ残すか | 防御処理がcredentialや個人情報の新しいcopyを作る |
| Occurrence identity | Provider object、repository、path、content revisionをどう結ぶか | 変更や再出現を既知扱いし、または同一候補を通知し続ける |
| Disposition | Owner、reason、expiry、再確認条件 | 意図した公開やfalse positiveが永久除外になる |
| Handoff | Candidate種別ごとのresponse ownerと受領確認 | Content削除、credential失効、影響調査の間に責任の空白ができる |
| Health | 最後の成功、部分取得、state・notification失敗をどう知らせるか | 監視停止期間がclean observationに見える |

## 観測手段の選び方

複数の手段は代替関係とは限りません。Coverageと運用責任を明示して組み合わせます。

| 手段 | 向く範囲 | 主な限界 |
|---|---|---|
| Source hosting providerのsecret scanning・push protection | Providerが受け入れるcontentの早期検出・拒否 | Provider外、未対応secret、過去copy、設定した対象外surfaceを網羅しない。SOURCE-002の境界 |
| Providerのcode・Issue・PR・Gist検索 | 攻撃者から発見できるcurrent public surfaceの候補 | Index、result上限、rate limit、scope、truncation、query構文に依存 |
| 一般Web index | Provider外のcacheやpublic pageを含む候補探索 | Index時刻とcoverageが不明で、owner attributionと誤検知対応が必要 |
| Organization inventoryとのvisibility照合 | 意図しないpublic repositoryやowner逸脱 | Inventory外の個人copy、fork、Gist、本文内の情報を単独では見つけない |
| 外部attack-surface service | 複数provider・domainを横断した運用 | 収集範囲、data handling、削除、retention、healthをservice契約で確認する必要がある |

Provider固有のqueryやAPI parameterは、将来の`implementations/`へ置きます。Pattern本文に固定しません。

## Coverageを結果へ結び付ける

観測記録には少なくとも、collectorまたはquery catalogのidentity、対象providerとsurface、開始・終了時刻、
cursorまたはtime range、取得page、providerが返した不完全状態、最後の成功、未対応surfaceを含めます。

Candidate数が0でも、次のいずれかがあれば完了扱いにしません。

- 認証または権限が期待したpublic viewと一致しない。
- Result cap、timeout、pagination、truncationへ到達した。
- Provider responseの形式を解釈できない。
- Candidate stateを読み書きできない。
- Notificationまたはcase作成に失敗し、担当者の受領を確認できない。
- 前回成功から定めた観測間隔を越えている。

Providerが「部分結果」を返し得る場合、candidate eventとcoverage degradationを別々に記録します。

## Match値を複製しない

Candidate stateと通知には、担当者が原位置を確認するためのprovider、object ID、repository、path、URL、
indicator IDなどを残します。Match snippetやtoken全体を保存する必要がある場合は、access、retention、削除、
監査を別途決めます。通常のchat、公開Actions log、長期artifactへ値を送らない設計を優先します。

Redactionは値を短く表示するだけでは足りません。同じ値がexception text、error、debug output、HTTP trace、
notification retry payloadへ流れないことを確認します。

## Occurrenceと判断のstate

一つのcandidateには、観測したprovider object、場所、内容のidentity、indicatorを結び付けます。
表示名、検索順位、取得時刻だけをidentityにしません。

| 状態 | 次の判断 |
|---|---|
| 初めて観測 | Ownerを割り当て、公開意図と影響を判断する |
| 同じoccurrenceを継続観測 | Last seenを更新し、未判断なら期限を越えて閉じない |
| Content identityが変化 | 同じpathでも再判断する |
| 意図した公開・false positive | Exact occurrence、owner、reason、expiryの範囲だけ抑制する |
| 是正後に再出現 | 新しい対応対象として開き直す |
| Searchから消失 | Index変動、削除、非公開化、取得失敗を区別するまで自動で是正完了にしない |

Stateへのwrite authorityはcollectorの入力から分離します。未信頼のpublic contentやPull Requestがquery、
抑制、cursor、notification destinationを変更できないようにします。

## Triageとresponse handoff

Candidateはまず、対象が自組織に属するか、意図した公開か、どの資産やidentityに影響するかを判断します。
Matchした文字列を実serviceへ提示して有効性を試すことは、このpatternの検証方法ではありません。

| Candidate | 主なhandoff |
|---|---|
| Credential、key、token、session情報 | Credential ownerとincident response。失効、関連session、利用履歴、派生権限を確認 |
| Internal endpoint、network・cloud設定 | Platform owner。公開到達性、認証、log、設定変更の必要性を判断 |
| Source code、設定、設計資料 | Repository・product owner。公開権限、copy、履歴、downstream利用を確認 |
| 個人情報・customer情報 | Privacy・legalを含む組織手順。一般ticketへ本文を複製しない |
| 意図した公開情報 | Exact occurrenceの期限付きdecision。将来の変更を自動承認しない |

## 実装例を今回追加しない理由

この主題には、provider検索、native secret scanning、Web index、外部serviceなど複数の実装経路があります。
GitHub Actions、Python collector、専用Git branchを選ぶことは自明ではなく、result上限、認証view、retention、
case management、組織のresponse運用に依存します。

旧PoCの具体実装は移植せず、[移行記録](../../../docs/PUBLIC_EXPOSURE_MIGRATION.md)に役割と限界を保持します。
実装例を追加するのは、採用provider、対象surface、state store、notification、response ownerを選び、
対象版、変更箇所、確認方法を具体化できる場合です。

## 確認方法

このpatternのレビューでは、[controlの診断で確認する項目](../../../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md#failure-checks)を使い、
provider固有の制限、state遷移、値の取扱い、healthとfindingの通知経路を確認します。
Synthetic fixtureやquery生成の成功だけで、実際のcoverage、candidateなし、通知、response完了を証明しません。

## 限界

Public searchは完全な履歴・copy inventoryではありません。監視頻度を上げても、indexされる前に取得されたcopy、
削除後のcache、private共有、screenshotを回収できません。このpatternは意図しない公開を減らし対応を早めますが、
SOURCE-002の事前拒否、SOURCE-004のcredential lifecycle、incident responseを置き換えません。
