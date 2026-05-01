---
name: dota2-stats
description: Query Dota 2 player records, match data and hero statistics. Supports player search by name, query by account_id, recent matches, hero stats, etc. Use --lang en for English output, default is Chinese. 查询 Dota 2 玩家战绩、比赛数据和英雄统计。支持通过玩家名搜索、通过 account_id 查询、查看最近比赛、英雄使用统计等功能。
---

# Dota 2 Stats Query Skill / Dota 2 战绩查询技能

This skill queries Dota 2 data via the [OpenDota API](https://docs.opendota.com/) using a Python script.

本技能使用 Python 脚本通过 [OpenDota API](https://docs.opendota.com/) 查询 Dota 2 相关数据。

## Language / 语言

- **Default**: Chinese (中文)
- **English**: add `--lang en` to any command
- **中文**: 默认输出中文，无需额外参数

Example:
```bash
# English output
python dota2_query.py player 105248644 --lang en

# Chinese output (default)
python dota2_query.py player 105248644
```

## Tool Script / 工具脚本

The query tool is located at:
查询工具位于：

```
~/.claude/skills/dota2-stats/dota2_query.py
```

The script uses **only Python standard library** (urllib, json), no third-party dependencies required.
该脚本**仅使用 Python 标准库**，无需安装任何第三方依赖。

## Available Commands / 可用命令

### 1. Search Player / 搜索玩家
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py search <player_name>
```
Use when user provides a player name instead of account_id.
**使用时机**：用户提供玩家名而非 account_id 时。

### 2. Player Profile / 获取玩家基本信息
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py player <account_id>
```

### 3. Win/Loss Stats / 获取胜负统计
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N]
```
- `--days N`: Last N days / 最近 N 天
- `--hero_id N`: Specific hero / 指定英雄 ID
- `--lobby_type N`: Lobby type / 大厅类型 (7=Ranked 排位)

### 4. Recent Matches / 获取最近比赛
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py recent <account_id>
```

### 5. Match History / 获取比赛历史
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N]
```

### 6. Hero Stats / 获取英雄使用统计
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py heroes <account_id> [--limit N]
```

### 7. Match Detail / 获取单场比赛详情
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py match <match_id>
```

### 8. Frequent Teammates / 获取一起玩的玩家
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py peers <account_id> [--limit N]
```

### 9. Hero List / 获取英雄列表
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py hero_list
```

### 10. Global Hero Stats / 获取英雄统计数据
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py hero_stats
```

### 11. Refresh Player Data / 刷新玩家数据
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py refresh <account_id>
```

## Usage Flow / 使用流程

### When user provides a player name / 当用户提供玩家名时：
1. Run `search <player_name>` to find the player
2. Show search results for confirmation (if multiple matches)
3. Use the confirmed `account_id` for further queries

### When user provides account_id or Steam ID / 当用户提供 account_id 或 Steam ID 时：
- Convert Steam 64-bit ID to 32-bit: `account_id = steam64_id - 76561197960265728`
- Query directly with account_id

### Standard flow for match queries / 查询战绩的标准流程：
1. Run `player <account_id>` for profile info and win rate
2. Run `recent <account_id>` for recent matches
3. Run `heroes` or `matches` based on user needs

## Rank Tier Decoding / 段位解读

| Tier | English | 中文 |
|------|---------|------|
| 1 | Herald | 先锋 |
| 2 | Guardian | 卫士 |
| 3 | Crusader | 中军 |
| 4 | Archon | 统帅 |
| 5 | Legend | 传奇 |
| 6 | Ancient | 万古流芳 |
| 7 | Divine | 超凡入圣 |
| 8 | Immortal | 冠绝一世 |

- Tens digit = tier, ones digit = stars (1-5)
- 十位数代表段位，个位数代表星数
- Example: `75` = Divine 5 / 神圣五星

## Common Game Modes / 常见游戏模式 ID

| ID | English | 中文 |
|----|---------|------|
| 1 | All Pick | 全英雄选择 |
| 2 | Captain's Mode | 队长模式 |
| 22 | All Pick Ranked | 排位全选 |
| 23 | Turbo | 加速模式 |

## Common Lobby Types / 常见大厅类型 ID

| ID | English | 中文 |
|----|---------|------|
| 0 | Normal | 普通 |
| 7 | Ranked | 排位 |

## Notes / 注意事项

1. The script uses only Python stdlib, no pip install needed / 脚本仅使用 Python 标准库
2. Player must enable "Expose Public Match Data" in Dota 2 client / 玩家需开启「公开比赛数据」
3. OpenDota API has rate limits, avoid excessive requests / API 有频率限制
4. Output language defaults to Chinese, use `--lang en` for English / 输出默认中文
5. Use system Python 3 (`python` or `python3`)
