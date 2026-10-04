# ENG-CICD-006: Workflow data and command boundary

外部入力を、固定した処理へデータとして渡す構成を選びます。CIの設計者が、**入力を渡す場所と、操作・対象を制限する場所**を決めるpatternです。[CICD-002](../../../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)が満たすべき特性を定め、[教材](../../../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/learning.md)が題名からコマンドが生まれる例を説明します。

## 入力から最後の解釈まで追う

最初に、値を変更できる人、届くイベント、実際に動くshell・言語・プログラム、そこで選べる操作を確認します。値の出所と使用箇所を結び、途中で出力やファイルに変わっても追います。

```text
外部の題名・本文・入力、上流の出力
  → 環境変数・構造化した引数・入力API
  → 固定した命令でデータを読む
  → 操作を選ぶ場合だけ、許可した名前・対象へ照合
  → 呼出先でも命令とデータを分けた処理
```

直接のコード生成を除く場所、引数を保持する場所、許可する意味を確認する場所は別です。一つの対策で全部が成立したとは扱いません。生成したスクリプト、設定、ログを別の処理が読み直す場合、その形式で値が命令や制御情報にならないかも確認します。

## 方式を選ぶ

| 方式 | 向く場面 | 確認する代償・失敗経路 |
|---|---|---|
| 固定したinline scriptへ環境変数で渡す | 少数のstepを直す。新しいActionを増やさずにコード生成を除ける | 対象shellで引数を保持する。評価命令や再補間が残ると分離が失われる |
| レビューしたAction・ライブラリへ構造化した入力を渡す | 既存の処理APIが使える。データからshell命令を作る必要を減らせる | 呼出先の内部処理と追加取得を確認する。`with:`や引数配列という形だけで安全とは判断しない |
| 許可した名前から固定の処理へ対応させる | 利用者が作業名や対象を選ぶ | 許可する値と実際の処理を対応させる。自由な命令文字列、任意のパス、任意のオプションを受け取らない |

自由な文章を使うだけなら、作業名向けの狭い文字制限へ押し込む必要はありません。操作・対象を選ぶ値は、その意味に応じて限定します。オプション終端の`--`は、呼出先が対応し、その位置で効く場合に使います。対象の所有・認可・パス境界までは保証しません。

## 受入時の確認を選ぶ

レビューでは、入力から解釈箇所までの流れを確認します。静的な検査を使う場合も、対象となるworkflow、composite Action、呼出先スクリプトを明示し、findingと解析不能、対象外を分けます。表示用の式をshell注入として数える検査は、実行箇所を確認する検査と区別します。

GitHubの`run:`への直接式をすべて禁止する規則は、組織が選べる厳しいprofileです。制約された値も拒否する代償があり、すべてのfindingが同じ攻撃可能性を持つわけではありません。逆に、その規則を満たしても、環境変数の再評価や呼出先の引数解釈は別に確認します。禁止文字の検索だけでcontrol全体を証明しません。

検査を必須にする構成では、検査定義・実行コード・受入設定の変更保護まで接続します。Scannerの固定取得、実行障害、対象revisionと結果の結び付きは[Scanner acquisition and evidence boundary](../../detection-verification/scanner-acquisition-and-evidence-boundary/README.md)へ渡します。Workflow検査とmerge判断の接続は[Workflow analysis gate and reporting](../workflow-analysis-gate-and-reporting/README.md)で検討できます。

## 隣接する責任と完了範囲

外部Actionの版は[Reviewed workflow dependency binding](../reviewed-workflow-dependency-binding/README.md)、使える権限は[Purpose-bound job authority](../purpose-bound-job-authority/README.md)、未信頼コード・artifact・cacheの昇格は[Untrusted PR boundary](../untrusted-pr-boundary/README.md)、host・残留状態は[CI state and runner lifecycle](../ci-state-and-runner-lifecycle/README.md)へ引き継ぎます。入力をデータとして渡しても、悪意あるコードを権限付きjobで実行する問題は残ります。

今回は方式の選択、失敗経路、[診断項目](../../../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md#診断で確認する項目異常時テスト)で完了とします。既存ガイダンスで入力の渡し方を判断できるため、独自scanner、配布workflow、中央サービスは追加しません。将来の独自実装は、既存の確認方法で残る具体的な不足と、導入・保守に見合う効果が説明できる時に選びます。

主にplatform and infrastructure、攻撃段階5の値から命令への変換を扱います。段階2の変更保護と段階6の権限を隣接条件として読み、段階7の実行境界、段階9の成果物、段階12の影響調査へ渡します。実GitHubの拒否、対象製品・全shellの入力処理は未確認です。[参照資料](../../../sources/README.md#ref-workflow-input-001)と[移行判断](../../../docs/MIGRATION_CI_CD.md#workflow-input-migration)を参照してください。
