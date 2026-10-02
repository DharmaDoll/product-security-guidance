# ファイルから消した秘密情報がpushで届く

[Control: PSB-SOURCE-002 Secret publication boundary](README.md) · [設計: Secret checks before publication](../../../../engineering/source-protection/secret-checks-before-publication/README.md)

開発者とリポジトリ管理者が、「何を調べ、どこで止めれば秘密情報を共有せずに済むか」を考える教材です。
守るのは認証情報や秘密鍵と、それらで操作できるサービスです。

## 二つのコミットを送る場面

開発者が設定ファイルへ認証情報を入れ、コミットしました。送信前に気付いたので、次のコミットで値を削除します。
手元のファイルはきれいになり、最新ファイルを調べるスクリプトも検出なしを返しました。

しかし、この二つのコミットをpushすると、最初のコミットにある値も送信対象になります。
共有先の履歴を読める人が過去のファイルを開けば、その値を取り出せます。
認証情報がまだ有効なら、ファイルを読む権限が別のサービスを操作する権限へつながります。

ここで必要なのは、最新ファイルの検査結果ではなく、**送る履歴にある内容の検査結果**です。
秘密情報を含むコミットを送信前に取り除く作業と、既に届いた認証情報を失効する作業も分けて考えます。

## 「手元のファイル」も一つではない

編集中のファイルを作業ツリー、`git add`で次のコミットに選んだ内容をステージ済みの内容（index）と呼びます。
値を含むファイルを`git add`した後、作業ツリーだけから値を消しても、コミット対象は更新されません。

そのため、commit前はステージ済みの内容とメッセージ、push前は送るコミットとその履歴を確認します。
ファイル以外に値が入る経路もあるので、何を検査するかは[SECRET-1・2](README.md#セキュリティ特性)で範囲を決めます。

## 「拒否した」は、どこで止めたかによって違う

Git hookは、commitやpushなどのタイミングでGitが呼ぶ処理です。
同じ検出ルールを使っても、実行場所によって止められる操作が違います。

| 検査する場所 | 拒否できた場合に言えること |
|---|---|
| 手元のcommit前 | 今回のコミット作成を止めた |
| 手元のpush前 | 今回送る対象の内容を、共有先へ送信する前に止めた |
| 受信側のref更新前 | 共有ブランチ・タグへの反映を止めた。ただし受信処理には内容が届いている |
| push後のCI | mergeや後続の利用を止められる。既に送った内容は未送信には戻らない |

Gitの受信側hook（`pre-receive`）では、受信した内容を一時的な隔離領域（quarantine）に置いてから判断します。
送信前に止めたいのか、共有先への反映を止めたいのかを選ぶ理由は、この違いにあります。

ローカルhookは利用者が省略・変更できます。全員へ配っただけで、共有先の必須検査が成立するわけではありません。
受信側の検査を独立させ、Web UIやAPIなど別の書込み経路も[設計pattern](../../../../engineering/source-protection/secret-checks-before-publication/README.md)で確認します。

実際の認証情報が共有先に届いたと分かったら、そのリポジトリが非公開でも所有者へ知らせ、誰に届き得たかと失効の要否を判断します。受信側で拒否された場合も、refへの反映がなかったことと送信先へ値が届かなかったことは別です。公開検索で見つからないことを待ったり、露出なしの根拠にしたりしません。

## 検出なしと、調べられなかった場合

検査器が動かない、履歴を取得できない、対応していない形式がある場合は、検出なしと判断する材料がありません。
必要な検査が終わるまで操作を止め、原因を直して同じ対象を調べ直します。
検出した値をログへ貼ると、検査自体が新しい漏えい先を作るため、調査には位置やルールなど最小限の情報を使います。

## 手元で試して、設計へ戻る

まずhookの動きと軽いルールを読んで試したい場合は[Python pattern scanner](../../../../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)、
受信側の独立検査や未対応入力の拒否まで確かめたい場合は[Git / Gitleaks例](../../../../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)へ進めます。
導入・smoke test・解除・製品ごとの制限は、各実装READMEを正本にしています。

試した後は、「この結果は今回のcommit、送る履歴、共有先の受入のどれに結び付いているか」を確認します。
一つの検出例の成功を、未対応形式やhookを通らない経路にも広げてはいけません。
診断のチェックリストは[controlの診断項目](README.md#failure-checks)で確認できます。

組織の既知経路外にある公開候補を探して判断へ渡す作業は[SOURCE-003の教材](../psb-source-003-public-source-exposure-triage/learning.md)、
認証情報や関連セッションの失効は[SOURCE-004](../psb-source-004-source-access-credential-lifecycle/README.md)、
漏えい後の被害範囲の調査・封じ込めは[GOV-004](../../governance-operations/psb-gov-004-credential-exposure-containment/README.md)へ引き継ぎます。

## 根拠と読み方

[REF-SECRET-PUBLICATION-001](../../../../sources/README.md#ref-secret-publication-001)のGit仕様を、実行場所と検査範囲の根拠にしています。
上の場面は本PJが作った説明用シナリオです。実装の代表経路の確認と、組織への導入・全書込み経路の確認は区別します。
