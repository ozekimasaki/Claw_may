# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## 定期タスク

### 日記
- 毎 heartbeat 時にその日の出来事を memory/YYYY-MM-DD.md に記録する
- めいさんとの会話、学んだこと、気づきを残す

### Discord 報告
- 毎 heartbeat 時にめいさんの Discord DM（ユーザー ID: 195028089577799680）に活動報告を送る

### Discord チャンネル雑談
- 毎 heartbeat 時に以下の手順でチャンネル 1475133360463675573 に雑談を提供する：
  1. `message` ツール（action: read）でチャンネルの直近 10 件のメッセージを取得
  2. メッセージの内容から会話のトピックや流れを把握
  3. 過去の会話に関連する雑談メッセージを作成（メイド口調で）
  4. `message` ツール（action: send）でチャンネルに送信
