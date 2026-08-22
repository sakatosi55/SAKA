"""
楽天API設定
"""
import os
from dotenv import load_dotenv

load_dotenv()

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
