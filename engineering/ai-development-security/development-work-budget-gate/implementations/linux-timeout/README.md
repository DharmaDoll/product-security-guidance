# Linux timeoutによるローカル実行期限

非対話の開発agentコマンドを、決めた時間で停止する例です。任意の手元のrepositoryやCIの起動コマンドにGNU `timeout`を付けます。Agentやmodelはsmoke testで呼び出さず、ローカルの無害なprocessで成功・停止・起動失敗を確認します。

対象はLinux、GNU coreutils **9.7**です。Smoke testはPython **3.10.4**で確認しました。ライブラリの追加は不要です。[GNU公式仕様](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html)と[資料記録](../../../../../sources/README.md#ref-linux-process-deadline-001)を参照してください。

## 手元へ入れる最短手順

まず`timeout --version`でGNU版と版を確認します。以下を、採用先の非対話agentの起動を管理するshell scriptまたはCI stepへ入れ、`your-agent`以降を実際のコマンドに置き換えます。この例の15分と停止猶予5秒は説明用の選択値です。作業の所有者が許可する時間と終了処理の猶予へ変えてください。

```sh
if timeout --signal=TERM --kill-after=5s 900s your-agent ...; then
    result=0
else
    result=$?
fi
case "$result" in
    0) printf '%s\n' 'LOCAL_COMMAND_EXITED_0' ;;
    124) printf '%s\n' 'DEADLINE_REACHED_REVIEW_PENDING_EFFECTS' >&2 ;;
    137) printf '%s\n' 'KILL_REPORTED_CHECK_PROCESS_AND_PENDING_EFFECTS' >&2 ;;
    *) printf '%s\n' 'COMMAND_OR_LAUNCH_FAILED' >&2 ;;
esac
exit "$result"
```

`0`はコマンドの正常終了であり、成果物や開発作業の正しさを証明しません。`124`は期限到達、`137`はKILLに関する状態です。`137`だけでは、監視対象と`timeout`自身のどちらがKILLされたかを区別できません。`125`は`timeout`の失敗、`126`は実行不能、`127`はコマンドが見つからない状態です。対象コマンド自身が同じ数値を返すこともあるので、終了コードだけで停止原因を完全に特定しません。

管理された起動設定は、agentが編集できる未信頼の作業ツリーから分けます。再試行時にこの900秒を毎回新しく与えると、一依頼の上限になりません。Launcher側で元の作業の残り時間を引き継ぐか、人が追加実行を承認します。前者の永続台帳はこの例には含めません。

`|| true`、自動的な再起動、無制限のretryを加えないでください。`--preserve-status`は期限到達のコードを保持しないため、この例では使いません。`--foreground`は子processを同じようにtimeoutしないため使いません。実行期限やKILL猶予を`0`にすると対応する期限が無効になります。

## 簡単なsmoke test

本PJのrootで実行します。任意のrepositoryへ設定を移す前にも使えます。

```sh
python3 -m unittest discover \
  -s engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout \
  -p 'test_*.py' -v
```

六件のテストで、正常終了、対象コマンドの失敗、期限による停止、TERMを無視した場合のKILL、同じprocess groupの子process停止、起動不能を確認します。使い捨ての一時ディレクトリに書くheartbeatが停止後に増えないことも観測します。自分で試す最短例は`timeout --kill-after=1s 1s sleep 10`です。終了コード`124`になります。API鍵、実model、ソース変更、ネットワークは不要です。

## 解除と限界

解除は、起動コマンドの`timeout`部分と終了状態の分岐を取り除くことです。その経路から実行期限もなくなるため、代替のjob期限があるかを確認します。

この例はTTY入力が不要で、監視対象が前景で動き続けるローカルprocessに適用します。期限でTERMを送り、猶予後に必要ならKILLを送ります。実際の停止時刻はschedulerなどの状態に左右され、厳密な時刻保証ではありません。親が先に終了して残すbackground処理、別sessionへ離脱したprocess、別job・container・遠隔serviceは、この例の停止対象として保証しません。悪意あるagentが監視processを止められる環境の隔離境界にもなりません。

Token・費用・呼び出し回数は数えません。送信済みの外部操作の取消、結果確認、認証情報の失効も行いません。実agentの採用時には子processの起動方式、停止、外部結果を別途確認します。[設計パターン](../../README.md)の共通予算管理と[AI-004](../../../../../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の認可・隔離を組み合わせて判断してください。
