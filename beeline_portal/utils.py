import pytz
from dateutil.parser import parse
from datetime import datetime


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


def parse_datetime(s: str) -> datetime:
    return parse(s).replace(tzinfo=pytz.utc)


def format_datetime(dt: datetime) -> str:
    return dt.astimezone(pytz.utc).strftime(DATETIME_FORMAT)


def format_date(d: datetime) -> str:
    return d.strftime(DATE_FORMAT)


def parse_datetime_from_milliseconds(m: int) -> datetime:
    return datetime.fromtimestamp(m / 1000)


def to_milliseconds(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)
