# Dota 2 Stats Query - Claude Code Skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for querying Dota 2 player records, match data, and hero statistics via the [OpenDota API](https://docs.opendota.com/).

用于查询 Dota 2 玩家战绩、比赛数据和英雄统计的 Claude Code 技能插件。

## Language Support

Default output is **Chinese**. Add `--lang en` to any command for **English** output.

默认输出**中文**。添加 `--lang en` 参数切换为**英文**输出。

## Features / 功能特性

| Feature | Command | Description |
|---------|---------|-------------|
| Search Player | `search <name>` | Find player account_id by Steam name / 通过名字查找 account_id |
| Player Info | `player <id>` | Rank, MMR, overall win rate / 段位、MMR、总胜率 |
| Win/Loss Stats | `wl <id>` | W/L with hero/days/lobby filters / 胜/负场次，支持筛选 |
| Recent Matches | `recent <id>` | Last ~20 matches with KDA, GPM / 最近约 20 场比赛 |
| Match History | `matches <id>` | Full history with pagination / 完整比赛历史 |
| Hero Stats | `heroes <id>` | Games, win rate per hero / 各英雄使用场次、胜率 |
| Match Detail | `match <match_id>` | Full match data for 10 players / 单场 10 名玩家数据 |
| Teammates | `peers <id>` | Frequent teammates with win rate / 经常一起玩的玩家 |
| Hero List | `hero_list` | All heroes with attributes and roles / 全部英雄列表 |
| Hero Stats | `hero_stats` | Global hero statistics / 全局英雄统计数据 |
| Refresh Data | `refresh <id>` | Force refresh player's recent matches / 强制刷新玩家数据 |

## Project Structure / 项目结构

```
dota2-stats/
├── SKILL.md          # Claude Code skill definition
├── dota2_query.py    # Python query script (core tool)
└── README.md         # This file
```

## Installation / 安装

### Prerequisites / 前提条件

- **Python 3.6+** (stdlib only, no dependencies)
- **Claude Code** installed

### Setup / 安装步骤

Place this directory in the Claude Code skills directory:

将本目录放置于 Claude Code 技能目录下：

```
~/.claude/skills/dota2-stats/
```

## Usage / 使用方式

### In Claude Code / 在 Claude Code 中使用

Just ask in natural language:

直接自然语言提问：

```
> Check Miracle-'s Dota 2 stats
> Show recent matches for account_id 105248644
> What heroes does this player use most?
```

Claude will auto-detect the intent and invoke the skill.

### CLI Usage / 命令行使用

```bash
# English output / 英文输出
python dota2_query.py search Miracle --lang en
python dota2_query.py player 105248644 --lang en
python dota2_query.py recent 105248644 --lang en

# Chinese output (default) / 中文输出（默认）
python dota2_query.py search Miracle
python dota2_query.py player 105248644
python dota2_query.py recent 105248644

# With filters / 带筛选条件
python dota2_query.py wl 105248644 --days 30 --lobby_type 7
python dota2_query.py heroes 105248644 --limit 10
python dota2_query.py peers 105248644 --limit 10
```

## Example Output / 输出示例

### Player Profile (English) / 玩家信息（英文）
```
==================================================
  Player Profile
==================================================
  Name:        SawagedKick
  Account ID:  105248644
  Rank:        Immortal
  Leaderboard: #16
  Total Games: 4062
  W/L:         2389W / 1673L
  Win Rate:    58.8%
==================================================
```

### Recent Matches (English) / 最近比赛（英文）
```
  Recent 20 Matches:

  Hero             Result K/D/A      GPM    XPM    Duration Date
  ------------------------------------------------------------------------------
  Bloodseeker      W      13/4/12    846    841    49:36    2025-01-21 00:12
  Night Stalker    L      13/6/7     669    812    53:13    2025-01-20 22:54
  Bristleback      W      9/1/10     743    786    31:45    2025-01-20 21:57

  Last 20: 13W 7L (Win Rate 65.0%)
```

### 玩家信息（中文）
```
==================================================
  玩家资料
==================================================
  名称:       SawagedKick
  Account ID: 105248644
  段位:       冠绝一世
  天梯排名:   #16
  总场次:     4062
  胜/负:      2389胜 / 1673负
  总胜率:     58.8%
==================================================
```

## Technical Details / 技术细节

- **API**: [OpenDota API](https://docs.opendota.com/) (free, no API key required)
- **Dependencies / 依赖**: Python stdlib only (`urllib`, `json`, `sys`, `time`, `datetime`)
- **Rate Limit / 频率限制**: OpenDota has rate limits for unauthenticated users
- **Data Availability / 数据可用性**: Player must enable "Expose Public Match Data" in Dota 2 client

## Notes / 注意事项

1. Steam ID conversion: `account_id = steam64_id - 76561197960265728`
2. Rank encoding: tens = tier (1-8), ones = stars (1-5)
3. Win/loss: determined by `player_slot` (0-127 Radiant / 128-255 Dire) combined with `radiant_win`
4. Timestamps converted to UTC+8 by default

## License / 许可证

MIT
