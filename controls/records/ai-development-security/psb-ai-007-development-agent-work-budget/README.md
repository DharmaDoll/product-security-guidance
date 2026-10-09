# PSB-AI-007 Development agent work budget

**開発agentの一つの作業が、決めた時間・費用・呼び出し回数を超える前に止まるか。**

## なぜ必要か

例えばCI上のagentがテスト修正を繰り返すと、個々の操作に問題がなくても、外部サービスへの負荷や費用が増え続けます。「そろそろ止めて」と指示するだけでは上限になりません。

## 満たすべきこと

1. **上限を作業に結び付ける。** 責任者、作業の範囲、必要な上限をagentの外側で決める。同じ作業の再開、再試行、子作業で残り予算を初期化しない（DEV-BUDGET-1）。
2. **次の処理を始める前に判断する。** 必要な利用量と実行中の割当を把握し、model・toolの次の呼び出しが使う分を実行側で確保する。並列処理も同じ残り予算を使う。経過時間は外側の実行期限で制限し、計測できない量をゼロにしない（DEV-BUDGET-2〜3）。
3. **止まったことを確かめる。** 上限到達や必要な計測の障害では新しい処理を許可しない。停止理由と結果不明の外部操作を分けて追跡し、承認の再利用や停止処理の故障も担当者へ渡す（DEV-BUDGET-4〜6）。

## 診断で確認する項目（異常時テスト）

- 作業を再開・分割しても、新しい予算で同じ依頼を続けられないか。
- 並列の呼び出しが同じ残り予算を二重に使わないか。内部の再試行や別のAPI接続が上限を迂回しないか。
- 利用量が欠けたとき、古いとき、単位が分からないときに、新しい処理を止められるか。
- 実行期限で親だけが止まり、子プロセスや別jobが動き続けないか。送信済みの外部変更を未実行と決めつけて再送しないか。
- 上限以内の処理でも、承認されていない操作や停止経路の故障を見逃していないか。

これらは確認項目であり、実agentの費用や呼び出しを制限した結果ではありません。

## フレームワークとの関係

開発agentの一作業に使える時間・費用・呼出し回数について、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に個別の関係は登録していません。一般的な資源制限や製品AIの要件を、そのままこの開発環境のControlへ割り当てません。

## このコントロールの範囲

対象はIDE・CLI・repository連携・CIで使う開発agentの一作業です。[製品のAI機能](../../../../docs/SECURITY_SCOPE.md)と組織全体の支出上限は扱いません。[AI-004](../psb-ai-004-development-agent-runtime-boundary/README.md)は「その操作をしてよいか」、AI-007は「許可された処理をどこまで続けてよいか」を判断します。予算が残っていることは操作許可になりません。停止しても、漏えいした認証情報の失効や、既に送った外部変更の復旧は別途必要です。

時間・費用・呼び出し数で異なる実現方法は[engineering](../../../../engineering/ai-development-security/development-work-budget-gate/README.md)を参照してください。[Linux timeoutの例](../../../../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)はローカルの実行時間だけを扱います。6つの特性と根拠のIDは[control.yaml](control.yaml)、学習用の場面は[教材](learning.md)、資料の採否は[Sources](../../../../sources/README.md#ref-development-work-budget-001)、旧項目との対応は[移行記録](../../../../docs/MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)にあります。
