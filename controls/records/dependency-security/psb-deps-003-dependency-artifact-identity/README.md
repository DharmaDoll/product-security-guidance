# PSB-DEPS-003 Dependency artifact identity

**レビューして承認した依存と、通常のビルドが実際に使うファイルは同じか。**

## なぜ必要か

例えば、依存の更新を承認した後に通常のビルドがlockfileを作り直すと、未レビューの推移依存が入ります。同じ名前と版でも、取得先やcacheから別のファイルを受け取ることがあります。
そのままビルドすると、承認していないコードをCIで実行したり、成果物へ入れたりする可能性があります。

## 満たすべきこと

1. **依存の一覧を固定する。** 対象のOSや構成で使う直接・推移依存を、レビューしたmanifestとlockfileに結び付ける（DEP-ID-2）。両者がずれていれば通常のinstallを止め、ビルド中にlockfileを作り直さない（DEP-ID-1・4）。更新は別の手順で差分をレビューする。
2. **使うファイルを照合する。** 外部から取得するファイルを承認済みのhashと利用前に比較し、一致しなければ使わない（DEP-ID-3）。取得したファイルのhashをその場で計算して自動承認するだけでは、事前のレビューにはならない。
3. **確認できなければ通さない。** 記録の欠落、未対応の取得形式、検証ツールの不在・失敗を「一致した」と扱わない（DEP-ID-5）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Manifestだけを変えたとき、古いlockfileのまま進む、またはlockfileを自動修復してビルドを続けられないか。
- 推移依存、別OS用、optional依存が固定対象から漏れ、通常のinstallで再解決されないか。
- 同じ名前と版で別のファイルを返したとき、mirrorやcache経由でも利用前に拒否するか。
- 展開済みの依存を再利用するとき、名前と版だけで検証済みと見なしていないか。
- Hashの欠落、未対応形式、検証失敗を、正常な照合結果に変えていないか。

これらは確認項目であり、実際のビルドで試した結果ではありません。

## フレームワークとの関係

| 参照先 | このコントロールとの関係 | ここでは扱えないこと |
| --- | --- | --- |
| [MITRE ATT&CK Enterprise v19.1 T1195.001](../../../../sources/README.md#spec-mitre-attack-v19-1) | レビュー後の依存解決や取得ファイルの差し替えを拒否し、改変された依存が入る経路を部分的に妨げる。 | 悪意ある内容を承認してしまった場合や、開発ツール自体の侵害は防げない。 |
| [NIST SSDF 1.1 PW.4.4](../../../../sources/README.md#spec-nist-ssdf-1-1) | 取得したファイルを事前に承認したhashと照合することが、第三者部品の完全性確認を支える。 | Hashの一致だけでは配布元の正当性や内容の無害性は分からない。 |

いずれも[マッピング](../../../../mappings/frameworks.yaml)上の部分的な設計関係です。フレームワークへの準拠や実際のビルドでの強制を示しません。

## このコントロールの範囲

対象は通常のビルドで使う依存の解決結果と取得ファイルです。Local workspaceやVCS由来の依存には、選んだ方式で同一性を確認できるか別に判断します。Hashの一致はファイルの同一性を示しますが、その中身が無害だとは示しません。変更を採用する判断は[DEPS-004](../psb-deps-004-dependency-change-review/README.md)、install時に動くコードの許可は[DEPS-002](../psb-deps-002-install-execution-policy/README.md)へ渡します。

Lockfile、hash、再利用する環境の扱いは[engineering](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)で選びます。[既存pip例](../../../../engineering/dependency-security/install-execution-policy/implementations/pip/README.md)はwheelとhashの限定例であり、全依存の固定を示すものではありません。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、採否を示す[Sources](../../../../sources/README.md#spec-dependency-lock-identity)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
