from datetime import datetime
from typing import List, Optional
from abc import ABC
from dataclasses import dataclass

from .utils import (
    parse_datetime_from_milliseconds,
    parse_datetime,
    format_date,
    to_milliseconds,
)


class BaseModel(ABC):
    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'BaseModel':
        raise NotImplementedError()

    def to_beeline_struct(self) -> dict:
        raise NotImplementedError()


@dataclass()
class Abonent(BaseModel):
    user_id: str
    phone: str
    first_name: str
    last_name: str
    extension: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'Abonent':
        return cls(
            beeline_struct['userId'],
            beeline_struct['phone'],
            beeline_struct.get('firstName', 'none'),
            beeline_struct['lastName'],
            beeline_struct.get('extension'),
            beeline_struct.get('email'),
            beeline_struct.get('department'),
        )

    def to_beeline_struct(self) -> dict:
        struct = {
            'userId': self.user_id,
            'phone': self.phone,
            'firstName': self.first_name,
            'lastName': self.last_name,
        }
        if self.extension:
            struct['extension'] = self.extension
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'Number':
        return cls(
            beeline_struct['numberId'],
            beeline_struct['phone'],
        )

    def to_beeline_struct(self) -> dict:
        return {'numberId': self.number_id, 'phone': self.phone}


@dataclass
class SubscriptionRequest(BaseModel):
    pattern: str
    expires: int
    subscription_type: str
    url: str

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'SubscriptionRequest':
        return cls(
            beeline_struct['pattern'],
            beeline_struct['expires'],
            beeline_struct['subscriptionType'],
            beeline_struct['url'],
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'Subscription':
        return cls(
            beeline_struct['subscriptionId'],
            beeline_struct['targetType'],
            beeline_struct['targetId'],
            beeline_struct['subscriptionType'],
            beeline_struct['expires'],
            beeline_struct['url'],
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
class IcrRouteRule(BaseModel):
    inbound_number: str
    extension: str

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'IcrRouteRule':
        return cls(beeline_struct['inboundNumber'], beeline_struct['extension'])

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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'Answer':
        return cls(
            beeline_struct['choice'],
            beeline_struct['answer'],
        )

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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'VoiceCampaignSchedule':
        return cls(
            beeline_struct['tryQuantity'],
            beeline_struct['fromHour'],
            beeline_struct['toHour'],
            beeline_struct['schedule'],
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'DateAndTime':
        return cls(parse_datetime(beeline_struct['date']), beeline_struct['time'])

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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'VoiceCampaign':
        return cls(
            beeline_struct['name'],
            beeline_struct['status'],
            beeline_struct['recordId'],
            beeline_struct['type'],
            beeline_struct['audioFile'],
            beeline_struct['phones'],
            beeline_struct['phoneNumber'],
            VoiceCampaignSchedule.from_beeline_struct(beeline_struct['schedule']),
            DateAndTime.from_beeline_struct(beeline_struct['from']),
            DateAndTime.from_beeline_struct(beeline_struct['to']),
            answers=[Answer.from_beeline_struct(r) for r in beeline_struct['answers']]
            if 'answers' in beeline_struct
            else None,
            abonent=Abonent.from_beeline_struct(beeline_struct['abonent'])
            if 'abonent' in beeline_struct
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
            'audioFile': self.audio_file,
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'VoiceCampaignAnswer':
        return cls(
            beeline_struct['answer'],
            beeline_struct['answerCode'],
            beeline_struct['amount'],
        )

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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'VoiceCampaignInfoNumber':
        return cls(
            beeline_struct['phone'],
            beeline_struct['result'],
            beeline_struct['attempts'],
            parse_datetime(beeline_struct['lastAttemptDate']),
            beeline_struct['isDone'],
            beeline_struct['answer'],
            beeline_struct['answerCode'],
        )

    def to_beeline_struct(self) -> dict:
        return {
            'phone': self.phone,
            'result': self.result,
            'attempts': self.attempts,
            'lastAttemptDate': format_date(self.last_attempt_date),
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'VoiceCampaignInfoReport':
        return cls(
            beeline_struct['campaignName'],
            parse_datetime(beeline_struct['reportDate']),
            beeline_struct['client'],
            beeline_struct['state'],
            parse_datetime(beeline_struct['startDate']),
            parse_datetime(beeline_struct['finishDate']),
            beeline_struct['total'],
            beeline_struct['processed'],
            beeline_struct['success'],
            beeline_struct['abandoned'],
            beeline_struct['busyOrNoAnswer'],
            [
                VoiceCampaignInfoNumber.from_beeline_struct(n)
                for n in beeline_struct['numberList']
            ],
            Abonent.from_beeline_struct(beeline_struct['abonent'])
            if beeline_struct.get('abonent')
            else None,
            [
                VoiceCampaignAnswer.from_beeline_struct(a)
                for a in beeline_struct['answerList']
            ]
            if beeline_struct.get('answerList')
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
            'success': self.success,
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
    duration: int
    department: Optional[str] = None
    call_forward: Optional[str] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'StatRecord':
        return cls(
            parse_datetime_from_milliseconds(beeline_struct['startDate']),
            Abonent.from_beeline_struct(beeline_struct['abonent']),
            beeline_struct['direction'],
            beeline_struct['status'],
            beeline_struct['phone'],
            beeline_struct['duration'],
            beeline_struct.get('department'),
            beeline_struct.get('callForward'),
        )

    def to_beeline_struct(self) -> dict:
        struct = {
            'startDate': to_milliseconds(self.start_date),
            'abonent': self.abonent.to_beeline_struct(),
            'direction': self.direction,
            'duration': self.duration,
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
    duration: int
    phone_to: Optional[str] = None
    phone_from: Optional[str] = None
    department: Optional[str] = None
    call_forward: Optional[str] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'StatRecordV2':
        return cls(
            parse_datetime_from_milliseconds(beeline_struct['startDate']),
            Abonent.from_beeline_struct(beeline_struct['abonent']),
            beeline_struct['direction'],
            beeline_struct['status'],
            beeline_struct['duration'],
            beeline_struct.get('phone_to'),
            beeline_struct.get('phone_from'),
            beeline_struct.get('department'),
            beeline_struct.get('callForward'),
        )

    def to_beeline_struct(self) -> dict:
        struct = {
            'startDate': to_milliseconds(self.start_date),
            'abonent': self.abonent.to_beeline_struct(),
            'direction': self.direction,
            'status': self.status,
            'duration': self.duration,
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'Cfb':
        return cls(
            beeline_struct.get('forwardAllCallsPhone'),
            beeline_struct.get('forwardBusyPhone'),
            beeline_struct.get('forwardUnavailablePhone'),
            beeline_struct.get('forwardNotAnswerPhone'),
            beeline_struct.get('forwardNotAnswerTimeout'),
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'CfbResponse':
        return cls(
            beeline_struct['status'], Cfb.from_beeline_struct(beeline_struct['cfb'])
        )

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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'BaseRule':
        return cls(
            beeline_struct['name'],
            beeline_struct['forwardToPhone'],
            beeline_struct['schedule'],
            beeline_struct['phoneList'],
            beeline_struct.get('id'),
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'CfsRule':
        return super(CfsRule, cls).from_beeline_struct(beeline_struct)  # type: ignore


@dataclass
class CfsStatusResponse(BaseModel):
    is_cfs_service_enabled: bool
    rule_list: Optional[List[CfsRule]] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'CfsStatusResponse':
        return cls(
            beeline_struct['isCfsServiceEnabled'],
            [CfsRule.from_beeline_struct(rule) for rule in beeline_struct['ruleList']]
            if 'ruleList' in beeline_struct
            else None,
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {'isCfsServiceEnabled': self.is_cfs_service_enabled}
        if self.rule_list:
            struct['ruleList'] = [r.to_beeline_struct() for r in self.rule_list]  # type: ignore
        return struct


@dataclass
class BwlRule(BaseRule):
    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'BwlRule':
        return super(BwlRule, cls).from_beeline_struct(beeline_struct)  # type: ignore


@dataclass
class BwlStatusResponse(BaseModel):
    status: str
    black_list: Optional[List[BwlRule]] = None
    white_list: Optional[List[BwlRule]] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'BwlStatusResponse':
        return cls(
            beeline_struct['status'],
            [BwlRule.from_beeline_struct(rule) for rule in beeline_struct['blackList']]
            if 'blackList' in beeline_struct
            else None,
            [BwlRule.from_beeline_struct(rule) for rule in beeline_struct['whiteList']]
            if 'whiteList' in beeline_struct
            else None,
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {'status': self.status}
        if self.black_list:
            struct['blackList'] = [r.to_beeline_struct() for r in self.black_list]  # type: ignore
        if self.white_list:
            struct['whiteList'] = [r.to_beeline_struct() for r in self.white_list]  # type: ignore
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'CallRecord':
        return cls(
            beeline_struct['id'],
            beeline_struct['externalId'],
            beeline_struct['callId'],
            beeline_struct['phone'],
            beeline_struct['direction'],
            parse_datetime(beeline_struct['date']),
            beeline_struct['duration'],
            beeline_struct['fileSize'],
            beeline_struct['comment'],
            Abonent.from_beeline_struct(beeline_struct['abonent']),
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
    error: Optional[dict] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'IcrNumbersResult':
        return cls(
            beeline_struct['phoneNumber'],
            beeline_struct['status'],
            beeline_struct.get('error'),
        )

    def to_beeline_struct(self) -> dict:
        struct: dict = {'phoneNumber': self.phone_number, 'status': self.status}
        if self.error:
            struct['error'] = self.error  # type: ignore
        return struct


@dataclass
class IcrRouteResult(BaseModel):
    rule: IcrRouteRule
    status: str
    error: Optional[dict] = None

    @classmethod
    def from_beeline_struct(cls, beeline_struct: dict) -> 'IcrRouteResult':
        return cls(
            IcrRouteRule.from_beeline_struct(beeline_struct['rule']),
            beeline_struct['status'],
            beeline_struct.get('error'),
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
    def from_beeline_struct(cls, beeline_struct: dict) -> 'VoiceCampaignMessage':
        return cls(
            beeline_struct['name'],
            beeline_struct['audioFile'],
            beeline_struct['phones'],
            beeline_struct['phoneNumber'],
            VoiceCampaignSchedule.from_beeline_struct(beeline_struct['schedule']),
            DateAndTime.from_beeline_struct(beeline_struct['from']),
            DateAndTime.from_beeline_struct(beeline_struct['to']),
        )

    def to_beeline_struct(self) -> dict:
        return {
            'name': self.name,
            'audioFile': self.audio_file,
            'phones': self.phones,
            'phoneNumber': self.phone_number,
            'schedule': self.schedule.to_beeline_struct(),
            'from': self.from_.to_beeline_struct(),
            'to': self.to_.to_beeline_struct(),
        }
