# PSB-DEPS-002 Install execution policy

**依存を取得するだけで、公開者が用意したコードを実行していないか。**

## なぜ必要か

例えば、依存を更新した直後、テスト開始前の準備用スクリプトがCIの公開用tokenを使えることがあります。パッケージを取得してよいかと、準備用コードを実行してよいかは別に判断します。
この実行を見落とすと、変更をマージする前でもCIの認証情報やファイルへアクセスされます。

## 満たすべきこと

1. **不要な実行を止める。** インストール時に動くスクリプトやbuild処理を把握し、未承認なら実行させない（DEP-EXEC-1）。直接依存だけでなく、推移依存や別の取得経路も対象にする。
2. **必要な実行だけを許可する。** どうして必要かを確認し、対象のパッケージ・版・取得物を限定して別の担当者が審査する（DEP-EXEC-2）。実行する場合も、認証情報や通信先への到達を必要な範囲に絞る。
3. **迂回と判定不能を許可しない。** 別のinstallコマンド、設定の上書き、source buildへの切替えで未承認コードを動かさない。設定や検査が欠けたときも許可扱いにしない（DEP-EXEC-3〜4）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 推移依存の準備用コードや、配布ファイルがないときのsource buildが、未承認のまま動かないか。
- 承認した名前を使って、別の版や別の取得物を実行できないか。
- コマンド、環境変数、設定ファイル、同じ変更で加えた実行方針から拒否を外せないか。
- 検査器の不在、未対応版、解析失敗、タイムアウトで実行を許可していないか。
- 未承認の処理を省略してinstallが成功したとき、必要な機能が欠けていないか。

これらは確認項目であり、実際の端末やCIで試した結果ではありません。

## フレームワークとの関係

- [MITRE ATT&CK Enterprise v19.1 T1195.001](../../../../sources/README.md#spec-mitre-attack-v19-1): 改変された依存に含まれる準備用コードが、インストール時に動く経路を部分的に妨げます。開発ツール自体の侵害や、インストール後のimport・testで動くコードは防げません。

これは[マッピング](../../../../mappings/frameworks.yaml)に記録した部分的な設計上の関係です。実際の実行拒否や、攻撃全体への対策完了を示すものではありません。

## このコントロールの範囲

対象は依存を取得・準備する途中で、公開者のコードが動く経路です。公開直後の版を待つ判断は[DEPS-001](../psb-deps-001-dependency-release-cooldown/README.md)、取得物の同一性は[DEPS-003](../psb-deps-003-dependency-artifact-identity/README.md)、変更を採用する判断は[DEPS-004](../psb-deps-004-dependency-change-review/README.md)です。承認した準備用コードの隔離は[BUILD-001](../../build-security/psb-build-001-build-containment/README.md)へ渡します。インストール後のimport・test・製品実行まで保証するものではありません。

実行停止、限定許可、隔離の選び方は[engineering](../../../../engineering/dependency-security/install-execution-policy/README.md)を参照してください。例外の対象・承認・期限は[GOV-002](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)、接続先は[consumer mapping](../../../../mappings/exception-consumers.yaml)にあります。[教材](learning.md)、4つの特性と参照資料IDを残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-install-execution-policy)へも辿れます。
