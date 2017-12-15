import datetime


class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('accountId')
        self.avatar = kwargs.get('avatar')
        self.last_update = datetime.datetime.strptime(kwargs.get('lastUpdated', ""), "%Y-%m-%dT%H:%M:%S.%f")
        self.nickname = kwargs.get("nickname")
        self.platform = kwargs.get('platform')
        self.pugbg_tracking_id = kwargs.get('pubgTrackerId')
        self.stats = [Stats(**data) for data in kwargs.get('stats', {})]


class Stats:
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
