"""Parse flattened `NamedTuple` records from Halo Infinite API responses.

The record format can be useful for dumping to files or databases and is faster
than parsing the entirety of the JSON responses.
"""

from .gamecms_hacs import MedalRecord, parse_medal_metadata
from .profile import User, parse_user, parse_users
from .skill import (
    PlayerSkillRecord,
    PlaylistCsrRecord,
    parse_match_skill,
    parse_playlist_csr,
)
from .stats import (
    MatchCountRecord,
    MatchHistoryRecord,
    MatchInfoRecord,
    PlayerCoreStatsRecord,
    PlayerMedalRecord,
    PlayerServiceRecord,
    TeamCoreStatsRecord,
    parse_match_count,
    parse_match_history,
    parse_match_info,
    parse_player_core_stats,
    parse_player_medals,
    parse_service_record,
    parse_team_core_stats,
)
from .ugc_discovery import AssetRecord, parse_asset

__all__ = [
    "AssetRecord",
    "MatchCountRecord",
    "MatchHistoryRecord",
    "MatchInfoRecord",
    "MedalRecord",
    "PlayerCoreStatsRecord",
    "PlayerMedalRecord",
    "PlayerSkillRecord",
    "PlaylistCsrRecord",
    "PlayerServiceRecord",
    "TeamCoreStatsRecord",
    "User",
    "parse_asset",
    "parse_match_count",
    "parse_match_history",
    "parse_match_info",
    "parse_medal_metadata",
    "parse_player_core_stats",
    "parse_player_medals",
    "parse_match_skill",
    "parse_playlist_csr",
    "parse_service_record",
    "parse_team_core_stats",
    "parse_user",
    "parse_users",
]
