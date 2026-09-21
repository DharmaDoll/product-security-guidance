# AI runtime migration reconciliation

## 判断と範囲

旧PSB-AI-004の26項目を、開発環境向けの3つの設計パターンへ再配置しました。[Control記録](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)も10の特性へ再編集しました。製品adapter・検証器は保留です。
移行元は`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`の[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)です。製品自体のAI securityは[対象外](SECURITY_SCOPE.md)です。

## 旧項目と判断の正本

| 旧項目 | 残す判断 | 設計の正本 |
|---|---|---|
| AAR-001〜004、006〜007 | 隔離、保護対象、認証情報、通信、迂回、管理方針 | [Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md) |
| AAR-005、008〜011 | 公開承認、操作分類、対象・期限・再利用防止 | [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md) |
| AAR-012、018 | 拡張とtoolの同一性、実行時一覧の完全性と鮮度 | [Agent extension admission](../engineering/ai-development-security/agent-extension-admission/README.md) |
| AAR-013〜017 | 効果の限定、人の注意、実行前の強制、発行者の認証、不可分な消費 | [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md) |
| AAR-019〜021 | 監査の最小化、宛先と接続先の照合 | [Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md) |
| AAR-022〜024 | Hook障害、結果不明、commandの間接呼出し | [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md) |
| AAR-025〜026 | 端末網羅、配送・通知、収集元と順序の認証 | [Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md) |

旧仕様・根拠は[SOURCES](../sources/README.md#ref-development-runtime-reconciliation-001)と旧controlに保持します。旧サンプルの時間・回数・DB・署名方式を普遍的な要件へ変換しません。新しい実装方式の選択肢は、旧実装で確認済みの挙動と区別します。

## Control記録へまとめる方針

PSB-AI-004の中心は「開発agentに渡す実効権限を、外側の管理方針と現在の操作許可の範囲に収めること」とします。
AI-002は拡張を採用してよいかを所有し、AI-004側は実際の読み込み・呼出しがその承認と一致するかを所有します。認証情報の発行・失効はSOURCE-004、buildの実行境界はBUILD-001に残します。
この境界で10特性を定義し、旧15関係を設計上の直接対応・部分対応・保留へ再割当しました。移行先に旧実装があるかのような根拠文は持ち込みません。

## 未完了

- Framework mappingの正式な再レビュー。旧関係は移行レビュー中であり、実検証ではありません。
- 製品別の設定優先順位、hook失敗、拡張一覧、実通信、監査収集の現在の挙動の確認。
- 実装を移す場合の安全な拒否・並行消費・配送障害試験。
- 実環境の鍵管理、収集者の信頼、通知先、運用責任者の確認。

これらを完了したと推論せず、control記録は17件、patternは17件です。
