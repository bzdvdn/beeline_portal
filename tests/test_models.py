import unittest
import json
from unittest.case import TestCase

from beeline_portal.models import (
    Abonent,
    Number,
    SubscriptionRequest,
    Subscription,
    IcrNumberResult,
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
