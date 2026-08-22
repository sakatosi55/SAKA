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

        # ペースト機能を追加
        self.url_entry.bind('<Control-v>', self.on_paste)
        self.url_entry.bind('<Button-3>', self.on_right_click)

        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.create_button = ttk.Button(button_frame, text="📝 投稿を作成", command=self.on_create_click)
        self.create_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_button = ttk.Button(button_frame, text="📋 コピー", command=self.on_copy_click, state=tk.DISABLED)
        self.copy_button.pack(side=tk.LEFT, padx=(0, 10))

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

    def on_paste(self, event=None):
        """Ctrl+V ペースト"""
        try:
            text = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, text)
        except:
            pass
        return "break"

    def on_right_click(self, event):
        """右クリックメニュー"""
        try:
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="貼り付け", command=lambda: self.on_paste())
            menu.post(event.x_root, event.y_root)
        except:
            pass

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
        """Playwright でブラウザ自動化してページから情報を抽出"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.set_status("⚠️ Playwright がインストールされていません")
            return self.get_default_product(url)

        try:
            self.set_status("🌐 ブラウザでページを読み込み中...")

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=30000)

                # ページが完全に読み込まれるまで待機
                page.wait_for_selector("h1, [data-test='item-name']", timeout=10000)

                # JavaScript で情報を抽出
                product_data = page.evaluate("""() => {
                    // 商品名
                    let title = document.querySelector("h1")?.innerText ||
                                document.querySelector("[data-test='item-name']")?.innerText ||
                                "商品";

                    // 価格
                    let price = 0;
                    let priceText = document.querySelector(".rakuten-pc-price-variable")?.innerText ||
                                   document.querySelector("[data-test='price']")?.innerText ||
                                   "";
                    let match = priceText.match(/\\d+/g);
                    if (match) price = parseInt(match.join(""));

                    // 画像
                    let image = document.querySelector(".slider-image")?.src ||
                               document.querySelector("[data-test='item-image']")?.src ||
                               document.querySelector("img[alt*='商品画像']")?.src ||
                               "";

                    // 評価
                    let rating = 0;
                    let ratingText = document.querySelector(".rating-value")?.innerText ||
                                    document.querySelector("[data-test='rating']")?.innerText ||
                                    "0";
                    let ratingMatch = ratingText.match(/[0-9.]+/);
                    if (ratingMatch) rating = parseFloat(ratingMatch[0]);

                    // レビュー数
                    let reviewCount = 0;
                    let reviewText = document.querySelector(".review-count")?.innerText ||
                                    document.querySelector("[data-test='review-count']")?.innerText ||
                                    "0";
                    let reviewMatch = reviewText.match(/\\d+/);
                    if (reviewMatch) reviewCount = parseInt(reviewMatch[0]);

                    // 説明
                    let description = document.querySelector("meta[name='description']")?.content ||
                                     document.querySelector(".item-caption")?.innerText ||
                                     title;

                    return {
                        title: title.trim(),
                        price: price,
                        image: image,
                        rating: rating,
                        reviewCount: reviewCount,
                        description: description.substring(0, 100)
                    };
                }""")

                browser.close()

                return {
                    'itemName': product_data.get('title', '商品'),
                    'itemPrice': product_data.get('price', 0),
                    'reviewAverage': product_data.get('rating', 0),
                    'reviewCount': product_data.get('reviewCount', 0),
                    'itemCaption': product_data.get('description', '楽天商品'),
                    'itemImage': product_data.get('image', ''),
                    'itemUrl': url
                }

        except Exception as e:
            self.set_status(f"⚠️ 読み込みエラー: {e}")
            return self.get_default_product(url)

    def get_default_product(self, url):
        """デフォルト商品情報を返す"""
        return {
            'itemName': "楽天商品",
            'itemPrice': 0,
            'reviewAverage': 0,
            'reviewCount': 0,
            'itemCaption': "楽天の商品です。詳細はリンクをご確認ください。",
            'itemImage': "",
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
            self.copy_button.config(state=tk.NORMAL)
            self.set_status(f"✅ 完成！保存先: {filepath}")

            messagebox.showinfo("成功", f"投稿を作成しました！\n\n保存先: {filepath}\n\n「📋 コピー」ボタンを押してSNSに貼り付けてください")

        except Exception as e:
            self.set_status(f"❌ エラー: {e}")
            messagebox.showerror("エラー", f"投稿作成に失敗しました:\n{e}")

        finally:
            self.create_button.config(state=tk.NORMAL)

    def on_copy_click(self):
        """投稿をクリップボードにコピー"""
        text = self.preview_text.get(1.0, tk.END)
        if text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.set_status("✅ クリップボードにコピーしました")
            messagebox.showinfo("成功", "投稿をコピーしました！\nSNSに貼り付けてください")
        else:
            messagebox.showwarning("警告", "投稿を作成してからコピーしてください")

    def on_clear_click(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://item.rakuten.co.jp/")
        self.update_preview("")
        self.set_status("準備完了")
        self.copy_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PostCreatorApp(root)
    root.mainloop()
