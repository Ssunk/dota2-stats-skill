---
name: dota2-stats-skill
description: Query Dota 2 player records, match data, hero statistics, pro scene, teams, leagues and live games via OpenDota API. Supports 27 commands covering all API endpoints. Use --lang en for English output, default is Chinese. 查询 Dota 2 玩家战绩、比赛数据、英雄统计、职业赛事、战队、联赛和实时比赛。支持27个命令覆盖所有 OpenDota API 端点。
---

# Dota 2 Stats Query Skill (Full API Coverage)

This skill uses a Python script to query Dota 2 data via the [OpenDota API](https://docs.opendota.com/), covering all API endpoints.

## Tool Script
### Claude Code
```
~/.claude/skills/dota2-stats-skill/scripts/dota2_query.py
```

### OpenClaw
```
~/.openclaw/plugin-skills/dota2-stats-skill/scripts/dota2_query.py
```


**Uses only Python standard library** - no third-party dependencies required. Configured with complete HTTP Headers to avoid 403 errors.

## Commands (27 total)

### Player Commands
```bash
python scripts/dota2_query.py search <name>              # Search for a player (SLOW: 1-2 min)
python scripts/dota2_query.py player <account_id>         # Player info/rank/winrate
python scripts/dota2_query.py wl <id> [--days/--hero_id/--lobby_type]  # Win/loss stats
python scripts/dota2_query.py recent <id>                 # Recent ~20 matches
python scripts/dota2_query.py matches <id> [--limit/--hero_id/--days]  # Full match history
python scripts/dota2_query.py heroes <id> [--limit N]     # Hero usage stats
python scripts/dota2_query.py peers <id> [--limit N]      # Frequent teammates
python scripts/dota2_query.py totals <id> [filters]       # Career totals (kills/assists etc)
python scripts/dota2_query.py counts <id>                 # Categorized stats
python scripts/dota2_query.py rankings <id>               # Player hero rankings
python scripts/dota2_query.py ratings <id>                # Rank history
python scripts/dota2_query.py refresh <id>                # Refresh player data
```

### Match Commands
```bash
python scripts/dota2_query.py match <match_id>            # Single match details (10 players)
```

### Hero Commands
```bash
python scripts/dota2_query.py hero_list                   # All heroes list
python scripts/dota2_query.py hero_stats                  # Global hero stats
python scripts/dota2_query.py hero_matchups <hero_id>     # Hero matchup winrates
python scripts/dota2_query.py hero_rankings <hero_id>     # Hero leaderboard (Top players)
python scripts/dota2_query.py benchmarks <hero_id>        # Hero performance benchmarks
```

### Global / Pro Commands
```bash
python scripts/dota2_query.py pro_players                 # Pro players list
python scripts/dota2_query.py pro_matches [--limit N]     # Pro matches
python scripts/dota2_query.py public_matches [--min_rank] # Public matches
python scripts/dota2_query.py live                        # Live matches
python scripts/dota2_query.py teams [--limit N]           # Teams list
python scripts/dota2_query.py team <team_id>              # Team details+roster+matches
python scripts/dota2_query.py leagues                     # Leagues list
python scripts/dota2_query.py constants <resource>        # Game constants (heroes/items etc)
python scripts/dota2_query.py find_matches --teamA 1,2 --teamB 3,4  # Search by hero lineup
```

### Common Filters
- `--days N` — Last N days
- `--hero_id N` — Specific hero ID
- `--lobby_type N` — Lobby type (7=Ranked)
- `--game_mode N` — Game mode
- `--limit N` — Limit results
- `--lang zh|en` — Output language (default Chinese)

## Usage Flow

### When user provides a player name:
1. `search <name>` → Get account_id
2. `player <id>` → View basic info
3. `recent <id>` → View recent matches

### Steam ID conversion:
`account_id = steam64_id - 76561197960265728`

## Rank Tier

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

## Notes
1. Uses only Python standard library - no pip install required
2. Configured with browser-level HTTP Headers to prevent 403 errors
3. Players need to have "Public Match Data" enabled
4. Built-in Chinese names for 127 heroes
5. Select the output language based on the language used in the user's question, use `--lang en` for English, `--lang zh` for Chinese
6. **`search` command is slow** (1-2 minutes) because it queries the entire OpenDota player database. When invoking this command, always remind the user that it may take a while and to please wait patiently. If the user already knows the player's Dota 2 account ID, suggest using `player <account_id>` directly for faster results