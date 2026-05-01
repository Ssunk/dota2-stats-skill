---
name: dota2-stats
description: 查询 Dota 2 玩家战绩、比赛数据和英雄统计。当用户询问 Dota 2 战绩、比赛记录、英雄数据、胜率等信息时使用此技能。支持通过玩家名搜索、通过 account_id 查询、查看最近比赛、英雄使用统计等功能。
---

# Dota 2 战绩查询技能

本技能使用 Python 脚本通过 [OpenDota API](https://docs.opendota.com/) 查询 Dota 2 相关数据。

## 工具脚本

查询工具位于本技能目录下：

```
~/.claude/skills/dota2-stats/dota2_query.py
```

该脚本**仅使用 Python 标准库**（urllib、json），无需安装任何第三方依赖。

## 可用命令

### 1. 搜索玩家（通过名字查找 account_id）
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py search <玩家名>
```
**使用时机**：用户提供玩家名而非 account_id 时，先用此命令搜索获取 account_id。

### 2. 获取玩家基本信息（段位、胜率等）
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py player <account_id>
```

### 3. 获取胜负统计（支持筛选）
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N]
```
- `--days N`：最近 N 天
- `--hero_id N`：指定英雄 ID
- `--lobby_type N`：大厅类型（7=排位）

### 4. 获取最近比赛（约20场）
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py recent <account_id>
```

### 5. 获取比赛历史（支持分页和筛选）
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N]
```

### 6. 获取英雄使用统计
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py heroes <account_id> [--limit N]
```

### 7. 获取单场比赛详情
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py match <match_id>
```

### 8. 获取一起玩的玩家统计
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py peers <account_id> [--limit N]
```

### 9. 获取英雄列表
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py hero_list
```

### 10. 获取英雄统计数据
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py hero_stats
```

### 11. 刷新玩家数据
```bash
python ~/.claude/skills/dota2-stats/dota2_query.py refresh <account_id>
```

## 使用流程

### 当用户提供玩家名时：
1. 运行 `search <玩家名>` 搜索玩家
2. 展示搜索结果让用户确认（如果多个匹配）
3. 使用确认的 `account_id` 查询后续数据

### 当用户提供 account_id 或 Steam ID 时：
- Steam 64位 ID 转 32位：`account_id = steam64_id - 76561197960265728`
- 直接使用 account_id 查询

### 查询战绩的标准流程：
1. 运行 `player <account_id>` 获取基本信息和胜率
2. 运行 `recent <account_id>` 获取最近比赛
3. 根据用户需要，进一步运行 `heroes` 或 `matches` 等命令

## 段位解读（rank_tier 字段）
- 十位数代表段位：1=先锋, 2=卫士, 3=中军, 4=执政官, 5=传奇, 6=远古, 7=神圣, 8=冠绝一世
- 个位数代表星数（1-5 颗星）
- 例：`75` = 神圣五星，`80` = 冠绝一世

## 常见游戏模式 ID
- 1: All Pick（全英雄选择）
- 2: Captain's Mode（队长模式）
- 22: All Pick Ranked（排位全选）
- 23: Turbo（加速模式）

## 常见大厅类型 ID
- 0: Normal（普通）
- 7: Ranked（排位）

## 注意事项

1. 脚本仅使用 Python 标准库，无需 pip install 任何依赖
2. 玩家需在 Dota 2 客户端中开启「公开比赛数据」选项才能查到完整数据
3. OpenDota API 有频率限制，避免短时间内大量请求
4. 所有输出均为中文格式
5. 运行时请使用系统 Python 3（`python` 或 `python3`）
