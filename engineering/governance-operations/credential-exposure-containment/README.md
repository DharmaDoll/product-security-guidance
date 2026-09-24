# Credential exposure containment and recovery

`ENG-GOV-003` / `governance-operations`

## 解く設計問題

Credential漏えい疑いを、単一の値の交換ではなく、旧authority・派生sessionの封じ込め、全consumerの移行、
exposure windowの影響調査、根拠のあるclosureへ変換します。対象読者はincident responder、credential・identity基盤担当、
source・CI・release platform担当、product securityです。

## 推奨構造

```text
Exposure signal
  → secret-free identity + class + exposure window
  → urgent bounded containment + evidence preservation
  → authority / session / consumer graph
  → narrow replacement + consumer disposition
  → independent old-authority denial
  → exact operation and artifact identities → GOV-001 impact assessment
  → unresolved scope or evidence-aware closure
```

一つの直列workflowを全incidentへ強制しません。切迫した被害があれば、観測済みauthorityを先に止め、証拠保全と
consumer発見を並行します。各stepのowner、判断時刻、入力、結果、未観測範囲を同じincident identityへ結び付けます。

## 方式の選択

| 判断 | 選択肢 | 確認事項 |
|---|---|---|
| 即時封じ込め | Disable/revoke、発行停止、policy・trust変更、session終了 | Classごとの失効単位、伝播時間、可用性、break-glass経路 |
| Replacement | 再発行、短命化、federation移行、consumer廃止 | 旧権限以下か、旧値のcopyになっていないか、配布経路 |
| Consumer移行 | In-place更新、段階移行、quarantine、remove | Exact consumer集合、owner、rollback、二重有効期間 |
| 拒否確認 | Provider state、session inventory、introspection、harmless operation | 新credentialの成功から独立しているか、値を再配布しないか、失敗をERRORにするか |
| 影響調査 | Audit query、source/release/artifact/deployment相関 | Exposure window、retention、時刻、pagination、取得権限、exact identity |

旧credentialによるactive probeが追加漏えいや副作用を起こす場合、provider stateとsession inventoryなどの安全な代替を使います。
`DENIED`だけでなく、対象、provider時刻、伝播待ち、確認方法、未確認の派生authorityを記録します。

## 責務の分離

- [SOURCE-002](../../../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)は公開前の検査と拒否を持つ。
- [SOURCE-003](../../../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)はpublic exposureの観測とtriageを持つ。
- [SOURCE-004](../../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)は通常時の発行、権限、inventory、失効条件を持つ。
- 本patternはincident中のauthority graph、封じ込め、replacement、consumer移行、拒否確認を持つ。
- [GOV-001](../../../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)は渡されたidentityからartifact・deployment影響と対応計画を判断する。

Contentの削除、history rewrite、package yank、artifact削除、deployment rollbackをcredential失効へ混ぜません。
これらは証拠と可用性を変えるため、影響調査と独立承認の後に扱います。

## Evidence contract

共有記録へcredential値、private key、authorization header、providerのsecret responseを入れません。最低限、次を追跡します。

- Incident、credential identifier、class、owner、issuer、resource、scope、consumer、派生authority。
- Signal時刻、推定exposure window、その根拠と時刻の不確かさ。
- Containment action、authorization、provider receipt identity、状態、伝播期限。
- Replacementのpurpose・scope・resource・consumer・lifetimeと旧authorityとの差。
- Consumer disposition、old-authority denial method、観測結果、未確認範囲。
- Audit coverage、exact operation・artifact identity、GOV-001 handoff、closure blocker。

Provider APIのtimeout、partial response、rate limit、権限不足、audit retention外、通知失敗を別の状態にします。
Retry可能な障害を「拒否済み」や「操作なし」へ変換しません。

## 失敗経路と確認方法

主要consumerだけの更新、派生sessionの見落とし、広いreplacement、自然失効への依存、新credentialの疎通による拒否確認の代用、
audit空結果の誤読、証拠保全前の破壊的cleanup、secret-bearing ticket、fixture `PASS`のlive証拠化を負のシナリオとして確認します。

Tabletop exerciseでは架空のidentifierとprovider responseを使い、未知consumer、失効伝播中、audit取得不能、通知失敗を
未解決として扱えるかを確認できます。Live testでは専用の非本番credentialと無害な操作を使い、実credentialや本番変更を
このpatternの例へ持ち込みません。Test codeがない場合も、上記観点を診断checklistとして保持できます。

## 具体実装を追加する条件

この主題はcredential classとproviderによってAPI、失効単位、session、trust、auditが変わるため、provider-neutralな
revoke scriptを作りません。具体実装は次を選定できる場合に追加します。

1. Provider、credential class、対象resource、検証用の非本番範囲が明確である。
2. 失効、session、発行条件、audit、rate limit、idempotencyの公式仕様を固定または確認できる。
3. Mutationと拒否確認を分離し、値を保存せず、安全なfailure modeをテストできる。
4. Dry-runまたはfixtureの結果をlive mutation evidenceと区別できる。

旧repositoryのJSON policy、synthetic response bundle、verifierはこの条件を満たさず、移植していません。
製品手順が自明でないcontrolへ一律にコードを付ける旧方式を繰り返さないためです。

## 関連資料と限界

[Control](../../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)、
[移行記録](../../../docs/CREDENTIAL_EXPOSURE_MIGRATION.md)、
[参照資料](../../../sources/README.md#ref-credential-exposure-containment-001)を参照してください。
このpatternは設計と確認項目を示すものであり、実際の認証情報、provider、consumer、audit、incident運用を検証していません。
