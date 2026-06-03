# FinSimLab

[![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://github.com/your-name/finsimlab)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FinSimLab** は、Python で金融工学とリスク管理の基礎を学ぶための**教育用シミュレーションライブラリ**です。

数式だけで理解するのが難しい概念を、短いコード、可視化、Jupyter Notebook、シミュレーションを通じて直感的に学べることを目指します。

> [!IMPORTANT]
> **免責事項**: FinSimLab は教育・研究目的のソフトウェアです。投資助言、金融商品の推奨、将来収益の保証を目的としたものではありません。実際の投資判断に利用しないでください。

## 🚀 クイックスタート

わずか数行で幾何ブラウン運動（GBM）による株価シミュレーションを実行できます。

```python
import finsimlab as fsl

# 1. 幾何ブラウン運動のパスを生成
paths = fsl.simulate_gbm(s0=100, mu=0.05, sigma=0.2, n_paths=10)

# 2. 結果を可視化
fsl.plot_paths(paths, title="株価シミュレーション (GBM)")
```

## 📖 学習リソース

FinSimLab は、手を動かしながら学べる環境を提供しています。

- **[Jupyter Notebooks](notebooks/)**: ステップバイステップで学べるメイン教材です。
  - [学習ガイド (LEARNING_PATH.md)](docs/LEARNING_PATH.md) に沿って進めるのがおすすめです。
- **[Examples](examples/)**: 特定の機能をすぐに試せるスクリプト集です。
- **[機能一覧](docs/FEATURES.md)**: 現在実装されている機能とロードマップの詳細です。

## 🛠 インストール

現在開発中のため、ローカル開発版としてインストールしてください。

### コア機能（推奨）
シミュレーションやリスク計算など、すべての主要機能が含まれます。
```bash
git clone https://github.com/your-name/finsimlab.git
cd finsimlab
pip install -e ".[dev,notebook]"
```

### AI 説明機能（任意）
OpenAI API を使用してシミュレーション結果の解説を生成したい場合のみ必要です。
```bash
pip install -e ".[education]"
```

## ✨ 主な機能

FinSimLab は、APIキーなしで動く**コア機能**を重視しています。

### コア機能 (APIキー不要)
- **確率過程シミュレーション**: ランダムウォーク、幾何ブラウン運動、平均回帰
- **デリバティブ**: Black-Scholes モデル、モンテカルロ価格評価、Greeks
- **リスク管理**: VaR (Value at Risk)、CVaR、損失分布の可視化
- **ポートフォリオ**: 平均分散分析、ランダムポートフォリオ、効率的フロンティア近似
- **債券**: 固定利付債価格、デュレーション、コンベクシティ

### AI サポート機能 (任意・OpenAI API)
- シミュレーション結果や金融用語の自動解説生成
- ※ 詳細は [docs/OPENAI_EXPLANATIONS.md](docs/OPENAI_EXPLANATIONS.md) (準備中) を参照してください。

## 🎯 想定ユーザー
- Python を使って金融工学を学びたい初学者
- 大学・勉強会・個人学習で使える教材を探している人
- 数式と実装の対応を確認したい人

## 📂 リポジトリ構成
- `finsimlab/`: ライブラリ本体（シミュレーション、オプション、リスク、債券など）
- `notebooks/`: 学習用 Jupyter Notebooks
- `examples/`: 短い実行例スクリプト
- `docs/`: 詳細ドキュメント、ロードマップ
- `tests/`: 単体テスト

## 🗺 開発ロードマップ
今後の予定については [docs/ROADMAP.md](docs/ROADMAP.md) を参照してください。

## 📄 ライセンス
[MIT License](LICENSE)
