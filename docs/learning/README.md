# 学習資料

[Workload federation boundary](../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/learning.md)では、
正規tokenの認証、workloadの許可、交換後の操作権限を分けて学びます。

学習ノートは、コントロールの要約を長くするためのものではありません。一つのセキュリティ問題を
具体的なシナリオから理解し、別のシステムへ応用できるようにする教材です。

## パイロットの学習ノート

[Managed is not currently trusted](managed-is-not-currently-trusted.md)では、登録済み端末の観測が止まった場面から、管理台帳・現在の状態・アクセス判断の違いを学びます。

[Approval is bound to an action](approval-is-bound-to-an-action.md)では、公開の承認後に対象が変わる場面から、拡張の採用・操作の許可・実行結果の違いを学びます。

[Reviewing an agent extension](reviewing-an-agent-extension.md)では、Skillの更新を例に、内容審査・権限・実際の読み込みをつなげて考えます。

[Impact is an evidence chain](impact-is-an-evidence-chain.md)で、component一致、稼働影響、侵害確定の違いを学びます。

[An exception is a decision, not a PASS](an-exception-is-not-a-pass.md)では、security checkの失敗と限定的なrisk acceptanceを分けて学びます。

[Zero findings is a scoped observation](zero-findings-is-a-scoped-observation.md)では、clean・finding・scanner errorとcoverageの違いを学びます。

[No events is not no incident](no-events-is-not-no-incident.md)では、検知なしと観測・通知できなかった状態を分けて学びます。

[Authentication is not object authorization](authentication-is-not-object-authorization.md)では、正規利用者でも対象・操作・tenantごとの許可が必要な理由を学びます。

[Authentic is not acceptable](authentic-is-not-acceptable.md)では、有効な署名でも想定外のソース・生成条件なら拒否する理由を学びます。

[Build code is not build authority](build-code-is-not-build-authority.md)では、承認済みbytesの依存でも、実行時の権限や通信を悪用できる理由を学びます。

[CI state and runner lifecycle](ci-state-and-runner-lifecycle.md)では、新しいrunnerでもcacheから悪意あるstateを復元できることと、cacheを使わなくてもhostにstateが残ることを比較します。

| 領域 | 学習ノート | 中心となる問い |
|---|---|---|
| Source Protection | [Source credential lifecycle](../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/learning.md) | なぜ認証情報を秘密文字列ではなく権限として扱うのか |
| Dependency Security | [Dependency release cooldown](../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/learning.md) | なぜ待機期間はパッケージの安全性ではなく観測時間を提供するのか |
| CI/CD Security | [Untrusted PR boundary](../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/learning.md) | なぜイベントやjobを分けても、状態のproducerとconsumerまで追わなければ境界は成立しないのか |

## 学習ノートに残すもの

[Reviewed dependency intake](reviewed-dependency-intake.md)は、採用判断、artifact同一性、実行許可の違いを
一つの更新シナリオから理解する共有教材です。

追加教材：[Install execution policy](../../controls/records/dependency-security/psb-deps-002-install-execution-policy/learning.md)。
取得・準備・利用を分け、test開始前のコード実行と権限の接続を理解します。

- 主体、データ、操作が分かる一つのシナリオ。
- 攻撃者に可能なこと、信頼境界、悪用経路。
- 初めて出る用語。
- セキュリティ不変条件と強制点。
- 合格／不合格、隣接するセキュリティ特性、保証しない範囲の判断基準。
- よくある誤解と、設計レビューで使える問い。

空の学習ノートや、コントロール本文の複製は作りません。

各学習ノートは、扱うシナリオを[横断分析の軸](../ANALYSIS_LENSES.md)へ接続し、
その成果物が詳しく扱う攻撃段階と、前後に残る境界を区別します。
