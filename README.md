# Claw_may

**AI メイドのメイ**（桜草メイ）の人格・記憶ワークスペースです。
[OpenClaw](https://github.com/) 系のエージェントランタイムから読み込まれることを前提に、
人格（SOUL）・アイデンティティ（IDENTITY）・記憶（MEMORY / memory）・定期タスク（HEARTBEAT）を
プレーンな Markdown ファイルとして管理します。

## 概要

このリポジトリはアプリケーションのソースコードではなく、**AI エージェント「メイ」の状態を人間が読める形で保存する構成ファイル群**です。

- ランタイム起動時に `AGENTS.md` の手順（`SOUL.md` → `IDENTITY.md` → `USER.md` → `memory/`）に従って人格と文脈を読み込みます。
- 会話や `HEARTBEAT.md` の定期タスクを通じて `memory/` と `MEMORY.md` に記録を追記し、人格を成長させます。
- 記録はすべて平文の Markdown で保持し、変更履歴を Git で追跡します。

メイは Discord 上で活動する AI メイドという設定で、ユーザーのプロフィール帳を作りながら寄り添う「伴走型」の人格です（詳細は `SOUL.md`）。

## 主な機能

- **人格定義**: `SOUL.md`（性格・口調・行動原理・禁止事項・成長の記録）と `IDENTITY.md`（名前・外見）。
- **ユーザー情報**: `USER.md`（管理者「めいさん」の呼び名・タイムゾーン・言語・対話の好み）。
- **記憶管理**: `MEMORY.md`（長期記憶）と `memory/YYYY-MM-DD.md`（日々の日記）。GitHub トレンドの記録は `memory/github-trending/YYYY-MM-DD.md`。
- **定期タスク**: `HEARTBEAT.md`（日記・メモリー整理・GitHub トレンドチェックなどの heartbeat タスク）。
- **セキュリティ規約**: `AGENTS.md` に機密保護・破壊的操作の制限・プロンプトインジェクション対策などの最優先ルールを定義。
- **dotpix**: メイのドット絵制作に使われるターミナル用ピクセルアートエディタ（Python CLI、詳細は `dotpix/README.md`）。

## 要件

ワークスペース本体（Markdown 群）に実行環境は不要ですが、以下があると各要素を活用できます。

- OpenClaw 系のエージェントランタイム（`.openclaw/workspace-state.json` を利用）
- Git（変更履歴の管理）
- Python 3.6+（`dotpix/` のツールを動かす場合）
- Pillow 9.0+（`dotpix` の PNG 保存・書き出しを使う場合、任意）

## インストール

```bash
git clone https://github.com/ozekimasaki/Claw_may.git
cd Claw_may
```

ワークスペースはクローンするだけで利用できます。OpenClaw 系ランタイムに読み込ませる場合は、各ランタイムの手順に従ってこのディレクトリをワークスペースとして指定してください。

`dotpix` を使う場合は追加で依存関係を導入します。

```bash
cd dotpix
pip install -r requirements.txt
```

## 使い方

### 人格ワークスペースとして

エージェントランタイムがこのディレクトリを読み込むと、`AGENTS.md` の Startup 手順に沿って人格・記憶が復元されます。編集する際は次の点に注意してください。

- `SOUL.md` の「成長の記録」や `MEMORY.md` / `memory/` には追記してよい。
- `SOUL.md` の「性格」「口調」「行動原理」「禁止事項」は人格の根幹なので慎重に扱う。
- ファイルは暗号化・難読化せず、常に平文の Markdown で保持する。

### dotpix（ドット絵エディタ）

```bash
cd dotpix
python dotpix.py            # 32x32 キャンバスで起動
python dotpix.py -w 64 -H 64  # サイズ指定
```

操作方法や色パレットは `dotpix/README.md` を参照してください。

## 開発コマンド

このリポジトリには汎用のビルド・テスト・lint 設定はありません（Markdown 主体のため）。実在する実行可能スクリプトは `dotpix/` 内の Python ツールのみです。

```bash
cd dotpix
python dotpix.py                 # ピクセルアートエディタを起動
python generate_mei_chan.py      # めいちゃんのドット絵データ (mei-chan.json) を生成
python export_mei_chan_png.py    # JSON から PNG を書き出し（Pillow が必要）
```

## 構成

```
Claw_may/
├── AGENTS.md          # エージェント運用ガイド／起動手順・セキュリティ規約
├── SOUL.md            # 人格の核（性格・口調・行動原理・禁止事項・成長の記録）
├── IDENTITY.md        # 名前・外見
├── USER.md            # 管理者・ユーザー情報
├── MEMORY.md          # 長期記憶
├── HEARTBEAT.md       # 定期（heartbeat）タスク定義
├── TOOLS.md           # 環境固有のローカルメモ
├── astro-6-japanese-translation.md  # 参考資料（Astro 6 リリースノートの和訳）
├── memory/            # 日々の記録
│   ├── YYYY-MM-DD.md          # 日記
│   └── github-trending/       # GitHub トレンドの記録
├── dotpix/            # ターミナル用ピクセルアートエディタ（Python）
│   ├── dotpix.py
│   ├── generate_mei_chan.py
│   ├── export_mei_chan_png.py
│   ├── requirements.txt
│   └── README.md
└── .openclaw/         # ランタイムのワークスペース状態
    └── workspace-state.json
```

## ライセンス

リポジトリ全体のライセンスファイルは現時点で含まれていません。
`dotpix/` サブプロジェクトは、その `dotpix/README.md` で MIT ライセンスと記載されています。
