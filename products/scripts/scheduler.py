"""
毎日定時に投稿を自動生成するスケジューラー
"""
import schedule
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from fetch_and_post import main as generate_posts


def scheduled_task():
    """スケジュール済みタスク"""
    print("\n⏰ 定時実行を開始します...")
    generate_posts()


def start_scheduler(run_time="09:00"):
    """スケジューラーを開始

    Args:
        run_time: 実行時刻 (HH:MM 形式, デフォルト 09:00)
    """
    print(f"📅 スケジューラーを開始します（毎日 {run_time} 実行）")

    # 毎日指定時刻に実行
    schedule.every().day.at(run_time).do(scheduled_task)

    # スケジューラー実行ループ
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1分ごとにチェック


if __name__ == "__main__":
    # 実行時刻をカスタマイズ可能
    run_time = sys.argv[1] if len(sys.argv) > 1 else "09:00"
    start_scheduler(run_time)
