---
name: dota2-stats
description: Query Dota 2 player records, match data, hero statistics, pro scene, teams, leagues and live games via OpenDota API. Supports 27 commands covering all API endpoints. Use --lang en for English output, default is Chinese. 查询 Dota 2 玩家战绩、比赛数据、英雄统计、职业赛事、战队、联赛和实时比赛。支持27个命令覆盖所有 OpenDota API 端点。
---

# Dota 2 Stats Query Skill (Full API Coverage)

本技能使用 Python 脚本通过 [OpenDota API](https://docs.opendota.com/) 查询 Dota 2 数据，覆盖全部 API 端点。

## Tool Script

```
~/.claude/skills/dota2-stats/dota2_query.py
```

**仅使用 Python 标准库**，无需第三方依赖。已配置完整 HTTP Headers 避免 403。

## Commands (27 total)

### Player Commands
```bash
python dota2_query.py search <name>              # 搜索玩家
python dota2_query.py player <account_id>         # 玩家信息/段位/胜率
python dota2_query.py wl <id> [--days/--hero_id/--lobby_type]  # 胜负统计
python dota2_query.py recent <id>                 # 最近~20场比赛
python dota2_query.py matches <id> [--limit/--hero_id/--days]  # 完整比赛历史
python dota2_query.py heroes <id> [--limit N]     # 英雄使用统计
python dota2_query.py peers <id> [--limit N]      # 一起玩的人
python dota2_query.py totals <id> [filters]       # 生涯总计(击杀/助攻等)
python dota2_query.py counts <id>                 # 分类统计
python dota2_query.py rankings <id>               # 玩家英雄排名
python dota2_query.py ratings <id>                # 段位历史
python dota2_query.py refresh <id>                # 刷新玩家数据
```

### Match Commands
```bash
python dota2_query.py match <match_id>            # 单场比赛详情(10人数据)
```

### Hero Commands
```bash
python dota2_query.py hero_list                   # 所有英雄列表
python dota2_query.py hero_stats                  # 英雄全局统计
python dota2_query.py hero_matchups <hero_id>     # 英雄对抗胜率
python dota2_query.py hero_rankings <hero_id>     # 英雄排行榜(Top玩家)
python dota2_query.py benchmarks <hero_id>        # 英雄表现基准
```

### Global / Pro Commands
```bash
python dota2_query.py pro_players                 # 职业选手列表
python dota2_query.py pro_matches [--limit N]     # 职业比赛
python dota2_query.py public_matches [--min_rank] # 公开比赛
python dota2_query.py live                        # 实时比赛
python dota2_query.py teams [--limit N]           # 战队列表
python dota2_query.py team <team_id>              # 战队详情+阵容+比赛
python dota2_query.py leagues                     # 联赛列表
python dota2_query.py constants <resource>        # 游戏常量(heroes/items等)
python dota2_query.py find_matches --teamA 1,2 --teamB 3,4  # 按英雄组合搜索
```

### Common Filters
- `--days N` — 最近 N 天
- `--hero_id N` — 指定英雄 ID
- `--lobby_type N` — 大厅类型 (7=排位)
- `--game_mode N` — 游戏模式
- `--limit N` — 限制结果数
- `--lang zh|en` — 输出语言 (默认中文)

## Usage Flow

### 用户提供玩家名时:
1. `search <名字>` → 获取 account_id
2. `player <id>` → 查看基本信息
3. `recent <id>` → 查看最近比赛

### Steam ID 转换:
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
1. 仅使用 Python 标准库，无需 pip install
2. 已配置浏览器级 HTTP Headers 防止 403
3. 玩家需开启「公开比赛数据」
4. 内置 127 个英雄的中文名映射
5. 默认输出中文，`--lang en` 切换英文
