# FinSimLab

FinSimLab は、Python で金融工学とリスク管理の基礎を学ぶための教育用シミュレーションライブラリです。

数式だけで理解するのが難しい概念を、短いコード、可視化、Notebook、シミュレーションを通じて直感的に学べることを目指します。

> 注意: FinSimLab は教育・研究目的のソフトウェアです。投資助言、金融商品の推奨、将来収益の保証を目的としたものではありません。

## 目的

FinSimLab は、金融工学を初めて学ぶ人が次のようなテーマを手元で試せるようにすることを目的とします。

- 株価過程のシミュレーション
- モンテカルロ法による価格評価
- オプション価格と Greeks の基礎
- ポートフォリオのリスク・リターン分析
- VaR / CVaR などのリスク指標
- 債券価格、割引現在価値、デュレーションの基礎
- Notebook による段階的な学習コンテンツ

## 想定ユーザー

- Python を使って金融工学を学びたい初学者
- 大学・勉強会・個人学習で使える教材を探している人
- 数式と実装の対応を確認したい人
- シンプルな金融シミュレーションをすぐ試したい人

## プロジェクト方針

- 初心者が読める API とドキュメントを優先します。
- 最初は合成データとシミュレーションを中心にします。
- 実データ連携は後回しにし、教育用途として安全な範囲から始めます。
- 金融理論の厳密さとコードの読みやすさのバランスを取ります。
- LLM / OpenAI API を使う機能は任意機能として扱い、コア機能は API キーなしで動作させます。

## 予定している主な機能

### シミュレーション

- ランダムウォーク
- 幾何ブラウン運動
- 平均回帰過程
- ポートフォリオ損益シミュレーション

### デリバティブ

- Black-Scholes モデル
- ヨーロピアンコール・プットの価格評価
- Monte Carlo option pricing
- Delta / Gamma / Vega / Theta / Rho の基礎計算

### リスク管理

- 分散・標準偏差・相関
- Value at Risk
- Conditional Value at Risk
- シナリオ分析

### ポートフォリオ

- リスク・リターン計算
- 共分散行列
- 効率的フロンティア
- リバランスの簡易シミュレーション

### 教材

- チュートリアル Notebook
- 数式とコードの対応説明
- 練習問題
- 可視化サンプル

## インストール

初期開発中のため、まだ PyPI には公開していません。

将来的には次のような形で利用できるようにする予定です。

```bash
pip install finsimlab
```

現時点では、ローカル開発版としてインストールします。

```bash
git clone https://github.com/your-name/finsimlab.git
cd finsimlab
python -m pip install -e ".[dev,notebook]"
```

## 使用例

幾何ブラウン運動のシミュレーション例です。

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

fsl.plot_paths(paths, title="GBM stock price simulation")
```

ランダムウォークと平均回帰過程も同じ戻り値形式で利用できます。

```python
import finsimlab as fsl

walk = fsl.simulate_random_walk(
    initial_value=0,
    drift=0.01,
    volatility=1.0,
    steps=100,
    n_paths=20,
    seed=7,
)

rates = fsl.simulate_mean_reversion(
    initial_value=3.0,
    long_term_mean=1.0,
    speed=1.5,
    volatility=0.3,
    years=2,
    steps=252,
    n_paths=20,
    seed=7,
)
```

各シミュレーション関数は、`(steps + 1, n_paths)` の `numpy.ndarray` を返します。最初の行には初期値が入ります。

Black-Scholesモデルでヨーロピアンオプションを価格評価できます。

```python
import finsimlab as fsl

call = fsl.black_scholes_call(
    spot=100,
    strike=100,
    time_to_maturity=1.0,
    risk_free_rate=0.05,
    volatility=0.2,
)

mc_call = fsl.monte_carlo_option_price(
    spot=100,
    strike=100,
    time_to_maturity=1.0,
    risk_free_rate=0.05,
    volatility=0.2,
    option_type="call",
    n_paths=50_000,
    seed=42,
)
```

VaR / CVaR は「損失を正の値」として扱います。

```python
import finsimlab as fsl

paths = fsl.simulate_gbm(
    s0=100,
    mu=0.05,
    sigma=0.2,
    years=1,
    steps=252,
    n_paths=5000,
    seed=42,
)

terminal_returns = paths[-1] / paths[0] - 1.0
losses = fsl.losses_from_returns(terminal_returns, portfolio_value=10_000)

var_95 = fsl.value_at_risk(losses, confidence_level=0.95)
cvar_95 = fsl.conditional_value_at_risk(losses, confidence_level=0.95)
```

ランダムポートフォリオを使って、平均分散分析の入口を試せます。ここでの効率的フロンティアは、最適化ではなくランダムに生成したポートフォリオの近似可視化です。

```python
import finsimlab as fsl

expected_returns = [0.04, 0.07, 0.10]
covariance = [
    [0.0100, 0.0018, 0.0011],
    [0.0018, 0.0225, 0.0026],
    [0.0011, 0.0026, 0.0400],
]

portfolios = fsl.generate_random_portfolios(
    expected_returns,
    covariance,
    n_portfolios=5000,
    risk_free_rate=0.01,
    seed=42,
)
```

固定利付債の価格、デュレーション、コンベクシティも計算できます。

```python
import finsimlab as fsl

price = fsl.fixed_coupon_bond_price(
    face_value=1000,
    coupon_rate=0.05,
    yield_to_maturity=0.04,
    years_to_maturity=5,
    payments_per_year=2,
)

duration = fsl.modified_duration(
    face_value=1000,
    coupon_rate=0.05,
    yield_to_maturity=0.04,
    years_to_maturity=5,
    payments_per_year=2,
)
```

学習用のローカル要約と、任意のOpenAI API説明生成も利用できます。OpenAI APIは任意機能で、コア機能はAPIキーなしで動きます。

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

summary = fsl.summarize_paths(paths)
text = fsl.generate_explanation(
    "幾何ブラウン運動による価格パス",
    summary,
    fallback=True,
)
```

OpenAI APIを使う場合は、任意依存を入れ、`OPENAI_API_KEY` を設定してから利用します。

```bash
python -m pip install -e ".[education]"
```

## 現在実装済みの機能

- ランダムウォーク
- 幾何ブラウン運動
- 平均回帰過程
- 乱数 seed による再現可能なシミュレーション
- 複数パスの統一戻り値形式
- 価格パスの可視化ヘルパー
- Black-Scholes のコール・プット価格
- Monte Carlo によるヨーロピアンオプション価格評価
- コール・プットの payoff
- Delta / Gamma / Vega / Theta / Rho
- リターン計算
- volatility 計算
- VaR / CVaR
- 損失分布の可視化
- ポートフォリオ期待リターン・分散・volatility
- 共分散行列・相関行列
- ランダムポートフォリオ生成
- ランダムポートフォリオによる効率的フロンティア近似
- 簡易リバランス計算
- 割引係数・現在価値
- 固定利付債価格
- Macaulay duration / modified duration
- 債券 convexity
- 債券価格と利回りの可視化
- 学習用の数値要約
- OpenAI APIを使った任意の説明生成
- Notebookごとの演習問題
- 学習順ドキュメント
- GBM の example
- Black-Scholes / Monte Carlo option pricing の example
- portfolio risk の example
- portfolio analysis の example
- bond pricing の example
- ランダムウォーク / GBM / 平均回帰過程の Notebook
- Monte Carlo option pricing の Notebook
- portfolio risk の Notebook
- VaR / CVaR の Notebook
- bonds and duration の Notebook

## 学習パス

Notebookを使った学習順は [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) にまとめています。

## リポジトリ構成案

```text
finsimlab/
  simulations/      # 確率過程・価格過程
  options/          # オプション価格・Greeks
  risk/             # VaR / CVaR / リスク指標
  portfolio/        # ポートフォリオ分析
  bonds/            # 債券・金利の基礎
  plotting/         # 可視化ヘルパー
examples/           # 短い実行例
notebooks/          # 学習用 Notebook
docs/               # 設計メモ・ロードマップ
tests/              # テスト
```

## 開発ロードマップ

今後の実装順や方針は [docs/ROADMAP.md](docs/ROADMAP.md) にまとめています。

## ライセンス

MIT License です。詳細は [LICENSE](LICENSE) を参照してください。
