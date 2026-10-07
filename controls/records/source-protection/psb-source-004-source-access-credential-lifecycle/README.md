# PSB-SOURCE-004: Source credential lifecycle

**Gitなどのソース管理に使う認証情報は、必要な人・処理と操作だけに使え、不要になったら確実に止められるか。**

たとえば、開発者のトークンを安全な場所に保管していても、すべてのリポジトリを書き換えられるなら、盗まれたときの被害は大きくなります。保管場所だけでなく、実際に使える権限と期間を確認します。

## 満たすべきこと

1. **権限を絞る。** 誰が、どのリポジトリで、何を、いつまでできるかを決める。発行や重要な変更では適切な本人確認を行う。自動処理には開発者個人の権限を使い回さない。
2. **使い道を守る。** 認証情報を保護された場所に置き、必要な処理だけへ渡す。現在使えるトークン・鍵・アプリの権限と所有者を把握し、発行・変更・利用・失効を調べられるようにする。
3. **古い権限を止める。** 退職、異動、端末紛失、用途終了などで、対象の認証情報と関連するセッションを失効させる。新しい値が使えることとは別に、古い権限でのアクセスが拒否されるか確かめる。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 一つのリポジトリを読むための認証情報で、無関係なリポジトリを書き換えられないか。
- 自動処理が開発者個人のトークンを使い、その人の退職後も動き続けられないか。
- 退職や端末紛失の後、トークンだけを止めても、既存セッションや別の鍵でアクセスできないか。
- 新しい認証情報へ切り替えた後も、古い認証情報で同じ操作が成功しないか。状態を確認できない場合に「失効済み」としていないか。

これらは確認項目であり、実環境で試した結果ではありません。

## このコントロールの範囲

対象は、ソース管理サービスが認める人と自動処理の権限、その認証情報とセッションです。開発端末の`.env`などに値を残さない方法は[SOURCE-007](../psb-source-007-developer-local-credential-storage/README.md)、漏えいが疑われた後の封じ込めと影響調査は[GOV-004](../../governance-operations/psb-gov-004-credential-exposure-containment/README.md)で扱います。権限を絞っても、既に複製されたソースコードは回収できません。

具体的な場面は[教材](learning.md)、認証情報の種類・保管と受け渡し・失効方法の選び方は[engineering](../../../../engineering/source-protection/source-access-credential-lifecycle/README.md)、GitHubでの設定例は[実装例](../../../../engineering/source-protection/source-access-credential-lifecycle/implementations/github/README.md)を参照してください。6つの特性と根拠のIDは[control.yaml](control.yaml)、資料の版と採否は[Sources](../../../../sources/README.md#spec-github-security-guidance)、フレームワークとの関係は[マッピング](../../../../mappings/frameworks.yaml)、旧成果物との対応は[移行記録](../../../../docs/MIGRATION_SOURCE_PROTECTION.md#source-credential-mapping)にあります。
