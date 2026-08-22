import random
import json
from datetime import datetime
from pathlib import Path

# ダミー商品データ
dummy_products = [
    {"Item": {"itemName": "子供用 浮き輪 70cm カラフル フロート", "itemPrice": 1980, "itemUrl": "https://item.rakuten.co.jp/example/floating-ring/", "itemCaption": "安全で楽しい夏の水遊び。耐久性の高いPVC素材で、UV対応。", "reviewAverage": 4.7, "reviewCount": 256}},
    {"Item": {"itemName": "キッズ プール 200L 組み立て式 ビニールプール", "itemPrice": 3480, "itemUrl": "https://item.rakuten.co.jp/example/kids-pool/", "itemCaption": "庭で気軽に水遊び。組み立て簡単、片付けも楽々。", "reviewAverage": 4.5, "reviewCount": 189}},
    {"Item": {"itemName": "ビーチボール 50cm カラフル 海水浴", "itemPrice": 980, "itemUrl": "https://item.rakuten.co.jp/example/beach-ball/", "itemCaption": "夏のビーチに欠かせない。大人数で遊べます。", "reviewAverage": 4.6, "reviewCount": 342}},
    {"Item": {"itemName": "日焼け止めクリーム キッズ用 SPF50+ 200ml", "itemPrice": 1580, "itemUrl": "https://item.rakuten.co.jp/example/sunscreen/", "itemCaption": "子供の敏感肌を守る。ウォータープルーフで汗に強い。", "reviewAverage": 4.8, "reviewCount": 521}},
    {"Item": {"itemName": "キッズ シュノーケルセット マスク フィン 3点セット", "itemPrice": 2890, "itemUrl": "https://item.rakuten.co.jp/example/snorkel-set/", "itemCaption": "海での探検が楽しい。初心者向けの安全設計。", "reviewAverage": 4.4, "reviewCount": 178}}
]

def generate_affiliate_link(item_url):
    separator = "&" if "?" in item_url else "?"
    return f"{item_url}{separator}aid=56c29d66.fa76986e.56c29d67.5df37f66"

def generate_post(item):
    item_data = item.get("Item", {})
    title = item_data.get("itemName", "商品")
    price = item_data.get("itemPrice", "価格未定")
    image_url = item_data.get("itemUrl", "")
    description = item_data.get("itemCaption", "")[:100]
    review_avg = item_data.get("reviewAverage", 0)
    review_count = item_data.get("reviewCount", 0)
    affiliate_url = generate_affiliate_link(image_url)
    templates = [
        f"🔥 今だけ絶対買い！\n\n{title}\n\n💰 ¥{price:,}\n⭐ {review_avg}/5.0 ({review_count:,}件の評価)\n\n\"{description}...\"\n\n🛒 在庫限定で数量制限あり\n👉 {affiliate_url}\n\n#楽天 #掘り出し物 #今すぐチェック",
        f"💎 売上NO.1商品発見\n\n『{title}』\n\n✅ {review_count:,}人が購入\n✅ 評価 {review_avg}点\n✅ 価格 ¥{price:,}\n\n{description}\n\n詳しく見る↓\n{affiliate_url}\n\n#楽天 #売れ筋 #おすすめ商品",
        f"これ知ってた？🤔\n\n{title}\n💰 ¥{price:,}\n\n⭐評価{review_avg}点\n🎯{review_count:,}人が選んでる\n\n{description}\n\n気になったらチェック👇\n{affiliate_url}\n\n#楽天 #商品紹介 #買う価値あり",
        f"👍 みんなが選んでる理由\n\n{title}\n\n💯 {review_count:,}件のレビュー\n⭐ {review_avg}/5 の高評価\n💵 ¥{price:,}だからお手頃\n\n{description}\n\nくわしくはこちら👇\n{affiliate_url}\n\n#楽天 #イチオシ #この商品は本当にいい",
        f"🎁 今週の推し商品\n\n📌 {title}\n💰 {price:,}円\n⭐ {review_avg}点（{review_count:,}評価）\n\n{description}\n\n👉 詳細ページはこちら\n{affiliate_url}\n\n#楽天 #新商品 #チェック必須"
    ]
    return random.choice(templates)

output_dir = Path.home() / "Desktop" / "投稿"
output_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("\n" + "="*60)
print("🚀 楽天商品投稿自動生成を開始します")
print("="*60 + "\n")

for i, product in enumerate(dummy_products, 1):
    print(f"📝 投稿 {i}/{len(dummy_products)} を生成中...")
    post = generate_post(product)
    filename = f"{timestamp}_{i:02d}"
    filepath = output_dir / f"{filename}_post.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post)
    print(f"✅ 投稿を保存しました: {filepath}")
    print("\n--- 投稿内容 ---")
    print(post)
    print("--- 終了 ---\n")

print("="*60)
print("✨ 処理が完了しました")
print("="*60)
print(f"\n📁 投稿フォルダ: {output_dir}")
