# Approval is bound to an action

[コントロール記録](README.md) · [設計パターン](../../../../engineering/ai-development-security/development-action-authorization/README.md)

## 「公開してよい」の後で何が変わったか

開発者はagentが作った修正を確認し、レビュー用branchへの公開を承認しました。ところが、リポジトリ内の作業用scriptには、別のremoteへ送信する処理が含まれていました。
Agentがscriptを実行でき、公開用の認証情報も使えれば、承認したつもりの範囲を越えてソースを送信できます。悪意あるscriptがあっても、公開権限がなく送信経路も閉じていれば、この経路は成立しません。

問題は確認画面の有無ではなく、確認した対象と実際の操作が同じかどうかです。

## 三つの判断を分ける

1. **読み込んでよいか**：その拡張や指示を採用する判断。内容の審査は、後のすべての操作を許可するものではありません。
2. **この操作をしてよいか**：誰が、どのリポジトリ・branchへ、どの内容を、どの方法で公開するかを決める判断。
3. **実際にどうなったか**：実行先が受け付けたか、変更したかを確認する判断。送信したことも、応答がないことも、結果の確定とは違います。

認可とは、特定の主体による特定の操作を許可することです。承認はその入力になり得ますが、agent自身が対象を書き換えたり、有効期限を延ばしたりできるなら強制力がありません。

## 応答が失われたら

公開要求を送った直後に通信が切れました。実行先では成功していても、開発端末では結果が分かりません。
同じ承認を使って再送すると、操作によっては重複したリリースや変更を作ります。元の要求の識別情報を保って実行先を確認し、結果不明を成功・未実行へ置き換えないことが重要です。

## Codex CLIでリポジトリをtrustedにする前に

別の開発者から受け取ったリポジトリをCodex CLIで開く場面を考えます。`AGENTS.md`に「ネットワークへ送信しない」と書かれていても、それはagentへの指示です。実際の権限は設定と実行環境で決まります。Trusted projectの`.codex/config.toml`はuser設定より優先されるため、信頼の判断にはリポジトリ内の設定を読ませるかという判断も含まれます。管理側のrequirementsは別の強制層です。

ここで確認するのは、(1) project設定、起動時の指定、管理方針を合わせた実効権限、(2) shell以外のWeb検索・MCP・hookを含む外部経路、(3) 設定とローカル履歴に秘密情報が残る経路です。例えばshellの通信を閉じても、別のtoolに通信経路があれば「外部へ出ない」とは判定できません。履歴を抑える設定についても、どの保存物に効くかを分けて確認します。

このシナリオは[Codex CLI Hardening Cheatsheetと公式資料の照合](../../../../sources/README.md#ref-codex-cli-hardening-001)から得た確認観点です。特定の設定例をそのまま適用する手順ではなく、実効権限の診断も未実施です。境界の置き方は[Development runtime isolation](../../../../engineering/ai-development-security/development-runtime-isolation/README.md)へ進みます。

## 設計レビューで問うこと

- 人が見た対象と実行対象を、どこで照合するか。
- Agentが持つ別の認証情報やshell経由で、その照合を迂回できないか。
- 一つの承認を二つの処理が同時に使用したらどうなるか。
- 結果不明の操作を誰が調べ、どの条件なら再実行するか。
- Trusted projectの設定を変更すると、user設定だけを確認した時より到達範囲が広がらないか。
- Shell、Web検索、MCP、hook、履歴を別々に確認し、未確認の経路を「拒否済み」としていないか。

具体的な方式と代償は[Development action authorization](../../../../engineering/ai-development-security/development-action-authorization/README.md)へ分けています。
供給経路では[攻撃段階3から2・6への受け渡し](../../../../docs/ANALYSIS_LENSES.md)に当たります。資料の版と、この教材における解釈は[参照資料](../../../../sources/README.md#ref-development-action-authorization-001)で確認できます。

対応する成果物：[コントロール記録](README.md) · [Development action authorization](../../../../engineering/ai-development-security/development-action-authorization/README.md)
