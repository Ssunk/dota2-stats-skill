#!/usr/bin/env python3
"""
Dota 2 Stats Query Tool - Based on OpenDota API
Usage:
    python dota2_query.py search <player_name> [--lang zh|en]
    python dota2_query.py player <account_id> [--lang zh|en]
    python dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N] [--lang zh|en]
    python dota2_query.py recent <account_id> [--lang zh|en]
    python dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N] [--lang zh|en]
    python dota2_query.py heroes <account_id> [--limit N] [--lang zh|en]
    python dota2_query.py match <match_id> [--lang zh|en]
    python dota2_query.py peers <account_id> [--limit N] [--lang zh|en]
    python dota2_query.py hero_list [--lang zh|en]
    python dota2_query.py hero_stats [--lang zh|en]
    python dota2_query.py refresh <account_id> [--lang zh|en]
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import time
from datetime import datetime, timezone, timedelta

BASE_URL = "https://api.opendota.com/api"

# ──────────────────────────────────────────────
#  Translations (zh / en)
# ──────────────────────────────────────────────
T = {
    "zh": {
        # Error messages
        "api_fail": "API 请求失败: HTTP",
        "not_found": "玩家未找到或数据不可用",
        "rate_limit": "请求频率过高，请稍后再试",
        "network_error": "网络错误:",
        "no_recent": "未找到最近比赛记录",
        "no_matches": "未找到比赛记录",
        "no_heroes": "未找到英雄使用记录",
        "no_peers": "未找到一起玩的玩家记录",
        "unknown_cmd": "未知命令:",
        "available_cmds": "可用命令:",

        # Search
        "search_no_result": "未找到匹配「{query}」的玩家",
        "search_header": "搜索「{query}」的结果（共 {count} 个）:",
        "search_col_id": "Account ID",
        "search_col_name": "玩家名",
        "search_col_last": "最后比赛时间",
        "search_col_sim": "相似度",

        # Player
        "player_header": "玩家资料",
        "player_name": "名称:",
        "player_account_id": "Account ID:",
        "player_steam_id": "Steam ID:",
        "player_rank": "段位:",
        "player_leaderboard": "天梯排名:",
        "player_mmr": "预估 MMR:",
        "player_games": "总场次:",
        "player_wl": "胜/负:",
        "player_winrate": "总胜率:",
        "player_steam_url": "Steam:",

        # WL
        "wl_header": "胜负统计",
        "wl_wins": "胜场:",
        "wl_losses": "负场:",
        "wl_total": "总场:",
        "wl_winrate": "胜率:",
        "wl_filter_days": "最近{days}天",
        "wl_filter_hero": "英雄:{hero}",
        "wl_filter_lobby": "大厅:{lobby}",

        # Recent
        "recent_header": "最近 {count} 场比赛:",
        "recent_col_hero": "英雄",
        "recent_col_result": "结果",
        "recent_col_gpm": "GPM",
        "recent_col_xpm": "XPM",
        "recent_col_duration": "时长",
        "recent_col_date": "日期",
        "recent_summary": "最近{total}场: {wins}胜 {losses}负 (胜率 {wr:.1f}%)",

        # Matches
        "matches_header": "比赛历史（共 {count} 场）:",
        "matches_col_id": "比赛ID",
        "matches_summary": "共{total}场: {wins}胜 {losses}负 (胜率 {wr:.1f}%)",

        # Heroes
        "heroes_header": "英雄使用统计（Top {limit}）:",
        "heroes_col_hero": "英雄",
        "heroes_col_games": "场数",
        "heroes_col_wins": "胜场",
        "heroes_col_winrate": "胜率",
        "heroes_col_last": "最后使用",

        # Match detail
        "match_header": "比赛详情 - Match ID:",
        "match_mode": "模式",
        "match_duration": "时长",
        "match_date": "日期",
        "match_score": "比分",
        "match_result_radiant": "天辉胜利",
        "match_result_dire": "夜魇胜利",
        "match_team_radiant": "天辉",
        "match_team_dire": "夜魇",
        "match_col_player": "玩家",
        "match_col_damage": "伤害",
        "match_col_lh": "补刀",
        "match_col_level": "等级",
        "match_anonymous": "匿名",

        # Peers
        "peers_header": "一起玩的玩家（Top {limit}）:",
        "peers_col_name": "玩家名",
        "peers_col_games": "同队场次",
        "peers_col_wins": "同队胜场",
        "peers_col_winrate": "同队胜率",
        "peers_col_last": "最后同场",

        # Hero list
        "herolist_header": "Dota 2 英雄列表（共 {count} 个）:",
        "herolist_col_id": "ID",
        "herolist_col_name": "英文名",
        "herolist_col_attr": "主属性",
        "herolist_col_atk": "攻击类型",
        "herolist_col_roles": "定位",

        # Hero stats
        "herostats_header": "英雄统计数据:",
        "herostats_col_id": "ID",
        "herostats_col_hero": "英雄",
        "herostats_col_turbo_picks": "加速场",
        "herostats_col_turbo_wins": "加速胜",
        "herostats_col_turbo_wr": "加速胜率",

        # Refresh
        "refresh_ok": "已提交刷新请求 (account_id: {aid})",
        "refresh_resp": "响应:",

        # Usage
        "usage_search": "用法: python dota2_query.py search <玩家名>",
        "usage_player": "用法: python dota2_query.py player <account_id>",
        "usage_wl": "用法: python dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N]",
        "usage_recent": "用法: python dota2_query.py recent <account_id>",
        "usage_matches": "用法: python dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N]",
        "usage_heroes": "用法: python dota2_query.py heroes <account_id> [--limit N]",
        "usage_match": "用法: python dota2_query.py match <match_id>",
        "usage_peers": "用法: python dota2_query.py peers <account_id> [--limit N]",

        # Common labels
        "win": "胜",
        "lose": "负",
        "unknown": "未知",
        "uncalibrated": "未校准",
        "n_a": "N/A",

        # Time ago
        "minutes_ago": "{n}分钟前",
        "hours_ago": "{n}小时前",
        "days_ago": "{n}天前",
        "months_ago": "{n}个月前",
        "years_ago": "{n}年前",

        # Rank tiers
        "rank_1": "先锋",
        "rank_2": "卫士",
        "rank_3": "中军",
        "rank_4": "执政官",
        "rank_5": "传奇",
        "rank_6": "远古",
        "rank_7": "神圣",
        "rank_8": "冠绝一世",
        "rank_unknown": "未知({tier})",

        # Game modes
        "mode_0": "Unknown",
        "mode_1": "全英雄选择",
        "mode_2": "队长模式",
        "mode_3": "随机征召",
        "mode_4": "单征召",
        "mode_5": "全阵营随机",
        "mode_12": "最少出场",
        "mode_15": "自定义",
        "mode_16": "队长征召",
        "mode_18": "技能征召",
        "mode_22": "排位全选",
        "mode_23": "加速模式",

        # Lobby types
        "lobby_0": "普通",
        "lobby_1": "练习",
        "lobby_2": "锦标赛",
        "lobby_4": "合作对抗电脑",
        "lobby_5": "排位单排/双排",
        "lobby_6": "排位组排",
        "lobby_7": "排位",
        "lobby_8": "1v1中路单挑",
        "lobby_9": "对战电脑",

        # Attributes
        "attr_agi": "敏捷",
        "attr_str": "力量",
        "attr_int": "智力",
        "attr_all": "全能",

        # Attack type
        "atk_melee": "近战",
        "atk_ranged": "远程",

        # Result symbols
        "result_win": "✅ 胜",
        "result_lose": "❌ 负",
    },

    "en": {
        # Error messages
        "api_fail": "API request failed: HTTP",
        "not_found": "Player not found or data unavailable",
        "rate_limit": "Rate limit exceeded, please try again later",
        "network_error": "Network error:",
        "no_recent": "No recent matches found",
        "no_matches": "No matches found",
        "no_heroes": "No hero stats found",
        "no_peers": "No peer records found",
        "unknown_cmd": "Unknown command:",
        "available_cmds": "Available commands:",

        # Search
        "search_no_result": "No players found matching \"{query}\"",
        "search_header": "Search results for \"{query}\" ({count} found):",
        "search_col_id": "Account ID",
        "search_col_name": "Player Name",
        "search_col_last": "Last Match",
        "search_col_sim": "Similarity",

        # Player
        "player_header": "Player Profile",
        "player_name": "Name:",
        "player_account_id": "Account ID:",
        "player_steam_id": "Steam ID:",
        "player_rank": "Rank:",
        "player_leaderboard": "Leaderboard:",
        "player_mmr": "Est. MMR:",
        "player_games": "Total Games:",
        "player_wl": "W/L:",
        "player_winrate": "Win Rate:",
        "player_steam_url": "Steam:",

        # WL
        "wl_header": "Win/Loss Stats",
        "wl_wins": "Wins:",
        "wl_losses": "Losses:",
        "wl_total": "Total:",
        "wl_winrate": "Win Rate:",
        "wl_filter_days": "last {days} days",
        "wl_filter_hero": "hero:{hero}",
        "wl_filter_lobby": "lobby:{lobby}",

        # Recent
        "recent_header": "Recent {count} Matches:",
        "recent_col_hero": "Hero",
        "recent_col_result": "Result",
        "recent_col_gpm": "GPM",
        "recent_col_xpm": "XPM",
        "recent_col_duration": "Duration",
        "recent_col_date": "Date",
        "recent_summary": "Last {total}: {wins}W {losses}L (Win Rate {wr:.1f}%)",

        # Matches
        "matches_header": "Match History ({count} matches):",
        "matches_col_id": "Match ID",
        "matches_summary": "Total {total}: {wins}W {losses}L (Win Rate {wr:.1f}%)",

        # Heroes
        "heroes_header": "Hero Stats (Top {limit}):",
        "heroes_col_hero": "Hero",
        "heroes_col_games": "Games",
        "heroes_col_wins": "Wins",
        "heroes_col_winrate": "Win Rate",
        "heroes_col_last": "Last Played",

        # Match detail
        "match_header": "Match Detail - Match ID:",
        "match_mode": "Mode",
        "match_duration": "Duration",
        "match_date": "Date",
        "match_score": "Score",
        "match_result_radiant": "Radiant Victory",
        "match_result_dire": "Dire Victory",
        "match_team_radiant": "Radiant",
        "match_team_dire": "Dire",
        "match_col_player": "Player",
        "match_col_damage": "Damage",
        "match_col_lh": "LH",
        "match_col_level": "Lvl",
        "match_anonymous": "Anonymous",

        # Peers
        "peers_header": "Frequent Teammates (Top {limit}):",
        "peers_col_name": "Player",
        "peers_col_games": "Together",
        "peers_col_wins": "Wins",
        "peers_col_winrate": "Win Rate",
        "peers_col_last": "Last Played",

        # Hero list
        "herolist_header": "Dota 2 Hero List ({count} heroes):",
        "herolist_col_id": "ID",
        "herolist_col_name": "Name",
        "herolist_col_attr": "Attribute",
        "herolist_col_atk": "Attack",
        "herolist_col_roles": "Roles",

        # Hero stats
        "herostats_header": "Hero Statistics:",
        "herostats_col_id": "ID",
        "herostats_col_hero": "Hero",
        "herostats_col_turbo_picks": "Turbo Picks",
        "herostats_col_turbo_wins": "Turbo Wins",
        "herostats_col_turbo_wr": "Turbo WR",

        # Refresh
        "refresh_ok": "Refresh request submitted (account_id: {aid})",
        "refresh_resp": "Response:",

        # Usage
        "usage_search": "Usage: python dota2_query.py search <player_name>",
        "usage_player": "Usage: python dota2_query.py player <account_id>",
        "usage_wl": "Usage: python dota2_query.py wl <account_id> [--days N] [--hero_id N] [--lobby_type N]",
        "usage_recent": "Usage: python dota2_query.py recent <account_id>",
        "usage_matches": "Usage: python dota2_query.py matches <account_id> [--limit N] [--hero_id N] [--days N]",
        "usage_heroes": "Usage: python dota2_query.py heroes <account_id> [--limit N]",
        "usage_match": "Usage: python dota2_query.py match <match_id>",
        "usage_peers": "Usage: python dota2_query.py peers <account_id> [--limit N]",

        # Common labels
        "win": "W",
        "lose": "L",
        "unknown": "Unknown",
        "uncalibrated": "Uncalibrated",
        "n_a": "N/A",

        # Time ago
        "minutes_ago": "{n} minutes ago",
        "hours_ago": "{n} hours ago",
        "days_ago": "{n} days ago",
        "months_ago": "{n} months ago",
        "years_ago": "{n} years ago",

        # Rank tiers
        "rank_1": "Herald",
        "rank_2": "Guardian",
        "rank_3": "Crusader",
        "rank_4": "Archon",
        "rank_5": "Legend",
        "rank_6": "Ancient",
        "rank_7": "Divine",
        "rank_8": "Immortal",
        "rank_unknown": "Unknown({tier})",

        # Game modes
        "mode_0": "Unknown",
        "mode_1": "All Pick",
        "mode_2": "Captain's Mode",
        "mode_3": "Random Draft",
        "mode_4": "Single Draft",
        "mode_5": "All Random",
        "mode_12": "Least Played",
        "mode_15": "Custom Game",
        "mode_16": "Captain's Draft",
        "mode_18": "Ability Draft",
        "mode_22": "All Pick Ranked",
        "mode_23": "Turbo",

        # Lobby types
        "lobby_0": "Normal",
        "lobby_1": "Practice",
        "lobby_2": "Tournament",
        "lobby_4": "Co-op vs Bots",
        "lobby_5": "Ranked Solo/Duo",
        "lobby_6": "Ranked Party",
        "lobby_7": "Ranked",
        "lobby_8": "1v1 Mid",
        "lobby_9": "Bot Match",

        # Attributes
        "attr_agi": "Agility",
        "attr_str": "Strength",
        "attr_int": "Intelligence",
        "attr_all": "Universal",

        # Attack type
        "atk_melee": "Melee",
        "atk_ranged": "Ranged",

        # Result symbols
        "result_win": "W",
        "result_lose": "L",
    }
}

# Global language, set during startup
LANG = "zh"


def t(key, **kwargs):
    """Look up a translated string by key, with optional format args."""
    s = T[LANG].get(key, T["zh"].get(key, key))
    if kwargs:
        return s.format(**kwargs)
    return s


def get_rank_name(tier):
    """Get localized rank tier name."""
    name_key = f"rank_{tier}"
    if name_key in T[LANG]:
        return T[LANG][name_key]
    return t("rank_unknown", tier=tier)


def get_mode_name(mode_id):
    """Get localized game mode name."""
    key = f"mode_{mode_id}"
    return t(key) if key in T[LANG] else str(mode_id)


def get_lobby_name(lobby_id):
    """Get localized lobby type name."""
    key = f"lobby_{lobby_id}"
    return t(key) if key in T[LANG] else str(lobby_id)


def get_attr_name(attr):
    """Get localized attribute name."""
    key = f"attr_{attr}"
    return t(key) if key in T[LANG] else attr


def get_atk_name(atk_type):
    """Get localized attack type name."""
    if atk_type == "Melee":
        return t("atk_melee")
    return t("atk_ranged")


# ──────────────────────────────────────────────
#  API helpers
# ──────────────────────────────────────────────

_hero_cache = None


def api_get(endpoint, params=None):
    """Send GET request to OpenDota API."""
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
        print(f"{t('api_fail')} {e.code}", file=sys.stderr)
        if e.code == 404:
            print(f"   {t('not_found')}", file=sys.stderr)
        elif e.code == 429:
            print(f"   {t('rate_limit')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"{t('network_error')} {e.reason}", file=sys.stderr)
        sys.exit(1)


def api_post(endpoint):
    """Send POST request to OpenDota API."""
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method="POST", headers={"User-Agent": "Dota2StatsSkill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"{t('network_error')} {e}", file=sys.stderr)
        sys.exit(1)


def get_hero_map():
    """Get hero ID → localized_name mapping (cached)."""
    global _hero_cache
    if _hero_cache is None:
        heroes = api_get("/heroes")
        _hero_cache = {h["id"]: h["localized_name"] for h in heroes}
    return _hero_cache


def format_duration(seconds):
    """Convert seconds to m:ss format."""
    return f"{seconds // 60}:{seconds % 60:02d}"


def format_time(unix_ts):
    """Convert Unix timestamp to readable date string (UTC+8)."""
    if not unix_ts:
        return t("unknown")
    dt = datetime.fromtimestamp(unix_ts, tz=timezone(timedelta(hours=8)))
    return dt.strftime("%Y-%m-%d %H:%M")


def format_time_ago(unix_ts):
    """Convert Unix timestamp to relative time string."""
    if not unix_ts:
        return t("unknown")
    now = time.time()
    diff = now - unix_ts
    if diff < 3600:
        return t("minutes_ago", n=int(diff / 60))
    elif diff < 86400:
        return t("hours_ago", n=int(diff / 3600))
    elif diff < 2592000:
        return t("days_ago", n=int(diff / 86400))
    elif diff < 31536000:
        return t("months_ago", n=int(diff / 2592000))
    else:
        return t("years_ago", n=int(diff / 31536000))


def is_win(player_slot, radiant_win):
    """Determine if the player won based on slot and radiant_win."""
    is_radiant = player_slot < 128
    return (is_radiant and radiant_win) or (not is_radiant and not radiant_win)


def decode_rank_tier(rank_tier):
    """Decode rank_tier integer to human-readable string with stars."""
    if not rank_tier:
        return t("uncalibrated")
    tier = rank_tier // 10
    stars = rank_tier % 10
    name = get_rank_name(tier)
    if tier == 8:
        return name
    return f"{name} {'*' * stars}" if stars else name


# ──────────────────────────────────────────────
#  Command handlers
# ──────────────────────────────────────────────

def cmd_search(args):
    """Search for players by name."""
    if not args:
        print(t("usage_search"))
        sys.exit(1)

    query = " ".join(args)
    results = api_get("/search", {"q": query})

    if not results:
        print(t("search_no_result", query=query))
        return

    print(f"\n{t('search_header', query=query, count=len(results))}\n")
    print(f"{t('search_col_id'):<15} {t('search_col_name'):<25} {t('search_col_last'):<20} {t('search_col_sim')}")
    print("-" * 75)
    for p in results[:15]:
        last_match = p.get("last_match_time", t("unknown"))
        if last_match and last_match != t("unknown"):
            last_match = last_match[:10]
        sim = f"{p.get('similarity', 0):.2f}"
        print(f"{p['account_id']:<15} {p.get('personaname', t('unknown')):<25} {last_match:<20} {sim}")


def cmd_player(args):
    """Get player profile info."""
    if not args:
        print(t("usage_player"))
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
    print(f"  {t('player_header')}")
    print(f"{'='*50}")
    print(f"  {t('player_name'):<12} {profile.get('personaname', t('unknown'))}")
    print(f"  {t('player_account_id'):<12} {profile.get('account_id', account_id)}")
    print(f"  {t('player_steam_id'):<12} {profile.get('steamid', t('unknown'))}")
    print(f"  {t('player_rank'):<12} {decode_rank_tier(rank_tier)}")
    if leaderboard_rank:
        print(f"  {t('player_leaderboard'):<12} #{leaderboard_rank}")
    if mmr:
        print(f"  {t('player_mmr'):<12} {mmr}")
    print(f"  {t('player_games'):<12} {total}")
    print(f"  {t('player_wl'):<12} {wl['win']}{t('win')} / {wl['lose']}{t('lose')}")
    print(f"  {t('player_winrate'):<12} {winrate:.1f}%")
    print(f"  {t('player_steam_url'):<12} {profile.get('profileurl', '-')}")
    print(f"{'='*50}")


def cmd_wl(args):
    """Get win/loss stats."""
    if not args:
        print(t("usage_wl"))
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
        filters.append(t("wl_filter_days", days=params["date"]))
    if "hero_id" in params:
        hero_map = get_hero_map()
        hero_name = hero_map.get(int(params["hero_id"]), f"ID:{params['hero_id']}")
        filters.append(t("wl_filter_hero", hero=hero_name))
    if "lobby_type" in params:
        lt = get_lobby_name(int(params["lobby_type"]))
        filters.append(t("wl_filter_lobby", lobby=lt))

    filter_str = f"（{', '.join(filters)}）" if filters else ""

    print(f"\n  {t('wl_header')}{filter_str}")
    print(f"  {t('wl_wins')} {wl['win']}")
    print(f"  {t('wl_losses')} {wl['lose']}")
    print(f"  {t('wl_total')} {total}")
    print(f"  {t('wl_winrate')} {winrate:.1f}%")


def cmd_recent(args):
    """Get recent matches."""
    if not args:
        print(t("usage_recent"))
        sys.exit(1)

    account_id = args[0]
    hero_map = get_hero_map()
    matches = api_get(f"/players/{account_id}/recentMatches")

    if not matches:
        print(t("no_recent"))
        return

    print(f"\n  {t('recent_header', count=len(matches))}\n")
    print(f"  {t('recent_col_hero'):<16} {t('recent_col_result'):<6} {'K/D/A':<10} {t('recent_col_gpm'):<6} {t('recent_col_xpm'):<6} {t('recent_col_duration'):<8} {t('recent_col_date')}")
    print("  " + "-" * 78)

    wins = 0
    for m in matches:
        hero = hero_map.get(m.get("hero_id", 0), t("unknown"))
        won = is_win(m.get("player_slot", 0), m.get("radiant_win"))
        if won:
            wins += 1
        result = t("result_win") if won else t("result_lose")
        kda = f"{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}"
        gpm = str(m.get("gold_per_min", 0))
        xpm = str(m.get("xp_per_min", 0))
        duration = format_duration(m.get("duration", 0))
        date = format_time(m.get("start_time"))

        print(f"  {hero:<16} {result:<6} {kda:<10} {gpm:<6} {xpm:<6} {duration:<8} {date}")

    total = len(matches)
    print(f"\n  {t('recent_summary', total=total, wins=wins, losses=total - wins, wr=wins/total*100)}")


def cmd_matches(args):
    """Get match history with pagination and filters."""
    if not args:
        print(t("usage_matches"))
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
        print(t("no_matches"))
        return

    print(f"\n  {t('matches_header', count=len(matches))}\n")
    print(f"  {t('matches_col_id'):<14} {t('recent_col_hero'):<16} {t('recent_col_result'):<6} {'K/D/A':<10} {t('recent_col_duration'):<8} {t('recent_col_date')}")
    print("  " + "-" * 78)

    wins = 0
    for m in matches:
        hero = hero_map.get(m.get("hero_id", 0), t("unknown"))
        won = is_win(m.get("player_slot", 0), m.get("radiant_win"))
        if won:
            wins += 1
        result = t("result_win") if won else t("result_lose")
        kda = f"{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}"
        duration = format_duration(m.get("duration", 0))
        date = format_time(m.get("start_time"))

        print(f"  {str(m.get('match_id', '')):<14} {hero:<16} {result:<6} {kda:<10} {duration:<8} {date}")

    total = len(matches)
    print(f"\n  {t('matches_summary', total=total, wins=wins, losses=total - wins, wr=wins/total*100)}")


def cmd_heroes(args):
    """Get hero usage stats for a player."""
    if not args:
        print(t("usage_heroes"))
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

    hero_stats = [h for h in hero_stats if h.get("games", 0) > 0]
    hero_stats.sort(key=lambda x: x.get("games", 0), reverse=True)
    hero_stats = hero_stats[:limit]

    if not hero_stats:
        print(t("no_heroes"))
        return

    print(f"\n  {t('heroes_header', limit=min(limit, len(hero_stats)))}\n")
    print(f"  {t('heroes_col_hero'):<18} {t('heroes_col_games'):<8} {t('heroes_col_wins'):<8} {t('heroes_col_winrate'):<10} {t('heroes_col_last')}")
    print("  " + "-" * 65)

    for h in hero_stats:
        hero = hero_map.get(h.get("hero_id", 0), f"ID:{h.get('hero_id', '?')}")
        games = h.get("games", 0)
        win = h.get("win", 0)
        winrate = f"{win / games * 100:.1f}%" if games > 0 else t("n_a")
        last_played = format_time_ago(h.get("last_played"))

        print(f"  {hero:<18} {games:<8} {win:<8} {winrate:<10} {last_played}")


def cmd_match(args):
    """Get single match details."""
    if not args:
        print(t("usage_match"))
        sys.exit(1)

    match_id = args[0]
    hero_map = get_hero_map()
    data = api_get(f"/matches/{match_id}")

    radiant_win = data.get("radiant_win")
    duration = format_duration(data.get("duration", 0))
    start_time = format_time(data.get("start_time"))
    game_mode = get_mode_name(data.get("game_mode", 0))
    r_score = data.get("radiant_score", 0)
    d_score = data.get("dire_score", 0)

    print(f"\n{'='*80}")
    print(f"  {t('match_header')} {match_id}")
    print(f"{'='*80}")
    print(f"  {t('match_mode')}: {game_mode}   |   {t('match_duration')}: {duration}   |   {t('match_date')}: {start_time}")
    print(f"  {t('match_score')}: {t('match_team_radiant')} {r_score} - {d_score} {t('match_team_dire')}   |   {t('match_result_radiant') if radiant_win else t('match_result_dire')}")
    print()

    players = data.get("players", [])
    radiant = [p for p in players if p.get("player_slot", 128) < 128]
    dire = [p for p in players if p.get("player_slot", 0) >= 128]

    def print_team(team_name, team_players):
        print(f"  {'─'*38} {team_name} {'─'*38}")
        print(f"  {t('match_col_player'):<18} {t('heroes_col_hero'):<16} {'K/D/A':<10} {t('recent_col_gpm'):<6} {t('recent_col_xpm'):<6} {t('match_col_damage'):<8} {t('match_col_lh'):<6} {t('match_col_level')}")
        print(f"  {'-'*76}")
        for p in team_players:
            name = p.get("personaname") or t("match_anonymous")
            if len(name) > 15:
                name = name[:14] + "…"
            hero = hero_map.get(p.get("hero_id", 0), t("unknown"))
            kda = f"{p.get('kills', 0)}/{p.get('deaths', 0)}/{p.get('assists', 0)}"
            gpm = str(p.get("gold_per_min", 0))
            xpm = str(p.get("xp_per_min", 0))
            dmg = str(p.get("hero_damage", 0))
            lh = str(p.get("last_hits", 0))
            lvl = str(p.get("level", 0))
            print(f"  {name:<18} {hero:<16} {kda:<10} {gpm:<6} {xpm:<6} {dmg:<8} {lh:<6} {lvl}")
        print()

    print_team(t("match_team_radiant"), radiant)
    print_team(t("match_team_dire"), dire)


def cmd_peers(args):
    """Get frequent teammates."""
    if not args:
        print(t("usage_peers"))
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
        print(t("no_peers"))
        return

    print(f"\n  {t('peers_header', limit=min(limit, len(peers)))}\n")
    print(f"  {t('peers_col_name'):<20} {t('peers_col_games'):<10} {t('peers_col_wins'):<10} {t('peers_col_winrate'):<10} {t('peers_col_last')}")
    print("  " + "-" * 70)

    for p in peers:
        name = p.get("personaname") or t("match_anonymous")
        if len(name) > 17:
            name = name[:16] + "…"
        games = p.get("with_games", 0)
        win = p.get("with_win", 0)
        winrate = f"{win / games * 100:.1f}%" if games > 0 else t("n_a")
        last = format_time_ago(p.get("last_played"))

        print(f"  {name:<20} {games:<10} {win:<10} {winrate:<10} {last}")


def cmd_hero_list(args):
    """Get full hero list."""
    heroes = api_get("/heroes")
    heroes.sort(key=lambda x: x["id"])

    print(f"\n{t('herolist_header', count=len(heroes))}\n")
    print(f"  {t('herolist_col_id'):<6} {t('herolist_col_name'):<28} {t('herolist_col_attr'):<8} {t('herolist_col_atk'):<8} {t('herolist_col_roles')}")
    print("  " + "-" * 80)

    for h in heroes:
        roles = ", ".join(h.get("roles", []))
        attr = get_attr_name(h.get("primary_attr", ""))
        atk = get_atk_name(h.get("attack_type", ""))
        print(f"  {h['id']:<6} {h['localized_name']:<28} {attr:<8} {atk:<8} {roles}")


def cmd_hero_stats(args):
    """Get global hero statistics."""
    heroes = api_get("/heroStats")
    heroes.sort(key=lambda x: x.get("id", 0))

    print(f"\n{t('herostats_header')}\n")
    print(f"  {t('herostats_col_id'):<5} {t('herostats_col_hero'):<24} {t('herostats_col_turbo_picks'):<12} {t('herostats_col_turbo_wins'):<12} {t('herostats_col_turbo_wr')}")
    print("  " + "-" * 65)

    for h in heroes:
        tp = h.get("turbo_picks", 0)
        tw = h.get("turbo_wins", 0)
        wr = f"{tw / tp * 100:.1f}%" if tp > 0 else t("n_a")
        print(f"  {h.get('id', 0):<5} {h.get('localized_name', t('unknown')):<24} {tp:<12} {tw:<12} {wr}")


def cmd_refresh(args):
    """Refresh player match data."""
    if not args:
        print("用法: python dota2_query.py refresh <account_id>")
        sys.exit(1)

    account_id = args[0]
    result = api_post(f"/players/{account_id}/refresh")
    print(f"  {t('refresh_ok', aid=account_id)}")
    print(f"  {t('refresh_resp')} {json.dumps(result, ensure_ascii=False)}")


# ──────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────

def main():
    global LANG

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Extract --lang from anywhere in args
    args = sys.argv[1:]
    filtered_args = []
    for a in args:
        if a == "--lang" or a == "-l":
            # handled in next iteration
            continue
        if args and len(filtered_args) < len(args):
            idx = args.index(a)
            if idx > 0 and args[idx - 1] in ("--lang", "-l"):
                LANG = a if a in ("zh", "en") else "zh"
                continue
        if a.startswith("--lang="):
            val = a.split("=", 1)[1]
            LANG = val if val in ("zh", "en") else "zh"
            continue
        filtered_args.append(a)

    if not filtered_args:
        print(__doc__)
        sys.exit(1)

    command = filtered_args[0]
    cmd_args = filtered_args[1:]

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
        print(f"{t('unknown_cmd')} {command}")
        print(f"{t('available_cmds')} {', '.join(commands.keys())}")
        sys.exit(1)

    commands[command](cmd_args)


if __name__ == "__main__":
    main()
