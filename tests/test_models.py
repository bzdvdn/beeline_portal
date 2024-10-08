import unittest
import pytz
import json
from dateutil.parser import parse

from beeline_portal.models import (
    Abonent,
    DateAndTime,
    Number,
    SubscriptionRequest,
    Subscription,
    IcrRouteRule,
    Answer,
    VoiceCampaign,
    VoiceCampaignSchedule,
    VoiceCampaignQuestion,
    VoiceCampaignAnswer,
    VoiceCampaignInfoNumber,
    VoiceCampaignInfoReport,
    VoiceCampaignMessage,
    StatRecord,
    StatRecordV2,
    Cfb,
    CfbResponse,
    CfsRule,
    CfsStatusResponse,
    BwlRule,
    BwlStatusResponse,
    CallRecord,
    IcrNumbersResult,
    IcrRouteResult,
)
from beeline_portal.utils import (
    parse_datetime,
    parse_datetime_from_milliseconds,
)


class AbonentTest(unittest.TestCase):
    def test_from_beeline_struct(self):
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
        abonent = Abonent.from_beeline_struct(data)
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
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"numberId": "9379992@beeline.ru",
            "phone":"9379992"}
            '''
        )
        number = Number.from_beeline_struct(data)
        assert number.number_id == '9379992@beeline.ru'
        assert number.phone == '9379992'

    def test_to_beeline_struct(self):
        number = Number('9379992@beeline.ru', '9379992',)
        struct = number.to_beeline_struct()
        assert struct['numberId'] == '9379992@beeline.ru'
        assert struct['phone'] == '9379992'


class SubscriptionRequestTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"pattern": "9379992",
            "expires":1234535,
            "subscriptionType":"BASIC_CALL",
            "url":"test.io"}
            '''
        )
        subs_request = SubscriptionRequest.from_beeline_struct(data)
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
    def test_from_beeline_struct(self):
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
        subs = Subscription.from_beeline_struct(data)
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


class IcrRouteRuleTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"inboundNumber": "+793799992",
            "extension":"2310"}
            '''
        )
        icr_route_rule = IcrRouteRule.from_beeline_struct(data)
        assert icr_route_rule.inbound_number == "+793799992"
        assert icr_route_rule.extension == "2310"
        return icr_route_rule

    def test_to_beeline_struct(self):
        icr_route_rule = self.test_from_beeline_struct()
        struct = icr_route_rule.to_beeline_struct()
        assert struct['inboundNumber'] == "+793799992"
        assert struct['extension'] == "2310"


class AnswerTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"choice": "B_1",
            "answer":"test"}
            '''
        )
        answer = Answer.from_beeline_struct(data)
        assert answer.choice == "B_1"
        assert answer.answer == "test"
        return answer

    def test_to_beeline_struct(self):
        answer = self.test_from_beeline_struct()
        struct = answer.to_beeline_struct()
        assert struct['choice'] == 'B_1'
        assert struct['answer'] == 'test'


class VoiceCampaignScheduleTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"tryQuantity": "Q1",
            "fromHour":"H1",
            "toHour":"H4",
            "schedule":"BUSINESS_DAY"}
            '''
        )
        voice_campaign_schedule = VoiceCampaignSchedule.from_beeline_struct(data)
        assert voice_campaign_schedule.try_quantity == "Q1"
        assert voice_campaign_schedule.from_hour == "H1"
        assert voice_campaign_schedule.to_hour == "H4"
        assert voice_campaign_schedule.schedule == "BUSINESS_DAY"
        return voice_campaign_schedule

    def test_to_beeline_struct(self):
        voice_campaign_schedule = self.test_from_beeline_struct()
        struct = voice_campaign_schedule.to_beeline_struct()
        assert struct['tryQuantity'] == "Q1"
        assert struct['fromHour'] == "H1"
        assert struct['toHour'] == "H4"
        assert struct['schedule'] == "BUSINESS_DAY"


class DateAndTimeTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"date": "2021-01-01",
            "time":"00:00:23"}
            '''
        )
        dt = DateAndTime.from_beeline_struct(data)
        assert dt.date == parse('2021-01-01').replace(tzinfo=pytz.utc)
        assert dt.time == '00:00:23'
        return dt

    def test_to_beeline_struct(self):
        dt = self.test_from_beeline_struct()
        struct = dt.to_beeline_struct()
        assert struct['date'] == '2021-01-01'
        assert struct['time'] == '00:00:23'


class VoiceCampaignTest(unittest.TestCase):
    def test_from_beeline_struct(self):
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
        vc = VoiceCampaign.from_beeline_struct(data)
        assert vc.name == 'MyVoiceCampaign'
        assert vc.status == 'SUSPENDED'
        assert vc.record_id == 'hhyth1231432'
        assert vc.answers == [Answer("B1", "test")]
        assert vc.audio_file == '<link>'
        assert vc.phones == ['93799992']
        assert vc.phone_number == '+799999999'
        assert vc.schedule == VoiceCampaignSchedule('Q1', 'H0', 'H4', 'ALL_WEEK')
        assert vc.from_ == DateAndTime(parse_datetime('2021-01-01'), '00:00:00')
        assert vc.to_ == DateAndTime(parse_datetime('2021-12-01'), '23:59:59')
        assert vc.abonent == Abonent.from_beeline_struct(
            json.loads(
                '''
                {"userId": "9379992@beeline.ru", "phone": "9379992", "firstName": "Ivan", "lastName": "Moody"}'''
            )
        )


class VoiceCampaignQuestionTest(unittest.TestCase):
    def test_to_beeline_struct(self):
        answers = [Answer('Q1', 'gadget')]
        schedule = VoiceCampaignSchedule('Q1', 'H1', 'H4', 'BUSINESS_DAY')
        from_ = DateAndTime(parse_datetime('2021-11-11'), '00:00')
        to_ = DateAndTime(parse_datetime('2021-11-21'), '00:00')
        campaign = VoiceCampaignQuestion(
            'q_campaign',
            answers,
            "<file>",
            ['+793799992'],
            '+7123212432',
            schedule,
            from_,
            to_,
        )
        struct = campaign.to_beeline_struct()
        assert struct['name'] == 'q_campaign'
        assert struct['answers'] == [{'choice': 'Q1', 'answer': 'gadget'}]
        assert struct['audioFile'] == "<file>"
        assert struct['phones'] == ['+793799992']
        assert struct['phoneNumber'] == '+7123212432'
        assert struct['schedule']['tryQuantity'] == "Q1"
        assert struct['schedule']['fromHour'] == "H1"
        assert struct['schedule']['toHour'] == "H4"
        assert struct['schedule']['schedule'] == "BUSINESS_DAY"
        assert struct['from']['date'] == "2021-11-11"
        assert struct['from']['time'] == "00:00"
        assert struct['to']['date'] == "2021-11-21"
        assert struct['to']['time'] == "00:00"


class VoiceCampaignAnswerTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"answer": "test",
            "answerCode":"1",
            "amount":1
            }
            '''
        )
        vca = VoiceCampaignAnswer.from_beeline_struct(data)
        assert vca.answer == 'test'
        assert vca.answer_code == '1'
        assert vca.amount == 1
        return vca

    def test_to_beeline_struct(self):
        vca = self.test_from_beeline_struct()
        struct = vca.to_beeline_struct()
        assert struct['answer'] == 'test'
        assert struct['answerCode'] == '1'
        assert struct['amount'] == 1


class VoiceCampaignInfoNumberTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"phone": "+793799992",
            "result":"test",
            "attempts":"attempts",
            "lastAttemptDate":"2021-11-01",
            "isDone":false,
            "answer":"done",
            "answerCode":"Q1"
            }
            '''
        )
        vc_info_number = VoiceCampaignInfoNumber.from_beeline_struct(data)
        assert vc_info_number.phone == '+793799992'
        assert vc_info_number.result == 'test'
        assert vc_info_number.attempts == 'attempts'
        assert vc_info_number.last_attempt_date == parse_datetime("2021-11-01")
        assert vc_info_number.is_done == False
        assert vc_info_number.answer == 'done'
        assert vc_info_number.answer_code == 'Q1'
        return vc_info_number

    def test_to_beeline_struct(self):
        vc_info_number = self.test_from_beeline_struct()
        struct = vc_info_number.to_beeline_struct()
        assert struct['phone'] == '+793799992'
        assert struct['result'] == 'test'
        assert struct['attempts'] == 'attempts'
        assert struct['lastAttemptDate'] == '2021-11-01'
        assert struct['isDone'] == False
        assert struct['answer'] == 'done'
        assert struct['answerCode'] == 'Q1'


class VoiceCampaignInfoReportTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {"campaignName": "VoiceCampaign1",
            "reportDate":"2021-11-01",
            "client":"bastion",
            "state":"PLANNED",
            "startDate":"2021-11-01",
            "finishDate":"2021-11-02",
            "total":23,
            "processed":10,
            "success":10,
            "abandoned":2,
            "busyOrNoAnswer":0,
            "numberList":[{"phone": "+793799992",
            "result":"test",
            "attempts":"attempts",
            "lastAttemptDate":"2021-11-01",
            "isDone":false,
            "answer":"done",
            "answerCode":"Q1"
            }],
            "abonent": {"userId": "9379992@beeline.ru",
            "phone":"9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "email": null,
            "department": "test",
            "extension": "2310"},
            "answerList": [{"answer": "Test", "answerCode": "Q1", "amount": 2}]
            }
            '''
        )
        vc_info_report = VoiceCampaignInfoReport.from_beeline_struct(data)
        assert vc_info_report.campaign_name == 'VoiceCampaign1'
        assert vc_info_report.report_date == parse_datetime('2021-11-01')
        assert vc_info_report.client == 'bastion'
        assert vc_info_report.state == 'PLANNED'
        assert vc_info_report.start_date == parse_datetime('2021-11-01')
        assert vc_info_report.finish_date == parse_datetime('2021-11-02')
        assert vc_info_report.total == 23
        assert vc_info_report.processed == 10
        assert vc_info_report.success == 10
        assert vc_info_report.abandoned == 2
        assert vc_info_report.number_list == [
            VoiceCampaignInfoNumber.from_beeline_struct(
                {
                    "phone": "+793799992",
                    "result": "test",
                    "attempts": "attempts",
                    "lastAttemptDate": "2021-11-01",
                    "isDone": False,
                    "answer": "done",
                    "answerCode": "Q1",
                }
            )
        ]
        assert vc_info_report.abonent == Abonent.from_beeline_struct(
            {
                "userId": "9379992@beeline.ru",
                "phone": "9379992",
                "firstName": "TestUser",
                "lastName": "TestUser1",
                "email": None,
                "department": "test",
                "extension": "2310",
            }
        )
        assert vc_info_report.answer_list == [
            VoiceCampaignAnswer.from_beeline_struct(
                {"answer": "Test", "answerCode": "Q1", "amount": 2}
            )
        ]
        return vc_info_report

    def test_to_beeline_struct(self):
        vc_info_report = self.test_from_beeline_struct()
        struct = vc_info_report.to_beeline_struct()
        assert struct['campaignName'] == 'VoiceCampaign1'
        assert struct['client'] == 'bastion'
        assert struct['state'] == 'PLANNED'
        assert struct['startDate'] == '2021-11-01'
        assert struct['reportDate'] == '2021-11-01'
        assert struct['finishDate'] == '2021-11-02'
        assert struct['total'] == 23
        assert struct['processed'] == 10
        assert struct['success'] == 10
        assert struct['abandoned'] == 2
        assert struct['busyOrNoAnswer'] == 0
        assert struct['numberList'] == [
            {
                "phone": "+793799992",
                "result": "test",
                "attempts": "attempts",
                "lastAttemptDate": "2021-11-01",
                "isDone": False,
                "answer": "done",
                "answerCode": "Q1",
            }
        ]
        assert struct['abonent'] == {
            "userId": "9379992@beeline.ru",
            "phone": "9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "department": "test",
            "extension": "2310",
        }
        assert struct['answerList'] == [
            {"answer": "Test", "answerCode": "Q1", "amount": 2}
        ]


class VoiceCampaignMessageTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
                {
                    "name": "Message campaign",
                    "audioFile": "file_id",
                    "phones": ["200"],
                    "phoneNumber": "+79379999992",
                    "schedule": {
                        "tryQuantity": "Q1",
                        "fromHour":"H1",
                        "toHour":"H4",
                        "schedule":"BUSINESS_DAY"
                    },
                    "from": {
                        "date": "2021-01-01",
                        "time":"00:00:23"
                    },
                    "to": {
                        "date": "2021-01-01",
                        "time":"00:00:23"
                    }
                }
            '''
        )
        vc_message = VoiceCampaignMessage.from_beeline_struct(data)
        assert vc_message.name == "Message campaign"
        assert vc_message.audio_file == "file_id"
        assert vc_message.phones == ['200']
        assert vc_message.phone_number == "+79379999992"
        assert vc_message.schedule == VoiceCampaignSchedule.from_beeline_struct(
            {
                "tryQuantity": "Q1",
                "fromHour": "H1",
                "toHour": "H4",
                "schedule": "BUSINESS_DAY",
            }
        )
        assert vc_message.from_ == DateAndTime.from_beeline_struct(
            {"date": "2021-01-01", "time": "00:00:23"}
        )
        assert vc_message.to_ == DateAndTime.from_beeline_struct(
            {"date": "2021-01-01", "time": "00:00:23"}
        )
        return vc_message

    def test_to_beeline_struct(self):
        vc_message = self.test_from_beeline_struct()
        struct = vc_message.to_beeline_struct()
        assert struct == {
            "name": "Message campaign",
            "audioFile": "file_id",
            "phones": ["200"],
            "phoneNumber": "+79379999992",
            "schedule": {
                "tryQuantity": "Q1",
                "fromHour": "H1",
                "toHour": "H4",
                "schedule": "BUSINESS_DAY",
            },
            "from": {"date": "2021-01-01", "time": "00:00:23"},
            "to": {"date": "2021-01-01", "time": "00:00:23"},
        }


class StatRecordTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
            "startDate": 1638432499281,
            "direction": "INBOUND",
            "phone": "+793799992",
            "duration": 0,
            "status": "MISSED",
            "abonent": {"userId": "9379992@beeline.ru",
            "phone":"9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "email": null,
            "department": "test",
            "extension": "2310"}
            }
            '''
        )
        statistic = StatRecord.from_beeline_struct(data)
        assert statistic.start_date == parse_datetime_from_milliseconds(1638432499281)
        assert statistic.direction == 'INBOUND'
        assert statistic.phone == '+793799992'
        assert statistic.duration == 0
        assert statistic.status == 'MISSED'
        assert statistic.abonent.user_id == '9379992@beeline.ru'
        assert statistic.abonent.phone == '9379992'
        assert statistic.abonent.first_name == 'TestUser'
        assert statistic.abonent.last_name == 'TestUser1'
        assert statistic.abonent.email is None
        assert statistic.abonent.department == 'test'
        assert statistic.abonent.extension == '2310'
        return statistic

    def test_to_beeline_struct(self):
        stats = self.test_from_beeline_struct()
        struct = stats.to_beeline_struct()
        assert struct['startDate'] == 1638432499281
        assert struct['direction'] == 'INBOUND'
        assert struct['phone'] == '+793799992'
        assert struct['duration'] == 0
        assert struct['status'] == 'MISSED'
        assert struct['abonent'] == {
            "userId": "9379992@beeline.ru",
            "phone": "9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "department": "test",
            "extension": "2310",
        }


class StatRecordV2Test(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
            "startDate": 1638432499281,
            "direction": "INBOUND",
            "phone_from": "+79379992",
            "duration": 0,
            "status": "MISSED",
            "abonent": {"userId": "9379992@beeline.ru",
            "phone":"9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "email": null,
            "department": "test",
            "extension": "2310"}
            }
            '''
        )
        stats = StatRecordV2.from_beeline_struct(data)
        assert stats.start_date == parse_datetime_from_milliseconds(1638432499281)
        assert stats.direction == 'INBOUND'
        assert stats.phone_from == '+79379992'
        assert stats.phone_to is None
        assert stats.duration == 0
        assert stats.status == 'MISSED'
        assert stats.abonent.user_id == '9379992@beeline.ru'
        return stats

    def test_to_beeline_struct(self):
        stats = self.test_from_beeline_struct()
        struct = stats.to_beeline_struct()
        assert struct['startDate'] == 1638432499281
        assert struct['direction'] == 'INBOUND'
        assert struct['phone_from'] == '+79379992'
        assert struct['duration'] == 0
        assert struct['status'] == 'MISSED'
        assert struct['abonent'] == {
            "userId": "9379992@beeline.ru",
            "phone": "9379992",
            "firstName": "TestUser",
            "lastName": "TestUser1",
            "department": "test",
            "extension": "2310",
        }


class CfbTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
            "forwardAllCallsPhone": "+79379992",
            "forwardBusyPhone": "+79379991",
            "forwardUnavailablePhone": "+79379993",
            "forwardNotAnswerPhone": "+79379994",
            "forwardNotAnswerTimeout": "123"
            }
            '''
        )
        cfb = Cfb.from_beeline_struct(data)
        assert cfb.forward_all_calls_phone == '+79379992'
        assert cfb.forward_busy_phone == '+79379991'
        assert cfb.forward_unavailable_phone == '+79379993'
        assert cfb.forward_not_answer_phone == '+79379994'
        assert cfb.forward_not_answer_timeout == '123'
        return cfb

    def test_to_beeline_struct(self):
        cfb = self.test_from_beeline_struct()
        struct = cfb.to_beeline_struct()
        assert struct == {
            "forwardAllCallsPhone": "+79379992",
            "forwardBusyPhone": "+79379991",
            "forwardUnavailablePhone": "+79379993",
            "forwardNotAnswerPhone": "+79379994",
            "forwardNotAnswerTimeout": "123",
        }


class CfbResponseTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''{
            "status": "ON",
            "cfb": {
                    "forwardAllCallsPhone": "+79379992",
                    "forwardBusyPhone": "+79379991",
                    "forwardUnavailablePhone": "+79379993",
                    "forwardNotAnswerPhone": "+79379994",
                    "forwardNotAnswerTimeout": "123"
                }
            }
            '''
        )
        cfb_response = CfbResponse.from_beeline_struct(data)
        assert cfb_response.status == 'ON'
        assert cfb_response.cfb.forward_all_calls_phone == '+79379992'
        assert cfb_response.cfb.forward_busy_phone == '+79379991'
        assert cfb_response.cfb.forward_unavailable_phone == '+79379993'
        assert cfb_response.cfb.forward_not_answer_phone == '+79379994'
        assert cfb_response.cfb.forward_not_answer_timeout == '123'
        return cfb_response

    def test_to_beeline_struct(self):
        cfb_response = self.test_from_beeline_struct()
        struct = cfb_response.to_beeline_struct()
        assert struct['status'] == 'ON'
        assert struct['cfb'] == {
            "forwardAllCallsPhone": "+79379992",
            "forwardBusyPhone": "+79379991",
            "forwardUnavailablePhone": "+79379993",
            "forwardNotAnswerPhone": "+79379994",
            "forwardNotAnswerTimeout": "123",
        }


class CfsRuleTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
                "id": "1",
                "name": "my cfs rule",
                "forwardToPhone": "+793999992",
                "schedule": "WORKING_TIME",
                "phoneList": ["+79399999992"]
            }
            '''
        )
        cfs_rule = CfsRule.from_beeline_struct(data)
        assert cfs_rule.name == 'my cfs rule'
        assert cfs_rule.id_ == '1'
        assert cfs_rule.forward_to_phone == '+793999992'
        assert cfs_rule.schedule == 'WORKING_TIME'
        assert cfs_rule.phone_list == ["+79399999992"]
        return cfs_rule

    def test_to_beeline_struct(self):
        cfs_rule = self.test_from_beeline_struct()
        struct = cfs_rule.to_beeline_struct()
        assert struct == {
            "id": "1",
            "name": "my cfs rule",
            "forwardToPhone": "+793999992",
            "schedule": "WORKING_TIME",
            "phoneList": ["+79399999992"],
        }


class CfsStatusResponseTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
                "isCfsServiceEnabled": true,
                "ruleList": [
                    {
                        "id": "1",
                        "name": "my cfs rule",
                        "forwardToPhone": "+793999992",
                        "schedule": "WORKING_TIME",
                        "phoneList": ["+79399999992"]
                    }
                ]
            }
            '''
        )
        cfs_status_response = CfsStatusResponse.from_beeline_struct(data)
        assert cfs_status_response.is_cfs_service_enabled is True
        assert cfs_status_response.rule_list == [
            CfsRule.from_beeline_struct(
                {
                    "id": "1",
                    "name": "my cfs rule",
                    "forwardToPhone": "+793999992",
                    "schedule": "WORKING_TIME",
                    "phoneList": ["+79399999992"],
                }
            )
        ]
        return cfs_status_response

    def test_to_beeline_struct(self):
        cfs_status_response = self.test_from_beeline_struct()
        struct = cfs_status_response.to_beeline_struct()
        assert struct['isCfsServiceEnabled'] is True
        assert struct['ruleList'] == [
            {
                "id": "1",
                "name": "my cfs rule",
                "forwardToPhone": "+793999992",
                "schedule": "WORKING_TIME",
                "phoneList": ["+79399999992"],
            }
        ]


class BwlRuleTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
                "id": "1",
                "name": "my bwl rule",
                "forwardToPhone": "+793999992",
                "schedule": "WORKING_TIME",
                "phoneList": ["+79399999992"]
            }
            '''
        )
        bwl_rule = BwlRule.from_beeline_struct(data)
        assert bwl_rule.name == 'my bwl rule'
        assert bwl_rule.id_ == '1'
        assert bwl_rule.forward_to_phone == '+793999992'
        assert bwl_rule.schedule == 'WORKING_TIME'
        assert bwl_rule.phone_list == ["+79399999992"]
        return bwl_rule

    def test_to_beeline_struct(self):
        bwl_rule = self.test_from_beeline_struct()
        struct = bwl_rule.to_beeline_struct()
        assert struct == {
            "id": "1",
            "name": "my bwl rule",
            "forwardToPhone": "+793999992",
            "schedule": "WORKING_TIME",
            "phoneList": ["+79399999992"],
        }


class BwlStatusResponseTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
                "status": "BLACK_LIST_ON",
                "blackList": [
                    {
                        "id": "1",
                        "name": "my bwl rule",
                        "forwardToPhone": "+793999992",
                        "schedule": "WORKING_TIME",
                        "phoneList": ["+79399999992"]
                    }
                ],
                "whiteList": [
                    {
                        "id": "2",
                        "name": "my bwl rule2",
                        "forwardToPhone": "+793999999",
                        "schedule": "WORKING_TIME",
                        "phoneList": ["+79399999993"]
                    }
                ]
            }
            '''
        )
        bwl_status_response = BwlStatusResponse.from_beeline_struct(data)
        assert bwl_status_response.status == 'BLACK_LIST_ON'
        assert bwl_status_response.black_list == [
            BwlRule.from_beeline_struct(
                {
                    "id": "1",
                    "name": "my bwl rule",
                    "forwardToPhone": "+793999992",
                    "schedule": "WORKING_TIME",
                    "phoneList": ["+79399999992"],
                }
            )
        ]
        assert bwl_status_response.white_list == [
            BwlRule.from_beeline_struct(
                {
                    "id": "2",
                    "name": "my bwl rule2",
                    "forwardToPhone": "+793999999",
                    "schedule": "WORKING_TIME",
                    "phoneList": ["+79399999993"],
                }
            )
        ]
        return bwl_status_response

    def test_to_beeline_struct(self):
        bwl_status_response = self.test_from_beeline_struct()
        struct = bwl_status_response.to_beeline_struct()
        assert struct == {
            "status": "BLACK_LIST_ON",
            "blackList": [
                {
                    "id": "1",
                    "name": "my bwl rule",
                    "forwardToPhone": "+793999992",
                    "schedule": "WORKING_TIME",
                    "phoneList": ["+79399999992"],
                }
            ],
            "whiteList": [
                {
                    "id": "2",
                    "name": "my bwl rule2",
                    "forwardToPhone": "+793999999",
                    "schedule": "WORKING_TIME",
                    "phoneList": ["+79399999993"],
                }
            ],
        }


class CallRecordTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
            {
                "id": "1",
                "externalId": "2310123243543",
                "callId": "2310123243541",
                "phone": "+79399999993",
                "direction": "INBOUND",
                "date": "2021-01-01",
                "duration": 2310,
                "fileSize": 2310,
                "comment": "test call",
                "abonent": {
                    "userId": "9379992@beeline.ru",
                    "phone": "9379992",
                    "firstName": "TestUser",
                    "lastName": "TestUser1",
                    "department": "test",
                    "extension": "2310"
                }
            }                  
        '''
        )
        call_record = CallRecord.from_beeline_struct(data)
        assert call_record.id_ == "1"
        assert call_record.external_id == "2310123243543"
        assert call_record.call_id == "2310123243541"
        assert call_record.phone == "+79399999993"
        assert call_record.direction == "INBOUND"
        assert call_record.date == parse_datetime("2021-01-01")
        assert call_record.duration == 2310
        assert call_record.file_size == 2310
        assert call_record.abonent == Abonent.from_beeline_struct(
            {
                "userId": "9379992@beeline.ru",
                "phone": "9379992",
                "firstName": "TestUser",
                "lastName": "TestUser1",
                "department": "test",
                "extension": "2310",
            }
        )
        return call_record

    def test_to_beeline_struct(self):
        call_record = self.test_from_beeline_struct()
        struct = call_record.to_beeline_struct()
        assert struct == {
            "id": "1",
            "externalId": "2310123243543",
            "callId": "2310123243541",
            "phone": "+79399999993",
            "direction": "INBOUND",
            "date": "2021-01-01",
            "duration": 2310,
            "fileSize": 2310,
            "comment": "test call",
            "abonent": {
                "userId": "9379992@beeline.ru",
                "phone": "9379992",
                "firstName": "TestUser",
                "lastName": "TestUser1",
                "department": "test",
                "extension": "2310",
            },
        }


class IcrNumbersResultTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
                {
                    "phoneNumber": "+73979999992",
                    "status": "SUCCESS"
                }
            '''
        )
        icr_number_result = IcrNumbersResult.from_beeline_struct(data)
        assert icr_number_result.phone_number == "+73979999992"
        assert icr_number_result.status == "SUCCESS"
        return icr_number_result

    def test_to_beeline_struct(self):
        icr_number_result = self.test_from_beeline_struct()
        struct = icr_number_result.to_beeline_struct()
        assert struct == {
            "phoneNumber": "+73979999992",
            "status": "SUCCESS",
        }


class IcrRouteResultTest(unittest.TestCase):
    def test_from_beeline_struct(self):
        data = json.loads(
            '''
                {
                    "rule": {   
                            "inboundNumber": "+793799992",
                            "extension":"2310"
                        },
                    "status": "FAULT"
                }
            '''
        )
        icr_route_result = IcrRouteResult.from_beeline_struct(data)
        assert icr_route_result.rule == IcrRouteRule.from_beeline_struct(
            {"inboundNumber": "+793799992", "extension": "2310"}
        )
        assert icr_route_result.status == "FAULT"
        return icr_route_result

    def test_to_beeline_struct(self):
        icr_route_result = self.test_from_beeline_struct()
        struct = icr_route_result.to_beeline_struct()
        assert struct == {
            "rule": {"inboundNumber": "+793799992", "extension": "2310"},
            "status": "FAULT",
        }

