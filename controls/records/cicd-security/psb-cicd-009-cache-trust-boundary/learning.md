# Cache trust boundary — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)

## シナリオ：新しいrunnerへ古い攻撃が届く

信頼できないPRのテストが、後続jobも読める共有cacheへ改変したtoolを保存できる構成を考えます。
次のrelease jobは新しいVMで始まりますが、そのcacheを復元してtoolを実行します。
Runnerを毎回破棄しても、外部に保存した内容から高権限jobへ届く経路は残ります。

Cache keyが一致することは、内容が正しいことを意味しません。攻撃には、書き手がcacheを変更できること、
後のjobが同じentryを取得できること、その内容を信頼して実行することが必要です。
GitHubの通常の`pull_request`が作るcacheはPRのmerge refに限られ、default branchのrunが復元する範囲とは異なります。
PRが保存したという事実だけで上の三条件が揃ったとは判断せず、[実際の取得範囲と権限](../../../../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md#githubの具体化と確認)を確認します。

## 保存ファイルと、既に動かせる環境を分ける

このcontrolで再利用するのは、取得した配布ファイルを保管するdownload cacheです。
そのファイルも利用前に承認したhashと照合します。Keyは探すための名前、hitは見つかったという結果です。
どちらも内容の正しさや、その後に実行してよいことを証明しません。

展開済みの依存環境やtoolをそのまま戻すと、今回の取得・照合を通らないファイルも動かせます。
取得ファイルと展開済み環境の違いは[DEPS-003の教材](../../dependency-security/psb-deps-003-dependency-artifact-identity/learning.md)で確認します。
高速化の対象を取得だけへ絞るか、別の方式で環境全体を検証するかは別の設計判断です。後者をこのcontrolのcache許可へ含めません。

## 保存と利用の両方を見る

Cacheの判断では、keyだけでなく次を結び付けます。

- 誰がどのrevisionとjobから保存できるか。
- どのrepository、branch、OS、architecture、tool版、lockfileに使えるか。
- Consumerがcache内容を実行・公開する前に何を再検証するか。
- Exact keyが見つからないとき、どのprefixや古いentryへfallbackするか。
- 復元が途中で失敗したとき、専用領域の残存ファイルを採用せず、正規の取得と同じ照合へ戻れるか。

同じhostに残るprocessやworkspaceはcacheとは保存場所と管理者が異なります。
[Runner lifecycle isolation](../psb-cicd-007-runner-lifecycle-isolation/learning.md)で別に確認します。

## 保存されなかったのにjobが成功する

GitHubではcacheの権限により保存が拒否・省略されても、jobの成功表示が残る場合があります。
成功表示だけで保存制限を確認済みとせず、実効mode、ログと保存先を照合します。
取得を省略した表示も、完全な復元や依存検証の成功ではありません。[製品仕様の記録](../../../../sources/README.md#spec-ci-cache-boundary)を参照してください。

## 振り返りで問うこと

- 信頼できないjobが、より強い権限を持つjobのcacheを書けないか。
- 広いrestore prefixで別branch、別OS、別tool版のentryを受け入れないか。
- Cache hitによってhash照合、install、build等の必要な確認を飛ばしていないか。
- Cache削除や期限切れだけで、consumer側の再検証を不要としていないか。
- 復元の障害や情報不足と、完全一致するcacheが見つからなかった結果を区別しているか。

具体的な診断項目は[control](README.md#failure-checks)にあります。
未信頼の実行から権限処理への全経路は[Untrusted PR boundary](../psb-cicd-005-untrusted-pr-boundary/learning.md)へ進めます。

この教材は[cache仕様](../../../../sources/README.md#spec-ci-cache-boundary)、[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)と
[攻撃段階5→7→9](../../../../docs/ANALYSIS_LENSES.md)を使い、外部stateからconsumerへの受け渡しを
読み解くためのリポジトリ独自の解釈です。実環境のcache設定を確認した記録ではありません。
