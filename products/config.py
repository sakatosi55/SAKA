"""
楽天API設定
"""
import os
from pathlib import Path

def load_env_file():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# 楽天API認証情報
RAKUTEN_API_KEY = os.getenv("RAKUTEN_API_KEY", "")
RAKUTEN_AFFILIATE_ID = os.getenv("RAKUTEN_AFFILIATE_ID", "")

# API エンドポイント
RAKUTEN_PRODUCT_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

# 取得設定
PRODUCTS_PER_DAY = 5  # 毎日取得する商品数
POPULAR_THRESHOLD = 1000  # 人気度の閾値（レビュー数など）

# 投稿設定
POSTS_OUTPUT_DIR = str(Path.home() / "Desktop" / "投稿")
