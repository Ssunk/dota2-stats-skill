# 🎮 Dota 2 战绩查询 - Claude Code Skill

基于 [OpenDota API](https://docs.opendota.com/) 的完整 Dota 2 数据查询技能，覆盖全部 API 端点，供 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 使用。

## ✨ 功能 (27 个命令)

### 🧑 玩家
| 命令 | 说明 |
|------|------|
| `search <name>` | 搜索玩家 |
| `player <id>` | 段位、MMR、胜率 |
| `wl <id>` | 胜负统计（支持筛选） |
| `recent <id>` | 最近 ~20 场 |
| `matches <id>` | 完整历史 |
| `heroes <id>` | 英雄统计 |
| `peers <id>` | 一起玩的人 |
| `totals <id>` | 生涯累计数据 |
| `counts <id>` | 分类统计 |
| `rankings <id>` | 英雄排名百分位 |
| `ratings <id>` | 段位变化历史 |
| `refresh <id>` | 刷新数据 |

### ⚔️ 比赛
| 命令 | 说明 |
|------|------|
| `match <match_id>` | 10 人完整数据 |

### 🦸 英雄
| 命令 | 说明 |
|------|------|
| `hero_list` | 英雄列表 |
| `hero_stats` | 全局统计 |
| `hero_matchups <hero_id>` | 对抗胜率 |
| `hero_rankings <hero_id>` | Top 玩家 |
| `benchmarks <hero_id>` | 表现基准 |

### 🌍 全局
| 命令 | 说明 |
|------|------|
| `pro_players` | 职业选手 |
| `pro_matches` | 职业比赛 |
| `public_matches` | 公开比赛 |
| `live` | 实时比赛 |
| `teams` | 战队列表 |
| `team <team_id>` | 战队详情+阵容+赛果 |
| `leagues` | 联赛列表 |
| `constants <resource>` | 游戏常量 |
| `find_matches` | 按英雄阵容搜索 |

## 📁 项目结构

```
dota2-stats/
├── SKILL.md          # Claude Code 技能描述
├── dota2_query.py    # Python 查询脚本（全部功能）
└── README.md         # 本文件
```

## 🚀 使用

### 在 Claude Code 中

将目录放在 `~/.claude/skills/dota2-stats/`，然后直接用自然语言提问：

```
> 查一下 Miracle 的 Dota 2 战绩
> 看看影魔对抗谁胜率最低
> 最近有什么职业比赛
```

### 命令行独立使用

```bash
python dota2_query.py search Miracle
python dota2_query.py player 105248644
python dota2_query.py recent 105248644
python dota2_query.py hero_matchups 11          # 影魔对抗数据
python dota2_query.py hero_rankings 74          # 祈求者 Top 玩家
python dota2_query.py pro_matches --limit 10
python dota2_query.py live
python dota2_query.py team 8291895              # 查战队
python dota2_query.py constants items           # 物品数据
```

### 筛选参数

```bash
python dota2_query.py wl 105248644 --days 30 --lobby_type 7    # 近30天排位
python dota2_query.py matches 105248644 --hero_id 11 --limit 5 # 影魔最近5场
python dota2_query.py --lang en player 105248644                # English output
```

## 🔧 技术

- **API**: OpenDota API v31（免费，无需 Key）
- **依赖**: 仅 Python 3.6+ 标准库
- **Headers**: 配置完整浏览器级 HTTP Headers 防止 403
- **本地化**: 内置 127 个英雄中文名 + 段位/模式中英双语

## 📄 License

MIT
