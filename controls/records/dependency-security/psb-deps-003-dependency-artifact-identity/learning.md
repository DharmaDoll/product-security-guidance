# Dependency artifact identity — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)

## シナリオ：レビューした内容とbuildが使う内容が違う

更新ボットがweb frameworkを更新し、推移依存も変わりました。担当者は差分をレビューして採用を承認します。
ところが通常buildはlockfileを使わずに再解決し、別の推移依存を選びます。あるいはmirrorが同じ名前とversionで
別のfileを返し、buildはhashを確認せず利用します。

レビューが正しくても、実際に使う入力がレビューしたgraphとbytesへ結び付いていなければ、未レビューの内容が入ります。

## Version、lock、hashの役割

Versionは選んだreleaseを表し、lockfileは直接・推移依存を含む解決結果を記録します。Hashは取得したfileのbytesを
識別します。複数OSやarchitecture用のfileがある場合、同じversionでも使用するfileごとにhashが必要です。

Hashが一致しても、そのpackageが安全とは限りません。悪意あるfileを承認して、そのhashを正しく記録した場合も
完全性検査は成功します。何を採用してよいかは[Dependency change review](../psb-deps-004-dependency-change-review/learning.md)、
準備用コードを動かしてよいかは[Install execution policy](../psb-deps-002-install-execution-policy/learning.md)が扱います。

## 振り返りで問うこと

- Manifestを変えたのに古いlockfileのまま通常buildを続けられないか。
- 通常buildがlockfileを生成・修復・書き換えていないか。
- 直接依存だけでなく、対象platformで使う推移依存とfileを固定しているか。
- Hashがない取得方式や未対応schemaを、検証済みとして扱っていないか。
- Registry、mirror、cacheから取得したbytesが承認済みhashと違えば、利用前に止まるか。

この教材は[製品別lock仕様](../../../../sources/README.md#spec-dependency-lock-identity)と
[攻撃段階4→7](../../../../docs/ANALYSIS_LENSES.md)を使ったリポジトリ独自の解釈です。
個別package managerへの導入済み状態は示しません。
