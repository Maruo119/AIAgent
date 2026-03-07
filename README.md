# AIAgent

AIAgent は、GitHub の issue を自動で解決する AI 搭載ツールです。issue の説明を分析し、コードを読み書きして修正し、テストが通るまで繰り返します。OpenAI の GPT モデルを統合し、GitHub 上でプルリクエストを作成します。

## 機能

- GitHub API を使用して issue を取得。
- 対象のコードファイルを読み書き。
- pytest を実行して修正を検証。
- 新しいブランチを作成し、コミットしてプッシュし、プルリクエストを提出。

## 前提条件

- Python 3.8 以上
- Git
- issue を持つ GitHub リポジトリ
- OpenAI API キー
- GitHub Personal Access Token

## インストール

1. リポジトリをクローン:
   ```sh
   git clone https://github.com/Maruo119/AIAgent.git
   cd AIAgent
   ```

2. 依存関係をインストール:
   ```sh
   pip install -r requirements.txt
   ```

3. `.env` に環境変数を設定:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_OWNER=your_github_owner
   GITHUB_REPO=your_github_repo
   GITHUB_ISSUE_NUMBER=issue_number
   GITHUB_TOKEN=your_github_token
   ```

## 使用方法

エージェントスクリプトを実行:
```sh
python agent.py
```

エージェントは以下の処理を行います:
- 指定された GitHub issue を取得。
- `target_code.py` のコードを分析。
- コードを修正し、テストが通るまで繰り返す。
- ブランチを作成、コミット、プッシュ、プルリクエストを作成。

## プロジェクト構造

- `agent.py`: AI エージェントのメインスクリプト。
- `target_code.py`: 修正対象のコード（例: `multiply` 関数）。
- `test_add.py`: コード変更を検証するテストファイル。
- `issue.txt`: ローカルの issue 説明（GitHub 取得失敗時のフォールバック）。
- `.env`: 環境変数。

## 貢献

1. リポジトリをフォーク。
2. 機能ブランチを作成。
3. 変更を加え、テストを実行。
4. プルリクエストを提出。

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。