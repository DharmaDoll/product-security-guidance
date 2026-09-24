# Build code is not build authority

[コントロール記録](README.md) · [設計パターン](../../../../engineering/build-security/build-execution-boundary/README.md)

## 一つの依存更新から考える

開発者が依存更新をレビューし、lockとhashを固定しました。Build jobは承認済みのbytesを取得します。
しかし、そのパッケージのtest pluginが、実行時に環境変数を読み、外部へ送信しようとします。
Hashが一致しても、この行動は止まりません。同じjobに公開tokenやcloud権限があれば、その権限も利用され得ます。

取得する内容を決める判断と、取得したコードに何をさせるかという判断は別です。
ビルド対象に含まれるコードを「build code」、ビルド基盤を管理・公開する権限を「build authority」と呼び、同じ場所へ置かないようにします。

## 攻撃経路をどこで切るか

```text
承認した依存 → pluginを実行 → jobの資産や権限を取得 → 外部送信／公開先変更
                  ↓
       秘密情報なし・限定入力・隔離・通信拒否
                  ↓
       固定した出力 → 別consumerが独立して受入判断
```

秘密情報を渡さず、hostの管理経路へ届かせず、入力取得後の通信も閉じれば、上の直接的な権限悪用・送信経路は狭まります。
一方、生成した成果物へ悪意あるコードを埋める経路は残ります。Digestや署名はその成果物の同一性を確認するもので、無害性の判定ではありません。

## 三つの直感を見直す

| 直感 | 見落とす境界 |
|---|---|
| 新しいrunnerなら安全 | 実行中に渡したtokenやmetadataへの到達性は、終了後の破棄では取り消せない |
| allowlistの宛先なら安全 | 許可したregistryやproxyへも、不要なデータを送れる場合がある |
| sensorにイベントがないなら安全 | 停止・欠落・配送障害なら行動を観測できない。Healthの確認が必要 |

Sensorは行動を知る手段、sandboxや通信制御は行動の可能性を制限する手段です。
センサーが動いても通信を拒否した証拠にはならず、拒否できてもログが届くとは限りません。

## レビューで確認する問い

どのコードがいつ実行され、どのファイル、token、socket、宛先へ届くかを実行環境から確認します。
取得サービス・provisioner・sensorに必要な権限は、ビルド対象のコードへ渡さない構造にします。
無害な拒否試験の結果と外側の制御ログを照合し、観測できなかった部分は未確認として残します。

[REF-PORTFOLIO-001](../../../../sources/README.md#ref-portfolio-001)ではplatformと外部依存からoperationsへの受け渡しを考える教材です。
[攻撃段階の索引](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md)の7を直接扱い、8の来歴、9の署名・consumer判断、12の調査へ責任を残します。
上のシナリオはリポジトリでの解釈であり、特定の事件・製品の動作報告ではありません。

- [Build containment](README.md)
- [方式と代償](../../../../engineering/build-security/build-execution-boundary/README.md)
