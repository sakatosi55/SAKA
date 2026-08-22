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

### 4. 依存パッケージをインストール

```bash
pip install -r products/requirements.txt
```

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

```
📦 【楽天の注目商品】

🏷️ 商品名

💰 価格: ¥12,345
⭐ 評価: 4.5/5.0 (123件)

商品説明...

🔗 詳細はこちら: https://item.rakuten.co.jp/...?aid=xxxx

#楽天 #商品紹介 #アフィリエイト
```

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
