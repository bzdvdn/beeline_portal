from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from abc import ABC
from dataclasses import dataclass

from .utils import parse_datetime_from_miliseconds, parse_datetime


class BaseModel(ABC):
    def from_dict(cls, model_dict: dict) -> BaseModel:
        raise NotImplementedError()

    def to_dict(self, native: bool = False) -> dict:
        raise NotImplementedError()


@dataclass()
class Abonent(BaseModel):
    user_id: str
    phone: str
    forst_name: str
    last_name: str
    extension: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> Abonent:
        return cls(
            model_dict['userId'],
            model_dict['phone'],
            model_dict['firstName'],
            model_dict['last_name'],
            model_dict['extension'],
        )


@dataclass
class Number(BaseModel):
    number_id: str
    phone: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Number':
        return cls(model_dict['numberId'], model_dict['phone'],)


@dataclass
class Subscription(BaseModel):
    subscription_id: str
    target_type: str
    target_id: str
    subscription_type: str
    expires: str
    url: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Subscription':
        return cls(
            model_dict['subscriptionId'],
            model_dict['targetType'],
            model_dict['targetId'],
            model_dict['subscriptionType'],
            model_dict['expires'],
            model_dict['url'],
        )


@dataclass
class IcrNumberResult(BaseModel):
    phone_number: str
    status: str
    error: Optional[dict] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'IcrNumberResult':
        return cls(
            model_dict['phoneNumber'], model_dict['status'], model_dict.get('error'),
        )


@dataclass
class IcrRouteRule(BaseModel):
    inbound_number: str
    extension: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'IcrRouteRule':
        return cls(model_dict['inboundNumber'], model_dict['extension'])


@dataclass
class Answer(BaseModel):
    choies: str
    answer: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Answer':
        return cls(model_dict['choice'], model_dict['answer'],)


@dataclass
class VoiceCampaignSchedule(BaseModel):
    try_quantity: str
    from_hour: str
    to_hour: str
    schedule: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'VoiceCampaignSchedule':
        return cls(
            model_dict['tryQuantity'],
            model_dict['fromHour'],
            model_dict['toHour'],
            model_dict['schedule'],
        )


@dataclass
class DateAndTime(BaseModel):
    date: datetime
    time: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'DateAndTime':
        return cls(parse_datetime(model_dict['date']), model_dict['time'])


@dataclass
class VoiceCampaign(BaseModel):
    name: str
    status: str
    record_id: str
    type_: str
    audio_file: str
    phones: List[str]
    phone_number: str
    schedule: VoiceCampaignSchedule
    from_: DateAndTime
    to_: DateAndTime
    answers: Optional[List[Answer]] = None
    abonent: Optional[Abonent] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'VoiceCampaign':
        return cls(
            model_dict['name'],
            model_dict['status'],
            model_dict['recordId'],
            model_dict['type'],
            model_dict['audioFile'],
            model_dict['phones'],
            model_dict['phoneNumber'],
            VoiceCampaignSchedule.from_dict(model_dict['schedule']),
            DateAndTime.from_dict(model_dict['from']),
            DateAndTime.from_dict(model_dict['to']),
            answers=[Answer.from_dict(r) for r in model_dict['answers']]
            if 'answers' in model_dict
            else None,
            abonent=Abonent.from_dict(model_dict['abonent'])
            if 'abonent' in model_dict
            else None,
        )


@dataclass
class CampaignQuation(BaseModel):
    name: str
    answers: List[Answer]
    audio_file: str
    phones: List[str]
    phone_number: str
