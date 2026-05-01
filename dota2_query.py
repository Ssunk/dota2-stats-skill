#!/usr/bin/env python3
"""
Dota 2 战绩查询工具 - 基于 OpenDota API
用法:
    python dota2_query.py search <玩家名>
    python dota2_query.py player <account_id>
    python dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N]
    python dota2_query.py recent <account_id>
    python dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N]
    python dota2_query.py heroes <account_id> [--limit N]
    python dota2_query.py match <match_id>
    python dota2_query.py peers <account_id> [--limit N]
    python dota2_query.py hero_list
    python dota2_query.py hero_stats
    python dota2_query.py refresh <account_id>
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import time
from datetime import datetime, timezone, timedelta

BASE_URL = "https://api.opendota.com/api"

# 段位映射
RANK_TIERS = {
    1: "先锋", 2: "卫士", 3: "中军", 4: "执政官",
    5: "传奇", 6: "远古", 7: "神圣", 8: "冠绝一世"
}

# 游戏模式映射
GAME_MODES = {
    0: "Unknown", 1: "全英雄选择", 2: "队长模式", 3: "随机征召",
    4: "单征召", 5: "全阵营随机", 12: "最少出场", 15: "自定义",
    16: "队长征召", 18: "技能征召", 22: "排位全选", 23: "加速模式"
}

# 大厅类型映射
LOBBY_TYPES = {
    0: "普通", 1: "练习", 2: "锦标赛", 4: "合作对抗电脑",
    5: "排位单排/双排", 6: "排位组排", 7: "排位", 8: "1v1中路单挑", 9: "对战电脑"
}

# 英雄名缓存
_hero_cache = None


def api_get(endpoint, params=None):
    """发送 GET 请求到 OpenDota API"""
    url = f"{BASE_URL}{endpoint}"
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url += "?" + urllib.parse.urlencode(filtered)
    
    req = urllib.request.Request(url, headers={"User-Agent": "Dota2StatsSkill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ API 请求失败: HTTP {e.code}", file=sys.stderr)
        if e.code == 404:
            print("   玩家未找到或数据不可用", file=sys.stderr)
        elif e.code == 429:
            print("   请求频率过高，请稍后再试", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def api_post(endpoint):
    """发送 POST 请求到 OpenDota API"""
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method="POST", headers={"User-Agent": "Dota2StatsSkill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def get_hero_map():
    """获取英雄 ID → 名称映射（带缓存）"""
    global _hero_cache
    if _hero_cache is None:
        heroes = api_get("/heroes")
        _hero_cache = {h["id"]: h["localized_name"] for h in heroes}
    return _hero_cache


def format_duration(seconds):
    """秒数转为 分:秒 格式"""
    return f"{seconds // 60}:{seconds % 60:02d}"


def format_time(unix_ts):
    """Unix 时间戳转为可读日期"""
    if not unix_ts:
        return "未知"
    dt = datetime.fromtimestamp(unix_ts, tz=timezone(timedelta(hours=8)))
    return dt.strftime("%Y-%m-%d %H:%M")


def format_time_ago(unix_ts):
    """Unix 时间戳转为「多久前」格式"""
    if not unix_ts:
        return "未知"
    now = time.time()
    diff = now - unix_ts
    if diff < 3600:
        return f"{int(diff / 60)}分钟前"
    elif diff < 86400:
        return f"{int(diff / 3600)}小时前"
    elif diff < 2592000:
        return f"{int(diff / 86400)}天前"
    elif diff < 31536000:
        return f"{int(diff / 2592000)}个月前"
    else:
        return f"{int(diff / 31536000)}年前"


def is_win(player_slot, radiant_win):
    """判断玩家是否胜利"""
    is_radiant = player_slot < 128
    return (is_radiant and radiant_win) or (not is_radiant and not radiant_win)


def decode_rank_tier(rank_tier):
    """解析段位"""
    if not rank_tier:
        return "未校准"
    tier = rank_tier // 10
    stars = rank_tier % 10
    name = RANK_TIERS.get(tier, f"未知({tier})")
    if tier == 8:
        return name
    return f"{name} {'⭐' * stars}" if stars else name


# ============ 命令处理函数 ============

def cmd_search(args):
    """搜索玩家"""
    if not args:
        print("用法: python dota2_query.py search <玩家名>")
        sys.exit(1)
    
    query = " ".join(args)
    results = api_get("/search", {"q": query})
    
    if not results:
        print(f"❌ 未找到匹配「{query}」的玩家")
        return
    
    print(f"\n🔍 搜索「{query}」的结果（共 {len(results)} 个）:\n")
    print(f"{'Account ID':<15} {'玩家名':<25} {'最后比赛时间':<20} {'相似度'}")
    print("-" * 75)
    for p in results[:15]:
        last_match = p.get("last_match_time", "未知")
        if last_match and last_match != "未知":
            last_match = last_match[:10]
        sim = f"{p.get('similarity', 0):.2f}"
        print(f"{p['account_id']:<15} {p.get('personaname', '未知'):<25} {last_match:<20} {sim}")


def cmd_player(args):
    """获取玩家信息"""
    if not args:
        print("用法: python dota2_query.py player <account_id>")
        sys.exit(1)
    
    account_id = args[0]
    data = api_get(f"/players/{account_id}")
    wl = api_get(f"/players/{account_id}/wl")
    
    profile = data.get("profile", {})
    rank_tier = data.get("rank_tier")
    leaderboard_rank = data.get("leaderboard_rank")
    mmr = data.get("computed_mmr")
    
    total = wl["win"] + wl["lose"]
    winrate = (wl["win"] / total * 100) if total > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"🎮 玩家资料")
    print(f"{'='*50}")
    print(f"  名称:       {profile.get('personaname', '未知')}")
    print(f"  Account ID: {profile.get('account_id', account_id)}")
    print(f"  Steam ID:   {profile.get('steamid', '未知')}")
    print(f"  段位:       {decode_rank_tier(rank_tier)}")
    if leaderboard_rank:
        print(f"  天梯排名:   #{leaderboard_rank}")
    if mmr:
        print(f"  预估 MMR:   {mmr}")
    print(f"  总场次:     {total}")
    print(f"  胜/负:      {wl['win']}胜 / {wl['lose']}负")
    print(f"  总胜率:     {winrate:.1f}%")
    print(f"  Steam:      {profile.get('profileurl', '无')}")
    print(f"{'='*50}")


def cmd_wl(args):
    """获取胜负统计"""
    if not args:
        print("用法: python dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N]")
        sys.exit(1)
    
    account_id = args[0]
    params = {}
    
    i = 1
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            params["date"] = args[i + 1]
            i += 2
        elif args[i] == "--hero_id" and i + 1 < len(args):
            params["hero_id"] = args[i + 1]
            i += 2
        elif args[i] == "--lobby_type" and i + 1 < len(args):
            params["lobby_type"] = args[i + 1]
            i += 2
        else:
            i += 1
    
    wl = api_get(f"/players/{account_id}/wl", params)
    total = wl["win"] + wl["lose"]
    winrate = (wl["win"] / total * 100) if total > 0 else 0
    
    filters = []
    if "date" in params:
        filters.append(f"最近{params['date']}天")
    if "hero_id" in params:
        hero_map = get_hero_map()
        hero_name = hero_map.get(int(params["hero_id"]), f"ID:{params['hero_id']}")
        filters.append(f"英雄:{hero_name}")
    if "lobby_type" in params:
        lt = LOBBY_TYPES.get(int(params["lobby_type"]), params["lobby_type"])
        filters.append(f"大厅:{lt}")
    
    filter_str = f"（{', '.join(filters)}）" if filters else ""
    
    print(f"\n📊 胜负统计{filter_str}")
    print(f"  胜场: {wl['win']}")
    print(f"  负场: {wl['lose']}")
    print(f"  总场: {total}")
    print(f"  胜率: {winrate:.1f}%")


def cmd_recent(args):
    """获取最近比赛"""
    if not args:
        print("用法: python dota2_query.py recent <account_id>")
        sys.exit(1)
    
    account_id = args[0]
    hero_map = get_hero_map()
    matches = api_get(f"/players/{account_id}/recentMatches")
    
    if not matches:
        print("❌ 未找到最近比赛记录")
        return
    
    print(f"\n🎮 最近 {len(matches)} 场比赛:\n")
    print(f"{'英雄':<16} {'结果':<6} {'K/D/A':<10} {'GPM':<6} {'XPM':<6} {'时长':<8} {'日期'}")
    print("-" * 80)
    
    wins = 0
    for m in matches:
        hero = hero_map.get(m.get("hero_id", 0), "未知")
        won = is_win(m.get("player_slot", 0), m.get("radiant_win"))
        if won:
            wins += 1
        result = "✅ 胜" if won else "❌ 负"
        kda = f"{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}"
        gpm = str(m.get("gold_per_min", 0))
        xpm = str(m.get("xp_per_min", 0))
        duration = format_duration(m.get("duration", 0))
        date = format_time(m.get("start_time"))
        
        print(f"{hero:<16} {result:<6} {kda:<10} {gpm:<6} {xpm:<6} {duration:<8} {date}")
    
    total = len(matches)
    print(f"\n📊 最近{total}场: {wins}胜 {total - wins}负 (胜率 {wins/total*100:.1f}%)")


def cmd_matches(args):
    """获取比赛历史"""
    if not args:
        print("用法: python dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N]")
        sys.exit(1)
    
    account_id = args[0]
    params = {}
    
    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            params["limit"] = args[i + 1]
            i += 2
        elif args[i] == "--hero_id" and i + 1 < len(args):
            params["hero_id"] = args[i + 1]
            i += 2
        elif args[i] == "--days" and i + 1 < len(args):
            params["date"] = args[i + 1]
            i += 2
        else:
            i += 1
    
    if "limit" not in params:
        params["limit"] = "20"
    
    hero_map = get_hero_map()
    matches = api_get(f"/players/{account_id}/matches", params)
    
    if not matches:
        print("❌ 未找到比赛记录")
        return
    
    print(f"\n🎮 比赛历史（共 {len(matches)} 场）:\n")
    print(f"{'比赛ID':<14} {'英雄':<16} {'结果':<6} {'K/D/A':<10} {'时长':<8} {'日期'}")
    print("-" * 80)
    
    wins = 0
    for m in matches:
        hero = hero_map.get(m.get("hero_id", 0), "未知")
        won = is_win(m.get("player_slot", 0), m.get("radiant_win"))
        if won:
            wins += 1
        result = "✅ 胜" if won else "❌ 负"
        kda = f"{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}"
        duration = format_duration(m.get("duration", 0))
        date = format_time(m.get("start_time"))
        
        print(f"{m.get('match_id', ''):<14} {hero:<16} {result:<6} {kda:<10} {duration:<8} {date}")
    
    total = len(matches)
    print(f"\n📊 共{total}场: {wins}胜 {total - wins}负 (胜率 {wins/total*100:.1f}%)")


def cmd_heroes(args):
    """获取英雄使用统计"""
    if not args:
        print("用法: python dota2_query.py heroes <account_id> [--limit N]")
        sys.exit(1)
    
    account_id = args[0]
    limit = 20
    
    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    hero_map = get_hero_map()
    hero_stats = api_get(f"/players/{account_id}/heroes")
    
    # 按场数排序，过滤掉0场的
    hero_stats = [h for h in hero_stats if h.get("games", 0) > 0]
    hero_stats.sort(key=lambda x: x.get("games", 0), reverse=True)
    hero_stats = hero_stats[:limit]
    
    if not hero_stats:
        print("❌ 未找到英雄使用记录")
        return
    
    print(f"\n🦸 英雄使用统计（Top {limit}）:\n")
    print(f"{'英雄':<18} {'场数':<8} {'胜场':<8} {'胜率':<10} {'最后使用'}")
    print("-" * 65)
    
    for h in hero_stats:
        hero = hero_map.get(h.get("hero_id", 0), f"ID:{h.get('hero_id', '?')}")
        games = h.get("games", 0)
        win = h.get("win", 0)
        winrate = f"{win / games * 100:.1f}%" if games > 0 else "N/A"
        last_played = format_time_ago(h.get("last_played"))
        
        print(f"{hero:<18} {games:<8} {win:<8} {winrate:<10} {last_played}")


def cmd_match(args):
    """获取比赛详情"""
    if not args:
        print("用法: python dota2_query.py match <match_id>")
        sys.exit(1)
    
    match_id = args[0]
    hero_map = get_hero_map()
    data = api_get(f"/matches/{match_id}")
    
    radiant_win = data.get("radiant_win")
    duration = format_duration(data.get("duration", 0))
    start_time = format_time(data.get("start_time"))
    game_mode = GAME_MODES.get(data.get("game_mode", 0), "未知")
    r_score = data.get("radiant_score", 0)
    d_score = data.get("dire_score", 0)
    
    print(f"\n{'='*80}")
    print(f"⚔️  比赛详情 - Match ID: {match_id}")
    print(f"{'='*80}")
    print(f"  模式: {game_mode}   |   时长: {duration}   |   日期: {start_time}")
    print(f"  比分: 天辉 {r_score} - {d_score} 夜魇   |   结果: {'天辉胜利 🟢' if radiant_win else '夜魇胜利 🔴'}")
    print()
    
    players = data.get("players", [])
    radiant = [p for p in players if p.get("player_slot", 128) < 128]
    dire = [p for p in players if p.get("player_slot", 0) >= 128]
    
    def print_team(team_name, team_players):
        print(f"  {'─'*38} {team_name} {'─'*38}")
        print(f"  {'玩家':<18} {'英雄':<16} {'K/D/A':<10} {'GPM':<6} {'XPM':<6} {'伤害':<8} {'补刀':<6} {'等级'}")
        print(f"  {'-'*76}")
        for p in team_players:
            name = p.get("personaname") or "匿名"
            if len(name) > 15:
                name = name[:14] + "…"
            hero = hero_map.get(p.get("hero_id", 0), "未知")
            kda = f"{p.get('kills', 0)}/{p.get('deaths', 0)}/{p.get('assists', 0)}"
            gpm = str(p.get("gold_per_min", 0))
            xpm = str(p.get("xp_per_min", 0))
            dmg = str(p.get("hero_damage", 0))
            lh = str(p.get("last_hits", 0))
            lvl = str(p.get("level", 0))
            print(f"  {name:<18} {hero:<16} {kda:<10} {gpm:<6} {xpm:<6} {dmg:<8} {lh:<6} {lvl}")
        print()
    
    print_team("🟢 天辉", radiant)
    print_team("🔴 夜魇", dire)


def cmd_peers(args):
    """获取一起玩的玩家统计"""
    if not args:
        print("用法: python dota2_query.py peers <account_id> [--limit N]")
        sys.exit(1)
    
    account_id = args[0]
    limit = 15
    
    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    peers = api_get(f"/players/{account_id}/peers")
    peers = peers[:limit]
    
    if not peers:
        print("❌ 未找到一起玩的玩家记录")
        return
    
    print(f"\n🤝 一起玩的玩家（Top {limit}）:\n")
    print(f"{'玩家名':<20} {'同队场次':<10} {'同队胜场':<10} {'同队胜率':<10} {'最后同场'}")
    print("-" * 70)
    
    for p in peers:
        name = p.get("personaname") or "匿名"
        if len(name) > 17:
            name = name[:16] + "…"
        games = p.get("with_games", 0)
        win = p.get("with_win", 0)
        winrate = f"{win / games * 100:.1f}%" if games > 0 else "N/A"
        last = format_time_ago(p.get("last_played"))
        
        print(f"{name:<20} {games:<10} {win:<10} {winrate:<10} {last}")


def cmd_hero_list(args):
    """获取所有英雄列表"""
    heroes = api_get("/heroes")
    heroes.sort(key=lambda x: x["id"])
    
    print(f"\n🦸 Dota 2 英雄列表（共 {len(heroes)} 个）:\n")
    print(f"{'ID':<6} {'英文名':<28} {'主属性':<8} {'攻击类型':<8} {'定位'}")
    print("-" * 80)
    
    for h in heroes:
        roles = ", ".join(h.get("roles", []))
        attr_map = {"agi": "敏捷", "str": "力量", "int": "智力", "all": "全能"}
        attr = attr_map.get(h.get("primary_attr", ""), h.get("primary_attr", ""))
        atk = "近战" if h.get("attack_type") == "Melee" else "远程"
        print(f"{h['id']:<6} {h['localized_name']:<28} {attr:<8} {atk:<8} {roles}")


def cmd_hero_stats(args):
    """获取英雄统计数据"""
    heroes = api_get("/heroStats")
    heroes.sort(key=lambda x: x.get("id", 0))
    
    print(f"\n📊 英雄统计数据:\n")
    print(f"{'ID':<5} {'英雄':<24} {'加速场':<10} {'加速胜':<10} {'加速胜率'}")
    print("-" * 65)
    
    for h in heroes:
        tp = h.get("turbo_picks", 0)
        tw = h.get("turbo_wins", 0)
        wr = f"{tw / tp * 100:.1f}%" if tp > 0 else "N/A"
        print(f"{h.get('id', 0):<5} {h.get('localized_name', '未知'):<24} {tp:<10} {tw:<10} {wr}")


def cmd_refresh(args):
    """刷新玩家数据"""
    if not args:
        print("用法: python dota2_query.py refresh <account_id>")
        sys.exit(1)
    
    account_id = args[0]
    result = api_post(f"/players/{account_id}/refresh")
    print(f"✅ 已提交刷新请求 (account_id: {account_id})")
    print(f"   响应: {json.dumps(result, ensure_ascii=False)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "search": cmd_search,
        "player": cmd_player,
        "wl": cmd_wl,
        "recent": cmd_recent,
        "matches": cmd_matches,
        "heroes": cmd_heroes,
        "match": cmd_match,
        "peers": cmd_peers,
        "hero_list": cmd_hero_list,
        "hero_stats": cmd_hero_stats,
        "refresh": cmd_refresh,
    }
    
    if command in ("--help", "-h", "help"):
        print(__doc__)
        sys.exit(0)
    
    if command not in commands:
        print(f"❌ 未知命令: {command}")
        print(f"可用命令: {', '.join(commands.keys())}")
        sys.exit(1)
    
    commands[command](args)


if __name__ == "__main__":
    main()
