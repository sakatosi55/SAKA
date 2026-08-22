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
)


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
    """商品から投稿テキストを生成"""
    item_data = item.get("Item", {})

    title = item_data.get("itemName", "商品")
    price = item_data.get("itemPrice", "価格未定")
    image_url = item_data.get("itemUrl", "")
    description = item_data.get("itemCaption", "")
    review_avg = item_data.get("reviewAverage", 0)
    review_count = item_data.get("reviewCount", 0)

    # アフィリエイトリンク
    affiliate_url = generate_affiliate_link(image_url)

    # 投稿テンプレート
    post = f"""
📦 【楽天の注目商品】

🏷️ {title}

💰 価格: ¥{price:,}
⭐ 評価: {review_avg}/5.0 ({review_count}件)

{description}

🔗 詳細はこちら: {affiliate_url}

#楽天 #商品紹介 #アフィリエイト
""".strip()

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


def main():
    """メイン処理"""
    print("\n" + "="*50)
    print("🚀 楽天商品投稿自動生成を開始します")
    print("="*50 + "\n")

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
