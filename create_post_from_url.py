"""
楽天商品URLから自動で投稿を生成
使い方: python create_post_from_url.py <楽天商品URL>
"""
import sys
import re
import json
import random
from datetime import datetime
from pathlib import Path

def scrape_rakuten_product(url):
    """楽天商品ページから情報を抽出（Windows用）"""
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        html = response.text

        # 商品名を抽出
        title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        title = title_match.group(1).strip() if title_match else "商品"

        # 価格を抽出
        price_patterns = [
            r'<span[^>]*class="rakuten-pc-price-variable"[^>]*>¥\s*([\d,]+)',
            r'"priceData":\s*{\s*"price":\s*"?(\d+)',
        ]
        price = "9999"
        for pattern in price_patterns:
            match = re.search(pattern, html)
            if match:
                price = match.group(1).replace(',', '')
                break

        # 評価を抽出
        rating_patterns = [
            r'"ratingAverage":\s*([0-9.]+)',
        ]
        rating = "4.5"
        for pattern in rating_patterns:
            match = re.search(pattern, html)
            if match:
                rating = match.group(1)
                break

        # レビュー数を抽出
        review_patterns = [
            r'"reviewCount":\s*(\d+)',
        ]
        review_count = "100"
        for pattern in review_patterns:
            match = re.search(pattern, html)
            if match:
                review_count = match.group(1).replace(',', '')
                break

        # 説明を抽出
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', html)
        description = desc_match.group(1)[:100] if desc_match else title[:100]

        # 画像URLを抽出
        image_patterns = [
            r'"imageUrl":\s*"([^"]+\.jpg[^"]*)',
            r'<img[^>]*class="slider-image"[^>]*src="([^"]+)"',
        ]
        image_url = ""
        for pattern in image_patterns:
            match = re.search(pattern, html)
            if match:
                image_url = match.group(1)
                if not image_url.startswith('http'):
                    image_url = 'https:' + image_url if image_url.startswith('//') else 'https://' + image_url
                break

        if not image_url:
            image_url = f"https://thumbnail.image.rakuten.co.jp/@0_mall/example/product.jpg"

        return {
            'itemName': title,
            'itemPrice': int(price),
            'reviewAverage': float(rating),
            'reviewCount': int(review_count),
            'itemCaption': description,
            'itemImage': image_url,
            'itemUrl': url
        }
    except Exception as e:
        print(f"⚠️ 情報取得エラー: {e}")
        print("デフォルト値を使用します\n")
        return {
            'itemName': "新商品",
            'itemPrice': 2980,
            'reviewAverage': 4.5,
            'reviewCount': 100,
            'itemCaption': "人気商品。安全で高品質。",
            'itemImage': "https://thumbnail.image.rakuten.co.jp/@0_mall/example/product.jpg",
            'itemUrl': url
        }

def generate_affiliate_link(item_url):
    separator = "&" if "?" in item_url else "?"
    return f"{item_url}{separator}aid=56c29d66.fa76986e.56c29d67.5df37f66"

def generate_post(item):
    item_data = item.get("Item", {})
    title = item_data.get("itemName", "商品")
    price = item_data.get("itemPrice", "価格未定")
    item_url = item_data.get("itemUrl", "")
    image_url = item_data.get("itemImage", "")
    description = item_data.get("itemCaption", "")[:100]
    review_avg = item_data.get("reviewAverage", 0)
    review_count = item_data.get("reviewCount", 0)
    affiliate_url = generate_affiliate_link(item_url)

    image_text = f"![商品画像]({image_url})\n\n" if image_url else ""

    templates = [
        f"🔥 今だけ絶対買い！\n\n{title}\n\n{image_text}💰 ¥{price:,}\n⭐ {review_avg}/5.0 ({review_count:,}件の評価)\n\n\"{description}...\"\n\n🛒 在庫限定で数量制限あり\n👉 {affiliate_url}\n\n#楽天 #掘り出し物 #今すぐチェック",
        f"💎 売上NO.1商品発見\n\n『{title}』\n\n{image_text}✅ {review_count:,}人が購入\n✅ 評価 {review_avg}点\n✅ 価格 ¥{price:,}\n\n{description}\n\n詳しく見る↓\n{affiliate_url}\n\n#楽天 #売れ筋 #おすすめ商品",
        f"これ知ってた？🤔\n\n{title}\n\n{image_text}💰 ¥{price:,}\n\n⭐評価{review_avg}点\n🎯{review_count:,}人が選んでる\n\n{description}\n\n気になったらチェック👇\n{affiliate_url}\n\n#楽天 #商品紹介 #買う価値あり",
        f"👍 みんなが選んでる理由\n\n{title}\n\n{image_text}💯 {review_count:,}件のレビュー\n⭐ {review_avg}/5 の高評価\n💵 ¥{price:,}だからお手頃\n\n{description}\n\nくわしくはこちら👇\n{affiliate_url}\n\n#楽天 #イチオシ #この商品は本当にいい",
        f"🎁 今週の推し商品\n\n📌 {title}\n\n{image_text}💰 ¥{price:,}\n⭐ {review_avg}点（{review_count:,}評価）\n\n{description}\n\n👉 詳細ページはこちら\n{affiliate_url}\n\n#楽天 #新商品 #チェック必須"
    ]
    return random.choice(templates)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 使い方: python create_post_from_url.py <楽天商品URL>")
        print("\n例: python create_post_from_url.py https://item.rakuten.co.jp/s-space2021/jha411/")
        sys.exit(1)

    url = sys.argv[1]

    print("🔍 楽天ページから情報を取得中...\n")
    product = scrape_rakuten_product(url)

    print("✅ 投稿を生成中...\n")
    post = generate_post({"Item": product})

    # Desktop/投稿 フォルダに保存
    output_dir = Path.home() / "Desktop" / "投稿"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"{timestamp}_post.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post)

    print("="*60)
    print("✨ 投稿が作成されました！")
    print("="*60)
    print(f"\n📁 保存先: {filepath}")
    print("\n--- 投稿内容 ---")
    print(post)
    print("--- 終了 ---\n")
    print("👉 このファイルをコピーして、SNSに貼り付けてください！")
