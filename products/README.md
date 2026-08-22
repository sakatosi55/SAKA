# 楽天API商品投稿自動生成

楽天APIから人気商品を毎日自動取得し、アフィリエイト付きの投稿を生成するシステムです。

## 📋 セットアップ手順

### 1. 楽天APIの登録

楽天ウェブサービスにアクセスして、APIキーを取得してください。

- **楽天ウェブサービス**: https://webservice.rakuten.co.jp/
- アプリケーションID（Application ID）を控えてください

### 2. 楽天アフィリエイトの登録

楽天アフィリエイトに登録し、アフィリエイトIDを取得してください。

- **楽天アフィリエイト**: https://affiliate.rakuten.co.jp/

### 3. 環境変数設定

`.env.example` をコピーして `.env` を作成し、APIキーを設定します：

```bash
cp products/.env.example products/.env
```

`.env` ファイルを編集：

```env
RAKUTEN_API_KEY=your_rakuten_application_id_here
RAKUTEN_AFFILIATE_ID=your_rakuten_affiliate_id_here
```

### 4. Twitter投稿設定（オプション）

Twitterに自動投稿したい場合は、以下の手順を実施：

#### 4-1. Twitter Developer登録

1. https://developer.twitter.com/en/portal/dashboard にアクセス
2. アプリケーションを作成
3. 認証情報を取得：
   - API Key (API_KEY)
   - API Secret (API_SECRET)
   - Access Token
   - Access Token Secret
   - Bearer Token

#### 4-2. 環境変数に追加

`.env` ファイルに以下を追加：

```env
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
ENABLE_TWITTER_POSTING=true
```

### 5. 依存パッケージをインストール

```bash
pip install -r products/requirements.txt
```

> **注**: Twitter投稿を使用しない場合でも、`tweepy` がインストールされます。使用しない場合は、後述の「トラブルシューティング」を参照してください。

## 🚀 実行方法

### 単発実行（テスト用）

```bash
python products/scripts/fetch_and_post.py
```

### 毎日定時実行（スケジューラー）

デフォルト（毎日09:00実行）：
```bash
python products/scripts/scheduler.py
```

カスタム時刻（例：毎日15:30実行）：
```bash
python products/scripts/scheduler.py 15:30
```

### バックグラウンド実行（Linux/Mac）

```bash
nohup python products/scripts/scheduler.py &
```

### systemd サービス登録（Linux）

`/etc/systemd/system/rakuten-posts.service`:

```ini
[Unit]
Description=Rakuten Product Auto Poster
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/SAKA
ExecStart=/usr/bin/python3 /path/to/SAKA/products/scripts/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

登録：
```bash
sudo systemctl enable rakuten-posts
sudo systemctl start rakuten-posts
sudo systemctl status rakuten-posts
```

## 📁 ディレクトリ構造

```
products/
├── config.py                    # API設定
├── requirements.txt             # 依存パッケージ
├── .env                        # 環境変数（.gitignore に追加）
├── .env.example                # テンプレート
├── README.md                   # このファイル
├── posts/                      # 生成された投稿
│   ├── 20240822_090000_01.md
│   ├── 20240822_090000_02.md
│   └── ...
└── scripts/
    ├── __init__.py
    ├── fetch_and_post.py       # メイン処理
    └── scheduler.py            # スケジューラー
```

## 🔧 カスタマイズ

### 取得商品数を変更

`products/config.py`:
```python
PRODUCTS_PER_DAY = 10  # デフォルト: 5
```

### 投稿テンプレートをカスタマイズ

`products/scripts/fetch_and_post.py` の `generate_post()` 関数を編集してください。

### 検索キーワード追加

楽天APIに検索キーワードを指定する場合、`fetch_popular_products()` の `params` に `keyword` を追加：

```python
params = {
    "keyword": "ビジネス書",
    # ... 他の設定
}
```

## 📊 出力される投稿

投稿は以下の5つのテンプレートからランダムに選択されます：

1. **緊急性・限定感型** — 「今だけ絶対買い！」
2. **数字・メリット型** — 「売上NO.1商品発見」
3. **質問・共感型** — 「これ知ってた？」
4. **ストーリー型** — 「みんなが選んでる理由」
5. **シンプル・直球型** — 「今週の推し商品」

すべての投稿にはアフィリエイトリンクが付与されます。

### 投稿先

- **ファイル**: `products/posts/YYYYMMDD_HHMMSS_XX.md` に保存
- **Twitter**: `ENABLE_TWITTER_POSTING=true` の場合、自動投稿されます

## ⚠️ トラブルシューティング

### APIキーエラー

```
❌ エラー: RAKUTEN_API_KEY が設定されていません
```

- `.env` ファイルが存在し、正しく設定されていることを確認
- `load_dotenv()` がコール前に実行されていることを確認

### API呼び出しエラー

```
❌ API呼び出しエラー
```

- APIキーが有効であることを確認
- 楽天APIの使用制限（レート制限）を確認
- ネットワーク接続を確認

### スケジューラーが起動しない

- `schedule` パッケージがインストールされていることを確認
- Python バージョンが 3.6 以上であることを確認

### Twitter投稿エラー

#### 認証エラー
```
❌ Twitter認証エラー: ...
```

- Twitter API認証情報が正しいことを確認
- `.env` ファイルに全ての認証情報が設定されていることを確認
- Twitter Developerポータルでアプリケーションのパーミッションが「Read and Write」に設定されていることを確認

#### tweepyがインストールされていない
```
⚠️  tweepyがインストールされていません
```

```bash
pip install tweepy
```

#### Twitter投稿が失敗する
- APIレート制限を確認してください（15分あたり300投稿など）
- ネットワーク接続を確認してください
- Twitterアカウントのセキュリティ設定を確認してください

## 📝 ログ確認

スケジューラー実行ログ：

```bash
journalctl -u rakuten-posts -f  # systemd
tail -f nohup.out  # nohup の場合
```

## 🔐 セキュリティ

- `.env` ファイルは **絶対に Git にコミットしないこと**
- `.gitignore` に `.env` が含まれていることを確認
- APIキーは定期的にローテーションしてください

## 📖 参考リンク

- [楽天ウェブサービス API ドキュメント](https://webservice.rakuten.co.jp/documentation)
- [楽天商品API](https://webservice.rakuten.co.jp/api/ichibaitemsearch/)
- [楽天アフィリエイト](https://affiliate.rakuten.co.jp/)

---

**作成日**: 2026-08-22
