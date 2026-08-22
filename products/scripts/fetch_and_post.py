"""
楽天API から人気商品を取得し、投稿を自動生成
毎日実行される
"""
import requests
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    RAKUTEN_API_KEY,
    RAKUTEN_AFFILIATE_ID,
    RAKUTEN_PRODUCT_API_URL,
    PRODUCTS_PER_DAY,
    POSTS_OUTPUT_DIR,
    ENABLE_TWITTER_POSTING,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
)

try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False


def fetch_popular_products():
    """楽天APIから人気商品を取得"""
    if not RAKUTEN_API_KEY:
        print("❌ エラー: RAKUTEN_API_KEY が設定されていません")
        return []

    params = {
        "applicationId": RAKUTEN_API_KEY,
        "hits": PRODUCTS_PER_DAY,
        "sort": "-itemPrice",  # 売上順にソート
        "availability": 1,  # 在庫ありのみ
    }

    try:
        print("🔄 楽天APIから商品を取得中...")
        response = requests.get(RAKUTEN_PRODUCT_API_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        items = data.get("Items", [])

        print(f"✅ {len(items)} 件の商品を取得しました")
        return items

    except requests.exceptions.RequestException as e:
        print(f"❌ API呼び出しエラー: {e}")
        return []


def generate_affiliate_link(item_url: str) -> str:
    """アフィリエイトリンクを生成"""
    if not RAKUTEN_AFFILIATE_ID:
        return item_url

    separator = "&" if "?" in item_url else "?"
    return f"{item_url}{separator}aid={RAKUTEN_AFFILIATE_ID}"


def generate_post(item: dict) -> str:
    """商品から投稿テキストを生成（複数テンプレートからランダム選択）"""
    import random

    item_data = item.get("Item", {})

    title = item_data.get("itemName", "商品")
    price = item_data.get("itemPrice", "価格未定")
    image_url = item_data.get("itemUrl", "")
    description = item_data.get("itemCaption", "")[:100]  # 最初の100文字
    review_avg = item_data.get("reviewAverage", 0)
    review_count = item_data.get("reviewCount", 0)

    # アフィリエイトリンク
    affiliate_url = generate_affiliate_link(image_url)

    # 複数の人気テンプレート
    templates = [
        # テンプレート1: 緊急性・限定感型
        f"""🔥 今だけ絶対買い！

{title}

💰 ¥{price:,}
⭐ {review_avg}/5.0 ({review_count:,}件の評価)

"{description}..."

🛒 在庫限定で数量制限あり
👉 {affiliate_url}

#楽天 #掘り出し物 #今すぐチェック""",

        # テンプレート2: 数字・メリット型
        f"""💎 売上NO.1商品発見

『{title}』

✅ {review_count:,}人が購入
✅ 評価 {review_avg}点
✅ 価格 ¥{price:,}

{description}

詳しく見る↓
{affiliate_url}

#楽天 #売れ筋 #おすすめ商品""",

        # テンプレート3: 質問・共感型
        f"""これ知ってた？🤔

{title}
💰 ¥{price:,}

⭐評価{review_avg}点
🎯{review_count:,}人が選んでる

{description}

気になったらチェック👇
{affiliate_url}

#楽天 #商品紹介 #買う価値あり""",

        # テンプレート4: ストーリー型
        f"""👍 みんなが選んでる理由

{title}

💯 {review_count:,}件のレビュー
⭐ {review_avg}/5 の高評価
💵 ¥{price:,}だからお手頃

{description}

くわしくはこちら👇
{affiliate_url}

#楽天 #イチオシ #この商品は本当にいい""",

        # テンプレート5: シンプル・直球型
        f"""🎁 今週の推し商品

📌 {title}
💰 {price:,}円
⭐ {review_avg}点（{review_count:,}評価）

{description}

👉 詳細ページはこちら
{affiliate_url}

#楽天 #新商品 #チェック必須""",
    ]

    # ランダムにテンプレートを選択
    post = random.choice(templates)
    return post


def save_post(post: str, timestamp: str) -> Path:
    """投稿をファイルに保存"""
    output_dir = Path(POSTS_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{timestamp}_post.md"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post)

    return filepath


def init_twitter_client():
    """Twitter APIクライアントを初期化"""
    if not TWITTER_AVAILABLE:
        return None

    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("⚠️  Twitter認証情報が不完全です（ENABLE_TWITTER_POSTINGは有効ですが、認証情報が足りません）")
        return None

    try:
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        return api
    except Exception as e:
        print(f"❌ Twitter認証エラー: {e}")
        return None


def post_to_twitter(api, post: str) -> bool:
    """Twitterに投稿"""
    if not api:
        return False

    try:
        api.update_status(post)
        print("✅ Twitterに投稿しました")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ Twitter投稿エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False


def main():
    """メイン処理"""
    print("\n" + "="*50)
    print("🚀 楽天商品投稿自動生成を開始します")
    print("="*50 + "\n")

    # Twitter投稿の初期化
    twitter_api = None
    if ENABLE_TWITTER_POSTING and TWITTER_AVAILABLE:
        print("🐦 Twitter投稿を有効化しています...")
        twitter_api = init_twitter_client()
        if twitter_api:
            print("✅ Twitterクライアントを初期化しました\n")
        else:
            print("⚠️  Twitterクライアントの初期化に失敗しました（ファイル保存のみ行います）\n")
    elif ENABLE_TWITTER_POSTING and not TWITTER_AVAILABLE:
        print("⚠️  tweepyがインストールされていません")
        print("   Twitter投稿を有効化するには: pip install tweepy\n")

    # 商品を取得
    items = fetch_popular_products()

    if not items:
        print("⚠️  商品が取得できませんでした")
        return

    # 各商品について投稿を生成・保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, item in enumerate(items, 1):
        print(f"\n📝 投稿 {i}/{len(items)} を生成中...")

        try:
            post = generate_post(item)
            filepath = save_post(post, f"{timestamp}_{i:02d}")

            print(f"✅ 投稿を保存しました: {filepath}")

            # Twitter に投稿
            if twitter_api:
                post_to_twitter(twitter_api, post)

            print("\n--- 投稿内容 ---")
            print(post)
            print("--- 終了 ---\n")

        except Exception as e:
            print(f"❌ 投稿生成エラー: {e}")
            continue

    print("="*50)
    print("✨ 処理が完了しました")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
