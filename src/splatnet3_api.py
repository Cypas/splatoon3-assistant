# SplatNet3 API module
# Based on reference-project/splatoon3-nso/s3s/splatoon.py (Splatoon class)
"""SplatNet3 GraphQL API wrapper."""

from typing import Optional, Dict, Any

from .nso_auth import NSOAuth, APP_USER_AGENT
from .graphql_utils import gen_graphql_body, GRAPHQL_URL
from .config import Config, default_config
from .http_client import AsyncHttpClient


class SplatNet3API:
    """
    SplatNet3 GraphQL API client (参照 splatoon3-nso Splatoon class)
    
    Usage:
        api = SplatNet3API(g_token, bullet_token)
        battles = await api.get_recent_battles()
    """
    
    def __init__(
        self,
        g_token: str,
        bullet_token: str,
        user_lang: str = "zh-CN",
        user_country: str = "JP",
        config: Optional[Config] = None,
    ):
        self.g_token = g_token
        self.bullet_token = bullet_token
        self.user_lang = user_lang
        self.user_country = user_country
        self.config = config or default_config
        self._client: Optional[AsyncHttpClient] = None
    
    def _get_client(self) -> AsyncHttpClient:
        """Get or create async HTTP client."""
        if self._client is None:
            self._client = AsyncHttpClient(self.config)
        return self._client
    
    def head_bullet(self, force_lang: Optional[str] = None, force_country: Optional[str] = None) -> Dict[str, str]:
        """构建请求 headers（参照 Splatoon.head_bullet()）"""
        if force_lang:
            lang = force_lang
            country = force_country or self.user_country
        else:
            lang = self.user_lang
            country = self.user_country
        
        splatnet3_url = "https://api.lp1.av5ja.srv.nintendo.net"
        
        graphql_head = {
            "Authorization": f"Bearer {self.bullet_token}",
            "Accept-Language": lang,
            "User-Agent": APP_USER_AGENT,
            "X-Web-View-Ver": NSOAuth.get_web_view_ver(),
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": splatnet3_url,
            "X-Requested-With": "com.nintendo.znca",
            "Referer": f"{splatnet3_url}/?lang={lang}&na_country={country}&na_lang={lang}",
            "Accept-Encoding": "gzip, deflate",
        }
        return graphql_head
    
    async def request(
        self,
        data: str,
        force_lang: Optional[str] = None,
        force_country: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """发送 GraphQL 请求（参照 Splatoon.request()）"""
        client = self._get_client()
        
        try:
            headers = self.head_bullet(force_lang, force_country)
            cookies = {"_gtoken": self.g_token}
            
            resp = await client.post(
                GRAPHQL_URL,
                data=data,
                headers=headers,
                cookies=cookies,
            )
            
            if resp.status_code != 200:
                print(f"Request failed with status {resp.status_code}")
                return None
            
            return resp.json()
            
        except Exception as e:
            print(f"Request error: {e}")
            return None
    
    # ============================================================
    # 对战查询方法 (参照 Splatoon class)
    # ============================================================
    
    async def get_recent_battles(self) -> Optional[Dict[str, Any]]:
        """最近对战查询"""
        data = gen_graphql_body("LatestBattleHistoriesQuery")
        return await self.request(data)
    
    async def get_regular_battles(self) -> Optional[Dict[str, Any]]:
        """涂地对战查询"""
        data = gen_graphql_body("RegularBattleHistoriesQuery")
        return await self.request(data)
    
    async def get_bankara_battles(self) -> Optional[Dict[str, Any]]:
        """蛮颓对战查询"""
        data = gen_graphql_body("BankaraBattleHistoriesQuery")
        return await self.request(data)
    
    async def get_x_battles(self) -> Optional[Dict[str, Any]]:
        """X对战查询"""
        data = gen_graphql_body("XBattleHistoriesQuery")
        return await self.request(data)
    
    async def get_event_battles(self) -> Optional[Dict[str, Any]]:
        """活动对战查询"""
        data = gen_graphql_body("EventBattleHistoriesQuery")
        return await self.request(data)
    
    async def get_private_battles(self) -> Optional[Dict[str, Any]]:
        """私房对战查询"""
        data = gen_graphql_body("PrivateBattleHistoriesQuery")
        return await self.request(data)
    
    async def get_battle_detail(self, battle_id: str) -> Optional[Dict[str, Any]]:
        """对战详情查询"""
        data = gen_graphql_body("VsHistoryDetailQuery", "vsResultId", battle_id)
        return await self.request(data)
    
    async def get_last_one_battle(self) -> Optional[Dict[str, Any]]:
        """最新一局对战id查询"""
        data = gen_graphql_body("PagerLatestVsDetailQuery")
        return await self.request(data)
    
    # ============================================================
    # 打工查询方法
    # ============================================================
    
    async def get_coops(self) -> Optional[Dict[str, Any]]:
        """打工历史查询"""
        data = gen_graphql_body("CoopHistoryQuery")
        return await self.request(data)
    
    async def get_coop_detail(self, coop_id: str) -> Optional[Dict[str, Any]]:
        """打工详情查询"""
        data = gen_graphql_body("CoopHistoryDetailQuery", "coopHistoryDetailId", coop_id)
        return await self.request(data)
    
    # ============================================================
    # 排名和其他查询
    # ============================================================
    
    async def get_x_ranking(self, region: str = "ATLANTIC") -> Optional[Dict[str, Any]]:
        """X排行榜top1查询"""
        data = gen_graphql_body("XRankingQuery", "region", region)
        return await self.request(data)
    
    async def get_home(self) -> Optional[Dict[str, Any]]:
        """主页数据查询"""
        data = gen_graphql_body("HomeQuery", "naCountry", "JP")
        return await self.request(data)
    
    async def get_history_summary(self) -> Optional[Dict[str, Any]]:
        """历史总览查询"""
        data = gen_graphql_body("HistoryRecordQuery")
        return await self.request(data)
    
    async def get_friends(self) -> Optional[Dict[str, Any]]:
        """好友列表查询"""
        data = gen_graphql_body("FriendListQuery")
        return await self.request(data)
    
    async def get_weapon_records(self) -> Optional[Dict[str, Any]]:
        """武器记录查询"""
        data = gen_graphql_body("WeaponRecordQuery")
        return await self.request(data)
    
    async def get_stage_records(self) -> Optional[Dict[str, Any]]:
        """场地记录查询"""
        data = gen_graphql_body("StageRecordQuery")
        return await self.request(data)
    
    async def get_schedule(self) -> Optional[Dict[str, Any]]:
        """日程表查询"""
        data = gen_graphql_body("StageScheduleQuery")
        return await self.request(data)
    
    async def close(self) -> None:
        """关闭 HTTP client"""
        if self._client:
            await self._client.close()
            self._client = None
