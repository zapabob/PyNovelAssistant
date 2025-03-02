PyNovelAssistant
EasyNovelAssistantをPyQt6を使って再構築したプロジェクトです。

機能
小説の執筆支援
AIを活用した文章生成
音声合成によるボイスオーバー生成
動画作成支援
インストール方法
# 依存パッケージのインストール
pip install -r requirements.txt
使用方法
# アプリケーションの起動
python run.py
ディレクトリ構造
PyNovelAssistant/
├── src/                  # ソースコード
│   ├── core/             # コアロジック
│   ├── gui/              # GUI関連
│   ├── models/           # モデル関連
│   └── utils/            # ユーティリティ
├── resources/            # リソースファイル
├── sample/               # サンプルテキスト
├── run.py                # 実行スクリプト
└── requirements.txt      # 依存パッケージ
