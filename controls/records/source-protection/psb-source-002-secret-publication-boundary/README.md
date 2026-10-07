# PSB-SOURCE-002 Secret publication boundary

**秘密情報を含む変更を、共有先へ送る前と受け入れる時点で見つけて止められるか。**

例えば、認証情報をコミットし、次のコミットで削除してからpushしても、値は送る履歴に残ります。最新のファイルだけを見て「検出なし」と判断できません。

## 満たすべきこと

1. **実際に送る内容を調べる。** 守る値と書込み経路を決め、コミット予定の内容、メッセージ、pushで導入する履歴を対象にする（SECRET-1〜2）。最新ファイル、作業ツリー、過去の検査結果だけで許可しない。読めない形式や対象外の範囲は「検出なし」に含めない。
2. **止める場所を分ける。** 手元のhookは送信前に止められるが省略できる。共有先でも、対象とする書込み経路で受入を判断する（SECRET-3〜5）。受入側が拒否しても送信先の受信処理には届いている。保存後のCIはmergeを止められても、送信前に戻すことはできない。
3. **検査不能と例外を管理する。** 検出、検出なし、失敗・未完了を区別し、必要な検査ができない変更を許可しない。ログや通知へ秘密値を写さず、誤検知の除外は対象・内容・期限・承認を限定する（SECRET-4・6〜7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- ステージ後に作業ツリーだけ直した場合や、過去コミットの値を最新コミットで消した場合も、実際に導入する内容を検査できるか。
- 新規ブランチ、複数ref、タグ、履歴書換え、merge結果、コミットメッセージで検査対象が欠けないか。履歴不足やLFSなど読めない内容を「検出なし」と扱っていないか。
- Hookを省略・変更しても、採用した共有先の受入制御が対象の混入を止められるか。Web UI・API・bot・mirrorと例外権限も確認しているか。
- 検査器の欠落、タイムアウト、設定の弱体化を許可に変えていないか。検出値を出力や例外申請に再掲していないか。
- 実際の認証情報が共有先へ届いたと判明したとき、非公開リポジトリや受入拒否を理由に影響調査を省略していないか。

これらは確認項目であり、すべての書込み経路で拒否を試した結果ではありません。試す場合は未発行の無害な検出用文字列を使います。

## このコントロールの範囲

対象はGitのファイル・メタデータ・履歴と、それらを共有する経路です。GitHub.comへ直接pushする場合、端末側hookとGitHub側で利用できるpush protectionの対象・設定・迂回条件は別に確認します。自前のGit受信先用`pre-receive`は[参考例](../../../../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)であり、GitHub.comには配置できません。

認証情報以外の顧客データなどは[SOURCE-008](../psb-source-008-sensitive-data-repository-admission/README.md)、端末での認証情報の保管は[SOURCE-007](../psb-source-007-developer-local-credential-storage/README.md)が扱います。実際の値が届いた場合は公開検索を待たず、所有者と[GOV-004](../../governance-operations/psb-gov-004-credential-exposure-containment/README.md)へ渡し、到達範囲・失効・利用履歴を確認します。履歴から値を消しても、既存のコピーや認証情報の効力は消えません。

検査を置く場所と実装例は[engineering](../../../../engineering/source-protection/secret-checks-before-publication/README.md)、履歴の場面は[教材](learning.md)を参照してください。７つの特性と参照資料IDは[control.yaml](control.yaml)、資料の採否は[Sources](../../../../sources/README.md#ref-secret-publication-001)、旧項目との対応は[移行記録](../../../../docs/MIGRATION_SOURCE_PROTECTION.md#git-hooks-migration)にあります。実環境への配布、GitHub側の設定、全経路の拒否は未確認です。
