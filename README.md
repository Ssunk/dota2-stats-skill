# 🎮 Dota 2 战绩查询 - Claude Code Skill

一个用于 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的技能插件，通过 [OpenDota API](https://docs.opendota.com/) 查询 Dota 2 玩家战绩、比赛数据和英雄统计。

## ✨ 功能特性

| 功能 | 命令 | 说明 |
|------|------|------|
| 🔍 搜索玩家 | `search <名字>` | 通过 Steam 名查找玩家 account_id |
| 👤 玩家信息 | `player <id>` | 段位、MMR、总胜率等概要信息 |
| 📊 胜负统计 | `wl <id>` | 胜/负场次，支持按英雄、天数、大厅类型筛选 |
| 🎮 最近比赛 | `recent <id>` | 最近约 20 场比赛的 KDA、GPM 等详情 |
| 📜 比赛历史 | `matches <id>` | 完整比赛历史，支持分页和筛选 |
| 🦸 英雄统计 | `heroes <id>` | 各英雄使用场次、胜率、最后使用时间 |
| ⚔️ 比赛详情 | `match <match_id>` | 单场比赛 10 名玩家的完整数据 |
| 🤝 好友统计 | `peers <id>` | 经常一起玩的玩家及同队胜率 |
| 📋 英雄列表 | `hero_list` | 全部英雄 ID、名称、属性、定位 |
| 📈 英雄数据 | `hero_stats` | 各英雄的全局统计数据 |
| 🔄 刷新数据 | `refresh <id>` | 强制刷新玩家最新比赛记录 |

## 📁 项目结构

```
dota2-stats/
├── SKILL.md          # Claude Code 技能描述文件
├── dota2_query.py    # Python 查询脚本（核心工具）
└── README.md         # 本文件
```

## 🚀 安装与使用

### 前提条件

- **Python 3.6+**（仅使用标准库，无需安装第三方依赖）
- **Claude Code** 已安装

### 安装

将本目录放置于 Claude Code 技能目录下：

```
~/.claude/skills/dota2-stats/
```

### 在 Claude Code 中使用

安装完成后，在 Claude Code 中直接用自然语言提问即可：

```
> 帮我查一下 Miracle 的 Dota 2 战绩
> 查看 account_id 105248644 的最近比赛
> 看看这个玩家最常用的英雄
```

Claude 会自动识别意图并调用 `/dota2-stats` 技能，通过 Python 脚本查询数据。

### 独立使用（命令行）

也可以直接在终端中运行脚本：

```bash
# 搜索玩家
python dota2_query.py search Miracle

# 查看玩家信息
python dota2_query.py player 105248644

# 查看最近比赛
python dota2_query.py recent 105248644

# 查看英雄统计（Top 10）
python dota2_query.py heroes 105248644 --limit 10

# 查看胜负（最近30天排位赛）
python dota2_query.py wl 105248644 --days 30 --lobby_type 7

# 查看比赛详情
python dota2_query.py match 8162889065

# 查看一起玩的人
python dota2_query.py peers 105248644 --limit 10
```

## 📖 输出示例

### 玩家信息
```
==================================================
🎮 玩家资料
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

### 最近比赛
```
🎮 最近 20 场比赛:

英雄               结果     K/D/A      GPM    XPM    时长       日期
--------------------------------------------------------------------------------
Bloodseeker      ✅ 胜    13/4/12    846    841    49:36    2025-01-21 00:12
Night Stalker    ❌ 负    13/6/7     669    812    53:13    2025-01-20 22:54
Bristleback      ✅ 胜    9/1/10     743    786    31:45    2025-01-20 21:57
...

📊 最近20场: 13胜 7负 (胜率 65.0%)
```

## 🔧 技术细节

- **API**: [OpenDota API v31](https://docs.opendota.com/)（免费，无需 API Key）
- **依赖**: 仅 Python 标准库（`urllib`、`json`、`sys`、`time`、`datetime`）
- **频率限制**: OpenDota API 对未认证用户有调用频率限制，正常使用不会触发
- **数据可用性**: 玩家需在 Dota 2 客户端设置中开启「公开比赛数据」

## 📝 注意事项

1. Steam ID 转换：`account_id = steam64_id - 76561197960265728`
2. 段位编码：十位数 = 段位（1-8），个位数 = 星数（1-5）
3. 胜负判断：结合 `player_slot`（0-127 天辉 / 128-255 夜魇）与 `radiant_win` 字段
4. 时间戳默认转换为 UTC+8（北京时间）

## 📄 License

MIT
