プロジェクト概要

このリポジトリは Flask を使った小規模なウェブアプリケーションです。主要なエントリポイントは [run.py](run.py) で、アプリ本体は `app/` ディレクトリに格納されています。

要件

- **Python**: 3.8+ を推奨
- **依存パッケージ**: `requirements.txt` を参照してください（例: Flask, Flask-SQLAlchemy）

セットアップ (Windows)

1. 仮想環境を作成して有効化

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

2. 依存関係をインストール

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

アプリの起動

- 開発サーバで実行するには:

```powershell
python run.py
```

ファイル構成（主要）

- **[run.py](run.py)**: アプリ起動スクリプト
- **[requirements.txt](requirements.txt)**: Python 依存パッケージ
- **app/**: アプリ本体
	- `app/__init__.py`: アプリファクトリと初期化処理
	- `app/routes.py`, `app/api/routes.py`, `app/logs/routes.py`: ルーティング
- **database/schema.sql**: データベーススキーマ

データベース

データベーススキーマは `database/schema.sql` にあります。ローカルで SQLite 等を使う場合は接続設定を `app/config.py` で確認してください。

注意事項

- `run.py` は開発向けに `debug=True` で起動します。本番環境では WSGI サーバ（Gunicorn 等）を利用し、デバッグを無効にしてください。
- 環境変数やシークレットは `app/config.py` と環境変数で管理してください。

