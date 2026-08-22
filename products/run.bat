@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ================================================
echo 楽天商品投稿自動生成ツール
echo ================================================
echo.

REM 必要なパッケージをインストール
echo パッケージをインストール中...
python -m pip install -q requests schedule APScheduler

if errorlevel 1 (
    echo エラー: パッケージのインストールに失敗しました
    pause
    exit /b 1
)

REM 環境変数を設定
set RAKUTEN_API_KEY=218bd070-1f01-4b29-a6fa-44447838e132
set RAKUTEN_AFFILIATE_ID=56c29d66.fa76986e.56c29d67.5df37f66
set RAKUTEN_ACCESS_TOKEN=pk_kBunykYolTdyA9NJkXJ3X8vmwBUcY0NwscnXz8k7WTB

REM スクリプト実行
echo.
echo スクリプトを実行中...
echo.

python scripts/fetch_and_post.py

if errorlevel 1 (
    echo.
    echo エラーが発生しました
    pause
    exit /b 1
)

echo.
echo ================================================
echo 完了しました！
echo ================================================
echo.
echo 投稿は products\posts\ フォルダに保存されました
echo.
pause
