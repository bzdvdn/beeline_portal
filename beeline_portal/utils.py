import pytz
from typing import Optional
from datetime import datetime


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


def parse_datetime(s: str) -> datetime:
    return datetime.strptime(s, DATETIME_FORMAT).replace(tzinfo=pytz.utc)


def format_datetime(dt: datetime) -> str:
    return dt.astimezone(pytz.utc).strftime(DATETIME_FORMAT)


def format_date(d: datetime) -> str:
    return d.strftime(DATE_FORMAT)


def parse_datetime_from_miliseconds(m: int) -> datetime:
    return datetime.fromtimestamp(m / 1000)

