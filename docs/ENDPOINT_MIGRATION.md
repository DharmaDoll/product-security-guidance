# Developer endpoint migration reconciliation

対象は旧`PSB-SOURCE-001`、domainは`source-protection`です。2026-09-21に29項目を棚卸しし、
[Managed developer endpoint](../engineering/source-protection/managed-developer-endpoint/README.md)へ端末管理の設計を先行移行しました。
Control記録、旧framework mapping、製品実装はまだ移行していません。

## 根拠と受入条件

移行元はコミット`3bfbeb21246bb2f58c55fa5212068805bca1719b`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/control.yaml)、
[実装ガイド](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/check-implementation-guide.md)です。
提供原文とbaselineの出自・採否は[参照資料記録](../sources/README.md#ref-developer-endpoint-baseline-001)へ保持します。

受入条件は、全29項目の追跡、端末管理と隣接領域の責任分界、状態悪化からアクセス制限への接続、
観測失敗と違反の区別、端末・製品設定を確認していない範囲の明示です。架空の安全／危険設定や検査成功を追加しません。

## 29項目の配置

`design-migrated`は設計判断の先行移行、`adjacent`は隣接する成果物への受け渡しです。
`adjacent`は旧項目の完全な移行や実装済みを意味しません。本文全体を複製せず、未対応部分を残します。

| 旧check | 主題 | 扱い | 配置・残る境界 |
|---|---|---|---|
| DEH-001 | 短命な認証情報 | adjacent | [SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)。ソース管理以外のクラウド等の認証情報は別途必要 |
| DEH-002 | 保護された保管 | adjacent | SOURCE-004。承認済み保管場所と実行中のアクセスを分ける |
| DEH-003 | ハードウェア保護鍵 | adjacent | SOURCE-004。鍵種別・利用者確認・失効の製品別検証は保留 |
| DEH-004 | pre-commit検査 | deferred | ローカルhookの導入・迂回・失敗時の扱いを、旧SOURCE-002と照合してから移す |
| DEH-005 | サーバー側検査 | deferred | ローカル検査と違い、送信・保存・mergeのどこで止めるかを明確化する。Required checkだけで送信前の流出防止とはしない |
| DEH-006 | install隔離 | adjacent | [Install execution policy](../engineering/dependency-security/install-execution-policy/README.md)と[Build execution boundary](../engineering/build-security/build-execution-boundary/README.md)。開発端末での隔離実装は保留 |
| DEH-007 | cooldownと例外 | adjacent | [DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)。更新採用は端末の良好状態とは別判断 |
| DEH-008 | 端末の通信制限 | design-migrated | ENG-SOURCE-002。配布設定と迂回できない通信経路を区別。実通信の検証は保留 |
| DEH-009 | 集中認証・MFA | adjacent | SOURCE-004。全業務サービスへのSSO適用は保証しない |
| DEH-010 | 機密データの公開防止 | deferred | ファイル形式・内容・公開経路の検査を旧SOURCE-003等と照合。拡張子やサイズだけで安全としない |
| DEH-011 | registry proxyの強制 | adjacent | [Cooldown pattern](../engineering/dependency-security/dependency-release-cooldown/README.md)。全端末・全package managerの迂回防止は未確認 |
| END-001 | ディスク暗号化 | design-migrated | ENG-SOURCE-002。回復鍵と電源断時の保護を、ログイン後のプロセス権限から分離 |
| END-002 | 画面ロック | design-migrated | ENG-SOURCE-002。再認証と物理的な不在時の利用防止 |
| END-003 | OS・ツール更新 | design-migrated | ENG-SOURCE-002。サポート対象、適用期限、再起動、期限付き例外 |
| END-004 | 通常権限・昇格 | design-migrated | ENG-SOURCE-002。標準ユーザーの権限悪用は残る |
| END-005 | workspaceの秘密情報 | adjacent | SOURCE-004と[Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md)。平文の残存と実行時の注入を分離 |
| END-006 | runtime socket | adjacent | Development runtime isolation。AI以外の開発環境への適用・実装検証は保留 |
| END-007 | debugサービス公開 | design-migrated | ENG-SOURCE-002。待受の制限を残し、未知のポートやトンネルまで検査済みとしない |
| END-008 | AIツールの通信 | adjacent | Development runtime isolation。開発ツールの通信境界のみ。提供先の保持・リージョン・テナントの契約と実効性は別途確認 |
| END-009 | mountの書込み範囲 | adjacent | Development runtime isolation。共有先の限定とcredential除外。汎用開発環境の製品設定は保留 |
| END-010 | バックアップ | design-migrated | ENG-SOURCE-002。暗号化・復元権限と復旧可能性を分ける |
| END-011 | アプリ・拡張の管理 | design-migrated | ENG-SOURCE-002。AI拡張の内容審査は[Agent extension admission](../engineering/ai-development-security/agent-extension-admission/README.md)へ |
| END-012 | EDR・XDR | design-migrated | ENG-SOURCE-002。登録・観測・通知・初動を分離。検知ルールと製品adapterは未移行 |
| END-013 | commit署名 | deferred | 署名者と検証条件、鍵の失効、repository側の拒否を別途整理。署名をコードの安全性・作者本人・端末健全性の保証にしない |
| END-014 | IDEのSAST・SCA | deferred | 開発者へのフィードバックを強制gateと区別。[DETECT-001](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)はIDE連携の導入証明ではない |
| END-015 | 管理された隔離環境 | adjacent | ENG-SOURCE-002で方式を比較し、Development runtime isolationへ接続。接続元端末の保護は残す |
| END-016 | sandbox制限・観測 | adjacent | Development runtime isolationとBuild execution boundary。端末全体のEDRとは別の範囲 |
| END-017 | 集中管理・是正 | design-migrated | ENG-SOURCE-002。登録、現在の観測、資産側のアクセス判断を分離 |
| END-018 | 物理保護・紛失 | design-migrated | ENG-SOURCE-002。保管・輸送、失効、調査、復旧。未到達の消去を完了扱いにしない |

集計は`design-migrated`11項目、`adjacent`13項目、`deferred`5項目です。
設計を分担しただけでSOURCE-001全体を移行済みには数えません。

## 旧実装とframework mapping

旧`policy.conf`の29宣言を検査するfixtureは移植しません。宣言の整合性が端末への導入証明にならないためです。
読み取り専用Linux assessmentは有用な候補として保留し、観測対象のOS・ホスト、権限、収集失敗の区別をレビューしてから判断します。
今回、ユーザーの実端末を検査・変更していません。

旧4件の対応関係は[旧metadata](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/control.yaml)へ保持します。

| Framework・版 | ID・関係・confidence | 今回の扱い |
|---|---|---|
| MITRE ATT&CK v19.1 | T1552.001 / mitigates / medium | 認証情報・検査側の分担を確認するまで保留 |
| MITRE ATT&CK v19.1 | T1555 / mitigates / medium | 認証情報保管側の分担を確認するまで保留 |
| NIST SSDF 1.1 (SP 800-218, 2022) | PS.3.1 / supports / medium | 元の広いcheck集合と新しい端末管理の特性を意味的に照合してから移す |
| NIST SSDF 1.1 (SP 800-218, 2022) | PW.4.1 / supports / medium | DEH-011の依存取得経路に対する関係。端末管理全体へ転用しない |

旧レビュー日（前3件2026-07-25、PW.4.1は2026-07-31）は履歴として保持し、今回の再レビュー日には置き換えません。
新しいframework関係や準拠の主張は追加していません。

## 次に進める範囲

端末管理のcontrol記録を作る際は、今回直接移した11項目を基に、独立して評価できる特性を定めます。
その後に旧mappingを照合し、ローカル観測と組織側のアクセス制御を分けた評価方法を選びます。
保留したhook・公開防止・署名・IDE連携は、別の境界として順次扱います。SOURCE-001へ再集約しません。
