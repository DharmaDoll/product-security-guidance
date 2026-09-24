# PSB-DESIGN-001: Object access authorization

学ぶ：[Authentication is not object authorization](learning.md) ·
設計する：[Object access boundary](../../../../engineering/secure-design/object-access-boundary/README.md) ·
試す：[Python / SQLite implementation](../../../../engineering/secure-design/object-access-boundary/implementations/python-sqlite/README.md)

## 問い

認証済みの利用者が対象IDや入力内容を変更しても、その利用者に許可されたtenant、対象、操作だけを実行できるか。

## できてはいけないこと

正規にログインした利用者が、他の利用者やtenantの対象を読み取り、変更、一覧、exportできてはいけません。
Requestに含まれるownerやtenantを許可の根拠として受け入れたり、認可情報を確認できない状態で処理を許可したりしてはいけません。

## 適用範囲と非適用

認証済み主体、対象ID、tenant、操作、DBにある所有関係、一覧・検索・batch・非同期処理を含む対象への到達経路が対象です。
利用者の認証方式、session保護、管理者権限の設計、入力値そのものの安全性、監査基盤全体は別の主題です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `OBJECT-AUTH-1` | 利用者とtenantを、request bodyや対象IDではなく、信頼できる認証済みcontextから取得する |
| `OBJECT-AUTH-2` | 対象のownerとtenantをサーバー側の記録から取得し、要求者との関係を照合する |
| `OBJECT-AUTH-3` | Read、update、delete、export等の操作ごとに許可を判断し、別操作の許可を流用しない |
| `OBJECT-AUTH-4` | 対象の取得・変更条件へ利用者とtenantを含め、許可確認後の対象差替えを防ぐ |
| `OBJECT-AUTH-5` | 単体取得だけでなく、一覧、検索、batch、非同期処理、cache等の到達経路へ同じ判断を適用する |
| `OBJECT-AUTH-6` | 認証context、所有関係、認可dataを確認できない場合は処理を許可せず、障害として区別する |

## 実装判断の羅針盤

認証は「誰か」を確認しますが、「この対象へこの操作をしてよいか」は決めません。対象IDは未信頼の指定として扱い、
許可に使うowner、tenant、権限はサーバー側から取得します。更新では、許可判断とDBの変更条件が離れるほど、
途中の状態変更や実装漏れで別対象を変更する危険が増えます。

共通middlewareだけに任せず、対象を取得・変更する場所でも利用者、tenant、操作を結び付けます。
拒否と「存在しない」を同じ応答にしても、件数、時間、一覧結果等から対象の存在が漏れないか別に確認します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。チェックリストとして使えます。
[限定した実装例](../../../../engineering/secure-design/object-access-boundary/implementations/python-sqlite/README.md)では一部を実行していますが、
本PJが実際のアプリケーション全体を診断した結果ではありません。

- 利用者Aが利用者Bまたは別tenantの対象IDを指定しても、読取り・変更・削除・exportできないか。
- Read権限だけを持つ利用者がupdate等の別操作を実行できないか。
- Request bodyの`owner_id`や`tenant_id`で、サーバー側の所有関係を書き換えられないか。
- 一覧、検索、batch、非同期job、cacheから同じ対象へ到達しても認可を省略できないか。
- 認証context不足、DB timeout、認可data取得失敗を、対象なしや許可として扱っていないか。
- 許可確認後にownerやtenantが変わった場合、古い判断で変更を続けないか。

## 境界と受け渡し

このControlはアプリケーション層の悪用経路を直接扱い、サプライチェーン攻撃の段階へ無理に割り当てません。
正規のsource、build、署名済みartifactでも認可欠陥は残ります。HTTP認証、すべてのendpoint、並行更新、
管理者・service accountの権限、組織への導入は個別実装と評価で確認します。

## 参照資料とマッピング

- [REF-APPLICATION-AUTHORIZATION-001](../../../../sources/README.md#ref-application-authorization-001)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
