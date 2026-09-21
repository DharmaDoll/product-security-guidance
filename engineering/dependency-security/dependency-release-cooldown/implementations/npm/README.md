# npm実装例: Dependency release cooldown

パターン：[Dependency release cooldown](../../README.md)

コントロール：[PSB-DEPS-001](../../../../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)

## 位置付けと境界

移行パイロットです。npmプロジェクトで、npm標準の最低待機時間設定を使う最小限の実装例です。
旧プロジェクトでは、npm `11.10.0`以上と7日間を基準にしていました。採用時には、対象とするnpmの
メジャーバージョンの公式文書、設定の優先順位、メタデータがない場合の挙動を再確認してください。

## 参照資料から採用した判断

| 参照資料 | この実装例で採用した判断 | この資料だけでは判断しないこと |
|---|---|---|
| npmの公式仕様 | `min-release-age`の対応バージョン、単位、設定方法、依存関係の解決時の挙動 | すべての更新経路で設定が強制されるか |
| `REF-DEPS-004` | パッケージマネージャー標準機能を候補として見つけ、設定の優先順位と回避経路を確認する | 外部例の待機時間を組織の基準にすること |
| `REF-PORTFOLIO-001` | この実装例を外部依存・サプライチェーンの一部分として扱い、後続工程の空白を隠さない | npmの製品挙動、待機時間、フレームワーク要件 |
| サプライチェーン攻撃段階 | 依存関係の解決からCI、ビルド、リリース、本番環境への受け渡しを明示する | 待機期間が後続工程の完全性や実行時検知を代替するという主張 |

採否と版の正本は[参照資料と仕様](../../../../../sources/README.md)、段階間の関係は
[横断分析の軸](../../../../../docs/ANALYSIS_LENSES.md)にあります。

この実装例は次を証明しません。

- チームのすべての更新経路で、この設定が実際に有効になること。
- CLI、環境変数、利用者設定から上書きされないこと。
- パッケージにマルウェアや脆弱性がないこと。
- ロックファイル、成果物の完全性、インストールスクリプトが安全であること。

## ファイル

- [`project.npmrc`](project.npmrc): プロジェクトへ取り込むための設定例。

隠しファイルである`.npmrc`をそのまま配布するのではなく、内容をレビューして既存のプロジェクト設定へ取り込む前提です。

## 設定例

```ini
registry=https://registry.npmjs.org/
min-release-age=7
save-exact=true
package-lock=true
```

- `min-release-age=7`は、旧パイロットの基準である168時間を日単位で表します。
- `save-exact=true`は、更新時にレビューしたバージョンを範囲指定にせず記録します。
- `package-lock=true`は、選択した依存関係グラフを通常ビルドで再現するための隣接設定です。

非公開レジストリまたは管理プロキシを使う場合、URLだけを置き換えて安全と判断してはいけません。
その接続先が公開時刻をどのように提供し、代替経路や別のレジストリをどのように扱うかを確認します。

## 導入手順

1. npmのバージョンと公式の設定仕様を確認する。
2. 既存の`.npmrc`、CLI、環境変数、利用者単位の設定について、優先順位を確認する。
3. `project.npmrc`の4項目をレビューし、リポジトリ直下の`.npmrc`へ取り込む。
4. 依存関係の更新処理を通常ビルドから分離する。
5. 更新時は採用するバージョンを一意に決め、公開後経過時間の判定後に、マニフェストとロックファイルを同じプルリクエストに含める。
6. 通常のCIとリリースビルドでは、レビュー済みのロックファイルを変更しないインストール方式を使う。
7. チームのリポジトリでは、npm標準の設定に加えて、信頼できる必須検査を検討する。

この実装例から、npmの全体設定、シェル、IDE、OSの設定を自動変更することはありません。

## 設定が実際に有効か確認する

対象プロジェクトとCIで、少なくとも次の実効値を確認します。

```bash
npm --version
npm config get min-release-age --location=project
npm config get save-exact --location=project
npm config get package-lock --location=project
```

パイロットで期待する値は`7`、`true`、`true`です。ただし、表示値だけでは依存関係の解決時の挙動や、
優先順位が高い設定から上書きされていないことを証明できません。

## 意味のあるテスト

採用環境に安全なテスト範囲を用意できる場合、次を確認します。

- 境界時刻を十分に過ぎたテスト候補は、依存関係の解決対象になる。
- 最低待機時間をまだ満たしていない候補は、インストール時のコードを実行する前に除外される。
- 公開時刻を取得できない候補は許可されない。
- 通常ビルドが、コミット済みのロックファイルを変更しない。
- チームのリポジトリでは、待機時間を満たさない候補がマージの必須検査を通過しない。

このパイロットには、特定バージョンで固定した実在のパッケージや、形式だけを確認する設定解析器を同梱しません。READMEの文字列や
`min-release-age=7`の存在だけを確認するテストでは、依存関係の解決時に設定が強制されることを証明できないためです。

## 緊急更新

既知の脆弱性修正を早く採用する必要がある場合でも、プロジェクト全体の最低待機時間を恒久的に下げません。
対象パッケージとバージョンを一つに特定し、対象リポジトリ、理由、所有者、別の承認者、有効期限を定めた例外を使い、
完全性確認、依存関係レビュー、インストール処理の隔離を維持します。
例外decisionの共通lifecycleは[Security exception decision boundary](../../../../governance-operations/security-exception-decision-boundary/README.md)を参照し、このnpm例だけを組織共通schemaとして扱いません。

## 公式資料

- [SPEC-NPM-CLI-11の参照資料記録](../../../../../sources/README.md#spec-npm-cli-11)
- [REF-DEPS-004と公式クライアント仕様](../../../../../sources/README.md#ref-deps-004)
- [npmレジストリのメタデータ仕様の状態](../../../../../sources/README.md#spec-npm-registry-metadata)
- [npm configuration](https://docs.npmjs.com/cli/v11/using-npm/config/)
- [npm install](https://docs.npmjs.com/cli/install/)
- [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
- [REF-PORTFOLIO-001の参照資料記録](../../../../../sources/README.md#ref-portfolio-001)
- [サプライチェーン攻撃段階と代表経路](../../../../../sources/README.md#local-supply-chain-attack-stages)
