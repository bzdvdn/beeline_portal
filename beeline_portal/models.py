from datetime import datetime
from typing import List, Optional
from abc import ABC
from dataclasses import dataclass

from .utils import (
    format_datetime,
    parse_datetime_from_milliseconds,
    parse_datetime,
    format_date,
)


class BaseModel(ABC):
    def from_dict(cls, model_dict: dict) -> 'BaseModel':
        raise NotImplementedError()

    def to_beeline_struct(self) -> dict:
        raise NotImplementedError()


@dataclass()
class Abonent(BaseModel):
    user_id: str
    phone: str
    first_name: str
    last_name: str
    extension: str
    email: Optional[str] = None
    department: Optional[str] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Abonent':
        return cls(
            model_dict['userId'],
            model_dict['phone'],
            model_dict['firstName'],
            model_dict['lastName'],
            model_dict['extension'],
            model_dict.get('email'),
            model_dict.get('department'),
        )

    def to_beeline_struct(self) -> dict:
        struct = {
            'userId': self.user_id,
            'phone': self.phone,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'extension': self.extension,
        }
        if self.email:
            struct['email'] = self.email
        if self.department:
            struct['department'] = self.department
        return struct


@dataclass
class Number(BaseModel):
    number_id: str
    phone: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Number':
        return cls(model_dict['numberId'], model_dict['phone'],)

    def to_beeline_struct(self) -> dict:
        return {'numberId': self.number_id, 'phone': self.phone}


@dataclass
class SubscriptionRequest(BaseModel):
    pattern: str
    expires: int
    subscription_type: str
    url: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'SubscriptionRequest':
        return cls(
            model_dict['pattern'],
            model_dict['expires'],
            model_dict['subscriptionType'],
            model_dict['url'],
        )

    def to_beeline_struct(self) -> dict:
        return {
            'pattern': self.pattern,
            'expires': self.expires,
            'subscriptionType': self.subscription_type,
            'url': self.url,
        }


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

    def to_beeline_struct(self) -> dict:
        return {
            'subscriptionId': self.subscription_id,
            'targetType': self.target_type,
            'targetId': self.target_id,
            'subscriptionType': self.subscription_type,
            'expires': self.expires,
            'url': self.url,
        }


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

    def to_beeline_struct(self) -> dict:
        return {
            'phoneNumber': self.phone_number,
            'status': self.status,
            'status': self.error,
        }


@dataclass
class IcrRouteRule(BaseModel):
    inbound_number: str
    extension: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'IcrRouteRule':
        return cls(model_dict['inboundNumber'], model_dict['extension'])

    def to_beeline_struct(self) -> dict:
        return {
            'inboundNumber': self.inbound_number,
            'extension': self.extension,
        }


@dataclass
class Answer(BaseModel):
    choice: str
    answer: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Answer':
        return cls(model_dict['choice'], model_dict['answer'],)

    def to_beeline_struct(self) -> dict:
        return {
            'choice': self.choice,
            'answer': self.answer,
        }


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

    def to_beeline_struct(self) -> dict:
        return {
            'tryQuantity': self.try_quantity,
            'fromHour': self.from_hour,
            'toHour': self.to_hour,
            'schedule': self.schedule,
        }


@dataclass
class DateAndTime(BaseModel):
    date: datetime
    time: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'DateAndTime':
        return cls(parse_datetime(model_dict['date']), model_dict['time'])

    def to_beeline_struct(self) -> dict:
        return {
            'date': format_date(self.date),
            'time': self.time,
        }


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

    def to_beeline_struct(self) -> dict:
        struct = {
            'name': self.name,
            'status': self.status,
            'recordId': self.record_id,
            'type': self.type_,
            'audioFile': self.audio_file,
            'phones': self.phones,
            'phoneNumber': self.phone_number,
            'schedule': self.schedule.to_beeline_struct(),
            'from': self.from_.to_beeline_struct(),
            'to': self.to_.to_beeline_struct(),
        }
        if self.answers:
            struct['answers'] = [a.to_beeline_struct() for a in self.answers]
        if self.abonent:
            struct['abonent'] = self.abonent.to_beeline_struct()
        return struct


@dataclass
class VoiceCampaignQuestion(BaseModel):
    name: str
    answers: List[Answer]
    audio_file: str
    phones: List[str]
    phone_number: str
    schedule: VoiceCampaignSchedule
    from_: DateAndTime
    to_: DateAndTime

    def to_beeline_struct(self) -> dict:
        return {
            'name': self.name,
            'answers': [a.to_beeline_struct() for a in self.answers],
            'phones': self.phones,
            'phoneNumber': self.phone_number,
            'schedule': self.schedule.to_beeline_struct(),
            'from': self.from_.to_beeline_struct(),
            'to': self.to_.to_beeline_struct(),
        }


@dataclass
class VoiceCampaignAnswer(BaseModel):
    answer: str
    answer_code: str
    amount: int

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'VoiceCampaignAnswer':
        return cls(model_dict['answer'], model_dict['answerCode'], model_dict['amount'])

    def to_beeline_struct(self) -> dict:
        return {
            'answer': self.answer,
            'answerCode': self.answer_code,
            'amount': self.amount,
        }


@dataclass
class VoiceCampaignInfoNumber(BaseModel):
    phone: str
    result: str
    attempts: str
    last_attempt_date: datetime
    is_done: bool
    answer: str
    answer_code: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'VoiceCampaignInfoNumber':
        return cls(
            model_dict['phone'],
            model_dict['result'],
            model_dict['attempts'],
            model_dict['lastAttemptDate'],
            model_dict['isDone'],
            model_dict['answer'],
            model_dict['answerCode'],
        )

    def to_beeline_struct(self) -> dict:
        return {
            'phone': self.phone,
            'result': self.result,
            'attempts': self.attempts,
            'lastAttemptDate': self.last_attempt_date,
            'isDone': self.is_done,
            'answer': self.answer,
            'answerCode': self.answer_code,
        }


@dataclass
class VoiceCampaignInfoReport(BaseModel):
    campaign_name: str
    report_date: datetime
    client: str
    state: str
    start_date: datetime
    finish_date: datetime
    total: int
    processed: int
    success: int
    abandoned: int
    busy_or_no_answer: int
    number_list: List[VoiceCampaignInfoNumber]
    abonent: Optional[Abonent] = None
    answer_list: Optional[List[VoiceCampaignAnswer]] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'VoiceCampaignInfoReport':
        return cls(
            model_dict['campaignName'],
            parse_datetime(model_dict['reportDate']),
            model_dict['client'],
            model_dict['state'],
            parse_datetime(model_dict['startDate']),
            parse_datetime(model_dict['finishDate']),
            model_dict['total'],
            model_dict['processed'],
            model_dict['success'],
            model_dict['abandoned'],
            model_dict['busyOrNoAnswer'],
            [VoiceCampaignInfoNumber.from_dict(n) for n in model_dict['numberList']],
            Abonent.from_dict(model_dict['abonent'])
            if model_dict.get('abonent')
            else None,
            [VoiceCampaignAnswer.from_dict(a) for a in model_dict['answerList']]
            if model_dict.get('answerList')
            else None,
        )

    def to_beeline_struct(self) -> dict:
        struct = {
            'campaignName': self.campaign_name,
            'reportDate': format_date(self.report_date),
            'client': self.client,
            'state': self.state,
            'startDate': format_date(self.start_date),
            'finishDate': format_date(self.finish_date),
            'total': self.total,
            'processed': self.processed,
            'abandoned': self.abandoned,
            'busyOrNoAnswer': self.busy_or_no_answer,
            'numberList': [n.to_beeline_struct() for n in self.number_list],
        }
        if self.abonent:
            struct['abonent'] = self.abonent.to_beeline_struct()
        if self.answer_list:
            struct['answerList'] = [a.to_beeline_struct() for a in self.answer_list]
        return struct


@dataclass
class StatRecord(BaseModel):
    start_date: datetime
    abonent: Abonent
    direction: str
    status: str
    phone: str
    department: Optional[str] = None
    call_forward: Optional[str] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'StatRecord':
        return cls(
            parse_datetime_from_milliseconds(model_dict['startDate']),
            Abonent.from_dict(model_dict['abonent']),
            model_dict['direction'],
            model_dict['status'],
            model_dict['phone'],
            model_dict.get('department'),
            model_dict.get('callForward'),
        )

    def to_dict(self) -> dict:
        struct = {
            'startDate': format_datetime(self.start_date),
            'abonent': self.abonent.to_beeline_struct(),
            'direction': self.direction,
            'status': self.status,
            'phone': self.phone,
        }
        if self.department:
            struct['department'] = self.department
        if self.call_forward:
            struct['callForward'] = self.call_forward
        return struct


@dataclass
class StatRecordV2(BaseModel):
    start_date: datetime
    abonent: Abonent
    direction: str
    status: str
    phone_to: Optional[str] = None
    phone_from: Optional[str] = None
    department: Optional[str] = None
    call_forward: Optional[str] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'StatRecordV2':
        return cls(
            parse_datetime_from_milliseconds(model_dict['startDate']),
            Abonent.from_dict(model_dict['abonent']),
            model_dict['direction'],
            model_dict['status'],
            model_dict.get('phone_to'),
            model_dict.get('phone_from'),
            model_dict.get('department'),
            model_dict.get('callForward'),
        )

    def to_dict(self) -> dict:
        struct = {
            'startDate': format_datetime(self.start_date),
            'abonent': self.abonent.to_beeline_struct(),
            'direction': self.direction,
            'status': self.status,
        }
        if self.phone_from:
            struct['phone_from'] = self.phone_from
        if self.phone_to:
            struct['phone_to'] = self.phone_to
        if self.department:
            struct['department'] = self.department
        if self.call_forward:
            struct['callForward'] = self.call_forward
        return struct


@dataclass
class Cfb(BaseModel):
    forward_all_calls_phone: Optional[str] = None
    forward_busy_phone: Optional[str] = None
    forward_unavailable_phone: Optional[str] = None
    forward_not_answer_phone: Optional[str] = None
    forward_not_answer_timeout: Optional[str] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'Cfb':
        return cls(
            model_dict.get('forwardAllCallsPhone'),
            model_dict.get('forwardBusyPhone'),
            model_dict.get('forwardUnavailablePhone'),
            model_dict.get('forwardNotAnswerPhone'),
            model_dict.get('forwardNotAnswerTimeout'),
        )

    def to_beeline_struct(self) -> dict:
        struct = {}
        if self.forward_all_calls_phone:
            struct['forwardAllCallsPhone'] = self.forward_all_calls_phone
        if self.forward_busy_phone:
            struct['forwardBusyPhone'] = self.forward_busy_phone
        if self.forward_unavailable_phone:
            struct['forwardUnavailablePhone'] = self.forward_unavailable_phone
        if self.forward_not_answer_phone:
            struct['forwardNotAnswerPhone'] = self.forward_not_answer_phone
        if self.forward_not_answer_timeout:
            struct['forwardNotAnswerTimeout'] = self.forward_not_answer_timeout
        return struct


@dataclass
class CfbResponse(BaseModel):
    status: str
    cfb: Cfb

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'CfbResponse':
        return cls(model_dict['status'], Cfb.from_dict(model_dict['cfb']))

    def to_beeline_struct(self) -> dict:
        return {'status': self.status, 'cfb': self.cfb.to_beeline_struct()}


@dataclass
class BaseRule(BaseModel):
    name: str
    forward_to_phone: str
    schedule: str
    phone_list: List[str]
    id_: Optional[str] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'BaseRule':
        return cls(
            model_dict['name'],
            model_dict['forwardToPhone'],
            model_dict['schedule'],
            model_dict['phoneList'],
            model_dict.get('id'),
        )

    def to_beeline_struct(self) -> dict:
        struct = {
            'name': self.name,
            'forwardToPhone': self.forward_to_phone,
            'schedule': self.schedule,
            'phoneList': self.phone_list,
        }
        if self.id_:
            struct['id'] = self.id_
        return struct


@dataclass
class CfsRule(BaseRule):
    @classmethod
    def from_dict(cls, model_dict: dict) -> 'CfsRule':
        return super(CfsRule, cls).from_dict(model_dict)  # type: ignore


@dataclass
class CfsStatusResponse(BaseModel):
    is_cfs_service_enabled: bool
    rule_list: Optional[List[CfsRule]] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'CfsStatusResponse':
        return cls(
            model_dict['isCfsServiceEnabled'],
            [CfsRule.from_dict(rule) for rule in model_dict['ruleList']]
            if 'ruleList' in model_dict
            else None,
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {'isCfsServiceEnabled': self.is_cfs_service_enabled}
        if self.rule_list:
            struct['ruleList'] = [r.to_beeline_struct() for r in self.rule_list]
        return struct


@dataclass
class BwlRule(BaseRule):
    @classmethod
    def from_dict(cls, model_dict: dict) -> 'BwlRule':
        return super(BwlRule, cls).from_dict(model_dict)  # type: ignore


@dataclass
class BwlStatusResponse(BaseModel):
    status: str
    black_list: Optional[List[BwlRule]] = None
    white_list: Optional[List[BwlRule]] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'BwlStatusResponse':
        return cls(
            model_dict['status'],
            [BwlRule.from_dict(rule) for rule in model_dict['blackList']]
            if 'blackList' in model_dict
            else None,
            [BwlRule.from_dict(rule) for rule in model_dict['whiteList']]
            if 'whiteList' in model_dict
            else None,
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {'status': self.status}
        if self.black_list:
            struct['blackList'] = [r.to_beeline_struct() for r in self.black_list]
        if self.white_list:
            struct['whiteList'] = [r.to_beeline_struct() for r in self.white_list]
        return struct


@dataclass
class CallRecord(BaseModel):
    id_: str
    external_id: str
    call_id: str
    phone: str
    direction: str
    date: datetime
    duration: int
    file_size: int
    comment: str
    abonent: Abonent

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'CallRecord':
        return cls(
            model_dict['id'],
            model_dict['externalId'],
            model_dict['callId'],
            model_dict['phone'],
            model_dict['direction'],
            parse_datetime(model_dict['date']),
            model_dict['duration'],
            model_dict['fileSize'],
            model_dict['comment'],
            Abonent.from_dict(model_dict['abonent']),
        )

    def to_beeline_struct(self) -> dict:
        return {
            'id': self.id_,
            'externalId': self.external_id,
            'callId': self.call_id,
            'phone': self.phone,
            'direction': self.direction,
            'date': format_date(self.date),
            'duration': self.duration,
            'fileSize': self.file_size,
            'comment': self.comment,
            'abonent': self.abonent.to_beeline_struct(),
        }


@dataclass
class IcrNumbersResult(BaseModel):
    phone_number: str
    status: str
    error: Optional[dict]

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'IcrNumbersResult':
        return cls(
            model_dict['phoneNumber'], model_dict['status'], model_dict.get('status'),
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {'phoneNumber': self.phone_number, 'status': self.status}
        if self.error:
            struct['error'] = self.error
        return struct


@dataclass
class IcrRouteResult(BaseModel):
    rule: IcrRouteRule
    status: str
    error: Optional[dict] = None

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'IcrRouteResult':
        return cls(
            IcrRouteRule.from_dict(model_dict['rule']),
            model_dict['status'],
            model_dict.get('error'),
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {
            'rule': self.rule.to_beeline_struct(),
            'status': self.status,
        }
        if self.error:
            struct['error'] = self.error
        return struct


@dataclass
class VoiceCampaignMessage(BaseModel):
    name: str
    audio_file: str
    phones: List[str]
    phone_number: str
    schedule: VoiceCampaignSchedule
    from_: DateAndTime
    to_: DateAndTime

    @classmethod
    def from_dict(cls, model_dict: dict) -> 'VoiceCampaignMessage':
        return cls(
            model_dict['name'],
            model_dict['audioFile'],
            model_dict['phones'],
            model_dict['phoneNumber'],
            VoiceCampaignSchedule.from_dict(model_dict['schedule']),
            DateAndTime.from_dict(model_dict['from']),
            DateAndTime.from_dict(model_dict['to']),
        )

    def to_beeline_struct(self) -> dict:
        return {
            'name': self.name,
            'audioFile': self.audio_file,
            'audioFile': self.phones,
            'phoneNumber': self.phone_number,
            'schedule': self.schedule.to_beeline_struct(),
            'from': self.from_.to_beeline_struct(),
            'to': self.to_.to_beeline_struct(),
        }
