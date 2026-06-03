# FinSimLab

FinSimLab は、Python で金融工学とリスク管理の基礎を学ぶための教育用シミュレーションライブラリです。
数式だけで理解するのが難しい概念を、短いコード、可視化、Notebook、シミュレーションを通じて直感的に学べることを目指します。

> **⚠️ 注意: 重要なお知らせ**
> FinSimLab は教育・研究目的のソフトウェアです。**投資助言、売買の推奨、金融商品の推奨、または将来の収益を保証するものではありません。** 本ライブラリを使用したことによるいかなる損失についても、制作者および貢献者は責任を負いません。

---

## 🚀 クイックスタート

数行のコードで幾何ブラウン運動（GBM）による株価シミュレーションを実行し、可視化できます。

```python
import finsimlab as fsl

# 幾何ブラウン運動のシミュレーション（1000パス）
paths = fsl.simulate_gbm(
    s0=100, mu=0.05, sigma=0.2, years=1, steps=252, n_paths=1000, seed=42
)

# パスの可視化
fsl.plot_paths(paths, title="GBM Stock Price Simulation")
```

その他の例については [examples/](examples/) フォルダをご覧ください。

## 📦 インストール

現在開発中のため、ローカル開発版としてインストールしてください。

```bash
git clone https://github.com/your-name/finsimlab.git
cd finsimlab

# 開発用およびNotebook用依存関係を含めてインストール
python -m pip install -e ".[dev,notebook]"
```

## ✨ 主な機能

FinSimLab は「コア機能（APIキー不要）」と「教育用補助機能（任意）」の2つで構成されています。

### 1. コア機能（APIキー不要・オフライン動作）
以下の機能はすべて無料で、外部APIを介さずに動作します。

- **シミュレーション**: ランダムウォーク、幾何ブラウン運動、平均回帰過程（Vasicekモデル等）
- **デリバティブ**: Black-Scholes モデルによる価格評価、モンテカルロ・オプション価格評価、Greeks計算
- **リスク管理**: VaR (Value at Risk)、CVaR (Conditional Value at Risk)、損失分布の可視化
- **ポートフォリオ分析**: リスク・リターン計算、共分散行列、ランダムポートフォリオによる効率的フロンティア近似
- **債券・金利**: 固定利付債の価格評価、デュレーション、コンベクシティ

### 2. 教育用補助機能（OpenAI APIが必要）
OpenAI API 連携を使用すると、シミュレーション結果に対する自然言語での解説を生成できます。

```bash
# 任意: 教育用依存関係のインストール
python -m pip install -e ".[education]"
```

詳細は [docs/OPENAI_EXPLANATIONS.md](docs/OPENAI_EXPLANATIONS.md)（準備中）を参照してください。

## 📖 学習ガイド

初めての方は、Jupyter Notebook を使って段階的に学ぶことをお勧めします。

1. [01_random_walk_and_gbm.ipynb](notebooks/01_random_walk_and_gbm.ipynb): 確率過程の基礎
2. [02_monte_carlo_option_pricing.ipynb](notebooks/02_monte_carlo_option_pricing.ipynb): オプション評価
3. [03_portfolio_risk.ipynb](notebooks/03_portfolio_risk.ipynb): ポートフォリオのリスク
4. [04_var_and_cvar.ipynb](notebooks/04_var_and_cvar.ipynb): リスク指標の理解
5. [05_bonds_and_duration.ipynb](notebooks/05_bonds_and_duration.ipynb): 債券の基礎

学習の全体像については [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) をご覧ください。

## 📂 リポジトリ構成

- [finsimlab/](finsimlab/): ライブラリのソースコード
- [notebooks/](notebooks/): 学習用チュートリアル
- [examples/](examples/): 実行可能なサンプルスクリプト
- [docs/](docs/): 詳細ドキュメント・ロードマップ
- [tests/](tests/): 単体テスト

## 🛠 開発と貢献

開発ロードマップについては [docs/ROADMAP.md](docs/ROADMAP.md) を参照してください。
バグ報告や機能提案は GitHub Issues で受け付けています。

## 📄 ライセンス

[MIT License](LICENSE)
