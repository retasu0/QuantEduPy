# Jules向けタスク定義

このドキュメントは、FinSimLabをOSSとして魅力的にするために、Google Julesへ順番に依頼するタスクと要件をまとめたものです。

FinSimLabは、金融工学とリスク管理をPythonで学ぶための教育用シミュレーションライブラリです。投資助言や売買推奨ではなく、初学者がコード、グラフ、Notebookを通じて概念を理解することを目的にします。

## 基本方針

Julesに依頼する作業は、次の方針に沿って進めます。

- 教育OSSとしての信頼性を上げる。
- インストールから最初の成功体験までを短くする。
- Notebook、examples、README、testsの整合性を高める。
- 投資助言と誤解される表現を避ける。
- コア機能はAPIキーなしで動く状態を維持する。
- OpenAI API連携は任意機能として明確に分離する。
- 実データ取得、売買シグナル、高頻度取引、投資推奨は入れない。
- 1タスクの差分はレビューしやすいサイズにする。

## Jules運用ルール

各タスクをJulesに投げるときは、次を守ります。

- 1回に1タスクだけ依頼する。
- 依頼文には「触ってよいファイル」と「触らないファイル」を明記する。
- 実装後は `python -m pytest`、Notebook JSON検証、example実行のうち該当するものを必ず確認させる。
- READMEやROADMAPなど共有ファイルを触るタスクは、他の大きな実装タスクと同時に投げない。
- 金融・投資に関する表現は教育目的に限定させる。
- 変更ファイル、検証結果、残課題をJulesの最終回答に必ず書かせる。

## 優先順位

### P0: 公開前に必ずやる

- タスク1: 公開前チェックリストを作る
- タスク2: READMEをOSS公開向けに磨く
- タスク3: CONTRIBUTING / SECURITY / CODE_OF_CONDUCTを追加する
- タスク4: Notebookとexamplesの検証導線を整える

### P1: OSSとして見栄えを上げる

- タスク5: 用語集を作る
- タスク6: APIリファレンス生成の土台を作る
- タスク7: サンプルギャラリーを作る
- タスク8: GitHub Actionsを強化する

### P2: 体験を広げる

- タスク9: Streamlitデモを追加する
- タスク10: OpenAI説明機能のドキュメントを安全に整える
- タスク11: 教材Notebookの演習を拡充する

### P3: 機能を広げる

- タスク12: シナリオ分析機能を追加する
- タスク13: パラメータ推定ヘルパーを追加する
- タスク14: オプション戦略payoff可視化を追加する
- タスク15: 金利モデルのシミュレーションを追加する

## タスク1: 公開前チェックリストを作る

### 目的

OSS公開前に必要な確認事項を一覧化し、リポジトリの未整備箇所を見えるようにする。

### Julesへの依頼文

```text
FinSimLabのOSS公開前チェックリストを作成してください。

触ってよいファイル:
- docs/RELEASE_CHECKLIST.md

触らないファイル:
- README.md
- docs/ROADMAP.md
- pyproject.toml
- finsimlab/**
- tests/**
- notebooks/**

要件:
- 日本語で書く。
- インストール、テスト、Notebook、examples、ライセンス、README、CI、セキュリティ、投資助言ではない旨の表記を確認項目に含める。
- 各項目はチェックボックス形式にする。
- 「必須」「推奨」「将来対応」に分ける。
- Julesが判断できない項目は「要確認」と書く。

完了後、変更ファイルと追加したセクションを報告してください。
```

### 完了条件

- `docs/RELEASE_CHECKLIST.md` が存在する。
- 公開前に見るべき項目がチェックボックスで整理されている。
- 金融教育OSSとしての注意事項が含まれている。

## タスク2: READMEをOSS公開向けに磨く

### 目的

READMEを、初見の開発者や学習者が「何ができるか」「どう試すか」をすぐ理解できる構成にする。

### Julesへの依頼文

```text
FinSimLabのREADMEをOSS公開向けに改善してください。

触ってよいファイル:
- README.md

触ってよい範囲:
- 構成の整理
- クイックスタート追加
- examples / notebooks / docs への導線追加
- 非投資助言の注意書きの整理

触らないファイル:
- pyproject.toml
- docs/ROADMAP.md
- finsimlab/**
- tests/**

要件:
- 日本語を基本にする。
- 最初の30秒で「教育用金融シミュレーションライブラリ」と分かるようにする。
- `pip install -e ".[dev,notebook]"` のローカル導入手順を残す。
- APIキーなしで使えるコア機能と、任意のOpenAI API機能を明確に分ける。
- examplesとnotebooksへのリンクを追加する。
- 投資助言・売買推奨ではないことを明記する。
- 長くなりすぎる場合は詳細をdocsへ逃がす提案を書く。

検証:
- Markdownリンクが相対パスとして成立しているか確認する。

完了後、変更点と残した課題を報告してください。
```

### 完了条件

- READMEの冒頭、導入、使用例、学習導線が読みやすい。
- APIキーなし機能と任意OpenAI機能が混同されない。
- 初学者が次に開くべきNotebookが分かる。

## タスク3: CONTRIBUTING / SECURITY / CODE_OF_CONDUCTを追加する

### 目的

OSSとして受け入れ可能な体裁を整え、外部貢献者が参加しやすい状態にする。

### Julesへの依頼文

```text
FinSimLabにOSS運営用ドキュメントを追加してください。

触ってよいファイル:
- CONTRIBUTING.md
- SECURITY.md
- CODE_OF_CONDUCT.md

触らないファイル:
- README.md
- docs/ROADMAP.md
- pyproject.toml
- finsimlab/**
- tests/**

要件:
- 日本語で書く。
- CONTRIBUTINGには、開発環境、テスト方法、Notebook更新方針、金融表現の注意点を書く。
- SECURITYには、脆弱性報告先は未定であること、公開前はGitHub Issuesではなくmaintainerへ相談する想定であることを書く。
- CODE_OF_CONDUCTは簡潔でよい。攻撃的表現、差別、嫌がらせを禁止する。
- 投資助言や個別銘柄推奨のPRは受け付けない方針をCONTRIBUTINGに明記する。

完了後、各ファイルの要約を報告してください。
```

### 完了条件

- 外部貢献者が最低限の作業方法を理解できる。
- 金融OSSとして避けるべきPRの方針が明記されている。

## タスク4: Notebookとexamplesの検証導線を整える

### 目的

Notebookとexamplesが壊れていないことを、ローカルとCIで確認しやすくする。

### Julesへの依頼文

```text
FinSimLabのNotebookとexamples検証導線を整えてください。

触ってよいファイル:
- scripts/check_notebooks.py
- scripts/run_examples.py
- .github/workflows/tests.yml
- docs/RELEASE_CHECKLIST.md

触らないファイル:
- finsimlab/**
- notebooks/**
- examples/**
- README.md
- pyproject.toml

要件:
- Notebookは実行ではなくJSON形式検証を行う。
- examplesは `--no-show` があるものはそれを使って実行する。
- `examples/explain_simulation.py` はOpenAI APIを呼ばないfallback実行にする。
- CIに追加する場合は、既存のpytestを壊さない。
- スクリプトは標準ライブラリ中心で作る。

検証:
- `python scripts/check_notebooks.py`
- `python scripts/run_examples.py`
- `python -m pytest`

完了後、追加したコマンドと検証結果を報告してください。
```

### 完了条件

- Notebook JSON検証を1コマンドで実行できる。
- examplesを1コマンドで実行できる。
- CIまたはチェックリストに検証手順が入っている。

## タスク5: 用語集を作る

### 目的

初学者がNotebookやREADMEで出てくる金融工学用語を確認できるようにする。

### Julesへの依頼文

```text
FinSimLabの初学者向け用語集を作成してください。

触ってよいファイル:
- docs/GLOSSARY.md

触らないファイル:
- README.md
- docs/ROADMAP.md
- finsimlab/**
- notebooks/**
- tests/**

要件:
- 日本語で書く。
- 用語は50音順またはカテゴリ順に整理する。
- 含めるカテゴリ:
  - 確率過程
  - オプション
  - リスク管理
  - ポートフォリオ
  - 債券・金利
  - シミュレーション
- 各用語は2〜4文で説明する。
- 投資助言に見えない表現にする。
- 必要なら「FinSimLabでの使い方」を1行追加する。

完了後、追加したカテゴリと代表的な用語を報告してください。
```

### 完了条件

- READMEやNotebookを読む補助資料として使える。
- 説明が短く、初学者向けである。

## タスク6: APIリファレンス生成の土台を作る

### 目的

関数が増えてきたため、将来的にドキュメントサイトを作れる土台を用意する。

### Julesへの依頼文

```text
FinSimLabのAPIリファレンス生成の土台を作ってください。

触ってよいファイル:
- docs/API_REFERENCE.md
- scripts/generate_api_reference.py

触らないファイル:
- finsimlab/**
- pyproject.toml
- README.md
- docs/ROADMAP.md

要件:
- 外部依存を追加しない。
- `finsimlab` の主要公開APIをimportし、関数名、モジュール、docstringの先頭行をMarkdownに出力するスクリプトを作る。
- 生成先は `docs/API_REFERENCE.md` とする。
- OpenAI APIを呼ばない。
- import時にAPIキーが必要にならないことを確認する。

検証:
- `python scripts/generate_api_reference.py`
- `python -m pytest`

完了後、生成されたAPIカテゴリと検証結果を報告してください。
```

### 完了条件

- 公開API一覧がMarkdownで確認できる。
- 依存追加なしで生成できる。

## タスク7: サンプルギャラリーを作る

### 目的

examplesとnotebooksが増えたため、何を試せるかを一覧できるドキュメントを作る。

### Julesへの依頼文

```text
FinSimLabのサンプルギャラリーを作成してください。

触ってよいファイル:
- docs/EXAMPLES.md

触らないファイル:
- examples/**
- notebooks/**
- finsimlab/**
- tests/**
- README.md

要件:
- 日本語で書く。
- 各exampleについて、目的、実行コマンド、期待される出力の概要を書く。
- 各Notebookについて、学べる内容、前提知識、試すパラメータを書く。
- `--no-show` があるexampleはその使い方を書く。
- `explain_simulation.py` はfallback実行とOpenAI API実行を分けて説明する。
- 投資助言ではなく教育目的であることを明記する。

完了後、追加したセクションを報告してください。
```

### 完了条件

- 初学者がどのサンプルから始めるべきか分かる。
- examplesとnotebooksの関係が分かる。

## タスク8: GitHub Actionsを強化する

### 目的

OSSとして最低限のCI品質を整える。

### Julesへの依頼文

```text
FinSimLabのGitHub Actionsを強化してください。

触ってよいファイル:
- .github/workflows/tests.yml

触らないファイル:
- finsimlab/**
- tests/**
- notebooks/**
- examples/**
- README.md
- pyproject.toml

要件:
- Python 3.10, 3.11, 3.12 のテストを維持する。
- `python -m pytest` を実行する。
- Notebook JSON検証とexamples実行スクリプトが存在する場合はCIに追加する。
- `education` extraのOpenAI API実呼び出しはCIで行わない。
- CIが長くなりすぎないようにする。

完了後、CIで実行されるコマンド一覧を報告してください。
```

### 完了条件

- CIでテスト、Notebook JSON検証、examples検証が走る。
- OpenAI APIキーなしでCIが通る設計になっている。

## タスク9: Streamlitデモを追加する

### 目的

Notebookに不慣れな人でも、ブラウザ上でシミュレーションを体験できるようにする。

### Julesへの依頼文

```text
FinSimLabに教育用Streamlitデモを追加してください。

触ってよいファイル:
- app/streamlit_app.py
- docs/STREAMLIT_DEMO.md
- pyproject.toml

触らないファイル:
- finsimlab/**
- tests/**
- notebooks/**
- README.md
- docs/ROADMAP.md

要件:
- Streamlitはoptional dependencyにする。
- デモは教育目的で、投資助言ではないことを画面内に明記する。
- 最初の画面でGBM、VaR/CVaR、Black-Scholesのいずれかを触れるようにする。
- スライダーで `mu`, `sigma`, `n_paths`, `strike` などを変えられるようにする。
- 実データ取得や個別銘柄入力は入れない。
- OpenAI APIは呼ばない。

検証:
- `python -m pytest`
- `python -m compileall app`

完了後、起動コマンドと追加した機能を報告してください。
```

### 完了条件

- `streamlit run app/streamlit_app.py` で動く想定のデモがある。
- 依存はoptionalで、コアインストールを重くしない。

## タスク10: OpenAI説明機能のドキュメントを安全に整える

### 目的

任意のOpenAI API機能を、誤って投資助言やAPI必須機能に見せないよう整理する。

### Julesへの依頼文

```text
FinSimLabのOpenAI説明機能のドキュメントを作成してください。

触ってよいファイル:
- docs/OPENAI_EXPLANATIONS.md

触らないファイル:
- finsimlab/**
- tests/**
- pyproject.toml
- README.md

要件:
- 日本語で書く。
- `fallback=True` のAPIキー不要利用を最初に説明する。
- OpenAI APIを使う場合の任意依存インストールと `OPENAI_API_KEY` 設定を書く。
- 投資助言ではなく教育説明であることを明記する。
- 実APIを呼ぶサンプルと、呼ばないサンプルを分ける。
- エラー時の対処を書きすぎず、最小限にする。

完了後、主なセクションを報告してください。
```

### 完了条件

- APIキーなし利用とAPI利用の違いが明確。
- OpenAI機能がコア機能ではないことが伝わる。

## タスク11: 教材Notebookの演習を拡充する

### 目的

Notebookを「読むだけ」から「手を動かして学ぶ教材」に近づける。

### Julesへの依頼文

```text
FinSimLabの教材Notebookに演習を追加してください。

触ってよいファイル:
- notebooks/01_random_walk_and_gbm.ipynb
- notebooks/02_monte_carlo_option_pricing.ipynb
- notebooks/03_portfolio_risk.ipynb
- notebooks/04_var_and_cvar.ipynb
- notebooks/05_bonds_and_duration.ipynb

触らないファイル:
- finsimlab/**
- tests/**
- README.md
- docs/**

要件:
- 各Notebookに演習を2つ以上追加する。
- 演習はパラメータ変更、グラフ観察、結果の短い解釈を中心にする。
- 完全な解答を長く書かない。
- 投資判断につながる表現を避ける。
- Notebook JSONを壊さない。

検証:
- 各Notebookを `python -m json.tool` で検証する。

完了後、各Notebookに追加した演習の要約を報告してください。
```

### 完了条件

- すべてのNotebookに学習者が試せる演習がある。
- JSONとして有効である。

## タスク12: シナリオ分析機能を追加する

### 目的

損失分布やポートフォリオに対して、簡単なショックを与えたときの影響を学べるようにする。

### Julesへの依頼文

```text
FinSimLabに教育用のシナリオ分析機能を追加してください。

触ってよいファイル:
- finsimlab/scenarios/__init__.py
- finsimlab/scenarios/shocks.py
- finsimlab/scenarios/reports.py
- examples/scenario_analysis.py
- notebooks/06_scenario_analysis.ipynb
- tests/test_scenarios.py

触らないファイル:
- README.md
- docs/ROADMAP.md
- pyproject.toml
- 既存の finsimlab/options/**
- 既存の finsimlab/risk/**
- 既存の finsimlab/portfolio/**
- 既存の tests/test_*.py

要件:
- 日本語のdocstringまたはコメントは必要最小限にする。関数名は英語にする。
- `apply_price_shock(prices, shock)` を実装する。`shock=-0.1` なら価格を10%下げる。
- `apply_return_shock(returns, shock)` を実装する。既存リターンにショックを加える。
- `scenario_loss(portfolio_value, return_shock)` を実装する。損失は正の値として返す。
- `scenario_report(scenarios: dict[str, float], *, portfolio_value: float)` を実装し、シナリオ名ごとの損失を辞書で返す。
- 実データ取得、銘柄入力、投資判断、売買推奨は入れない。
- exampleは `--no-show` なしでもよいが、OpenAI APIや外部通信は使わない。
- Notebookでは「シナリオ分析は予測ではなく、仮定を置いた感度確認」と明記する。

検証:
- `python -m pytest`
- `python examples/scenario_analysis.py`
- `python -m json.tool notebooks/06_scenario_analysis.ipynb`

完了後、追加API、変更ファイル、検証結果、残課題を報告してください。
```

### 完了条件

- 価格ショック、リターンショック、シナリオ別損失を計算できる。
- 損失は正の値として扱う方針が既存のVaR/CVaRと整合している。
- Notebookでシナリオ分析の限界が説明されている。

## タスク13: パラメータ推定ヘルパーを追加する

### 目的

シミュレーションの入力値をどう決めるかを学べるよう、リターン系列から簡単なパラメータ推定を行う機能を追加する。

### Julesへの依頼文

```text
FinSimLabに教育用のパラメータ推定ヘルパーを追加してください。

触ってよいファイル:
- finsimlab/estimation/__init__.py
- finsimlab/estimation/returns.py
- finsimlab/estimation/gbm.py
- examples/estimate_parameters.py
- notebooks/07_parameter_estimation.ipynb
- tests/test_estimation.py

触らないファイル:
- README.md
- docs/ROADMAP.md
- pyproject.toml
- 既存の finsimlab/simulations/**
- 既存の tests/test_*.py

要件:
- `estimate_mean_return(returns, *, periods_per_year=252)` を実装する。
- `estimate_volatility(returns, *, periods_per_year=252)` を実装する。
- `estimate_gbm_parameters(prices, *, periods_per_year=252)` を実装し、`mu` と `sigma` を含む辞書を返す。
- `prices` は正の値のみ受け付ける。
- 推定値は教育用途の単純推定であることをdocstringとNotebookに明記する。
- 実データ取得は入れない。exampleは合成データか固定の小さな配列を使う。
- 推定結果を投資判断に使うような説明は避ける。

検証:
- `python -m pytest`
- `python examples/estimate_parameters.py`
- `python -m json.tool notebooks/07_parameter_estimation.ipynb`

完了後、追加API、推定式の概要、検証結果を報告してください。
```

### 完了条件

- リターン系列と価格系列から基本的な年率リターン・volatilityを推定できる。
- シミュレーションの入力値と推定値の関係をNotebookで学べる。

## タスク14: オプション戦略payoff可視化を追加する

### 目的

コール・プット単体だけでなく、複数のオプションを組み合わせたpayoffを教育用に可視化できるようにする。

### Julesへの依頼文

```text
FinSimLabにオプション戦略payoffの教育用可視化を追加してください。

触ってよいファイル:
- finsimlab/options/strategies.py
- finsimlab/options/strategy_plots.py
- examples/option_strategy_payoff.py
- notebooks/08_option_strategy_payoff.ipynb
- tests/test_option_strategies.py

触らないファイル:
- README.md
- docs/ROADMAP.md
- pyproject.toml
- finsimlab/options/black_scholes.py
- finsimlab/options/monte_carlo.py
- finsimlab/options/greeks.py
- 既存の tests/test_options.py

要件:
- `option_leg_payoff(prices, *, option_type, strike, premium=0.0, quantity=1)` を実装する。
- `strategy_payoff(prices, legs)` を実装する。`legs` は辞書のリストでよい。
- `plot_strategy_payoff(prices, payoff, *, title=None, ax=None)` を実装する。
- strategy builderとして `long_call`, `long_put`, `bull_call_spread`, `straddle` の小さなヘルパーを追加してよい。
- これは売買推奨ではなく、payoff構造を学ぶ教材であるとNotebookに明記する。
- 損益図ではpremiumを反映できるようにする。
- 外部データや実銘柄は使わない。

検証:
- `python -m pytest`
- `python examples/option_strategy_payoff.py --no-show`
- `python -m json.tool notebooks/08_option_strategy_payoff.ipynb`

完了後、追加API、対応した戦略、検証結果を報告してください。
```

### 完了条件

- 複数legのpayoffを合算できる。
- 初学者がオプション戦略の形をグラフで理解できる。
- 投資助言に見えない説明になっている。

## タスク15: 金利モデルのシミュレーションを追加する

### 目的

債券価格やデュレーションの前段として、金利が時間とともに変化する単純モデルを学べるようにする。

### Julesへの依頼文

```text
FinSimLabに教育用の金利モデルシミュレーションを追加してください。

触ってよいファイル:
- finsimlab/rates/__init__.py
- finsimlab/rates/vasicek.py
- finsimlab/rates/plots.py
- examples/interest_rate_simulation.py
- notebooks/09_interest_rate_models.ipynb
- tests/test_rates.py

触らないファイル:
- README.md
- docs/ROADMAP.md
- pyproject.toml
- finsimlab/bonds/**
- finsimlab/simulations/**
- 既存の tests/test_*.py

要件:
- `simulate_vasicek(initial_rate, long_term_mean, speed, volatility, *, years=1.0, steps=252, n_paths=1, seed=None)` を実装する。
- 戻り値は既存の価格パスと同じく `(steps + 1, n_paths)` の `numpy.ndarray` にする。
- `plot_rate_paths(paths, *, title=None, ax=None)` を実装する。
- 入力検証は既存simulation系と同じ雰囲気にする。
- Vasicekは負の金利を取り得ることをNotebookに明記する。
- CIRなど、非負制約付きモデルは今回は入れない。
- 実データ取得や金利予測は入れない。

検証:
- `python -m pytest`
- `python examples/interest_rate_simulation.py --no-show`
- `python -m json.tool notebooks/09_interest_rate_models.ipynb`

完了後、追加API、モデルの制約、検証結果を報告してください。
```

### 完了条件

- Vasicek型の金利パスを複数本シミュレーションできる。
- 既存のsimulation APIと戻り値形式がそろっている。
- 金利予測ではなく教育用モデルであることが明記されている。

## Julesに投げる順番

最初は次の順番がよいです。

1. タスク1: 公開前チェックリストを作る
2. タスク3: CONTRIBUTING / SECURITY / CODE_OF_CONDUCTを追加する
3. タスク4: Notebookとexamplesの検証導線を整える
4. タスク2: READMEをOSS公開向けに磨く
5. タスク5: 用語集を作る
6. タスク7: サンプルギャラリーを作る
7. タスク8: GitHub Actionsを強化する
8. タスク12: シナリオ分析機能を追加する
9. タスク13: パラメータ推定ヘルパーを追加する
10. タスク14: オプション戦略payoff可視化を追加する
11. タスク15: 金利モデルのシミュレーションを追加する

Streamlitデモは見栄えが良くなりますが、依存追加とUIレビューが必要です。先にドキュメント、検証導線、OSS運営ファイル、教育用の追加機能を整えた方が、公開時の信頼性が上がります。

## Julesへの共通テンプレート

各タスクを依頼するときは、次の一文を先頭に付けると安全です。

```text
このリポジトリは教育目的の金融工学シミュレーションOSSです。投資助言、売買推奨、個別銘柄推奨に見える表現や機能は追加しないでください。指定されたファイル以外は変更しないでください。変更後は、実行した検証コマンドと結果、変更ファイル一覧、残課題を日本語で報告してください。
```
