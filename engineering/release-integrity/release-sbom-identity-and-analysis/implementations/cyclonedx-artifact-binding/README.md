# CycloneDX 1.7 artifact binding

## 何をするものか

配布するファイルのSHA-256を計算し、CycloneDX 1.7 JSONのroot componentに記録されたhashと比較する小さなPython実装です。合わせて、文書内の`build`／`post-build`という記述、SBOMの識別子、version付きPURL、`bom-ref`とdependency参照、root assemblyのcomposition状態を検査します。

例えば、SBOM生成後に成果物が変わった場合の取り違えを検出できます。実際に完成物を調べてSBOMを作ったかは、生成処理側で確認します。Hashやphaseの記述だけで、その事実を証明するものではありません。

通常のreleaseでは、final artifactとSBOMを作った直後、公開前に次のcommandを実行します。成功時に出力されるdigestとidentityをpublication manifestへ渡します。終了codeが`1`または`2`ならreleaseを止めます。

```bash
python3 verify_binding.py \
  --artifact dist/product.tar.gz \
  --sbom dist/bom.cdx.json
```

これは[PSB-REL-003](../../../../../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)の限定実装です。SBOM schema全体、component coverage、公開storage、Dependency-Track等のanalysis処理、deployment inventoryは別に確認します。
終了code `0`はこの限定検査の成功です。`composition: unknown`や`incomplete`を公開可能とするかは、artifact typeごとのcoverage判断で別に決めます。

## 対象と前提

- Python `3.11`以上。外部Python packageは不要です。
- CycloneDX JSON `1.7`だけを対象にします。
- SBOMはfinal artifactの`build`または`post-build`観測として生成済みであること。
- Root componentと各componentには、この実装のlocal policyとしてversion付きPURLを要求します。
- Root componentの`hashes`にはSHA-256を一つだけ記録します。
- Root assemblyを説明するcomposition stateを一つ記録します。
- Dependencyとcompositionの参照先は同じSBOM内のcomponentに限ります。外部BOMへの参照はこの実装の対象外です。

CycloneDX仕様ではPURL、root hash、compositionはすべてのSBOMに一律必須ではありません。この実装はrelease artifact binding用の追加contractとして要求します。

## 手元のrepositoryへ入れる

本PJのルートで、`target`を導入先repositoryの絶対パスへ変更して実行します。既存の同名ファイルがある場合は止めます。

```bash
(
  set -eu
  guidance_root="$PWD"
  target=/absolute/path/to/your-repository
  source_dir="$guidance_root/engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding"
  test -f "$source_dir/verify_binding.py"
  test "$(git -C "$target" rev-parse --show-toplevel)" = "$target"
  test ! -e "$target/tools/sbom/verify_binding.py"
  test ! -L "$target/tools/sbom/verify_binding.py"
  mkdir -p "$target/tools/sbom"
  cp "$source_dir/verify_binding.py" "$target/tools/sbom/verify_binding.py"
  python3 "$target/tools/sbom/verify_binding.py" \
    --artifact "$source_dir/examples/release.txt" \
    --sbom "$source_dir/examples/bom.cdx.json"
)
```

コピー先で同梱例の照合が成功することを確認します。ここでは生成・公開・分析基盤への送信は行いません。`python3`は対象と前提に合う版を使ってください。

実際のリリースへ接続するときは、次の順に確認します。

1. Release jobでfinal artifactを作った後、採用したgeneratorでCycloneDX 1.7 JSONを生成します。
2. [固定したCycloneDX公式1.7 JSON Schema](https://github.com/CycloneDX/specification/blob/4b3f59453366e27c8073fd24e98bf21ef8892c8e/schema/bom-1.7.schema.json)を取得し、SHA-256 `df472ef4aaf593904c479293723a1a5c191d6672715c93b3c0b5c318f3914221`を確認してから、対応するschema validatorでSBOM全体を検証します。
3. 実際の生成入力・観測範囲を確認したうえで、`metadata.lifecycles`とroot componentのSHA-256が、その観測段階・対象を示すことを確かめます。Source SBOMへラベルとhashだけを追記して代用しません。
4. Public／upload stepの前にこのscriptを実行し、non-zeroなら後続処理を止めます。
5. 成功JSONのartifact digest、SBOM digest、serial、version、root ref、compositionをrelease manifestまたは次のjobへ渡します。

最小のCI処理は次の形です。ArtifactやSBOM pathは利用するbuild systemに合わせて固定してください。

```bash
set -eu
python3 tools/sbom/verify_binding.py \
  --artifact "$ARTIFACT_PATH" \
  --sbom "$SBOM_PATH" \
  > sbom-binding-receipt.json
```

`ARTIFACT_PATH`と`SBOM_PATH`を未信頼入力からそのまま組み立てず、release jobが作った既知のpathを渡します。Receiptはsignatureやattestationではありません。後段で改変され得る場所へ置く場合は、protected artifactとして扱います。

## すぐ試す

このdirectoryで実行します。

```bash
python3 verify_binding.py \
  --artifact examples/release.txt \
  --sbom examples/bom.cdx.json
```

成功時は一行のJSONを返します。

```json
{"artifact_sha256":"…","bom_serial":"urn:uuid:…","bom_version":1,"component_count":1,"composition":"incomplete","observation_phases":["post-build"],"root_ref":"pkg:generic/example-release@1.0.0","sbom_sha256":"…","status":"PASS"}
```

簡単な異常時テストは次で実行できます。

```bash
python3 -m unittest -v test_verify_binding.py
```

次を実際に確認します。

- 正しいartifactとSBOMが`0`で成功する。
- Artifactを変更するとdigest mismatchで`1`になる。Artifact内容はerrorへ表示しない。
- `pre-build`だけのSBOMをrelease authorityとして拒否する。
- 存在しないcomponentへのdependency参照を拒否する。
- Dependency参照に文字列以外が混ざっても、例外tracebackを出さず拒否する。
- 存在しないcomponentへのcomposition参照を拒否する。
- `unknown` compositionを`complete`へ変えず、そのまま成功receiptへ出す。
- Parse不能なJSONを`PASS`やfindingなしにせず`2 / ERROR`にする。
- 同じJSON keyの重複を拒否する。

## 終了code

| Code | 意味 |
|---|---|
| `0` | この限定contractの検査に成功 |
| `1` | 読み取れたartifact／SBOMがcontractに不一致。Releaseを拒否する |
| `2` | File取得、size、JSON parse等により評価不能。Releaseを止める |

DefaultではSBOM入力を10 MiBまでに制限します。変更する場合は、runner memoryと想定inventoryを確認して`--max-sbom-bytes`を明示します。

## 更新・解除

- CycloneDX versionを変更する場合は、scriptの対応version、固定schema、test fixture、composition値、lifecycle、参照規則を一緒にreviewします。`specVersion`だけを書き換えません。
- Scriptを更新したら上のtestを実行し、導入先の実artifactとgenerator出力でも確認します。
- 切り戻す場合はCIの呼出し、copyしたscript、receiptの参照を一緒に直前のreview済み状態へ戻します。検査の撤去はrelease判断を弱めるため、代替のbinding確認とconsumerへの影響をrelease policyで扱います。

## 制限

- CycloneDX公式JSON Schema全体を実装しません。Productionではversion-pinned schema validatorを先に使います。
- Version付きPURLの判定はこのlocal contractの簡易形で、PURL仕様全体のparserではありません。
- Componentの走査範囲は`metadata.component`と最上位の`components`です。入れ子のcomponentやservice、外部BOMの参照整合性は検査しません。この出力の`component_count`は最上位`components`の件数であり、全階層の部品数ではありません。
- `complete`が正しいことを証明しません。明示されたstateを保持するだけです。
- Generator、build環境、SBOMのauthenticityや署名を検証しません。
- 同梱SBOMは照合を試すための手書き例です。`release.txt`を解析して部品を発見した結果ではありません。
- Publication、consumer retrieval、immutability、retention、Dependency-Track処理、vulnerability data、deployment joinを確認しません。
- Exampleとunit testの成功は、組織のrelease pipelineへ導入済みであることを示しません。

## 根拠

- [CycloneDX 1.7 JSON reference](https://cyclonedx.org/docs/1.7/json/)
- [REF-RELEASE-SBOM-LIFECYCLE-001](../../../../../sources/README.md#ref-release-sbom-lifecycle-001)
- [設計pattern](../../README.md)
- [教材：そのSBOMは、どこを調べて作ったものか](../../../../../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/learning.md)
