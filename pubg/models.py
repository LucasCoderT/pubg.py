import datetime


class User:
    """
    Represents a Pubg player

    Attributes
    ----------
    id : str
        account ID
    avatar : str
        url of the avatar
    last_update : :class:`Datetime`
        datetime when account was last updated
    nickname : str
        Current nickname
    platform : str
        Platform code of the player
    tracking_id : str
        The tracking ID of the user
    stats : list[:class:`Stats`]
        List of all the stats for the user

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('accountId')
        self.avatar = kwargs.get('avatar')
        if kwargs.get('lastUpdated') is not None:
            self.last_update = datetime.datetime.strptime(kwargs.get('lastUpdated'), "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.last_update = None
        self.nickname = kwargs.get("nickname")
        self.platform = kwargs.get('platform')
        self.tracking_id = kwargs.get('pubgTrackerId')
        self.stats = [Stats(**data) for data in kwargs.get('stats', {})]

    def __str__(self):
        return self.nickname


class Stats:
    """

    Attributes
    ----------
    mode : str
        Mode of the specific obj
    region : str
        The region of the mode
    season : str
        The season
    stats : dict
        detailed stats view
    """

    def __init__(self, **kwargs):
        self.mode = kwargs.get('mode')
        self.region = kwargs.get('region')
        self.season = kwargs.get('season')
        self.stats = kwargs.get('stats')


class Match:
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __gt__(self, other):
        return self.ratingRank > other.ratingRank

    def __le__(self, other):
        return self.ratingRank < other.ratingRank

    def __eq__(self, other):
        return self.ratingRank == other.ratingRank
