# A release can have provenance and still leave an artifact unverifiable

## シナリオ

あるreleaseにはLinux、macOS、Windowsの三つのbinaryとcontainer imageがありました。Release automationは`provenance.intoto.jsonl`を一つuploadし、画面には「provenanceあり」と表示されます。

そのfileが説明するsubjectはLinux binaryだけでした。Windows利用者は同じrelease pageからfileを取得できましたが、自分がdownloadしたdigestに対応するprovenanceはありません。Container利用者はregistryからimageを取得するため、source hostingのrelease pageにあるprovenanceの存在も知りませんでした。

一か月後、cleanup jobはprovenance fileを削除しました。Binaryとimageはmirrorとregistryに残り、引き続き取得できます。Monitoringはrelease recordの`provenance_required: true`だけを見ていたため、取得不能を検知しませんでした。

## 何が境界だったか

「Releaseにprovenanceがある」と「利用者が取得したartifactに対応するprovenanceを取得できる」は異なります。一releaseには複数artifactがあり、一artifactには複数種類のattestationがあり得ます。

必要なのは、次の鎖です。

```text
consumerが取得したartifact digest
  -> 配布channelでのartifact identity
  -> artifactに対応するattestation identityの一覧
  -> immutable provenance bytesの取得
  -> consumer-owned policyによる検証
```

このcontrolは中央の配布部分を扱います。最後の検証はREL-001の責任です。

## 用語

- **Artifact-level binding**：Release名ではなく、artifactのcryptographic digestから対応するattestationを識別できる関係。
- **Attestation**：あるsubjectについて主体が行う署名可能なstatement。Build provenanceはattestationの一種。一artifactに複数存在し得る。
- **Discovery relation**：Artifactから対応するattestationを探す規則またはindex。Sidecar名、registry attachment、manifest、API等で表せる。
- **Intended consumer**：Artifactを取得・検証することを許可された利用者、service、package client。Public userだけとは限らない。
- **Publication completion**：Artifact、required provenance、discovery relationが、利用者の経路からdurableに取得可能になった状態。
- **No downgrade**：一度requiredとしたartifact familyやchannelで、欠落・取得不能・tool障害をoptionalまたはlegacyへ自動的に弱めないこと。

## 悪用・失敗経路を分解する

1. Release automationが複数artifactを公開する。
2. Provenanceをrelease単位のfile名やmutable tagへ置き、artifact digestとのrelationを持たない。
3. Artifact uploadだけが成功し、provenanceまたはindexは失敗・遅延する。
4. Producer側のcredentialでは取得できるため、releaseをcompleteにする。
5. Consumerのpackage client、registry、mirror、networkからはprovenanceを発見・取得できない。
6. Storage lifecycle、cleanup、replication failureでprovenanceだけが消える。
7. Monitoringがpolicy flagや古いinventoryだけを見て、実取得不能を正常とする。
8. Consumerは検証を省略するか、別artifact向けのprovenanceを誤って使う。

## よくある誤解

### 「Releaseにprovenance fileが一つあればよい」

Releaseは複数artifactを含み、後から追加される場合もあります。各artifact digestから対応するprovenanceを選べる必要があります。逆に一artifactへ複数attestationが付くこともあります。

### 「Artifactと同じfile名なら対応は明らか」

Filenameやpathは変更・再利用され得ます。発見の手掛かりにはできますが、最終的な対応はexact digestとimmutable attestation identityで確認します。

### 「Upload APIが成功したので利用者も取得できる」

Producer write権限とconsumer read権限、region、mirror、media type対応、package clientのdiscoveryは異なります。Intended consumerの経路からprobeします。

### 「Provenanceはpublicにすべき」

SLSAはconsumerへ配布することを求めますが、private artifactのprovenanceまでpublicにする必要はありません。Intended consumerがcredentialを漏らさず取得できるaccessを設計します。

### 「365日保持すれば十分」

必要期間はartifactのdownload、support、使用、監査、incident調査の期間で決まります。固定日数を全productへ配りません。Artifactが残るのにprovenanceだけ先に消える状態を避けます。

## 判断基準

- Provenanceをrequiredとするartifact family、channel、consumerはどれか。
- 一releaseの全artifactを何のdigestで列挙し、後からの追加をどう扱うか。
- Artifactから一つ以上のprovenanceをどの規則・index・APIで発見するか。
- Artifact、provenance、relationをどのimmutable identityで参照するか。
- Release complete前に、どのconsumer viewから何を取得確認するか。
- Artifactの取得・support・調査期間に対して、provenanceとindexをいつまで保持するか。
- Mirror、cache、replica、withdrawal、collection failureをどの状態として扱うか。

次に[control](README.md)で必要な特性を確認し、[pattern](../../../../engineering/release-integrity/provenance-distribution-and-availability/README.md)でartifact ecosystemへ落とします。
