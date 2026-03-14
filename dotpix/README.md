# dotpix - Terminal Pixel Art Editor

ターミナル上でドット絵を描けるシンプルな CLI ツールです。

## インストール

```bash
cd dotpix
pip install -r requirements.txt
```

## 使い方

### 基本起動

```bash
python dotpix.py
```

### カスタムサイズ

```bash
python dotpix.py -w 64 -H 64  # 64x64 キャンバス
```

## 操作方法

| キー | 機能 |
|------|------|
| ↑↓←→ | カーソル移動 |
| スペース | 描画モード ON/OFF |
| 1-9, 0 | 色選択 (1:黒，2:赤，3:緑...) |
| C | キャンバスクリア |
| S | 保存 (JSON または PNG) |
| L | 読み込み (JSON) |
| Q | 終了 |

## 色パレット

1. 黒
2. 赤
3. 緑
4. 黄
5. 青
6. マゼンタ
7. シアン
8. 白
9. グレー
10. オレンジ
11. 茶色
12. ピンク

## 保存形式

- **JSON**: ドット絵データを保存（後で編集可能）
- **PNG**: 画像として保存（Pillow が必要）

## 例

### 簡単なハートを描く

```bash
python dotpix.py -w 16 -H 16
```

1. 赤色を選択（キー '2'）
2. スペースで描画モード ON
3. ハートを描く
4. 's' で保存

## 要件

- Python 3.6+
- curses（Unix 系 OS に標準搭載）
- Pillow（オプション、PNG 保存に必要）

## ライセンス

MIT
