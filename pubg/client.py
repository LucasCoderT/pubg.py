import aiohttp
import asyncio
import logging
from pubg import models, errors

logger = logging.getLogger(__name__)


class PubGClient:
    base_url = "https://api.pubgtracker.com/v2"

    valid_regions = ("na", "eu", "as", "oc", "sa", "sea", "krjp")
    seasons = ("2017-pre1", "2017-pre2", "2017-pre3", "2017-pre4", "2017-pre5", "2017-pre6")
    modes = ("solo", "duo", "squad", "solo-fpp", "duo-fpp", "squad-fpp")
    valid_types = ("pc",)

    def __init__(self, api_key, *, session=None, loop=None):
        """

        The main client for making requests

        Parameters
        ----------
        api_key : str
            The API Key
        session : `class:ClientSession`
            the aiohttp ClientSession obj for making requests. Will create one if none provided
        loop : `class:AbstractEventLoop`
            The loop for the program to attach too
        """
        self.api_key = api_key
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.cooldown = asyncio.Event()
        self.cooldown.set()
        self.last_header = None
        self.headers = {"TRN-Api-Key": self.api_key}

    @asyncio.coroutine
    def __http(self, endpoint, params=None, headers=None):
        if headers is None:
            headers = self.headers
        yield from self.cooldown.wait()
        if self.last_header is not None:
            if int(self.last_header['X-RateLimit-Remaining-minute']) == 0:
                self.cooldown.set()
                yield from asyncio.sleep(2)
                self.cooldown.clear()
        try:
            if params is None:
                session = yield from self.session.get(endpoint, headers=headers)
            else:
                session = yield from self.session.get(endpoint, params=params, headers=headers)
            if session.status == 200:
                response_data = yield from session.json()
                if "code" in response_data:
                    raise errors.BaseException(response_data)
                self.last_header = dict(session.headers)
                return response_data
            elif session.status != 429:
                response_data = yield from session.json()
                self.cooldown.clear()
                yield from asyncio.sleep(2)
                self.cooldown.set()
                return response_data
        except:
            pass
        finally:
            session.close()

    @asyncio.coroutine
    def get_user(self, nickname, season=None, mode=None, region=None, type="pc"):
        """|coro|

        Parameters
        ----------
        nickname : str
            The nickname to search/retrieve
        season : Optional[str]
            The season to filter by
        mode : Optional[str]
            the mode to filter by
        region : Optional[str]
            the region to filter by
        type :
            the platform type. This exists in case more platforms become available later on

        Returns
        -------
        :class:`User`
            if any found otherwise returns ``None``

        """
        if season not in self.seasons and season is not None:
            raise errors.BadArgument(season)
        if mode not in self.modes and mode is not None:
            raise errors.BadArgument(mode)
        if region not in self.valid_regions and region is not None:
            raise errors.BadArgument(region)
        if type not in self.valid_types and type is not None:
            raise errors.BadArgument(type)
        params = {}
        for pub_filter, data in {"season": season, "mode": mode, "region": region}.items():
            if data is not None:
                params[pub_filter] = data
        endpoint = "{0}/profile/{1}/{2}".format(self.base_url, type, nickname)
        response = yield from self.__http(endpoint, params)
        if response is not None:
            return models.User(**response)

    @asyncio.coroutine
    def get_nickname_by_steam(self, steam_id, type="steam"):
        """|coro|

        Parameters
        ----------
        steam_id : str
            the steamID to query
        type : Optional[str]
            the platform type. This exists in case more platforms become available later on


        Returns
        -------
        str
            The nickname if any found

        """
        if type not in self.valid_types:
            raise errors.BadArgument(type)
        endpoint = "{0}/search/{1}".format(self.base_url, type)
        response = yield from self.__http(endpoint, {"steamId": steam_id})
        if response is not None:
            return response

    @asyncio.coroutine
    def get_match_history(self, account_id, type="pc"):
        """|coro|

        Parameters
        ----------
        account_id : Union[:class:`User`,str]
            account to query for match history, can be a type :class:`User` or str
        type : Optional[str]
            the platform type. This exists in case more platforms become available later on

        Returns
        -------
        list[:class:`Match`]

        """
        if isinstance(account_id, models.User):
            account_id = account_id.id
        endpoint = "{0}/matches/{1}/{2}".format(self.base_url, type, account_id)
        response = yield from self.__http(endpoint)
        if response is not None:
            return [models.Match(**data) for data in response]
        else:
            return []

    def __del__(self):
        self.session.close()
