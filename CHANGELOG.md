# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] — 2026-05-23

### Added
- **初回起動時に「インポート」モードを追加**
  - 秘書がオーナーに「A. インポート ／ B. ヒアリング」の2択を提示するようになった
  - インポート方式：ChatGPT・Gemini など他のAIで話していた内容をペーストすれば、秘書が自動解析して `secretary/owner-profile.md` に書き起こす
  - これにより、ゼロから1問1問のヒアリングを回す必要がなくなり、既存ユーザーの移行が圧倒的に楽になった
  - 長文のペースト元テキストは `secretary/inbox/imported-YYYY-MM-DD.md` に原文保存

### Changed
- `secretary/owner-profile.md` 冒頭にインポート機能の案内を追記
- `secretary/CLAUDE.md` にインポート時の運用ルールを明文化
- README のクイックスタートを2択構成に書き直し

## [0.4.0] — 2026-05-23

### Changed
- 「秘書しおり」のキャラ名を **「秘書」** に統一（他キャラ：ハンター／バンカー／番頭等と同じく役割名のみで揃える）
- README の解凍手順を **Mac／Windows 両対応** に拡張
  - Mac: ダブルクリックで自動展開
  - Windows: 右クリック →「すべて展開」→「展開」

## [0.3.0] — 2026-05-23

### Changed
- README のクイックスタートを **Claude Code デスクトップアプリ前提** に変更
  - 「フォルダを開く」ボタンで作業フォルダを選択する流れに
  - ターミナルコマンドは「CLI派の方向け」の補足として残す
- FAQ にデスクトップアプリ／CLI両対応の説明を追加

## [0.2.0] — 2026-05-23

### Added
- `secretary/owner-profile.md` — オーナープロフィール専用ファイル
- ルート CLAUDE.md に「初回起動時の秘書ヒアリング」ルールを追加
  - 初回起動時、`owner-profile.md` が空欄なら秘書が対話形式でヒアリング
  - 1問ずつ・スキップOK・回答ごとに `owner-profile.md` を更新
- `secretary/CLAUDE.md` にプロフィール管理の役割を明示

### Changed
- オーナープロフィールの管理を CLAUDE.md から `secretary/owner-profile.md` に分離
  - 組織のコア設定（CLAUDE.md）と個人データ（プロフィール）を分離
  - 受講者が CLAUDE.md を直接編集しなくて済む設計に
- README のクイックスタートを「秘書ヒアリング」ベースに書き直し

## [0.1.0] — 2026-05-24

### Added
- 初版リリース
- 司令塔1 + オフェンス3 + ディフェンス3 の7部署構成
  - 🎯 秘書
  - ⚔️ 物件開拓＆リサーチ（ハンター）
  - ⚔️ 融資（バンカー）
  - ⚔️ 戦略・参謀（軍師）
  - 🛡️ 賃貸管理（番頭）
  - 🛡️ 経理（帳簿番）
  - 🛡️ 法務（奉行）
- ルート `CLAUDE.md`（オーナープロフィール記入欄つき）
- `.claude/rules/departments.md` — 各部署の詳細・口調・判断軸
- `.claude/settings.json` — 推奨セキュリティルール
- サンプルデータ
  - `property/portfolio/sample-apartment.md`
  - `banking/banks/sample-shinkin.md`
  - `legal/contracts/sample-rental-contract.md`
- 各部署のテンプレート（`_template.md`）
- `.gitignore`（個人情報・OS固有ファイル除外）
