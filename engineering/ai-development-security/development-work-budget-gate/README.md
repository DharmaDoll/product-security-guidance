# Development work budget gate

`ENG-AI-006` / `ai-development-security`

## 解く設計問題

開発agentの一依頼がmodel・tool呼び出しを重ねても、どこで残り予算を確認し、誰が新しい処理を止めるか。[AI-007](../../../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)のDEV-BUDGET-1〜6を具体化します。製品のAI機能の予算設計は[別PJ](../../../docs/SECURITY_SCOPE.md)へ委ねます。

例えばテスト修正を繰り返すCI agentでは、一度のtool実行の許可だけでは、修正とテストの反復が終わりません。必要な境界は、agentの提案から次の実行へ進む地点と、一作業を存続させる外側の実行環境です。

```text
管理者が決めた作業ID・上限・実行期限
       ↓
agentの次の提案 → 個別操作の認可（AI-004）
       ↓
model／toolを実行する側で、同じ作業の残り予算を予約
       ├─ 上限・必要情報の欠落 → 新規実行を拒否、停止理由を保存
       └─ 許可 → 実行 → 実消費と結果を照合
外側の実行期限 → ローカル停止、外部の結果不明は別に照合
```

## 最初に選ぶ上限

| 方式 | 使える判断 | 制約・代償 |
|---|---|---|
| 外側のprocess／job実行期限 | ローカル作業をいつまで存続させるか | 統合が少なく始めやすい。API費用、呼び出し数、別jobや送信済みの遠隔処理は制限しない |
| Agent製品の呼び出し・turn制限 | 選んだ製品が数える反復をどこまで許すか | 数え方、再開・子agent・内部retry、tool実行との関係を公式仕様と採用先で確認する。製品名だけで効果を推定しない |
| Model・tool実行側の共通予算管理 | 複数の経路・並列処理を同じ作業の上限へ結ぶ | 信頼できる作業ID、予約の不可分な更新、取消・結果不明の管理が必要。独立にAPIへ接続できる認証情報があると迂回される |
| Provider／組織のquota | 複数作業の合計消費を抑える | 一作業の終了や他作業への配分を決める仕組みは別に必要。通知だけの設定をhard capと扱わない |

採用時には必要な量と単位を選びます。費用・token、時間、tool回数、再試行、同時実行・子作業の上限は互換ではありません。全てを一律に必須とせず、測定・制限できない量と、それが守れない資産を明示します。

## 残り予算を実行へ結ぶ

作業IDはagentが自由に選ぶsession名から作らず、依頼を受け入れる側で割り当てます。同じ依頼の再開や子作業へは元のIDと残り予算を渡します。追加枠は管理者の明示的な判断で変更し、上限超過を隠す再起動にしません。

各実行前に、使用済み量に加えて未完了の予約を差し引き、次の要求の分を不可分に確保します。Model費用を厳密に制限する場合は、次の入力と最大出力、適用するmodel・料金・単位などを固定できることが条件です。消費の上界が分からない経路で「費用のhard cap」を主張しません。応答後の実消費を照合して予約を調整しますが、タイムアウトした要求の分を、未実行と決めつけて返却しません。

Toolの内部再試行や直接接続がこの境界を通らない場合は、その側の上限を別に設けるか、利用できる経路を狭めます。Agentが予算台帳や停止設定を変更できないよう、実行設定・認証情報・通信は[AI-004](../../../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の外側の管理境界に置きます。

## 上限で止まる経路

警告は任意の補助です。警告の通知だけで実行を止めた扱いにしません。上限到達や必須の計測・予約処理の障害では、次のmodel・tool実行を許可しません。既に動いているローカル処理の終了期限と、送信済みの外部変更の照合を分けます。Cleanup・要約を許可する場合も、先に予約した有限の枠を使います。

通常終了、上限による停止、起動失敗、判定不能、外部の結果不明を別に記録します。作業ID、方針版、必要な計測と未完了の割当、停止理由を残し、prompt全文・tool引数・ソース・認証情報を集約しません。予算以内でも承認再利用や停止機構の障害があれば[操作認可](../development-action-authorization/README.md)と調査担当へ渡します。全端末の封じ込め・復旧完了は別の責任です。

## 実装で確かめる

[Linux timeout](implementations/linux-timeout/README.md)は、GNU coreutils 9.7で非対話のprocessを実行期限に結ぶ限定例です。正常終了、コマンド失敗、期限による停止、TERMを無視した場合のKILL、同じprocess groupの子process、起動不能を手元で観測します。これはelapsed timeの一部分で、model費用や呼び出し予約の実装ではありません。別session・別jobや親の早期終了で残るprocess、遠隔処理の完了は保証しません。

各呼び出しの予算管理は、agent・版、modelとtoolの接続、利用量・料金の取得元、実行前に拒否する位置を選んでから限定実装へ進みます。[診断項目](../../../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md#診断で確認する項目異常時テスト)で再開・並列・障害・迂回を確認し、宣言と実拒否を分けます。

[教材](../../../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/learning.md)、[参照資料](../../../sources/README.md#ref-development-work-budget-001)、[移行判断](../../../docs/MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)へ続きます。
