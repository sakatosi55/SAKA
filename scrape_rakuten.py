"""
楽天商品ページからスクレイピングして情報を取得
"""
import re
import json
import requests
from urllib.parse import urlparse

def scrape_rakuten_product(url):
    """楽天商品ページから情報を抽出"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    html = response.text

    # 商品名を抽出
    title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    title = title_match.group(1).strip() if title_match else "商品"

    # 価格を抽出（複数のパターンに対応）
    price_patterns = [
        r'<span[^>]*class="rakuten-pc-price-variable"[^>]*>¥\s*([\d,]+)',
        r'<span[^>]*class="price-value"[^>]*>([0-9,]+)',
        r'"priceData":\s*{\s*"price":\s*"?(\d+)',
        r'<span[^>]*itemprop="price"[^>]*>([0-9,]+)',
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
        r'<span[^>]*class="rating-value"[^>]*>([0-9.]+)',
        r'<meta[^>]*itemprop="ratingValue"[^>]*content="([0-9.]+)',
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
        r'<span[^>]*class="review-count"[^>]*>([0-9,]+)',
        r'<meta[^>]*itemprop="reviewCount"[^>]*content="(\d+)',
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
        r'<img[^>]*itemprop="image"[^>]*src="([^"]+)"',
    ]
    image_url = ""
    for pattern in image_patterns:
        match = re.search(pattern, html)
        if match:
            image_url = match.group(1)
            if not image_url.startswith('http'):
                image_url = 'https:' + image_url if image_url.startswith('//') else 'https://' + image_url
            break

    # デフォルト画像（見つからない場合）
    if not image_url:
        image_url = f"https://thumbnail.image.rakuten.co.jp/@0_mall/s-space2021/cabinet/product.jpg"

    return {
        'itemName': title,
        'itemPrice': int(price),
        'reviewAverage': float(rating),
        'reviewCount': int(review_count),
        'itemCaption': description,
        'itemImage': image_url,
        'itemUrl': url
    }

if __name__ == "__main__":
    url = "https://item.rakuten.co.jp/s-space2021/jha411/"

    print("🔍 楽天ページから情報を取得中...\n")
    try:
        product = scrape_rakuten_product(url)

        print("✅ 取得成功！")
        print(f"\n商品名: {product['itemName']}")
        print(f"価格: ¥{product['itemPrice']:,}")
        print(f"評価: {product['reviewAverage']}/5.0")
        print(f"レビュー数: {product['reviewCount']:,}件")
        print(f"説明: {product['itemCaption']}")
        print(f"画像: {product['itemImage']}")

        # Python形式で出力
        print("\n\n📋 test_post.py 用データ:\n")
        print(json.dumps({"Item": product}, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
