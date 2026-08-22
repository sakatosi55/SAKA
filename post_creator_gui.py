"""
楽天投稿自動生成 GUI アプリケーション
Desktop/投稿 フォルダから実行
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import re
import random
from datetime import datetime
from pathlib import Path
import requests

class PostCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("楽天投稿自動生成")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # カラースキーム
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        # メインフレーム
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # タイトル
        title_label = ttk.Label(main_frame, text="楽天商品投稿自動生成", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # URL入力エリア
        url_label = ttk.Label(main_frame, text="楽天商品URL:")
        url_label.pack(anchor=tk.W)

        self.url_entry = ttk.Entry(main_frame, width=80)
        self.url_entry.pack(fill=tk.X, pady=(0, 20))
        self.url_entry.insert(0, "https://item.rakuten.co.jp/")

        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.create_button = ttk.Button(button_frame, text="📝 投稿を作成", command=self.on_create_click)
        self.create_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(button_frame, text="🗑️ クリア", command=self.on_clear_click)
        self.clear_button.pack(side=tk.LEFT)

        # 投稿プレビューエリア
        preview_label = ttk.Label(main_frame, text="📄 投稿プレビュー:")
        preview_label.pack(anchor=tk.W, pady=(10, 0))

        self.preview_text = scrolledtext.ScrolledText(main_frame, height=20, width=80)
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.preview_text.config(state=tk.DISABLED)

        # ステータスバー
        self.status_label = ttk.Label(main_frame, text="準備完了", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, pady=(10, 0))

        self.output_dir = Path.home() / "Desktop" / "投稿"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def set_status(self, message):
        self.status_label.config(text=message)
        self.root.update()

    def update_preview(self, text):
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, text)
        self.preview_text.config(state=tk.DISABLED)
        self.root.update()

    def scrape_rakuten_product(self, url):
        """楽天商品ページから情報を抽出"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            html = response.text

            # 商品名
            title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
            title = title_match.group(1).strip() if title_match else "商品"

            # 価格
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

            # 評価
            rating_match = re.search(r'"ratingAverage":\s*([0-9.]+)', html)
            rating = rating_match.group(1) if rating_match else "4.5"

            # レビュー数
            review_match = re.search(r'"reviewCount":\s*(\d+)', html)
            review_count = review_match.group(1) if review_match else "100"

            # 説明
            desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', html)
            description = desc_match.group(1)[:100] if desc_match else title[:100]

            # 画像
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
                image_url = "https://thumbnail.image.rakuten.co.jp/@0_mall/example/product.jpg"

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
            self.set_status(f"⚠️ 取得エラー: {e} デフォルト値を使用します")
            return {
                'itemName': "新商品",
                'itemPrice': 2980,
                'reviewAverage': 4.5,
                'reviewCount': 100,
                'itemCaption': "人気商品。安全で高品質。",
                'itemImage': "https://thumbnail.image.rakuten.co.jp/@0_mall/example/product.jpg",
                'itemUrl': url
            }

    def generate_affiliate_link(self, item_url):
        separator = "&" if "?" in item_url else "?"
        return f"{item_url}{separator}aid=56c29d66.fa76986e.56c29d67.5df37f66"

    def generate_post(self, item):
        item_data = item.get("Item", {})
        title = item_data.get("itemName", "商品")
        price = item_data.get("itemPrice", "価格未定")
        item_url = item_data.get("itemUrl", "")
        image_url = item_data.get("itemImage", "")
        description = item_data.get("itemCaption", "")[:100]
        review_avg = item_data.get("reviewAverage", 0)
        review_count = item_data.get("reviewCount", 0)
        affiliate_url = self.generate_affiliate_link(item_url)

        image_text = f"![商品画像]({image_url})\n\n" if image_url else ""

        templates = [
            f"🔥 今だけ絶対買い！\n\n{title}\n\n{image_text}💰 ¥{price:,}\n⭐ {review_avg}/5.0 ({review_count:,}件の評価)\n\n\"{description}...\"\n\n🛒 在庫限定で数量制限あり\n👉 {affiliate_url}\n\n#楽天 #掘り出し物 #今すぐチェック",
            f"💎 売上NO.1商品発見\n\n『{title}』\n\n{image_text}✅ {review_count:,}人が購入\n✅ 評価 {review_avg}点\n✅ 価格 ¥{price:,}\n\n{description}\n\n詳しく見る↓\n{affiliate_url}\n\n#楽天 #売れ筋 #おすすめ商品",
            f"これ知ってた？🤔\n\n{title}\n\n{image_text}💰 ¥{price:,}\n\n⭐評価{review_avg}点\n🎯{review_count:,}人が選んでる\n\n{description}\n\n気になったらチェック👇\n{affiliate_url}\n\n#楽天 #商品紹介 #買う価値あり",
            f"👍 みんなが選んでる理由\n\n{title}\n\n{image_text}💯 {review_count:,}件のレビュー\n⭐ {review_avg}/5 の高評価\n💵 ¥{price:,}だからお手頃\n\n{description}\n\nくわしくはこちら👇\n{affiliate_url}\n\n#楽天 #イチオシ #この商品は本当にいい",
            f"🎁 今週の推し商品\n\n📌 {title}\n\n{image_text}💰 ¥{price:,}\n⭐ {review_avg}点（{review_count:,}評価）\n\n{description}\n\n👉 詳細ページはこちら\n{affiliate_url}\n\n#楽天 #新商品 #チェック必須"
        ]
        return random.choice(templates)

    def on_create_click(self):
        url = self.url_entry.get().strip()

        if not url or url == "https://item.rakuten.co.jp/":
            messagebox.showwarning("警告", "URLを入力してください")
            return

        if "rakuten.co.jp" not in url:
            messagebox.showerror("エラー", "楽天のURLを入力してください")
            return

        self.create_button.config(state=tk.DISABLED)
        self.set_status("🔄 処理中...")

        # スレッドで実行（UIがフリーズしないように）
        thread = threading.Thread(target=self.create_post_thread, args=(url,))
        thread.daemon = True
        thread.start()

    def create_post_thread(self, url):
        try:
            self.set_status("🔍 商品情報を取得中...")
            product = self.scrape_rakuten_product(url)

            self.set_status("📝 投稿を生成中...")
            post = self.generate_post({"Item": product})

            # ファイルに保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.output_dir / f"{timestamp}_post.md"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(post)

            self.update_preview(post)
            self.set_status(f"✅ 完成！保存先: {filepath}")

            messagebox.showinfo("成功", f"投稿を作成しました！\n\n保存先: {filepath}\n\nコピーしてSNSに貼り付けてください")

        except Exception as e:
            self.set_status(f"❌ エラー: {e}")
            messagebox.showerror("エラー", f"投稿作成に失敗しました:\n{e}")

        finally:
            self.create_button.config(state=tk.NORMAL)

    def on_clear_click(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://item.rakuten.co.jp/")
        self.update_preview("")
        self.set_status("準備完了")

if __name__ == "__main__":
    root = tk.Tk()
    app = PostCreatorApp(root)
    root.mainloop()
