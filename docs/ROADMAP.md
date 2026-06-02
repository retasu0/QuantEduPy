# FinSimLab 作業ロードマップ

このドキュメントは、FinSimLab の実装順、設計方針、コンテンツ拡充方針を管理するための作業メモです。

最初から大きな金融工学ライブラリを作るのではなく、初心者が実際に動かしながら学べる小さな機能を積み上げていきます。

## 基本方針

- 教育用途を第一にする。
- API は短く、読みやすく、Notebook で説明しやすい形にする。
- 実装は NumPy / pandas / matplotlib を中心にし、依存関係を増やしすぎない。
- コア機能は OpenAI API や外部サービスなしで動くようにする。
- LLM を使う説明生成やチューター機能はオプション機能として後から追加する。
- 投資助言と誤解される表現は避ける。
- README、Notebook、examples、tests を機能追加と同時に更新する。

## 対象範囲

### 入れるもの

- 金融工学の基礎を学ぶためのシミュレーション
- 価格過程、リスク指標、オプション評価、ポートフォリオ分析
- 初学者向けの説明、グラフ、Notebook
- 小さく再現可能な examples
- テストしやすい純粋関数

### 最初は入れないもの

- 実運用向けの売買シグナル生成
- 投資推奨
- 高頻度取引
- 複雑な市場データ連携
- 過度に高度な数値計算エンジン
- ブラックボックスなAI予測モデル

## 想定リポジトリ構成

```text
finsimlab/
  __init__.py
  simulations/
    __init__.py
    random_walk.py
    gbm.py
    mean_reversion.py
  options/
    __init__.py
    black_scholes.py
    monte_carlo.py
    greeks.py
  risk/
    __init__.py
    var.py
    metrics.py
  portfolio/
    __init__.py
    metrics.py
    efficient_frontier.py
  bonds/
    __init__.py
    pricing.py
    duration.py
  plotting/
    __init__.py
    paths.py
    distributions.py
examples/
  gbm_simulation.py
  black_scholes_option.py
  portfolio_risk.py
notebooks/
  01_random_walk_and_gbm.ipynb
  02_monte_carlo_option_pricing.ipynb
  03_portfolio_risk.ipynb
  04_var_and_cvar.ipynb
docs/
  ROADMAP.md
tests/
```

## 実装フェーズ

### Phase 0: プロジェクト初期化

- [x] README を作成する
- [x] ロードマップを作成する
- [x] `pyproject.toml` を作成する
- [x] Python パッケージ構成を作成する
- [x] 最低限のテスト環境を作成する
- [x] GitHub Actions を追加する
- [x] ライセンスを決める

### Phase 1: シミュレーション基盤

- [x] ランダムウォークを実装する
- [x] 幾何ブラウン運動を実装する
- [x] 平均回帰過程を実装する
- [x] 乱数 seed を扱えるようにする
- [x] 複数パスの戻り値形式を統一する
- [x] 価格パスの可視化ヘルパーを実装する
- [x] `examples/gbm_simulation.py` を追加する
- [x] `notebooks/01_random_walk_and_gbm.ipynb` を追加する

### Phase 2: オプション価格評価

- [x] Black-Scholes のコール価格を実装する
- [x] Black-Scholes のプット価格を実装する
- [x] put-call parity の説明とテストを追加する
- [x] Monte Carlo によるヨーロピアンオプション価格評価を実装する
- [x] payoff 関数を実装する
- [x] Greeks の基本計算を追加する
- [x] `examples/black_scholes_option.py` を追加する
- [x] `notebooks/02_monte_carlo_option_pricing.ipynb` を追加する

### Phase 3: リスク管理

- [x] リターン計算を実装する
- [x] volatility 計算を実装する
- [x] VaR を実装する
- [x] CVaR を実装する
- [x] ヒストリカル法とシミュレーション法の違いを説明する
- [x] 損益分布の可視化を実装する
- [x] `examples/portfolio_risk.py` を追加する
- [x] `notebooks/04_var_and_cvar.ipynb` を追加する

### Phase 4: ポートフォリオ分析

- [x] ポートフォリオ期待リターンを実装する
- [x] ポートフォリオ分散・標準偏差を実装する
- [x] 共分散行列を扱う関数を実装する
- [x] ランダムポートフォリオ生成を実装する
- [x] 効率的フロンティアの可視化を実装する
- [x] リバランスの簡易シミュレーションを実装する
- [x] `notebooks/03_portfolio_risk.ipynb` を追加する

### Phase 5: 債券・金利の基礎

- [x] 現在価値計算を実装する
- [x] 割引係数を実装する
- [x] 固定利付債の価格計算を実装する
- [x] デュレーションを実装する
- [x] コンベクシティを実装する
- [x] 金利変化と債券価格の関係を可視化する

### Phase 6: 教材とLLM補助機能

- [x] 各関数に初学者向け docstring を追加する
- [x] Notebook に数式と直感的説明を追加する
- [x] 演習問題を追加する
- [x] OpenAI API を使った説明生成の実験機能を追加する
- [x] シミュレーション結果の要約機能を追加する
- [x] API キーなしでも全コア機能が動くことを確認する

## API 設計メモ

初学者向けに、次のような呼び出しやすい API を優先します。

```python
import finsimlab as fsl

paths = fsl.simulate_gbm(
    s0=100,
    mu=0.05,
    sigma=0.2,
    years=1,
    steps=252,
    n_paths=1000,
    seed=42,
)
```

内部モジュールは分けつつ、よく使う関数はトップレベルからも呼べるようにします。

```python
from finsimlab.options import black_scholes_call
from finsimlab.risk import value_at_risk, conditional_value_at_risk
from finsimlab.portfolio import portfolio_return, portfolio_volatility
```

## 品質方針

- 数式ベースの関数には、既知の値を使った単体テストを追加する。
- 乱数を使う関数は seed を固定したテストを用意する。
- 戻り値の shape をテストする。
- エラー条件を明示する。
- 初学者が理解しにくい例外メッセージは避ける。
- パフォーマンス最適化より、まず正確さと読みやすさを優先する。

## ドキュメント方針

- README は外向けの概要と最短サンプルに集中する。
- このロードマップは実装作業の進行管理に使う。
- 各 Notebook は 1 テーマに絞る。
- 数式は必要最小限にし、直感的な説明とコード例を添える。
- 投資判断に使えるような表現は避ける。

## OpenAI API credits の利用案

申請する場合、API credits は次の用途に使う計画として説明できます。

- 初学者向けの概念説明生成
- Notebook の演習問題と解答例の生成
- シミュレーション結果の自然言語要約
- 入力パラメータ変更時の結果解釈
- 金融工学用語の対話型チューター
- ドキュメント改善のためのレビュー補助

ただし、これらは任意機能として扱い、ライブラリ本体は OpenAI API なしで利用できるようにします。

## 直近の作業順

1. 公開前チェックリストを作成する。
2. `docs/GLOSSARY.md` を作成する。
3. PyPI公開前のパッケージmetadataを確認する。
4. READMEのGitHub URLを実リポジトリに合わせる。
5. Notebookの実行済み出力を含めるか方針を決める。
6. Streamlitデモを追加するか検討する。
7. OSS申請用の短いプロジェクト説明文を作成する。
