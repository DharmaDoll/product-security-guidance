# Workflow input handlingを具体例から読む

[PSB-CICD-002](README.md)の教材です。PRの題名を確認する処理を追い、**値を文字列として渡すことと、呼出先に許してよい操作を選ぶこと**を分けて理解します。

## 題名を表示するだけのはずだった

チームは、PRの題名をCIで表示したいと考えました。GitHub Actionsのstepに次の行を置きます。

```yaml
run: echo "Reviewing ${{ github.event.pull_request.title }}"
```

題名はPRの作成者が変更できます。式`${{ ... }}`はshellが起動する前に評価され、生成されるスクリプトへ結果が埋め込まれます。外側に引用符を置いても、題名そのものが引用符を含めば、生成後の構文を変えられます。[GitHubのScript injections](https://docs.github.com/en/actions/concepts/security/script-injections)が説明する経路です。

説明用に、題名が次の文字列だったとします。追加処理は無害な表示だけで、本番のworkflowへ投入する手順ではありません。

```text
docs"; printf '%s\n' 'UNEXPECTED-STEP'; #
```

生成後のスクリプトは概念的に次の形になります。

```sh
echo "Reviewing docs"; printf '%s\n' 'UNEXPECTED-STEP'; #"
```

元の`echo`の後に別の`printf`が加わりました。値を使うはずの処理が、値から命令を作る処理へ変わっています。問題は引用符の数より前に、**題名をスクリプトのソースへ入れたこと**にあります。

## 値は環境変数で渡し、命令を固定する

GitHubは、inline scriptへ渡す値を環境変数へ置く方式を案内しています。次は違いを読むためのBashのstep断片です。配布・導入用のworkflowではありません。

```yaml
env:
  PR_TITLE: ${{ github.event.pull_request.title }}
shell: bash
run: |
  printf 'Reviewing: %s\n' "$PR_TITLE"
```

命令は固定した`printf`です。環境変数の値は、その引数へ渡されます。先ほどの題名が引用符や区切り文字を含んでも、この通常の変数展開で追加のshell命令へ読み直すことはありません。引数を引用することで空白やワイルドカードによる分割・展開も避けます。GitHubの[Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use#good-practices-for-mitigating-script-injection-attacks)と、[Bash 5.2の仕様記録](../../../../sources/README.md#spec-bash-shell-expansion-5-2)を参照してください。

ここで文字を削除したわけではありません。元の値を命令へ変えずに渡しました。`run:`で`${{ env.PR_TITLE }}`を使うと、再び式の結果をソースへ埋め込む方式に戻ります。また、環境変数を`eval`や値を埋め込んだ`bash -c`へ渡せば、後段で命令として読み直されます。

## 引数を一つに保っても、操作は別に決める

次にチームは、利用者が入力した値から実行する作業を選びたくなりました。この値を引用して渡すだけでは、作業の選択が正しいかは決まりません。

| 値の使い道 | 追加で判断すること |
|---|---|
| 題名を文字列として表示する | 固定した出力形式とデータを分ける。ログ側での表示・制御文字の扱いは別に確認する |
| 実行する作業名を選ぶ | 許可した名前から固定の処理へ対応させる。未知の名前は実行しない |
| プログラムへ対象を渡す | 一つの引数でもオプションとして解釈されないか、対象範囲を外れないか確認する |
| Actionやスクリプトへ渡す | 呼出先が値から命令文字列や実行ファイルを作らないか確認する |

「引用符で囲んだ」は、引数を保つ対策です。「この値が指定する操作を許可する」は、操作の意味を制限する対策です。後者には許可リストや呼出先の引数仕様が必要です。`--`をオプションの終端として使える製品もありますが、対応と位置を確認します。これだけで任意のパス・URL・作業の使用まで許可されるわけではありません。[OWASPの引数注入と対策](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html#argument-injection)を、この二つを区別する補助に使います。

## 被害はjobの実効権限で変わる

題名が追加コマンドになるには、作成者が値を変更でき、その題名を使うイベント・jobが動き、命令として解釈される必要があります。その後の被害はjobに渡した権限と後続への受け渡しで変わります。

書込みtokenもsecretもないjobでも、workspaceや検証結果を変えたり処理を停止したりできます。公開権限やcloud認証情報があれば、その対象への操作も問題になります。前段が作ったartifactやcacheを後段が信用すれば、前段がread-onlyでも影響を引き継ぐ可能性があります。

PR作成者のコードをすでに同じ権限で実行しているjobでは、この欠陥だけで新しい権限が増えるとは限りません。題名だけを扱うはずのjobが初めてコードを実行する場合とは分けて評価します。権限は[CICD-004の教材](../psb-cicd-004-workflow-authority-minimization/learning.md)、未信頼コードと後段への昇格は[CICD-005の教材](../psb-cicd-005-untrusted-pr-boundary/learning.md)で続けて読めます。

## レビューでたどる順序

1. 誰が値を変更でき、どの処理へ届けられるかを確認する。Manual input、matrix、step出力も名前だけで信頼しない。
2. 値が最後にどの言語・プログラムで解釈されるかを追う。環境変数に移した箇所で追跡を終えない。
3. 命令とデータの分離、引数の保持、許可する操作・対象をそれぞれ確認する。
4. 検査で確認できた範囲と未確認の呼出先を分ける。表示名に式があるだけで実行への注入とは判断しない。
5. [診断項目](README.md#診断で確認する項目異常時テスト)を対象構成へ当てはめる。項目があることを拒否の確認済みとはしない。

方式の選択は[Workflow data and command boundary](../../../../engineering/cicd-security/workflow-data-and-command-boundary/README.md)、資料の採否と旧scannerの扱いは[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-input-migration)へ進んでください。
