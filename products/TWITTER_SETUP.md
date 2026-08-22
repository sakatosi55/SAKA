# Twitter自動投稿セットアップガイド

楽天商品投稿をTwitterに自動投稿するための手順書です。

## 📋 事前準備

Twitter APIを使用するには、以下が必要です：

- Twitterアカウント（X for Business推奨）
- Twitter Developer登録済み
- アプリケーション作成済み

## 🔑 認証情報の取得

### ステップ1: Twitter Developer Portalにアクセス

https://developer.twitter.com/en/portal/dashboard にアクセスしてログイン

### ステップ2: アプリケーション選択または作成

- 既存アプリケーションを選択するか、新規作成
- アプリケーション名は任意（例：`rakuten-auto-poster`）

### ステップ3: APIキーと認証トークンを取得

以下の情報をコピーします：

#### **Keys and Tokens** タブから：

1. **API Key** (API_KEY)
   - 別名: Consumer Key
   - 形式: `abcdef1234...`

2. **API Secret** (API_SECRET)
   - 別名: Consumer Secret
   - 形式: `abcdef1234...`
   - **安全に保管してください（再表示できません）**

3. **Access Token** (ACCESS_TOKEN)
   - 形式: `1234567890-abcdef...`
   - 「Regenerate」で再生成可能

4. **Access Token Secret** (ACCESS_TOKEN_SECRET)
   - 形式: `abcdef1234...`
   - **安全に保管してください（再表示できません）**

5. **Bearer Token** (BEARER_TOKEN)
   - 形式: `AAAAAabc...`
   - 長い英数字の文字列

### ステップ4: パーミッション確認

アプリケーション設定で以下のパーミッションが有効か確認：

- **Read and Write** または **Read, Write, and Direct Messages**
- 「Save」をクリック

> **重要**: デフォルトは「Read Only」のため、必ず変更してください

## 🔧 環境変数設定

### 1. `.env` ファイルを開く

```bash
nano products/.env
```

### 2. Twitter認証情報を追加

以下を追加または更新：

```env
TWITTER_API_KEY=abcdef1234...
TWITTER_API_SECRET=abcdef1234...
TWITTER_ACCESS_TOKEN=1234567890-abcdef...
TWITTER_ACCESS_TOKEN_SECRET=abcdef1234...
TWITTER_BEARER_TOKEN=AAAAAabc...
ENABLE_TWITTER_POSTING=true
```

### 3. ファイル保存

`nano` の場合：
- `Ctrl + X`
- `Y` キー
- `Enter`

## ✅ 動作確認

### 単発テスト実行

```bash
python products/scripts/fetch_and_post.py
```

**期待される出力:**

```
==================================================
🚀 楽天商品投稿自動生成を開始します
==================================================

🐦 Twitter投稿を有効化しています...
✅ Twitterクライアントを初期化しました

🔄 楽天APIから商品を取得中...
✅ 5 件の商品を取得しました

📝 投稿 1/5 を生成中...
✅ 投稿を保存しました: products/posts/20260822_120000_01.md
✅ Twitterに投稿しました

--- 投稿内容 ---
🔥 今だけ絶対買い！
...
--- 終了 ---
```

### Twitter確認

自分のTwitterアカウントで投稿が表示されたら成功です！

## 🔄 スケジューラー実行

毎日自動投稿するには：

### Linux/Mac

```bash
python products/scripts/scheduler.py 09:00
```

バックグラウンド実行：

```bash
nohup python products/scripts/scheduler.py 09:00 > twitter_posts.log 2>&1 &
```

### Windows

`products/run.bat` を実行するか、PowerShellで：

```powershell
python products/scripts/scheduler.py 09:00
```

## 🚨 トラブルシューティング

### 「Twitter認証エラー」

**原因**: API認証情報が正しくない

**対策**:
1. `.env` ファイルの認証情報を再確認
2. Twitter Developer Portalで最新の認証情報をコピー
3. アプリケーションのパーミッションが「Read and Write」か確認
4. 認証情報に空白や改行が含まれていないか確認

### 「tweepyがインストールされていません」

**原因**: `tweepy` パッケージがインストールされていない

**対策**:
```bash
pip install tweepy
```

### 「Twitter投稿エラー」

**原因**: APIレート制限、アカウントロック、ネットワークエラー

**対策**:
- ネットワーク接続を確認
- Twitterアカウントがロックされていないか確認
- APIレート制限（15分間に300投稿）に達していないか確認
- 投稿テキストが140文字以下か確認（Twitterの仕様）

### 「投稿は保存されるが、Twitterに投稿されない」

**原因**: `ENABLE_TWITTER_POSTING=true` が設定されていない

**対策**:
```env
ENABLE_TWITTER_POSTING=true
```

## 🔐 セキュリティのベストプラクティス

1. **認証情報は絶対に公開しない**
   - `.env` をGitにコミットしない
   - `git add` の前に確認

2. **定期的にトークンをリセット**
   - Twitter Developer Portalで「Regenerate」
   - 危険を感じたら即座にリセット

3. **不要なパーミッションは付与しない**
   - 「Read and Write」のみで十分
   - DM機能が必要でなければ外す

4. **アプリケーション連携を定期監査**
   - Twitter設定の「Apps and sessions」で接続済みアプリを確認
   - 不要なアプリは削除

## 📞 サポート

問題が解決しない場合：

- Twitter Developer ドキュメント: https://developer.twitter.com/en/docs
- tweepyドキュメント: https://docs.tweepy.org/
- このプロジェクトのREADME: `products/README.md`

---

**注意**: Twitter APIの仕様は変更される可能性があります。最新情報は公式ドキュメントを参照してください。
