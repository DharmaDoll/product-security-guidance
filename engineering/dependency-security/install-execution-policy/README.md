# ENG-DEPS-002: Install execution policy

## 利用場面

依存パッケージの準備で外部コードが動き、開発端末やCIの権限を使える設計を見直すときに使います。
読者は、実行をなくす方式と、必要な実行を限定する方式を選べるようになります。

## 推奨構成と信頼境界

```text
保護されたpolicy・レビュー済みgraph・artifact identity
  → 実行を伴わない取得と照合
  → 準備用コードが必要か判定
       ├ 不要: script・source buildを拒否
       └ 必要: 対象を限定して承認 → 権限・通信を絞った使い捨てbuild
  → 準備済みの内容を固定 → 別の実行境界でimport・test
```

公開者は準備用コードを変更できますが、そのコード自身が実行許可や実行環境の権限を決める構造にしません。
PRでpolicyを変えられる場合、同じPRの変更を自動的に信頼する検査は強制点になりません。

## 方式を選ぶ

| 方式 | 適する状況 | 代償・失敗経路 |
|---|---|---|
| install-time executionを全面停止 | scriptが不要、承認済みwheel等で機能を満たせる | native機能が不足する場合がある。失敗時にsource fallbackを追加すると境界が消える |
| native approvalを対象限定で使う | 特定packageの準備処理が必要 | 製品によって許可単位が異なる。名前だけの許可で将来versionへ広げない |
| 独立した隔離buildで準備する | source buildが必要、通常CIに高価値資産がある | build用依存、出力の同一性、引き渡しの設計と運用コストが増える |

必要な実行は、package公開、署名、deploy用の認証情報やhost管理socketから分離します。
通信は必要な取得先に限定し、後続へ渡す内容を固定します。この隔離は、installの許可機能とは別の設計です。

## 観測する状態

未承認の準備処理を持つ無害なpackageで、backendやhookが起動しないことを確認します。
許可するpackageも確認し、拒否設定で機能が壊れた状態を見逃さないようにします。
設定文字列の検査と、実際の起動抑止の検査を別の結果として扱います。

## 関係と限界

[Cooldown](../dependency-release-cooldown/README.md)は観測時間を確保し、このpatternは実行許可を配置します。
取得内容の完全性、許可したbuildの隔離、後続のimport・test、runner破棄は別途必要です。
七レイヤーの外部依存からプラットフォーム・ガバナンスへ、攻撃段階4から7へ責任を接続します。

- [pip実装例](implementations/pip/README.md)
- [control](../../../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)
- [仕様・採否・未確認の製品候補](../../../sources/README.md#spec-install-execution-policy)
- [横断分析](../../../docs/ANALYSIS_LENSES.md)
