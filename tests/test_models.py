import unittest
import pytz
import json
from unittest.case import TestCase
from dateutil.parser import parse

from beeline_portal.models import (
    Abonent,
    DateAndTime,
    Number,
    SubscriptionRequest,
    Subscription,
    IcrNumberResult,
    IcrRouteRule,
    Answer,
    VoiceCampaign,
    VoiceCampaignSchedule,
)


class AbonentTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"userId": "9379992@beeline.ru",
            "phone":"9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "email": null,
            "department": "test",
            "extension": "2310"}
            '''
        )
        abonent = Abonent.from_dict(data)
        assert abonent.user_id == '9379992@beeline.ru'
        assert abonent.phone == '9379992'
        assert abonent.first_name == 'TestUser'
        assert abonent.last_name == 'TestUser1'
        assert abonent.email is None
        assert abonent.department == 'test'
        assert abonent.extension == '2310'

    def test_to_beeline_struct(self):
        abonent = Abonent(
            '9379992@beeline.ru',
            '9379992',
            'user',
            'name',
            '2310',
            'test@gmail.com',
            'test',
        )
        struct = abonent.to_beeline_struct()
        assert struct['userId'] == '9379992@beeline.ru'
        assert struct['phone'] == '9379992'
        assert struct['firstName'] == 'user'
        assert struct['lastName'] == 'name'
        assert struct['extension'] == '2310'
        assert struct['email'] == 'test@gmail.com'
        assert struct['department'] == 'test'


class NumberTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"numberId": "9379992@beeline.ru",
            "phone":"9379992"}
            '''
        )
        number = Number.from_dict(data)
        assert number.number_id == '9379992@beeline.ru'
        assert number.phone == '9379992'

    def test_to_beeline_struct(self):
        number = Number('9379992@beeline.ru', '9379992',)
        struct = number.to_beeline_struct()
        assert struct['numberId'] == '9379992@beeline.ru'
        assert struct['phone'] == '9379992'


class SubscriptionRequestTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"pattern": "9379992",
            "expires":1234535,
            "subscriptionType":"BASIC_CALL",
            "url":"test.io"}
            '''
        )
        subs_request = SubscriptionRequest.from_dict(data)
        assert subs_request.pattern == '9379992'
        assert subs_request.expires == 1234535
        assert subs_request.subscription_type == 'BASIC_CALL'
        assert subs_request.url == 'test.io'

    def test_to_beeline_struct(self):
        subs_request = SubscriptionRequest('9379992', 1234535, 'BASIC_CALL', 'test.io')
        struct = subs_request.to_beeline_struct()
        assert struct['pattern'] == '9379992'
        assert struct['expires'] == 1234535
        assert struct['subscriptionType'] == 'BASIC_CALL'
        assert struct['url'] == 'test.io'


class SubscriptionTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"subscriptionId": "jsjkgksj12323",
            "targetType":"ABONENT",
            "targetId":"jsjkgksj12323",
            "subscriptionType":"BASIC_CALL",
            "expires":2132543,
            "url":"test.io"}
            '''
        )
        subs = Subscription.from_dict(data)
        assert subs.subscription_id == "jsjkgksj12323"
        assert subs.target_type == "ABONENT"
        assert subs.target_id == "jsjkgksj12323"
        assert subs.subscription_type == "BASIC_CALL"
        assert subs.expires == 2132543
        assert subs.url == "test.io"

    def test_to_beeline_struct(self):
        subs = Subscription(
            "jsjkgksj12323",
            "ABONENT",
            "jsjkgksj12323",
            "BASIC_CALL",
            2132543,
            "test.io",
        )
        struct = subs.to_beeline_struct()
        assert struct['subscriptionId'] == "jsjkgksj12323"
        assert struct['targetType'] == "ABONENT"
        assert struct['targetId'] == "jsjkgksj12323"
        assert struct['subscriptionType'] == "BASIC_CALL"
        assert struct['expires'] == 2132543
        assert struct['url'] == "test.io"


class IcrNumberResultTest(TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"phoneNumber": "+793799992",
            "status":"TEST"}
            '''
        )
        icr_number_result = IcrNumberResult.from_dict(data)
        assert icr_number_result.phone_number == "+793799992"
        assert icr_number_result.status == "TEST"
        assert icr_number_result.error is None
        return icr_number_result

    def test_to_beeline_struct(self):
        icr_number_result = self.test_from_dict()
        struct = icr_number_result.to_beeline_struct()
        assert struct['phoneNumber'] == "+793799992"
        assert struct['status'] == "TEST"
        assert struct.get('error') is None


class IcrRouteRuleTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"inboundNumber": "+793799992",
            "extension":"2310"}
            '''
        )
        icr_route_rule = IcrRouteRule.from_dict(data)
        assert icr_route_rule.inbound_number == "+793799992"
        assert icr_route_rule.extension == "2310"
        return icr_route_rule

    def test_to_beeline_struct(self):
        icr_route_rule = self.test_from_dict()
        struct = icr_route_rule.to_beeline_struct()
        assert struct['inboundNumber'] == "+793799992"
        assert struct['extension'] == "2310"


class AnswerTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"choice": "B_1",
            "answer":"test"}
            '''
        )
        answer = Answer.from_dict(data)
        assert answer.choice == "B_1"
        assert answer.answer == "test"
        return answer

    def test_to_beeline_struct(self):
        answer = self.test_from_dict()
        struct = answer.to_beeline_struct()
        assert struct['choice'] == 'B_1'
        assert struct['answer'] == 'test'


class VoiceCampaignScheduleTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"tryQuantity": "Q1",
            "fromHour":"H1",
            "toHour":"H4",
            "schedule":"BUSINESS_DAY"}
            '''
        )
        voice_campaign_schedule = VoiceCampaignSchedule.from_dict(data)
        assert voice_campaign_schedule.try_quantity == "Q1"
        assert voice_campaign_schedule.from_hour == "H1"
        assert voice_campaign_schedule.to_hour == "H4"
        assert voice_campaign_schedule.schedule == "BUSINESS_DAY"
        return voice_campaign_schedule

    def test_to_beeline_struct(self):
        voice_campaign_schedule = self.test_from_dict()
        struct = voice_campaign_schedule.to_beeline_struct()
        assert struct['tryQuantity'] == "Q1"
        assert struct['fromHour'] == "H1"
        assert struct['toHour'] == "H4"
        assert struct['schedule'] == "BUSINESS_DAY"


class DateAndTimeTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"date": "2021-01-01",
            "time":"00:00:23"}
            '''
        )
        dt = DateAndTime.from_dict(data)
        assert dt.date == parse('2021-01-01').replace(tzinfo=pytz.utc)
        assert dt.time == '00:00:23'
        return dt

    def test_to_beeline_struct(self):
        dt = self.test_from_dict()
        struct = dt.to_beeline_struct()
        assert struct['date'] == '2021-01-01'
        assert struct['time'] == '00:00:23'


class VoiceCampaignTest(unittest.TestCase):
    def test_from_dict(self):
        data = json.loads(
            '''
            {"name": "MyVoiceCampaign",
            "status":"SUSPENDED",
            "recordId":"hhyth1231432",
            "type":"QUESTION",
            "answers": [{"choice":"B1", "answer":"test"}],
            "audioFile":"<link>",
            "phones": ["93799992"],
            "phoneNumber": "+799999999",
            "schedule": {"tryQuantity": "Q1", "fromHour": "H0", "toHour": "H4", "schedule": "ALL_WEEK"},
            "from": {"date": "2021-01-01", "time":"00:00:00"},
            "to": {"date": "2021-12-01", "time":"23:59:59"},
            "abonent": {"userId": "9379992@beeline.ru", "phone": "9379992", "firstName": "Ivan", "lastName": "Moody"}
            }
            '''
        )
        vc = VoiceCampaign.from_dict(data)
        assert vc.name == 'MyVoiceCampaign'
        assert vc.status == 'SUSPENDED'
        assert vc.record_id == 'hhyth1231432'
        assert vc.answers == [Answer("B1", "test")]
        assert vc.audio_file == '<link>'
        assert vc.phones == ['93799992']
        assert vc.phone_number == '+799999999'
        assert vc.schedule == VoiceCampaignSchedule('Q1', 'H0', 'H4', 'ALL_WEEK')
        assert vc.from_ == DateAndTime('2021-01-01', '00:00:00')
        assert vc.to_ == DateAndTime('2021-12-01', '23:59:59')
        assert vc.abonent == Abonent.from_dict(
            json.loads(
                '''
                {"userId": "9379992@beeline.ru", "phone": "9379992", "firstName": "Ivan", "lastName": "Moody"}'''
            )
        )

