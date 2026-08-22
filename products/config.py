"""
楽天API & Twitter API設定
"""
import os

# 楽天API認証情報
RAKUTEN_API_KEY = os.getenv("RAKUTEN_API_KEY", "")
RAKUTEN_AFFILIATE_ID = os.getenv("RAKUTEN_AFFILIATE_ID", "")

# API エンドポイント
RAKUTEN_PRODUCT_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

# 取得設定
PRODUCTS_PER_DAY = 5  # 毎日取得する商品数
POPULAR_THRESHOLD = 1000  # 人気度の閾値（レビュー数など）

# 投稿設定
POSTS_OUTPUT_DIR = "./products/posts"

# Twitter API認証情報
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
ENABLE_TWITTER_POSTING = os.getenv("ENABLE_TWITTER_POSTING", "false").lower() == "true"
