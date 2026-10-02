# Dependency artifact identity — 学習ノート

[コントロール記録](README.md) · [設計パターン](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)

## シナリオ：レビューした内容とbuildが使う内容が違う

更新ボットがWeb frameworkを更新し、その先で使うパッケージ（推移依存）も変わりました。
担当者は差分をレビューして採用を承認します。ところが通常buildはlockfileを使わずに依存を選び直し、
承認したものとは別の推移依存を取得しました。攻撃者がその未レビューの依存へコードを入れられるなら、
承認したつもりのbuildへ入り、後の準備処理やテストでCIの権限を使う経路が生まれます。

レビューが正しくても、実際に使う依存関係とファイルがその判断へ結び付いていなければ、未レビューの内容が入ります。

## Version、lock、hashの役割

Manifestは、必要なパッケージと許容するバージョンなどを記した入力です。Versionは選んだreleaseを表し、
lockfileは直接・推移依存を含む選択結果を記録します。Hashは取得したファイルの内容を識別します。
同じ名前とversionでも、mirrorが別ファイルを返す可能性があるため、利用前に承認したhashへ照合します。
複数OSやarchitecture向けの配布物がある場合、使うファイルごとにhashと対象範囲が必要です。

Hashが一致しても、そのパッケージが安全とは限りません。悪意あるファイルを承認して、そのhashを正しく記録した場合も
完全性検査は成功します。何を採用してよいかは[Dependency change review](../psb-deps-004-dependency-change-review/learning.md)、
準備用コードを動かしてよいかは[Install execution policy](../psb-deps-002-install-execution-policy/learning.md)が扱います。

## lockを書き換えないだけでは足りない

Manifestを変えたのに古いlockを使い続ける場合と、build中にlockを修復して新しい依存を選ぶ場合では、
どちらもレビューとの対応が崩れます。「今のmanifestに対応しているか」と「通常buildで変更しないか」を別に確認します。
不一致なら更新とレビューへ戻し、通常buildの成功を優先して自動修復しません。

## 既に入っている依存は何を根拠に使うか

取得ファイルのhashと、展開済みの依存環境の状態も別物です。
以前の環境を復元し、名前とversionが同じというだけで使うと、今回のhash照合を通らない内容が残ることがあります。
既存状態を承認した入力へ結び付けて確認するか、新しい環境で依存を取得・照合するかを選びます。
取得時のhashが一致していても、その後の書換えまで検知するわけではありません。

[pip例](../../../../engineering/dependency-security/install-execution-policy/implementations/pip/README.md)では、空の専用環境から始める手順を示します。
この例だけでmanifestとの対応や依存関係全体の固定が完成したとは扱いません。

## 振り返りで問うこと

- Manifestを変えたのに古いlockfileのまま通常buildを続けられないか。
- 通常buildがlockfileを生成・修復・書き換えていないか。
- 直接依存だけでなく、対象platformで使う推移依存とfileを固定しているか。
- Hashがない取得方式や未対応schemaを、検証済みとして扱っていないか。
- Registry、mirror、cacheから取得したbytesが承認済みhashと違えば、利用前に止まるか。

この教材は[製品別lock仕様](../../../../sources/README.md#spec-dependency-lock-identity)と
[攻撃段階4→7](../../../../docs/ANALYSIS_LENSES.md)を使ったリポジトリ独自の解釈です。
個別package managerへの導入済み状態は示しません。
診断のチェックリストは[control](README.md#failure-checks)、入力をレビューからbuildへ渡す方式は[設計pattern](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)にあります。
