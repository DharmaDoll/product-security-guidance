# An accepted SBOM can still describe the wrong release

## シナリオ

あるteamはpull requestごとにdependency manifestからCycloneDX SBOMを生成し、release時に同じfileをDependency-Trackへuploadしていました。Upload APIはtokenを返し、project画面にはcomponentが表示されます。Teamはこれを「release SBOMの処理完了」と記録しました。

実際のcontainer imageには、base imageのOS package、build中に取得したbinary、bundleへ取り込んだtransitive libraryが含まれていました。Source SBOMにはどれもありません。さらに、upload後のvalidation jobは失敗していましたが、pipelineはAPI受付を成功としたためreleaseを続行しました。

数週間後、bundle内のlibraryに重大な脆弱性が報告されました。Dependency-Trackのprojectを検索してもcomponentは見つからず、teamは一度「影響なし」と判断しました。問題はSBOM fileの不存在ではなく、観測時点、artifact binding、coverage、処理状態を一つの`uploaded`へ潰したことでした。

## 境界を分ける

```text
source／pre-build observation
  -> 早期feedback。final artifactの正本ではない

final artifact bytes
  -> build／post-build SBOM
  -> artifact digest + SBOM digest／serial／version
  -> schema・identity・relationship・coverage state
  -> immutable publication + intended-consumer retrieval
  -> exact analysis projectへのupload
  -> validation -> ingestion -> analysis completion
  -> deployment digestとの関係
  -> componentから稼働製品への影響調査
```

各矢印で別の失敗が起きます。前段の成功を後段の成功へ読み替えません。

## 用語

- **Observation phase**：SBOMの情報を取得した時点。CycloneDX 1.7には`pre-build`、`build`、`post-build`、`operations`等のlifecycle phaseがあります。
- **Release-authoritative SBOM**：配布するfinal artifactを対象に作られ、そのartifact digestへ結ばれたrelease inventory。完全性を自動的に意味しません。
- **Artifact binding**：SBOMのroot subjectが、実際に配布するartifact bytesのcryptographic digestと一致する関係。
- **Composition／completeness claim**：Inventoryやrelationshipをどこまで含むとproducerが表明するか。`complete`はschemaが証明する事実ではなく、generator coverageと生成条件によるclaimです。
- **Transport acceptance**：Upload requestをserverが受け付けた状態。Validation、ingestion、analysis完了とは異なります。
- **Analysis health**：Parser、queue、analyzer、外部data、pagination等が、判断に必要な範囲で利用可能・freshである状態。

## 悪用・失敗経路

1. Source treeまたはmanifestからSBOMを作る。
2. Final artifactにOS package、vendored code、generated bundle、downloaded binaryが加わる。
3. Product versionやfilenameだけでsource SBOMをreleaseへ添付する。
4. SBOMのformatが正しい、または`complete`と書かれているため、coverageを確認しない。
5. Analysis platformのupload受付を処理完了としてreleaseを続ける。
6. Validation／processing失敗、古いvulnerability data、page欠落を空のfinding一覧へ変える。
7. Component検索が0件となり、未収載を非該当と誤認する。
8. Deployment inventoryもsource SBOMと同じidentityへ上書きされ、actual artifact digestへ戻れない。

## よくある誤解

### 「SBOMは一度取得すれば、どの段階の判断にも使える」

PR時には依存関係定義が見え、build後には完成したimageやbinaryに加わったcomponentが見えます。Deployment後は、どのartifactが実際に稼働しているかを観測できます。取得する場所が違えば、見える対象も、見えない対象も変わります。同じfileを全段階の正本として使わず、各観測をcommit・artifact digest・deployment IDでつなぎます。

### 「CycloneDXとしてvalidなら完全なSBOMである」

Schema validationはfieldと型の整合性を確認します。Generatorがartifactの全surfaceを観測したか、除外設定が妥当か、componentが欠落していないかは別の問いです。

### 「`complete`と書けば完全性を検証できる」

Compositionはknown unknownをconsumerへ伝えるために有用です。ただし値そのものはproducerのclaimです。Artifact type、generator方式、入力、除外、比較対象、失敗状態を合わせて判断します。

### 「Uploadが成功すればanalysisは終わっている」

非同期platformでは、受付後にvalidation、ingestion、component分析、vulnerability照合が続きます。対象SBOMとprojectへ結ばれた完了状態を待ちます。

### 「Findingが0件なら脆弱性はない」

未収載component、古いadvisory data、analyzer停止、alias・version rangeの品質、partial collectionでも0件になり得ます。正常な0件と評価不能を分けます。

### 「Source、build、runtimeのSBOMを一元化するなら一つに上書きすべき」

一元化するのは検索と関係です。観測時点とauthorityが異なるdocumentは別identityのまま、commit、artifact digest、deployment IDでつなぎます。

## 判断基準

- Releaseの正本にするSBOMは、どのfinal artifact bytesを、どのphaseとtoolで観測したか。
- Artifact digest、SBOM digest、serial、version、root componentをどこで結ぶか。
- Artifact typeに含まれ得るcomponent surfaceと、generatorが観測できない範囲は何か。
- Format validity、relationship consistency、composition claim、実際のcoverageを誰がどう確認するか。
- ArtifactとSBOMの公開をどのcomplete stateでそろえ、consumer viewからどう取得確認するか。
- Analysis targetを何のproject／release identityで固定し、upload identityへどこまで権限を渡すか。
- 受付、validation、ingestion、analysis完了、data freshnessをどう分けるか。
- Componentからbuild artifact、deployment、製品ownerへ逆引きできるか。Collector失敗をどの状態にするか。

次に[control](README.md)で必要な特性を確認し、[pattern](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)で実装境界を選びます。
