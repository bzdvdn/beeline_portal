## Beeline cloudpbx portal api wrapper

#### Install

Install using `pip`...

    pip install beeline-portal

#### Usage

```python
from beeline_portal import BeelinePBX

client = BeelinePBX('<access_token>')
```

##### get abonents

```python
abonents = client.get_abonents() # return map[Abonent]
```

##### find abonent

```python
abonent = client.find_abonent('<pattern>') # raise BeelinePBXException or return Abonent
```

##### get abonent agent status

```python
result = client.get_abonent_agent_status('<pattern>') # raise BeelinePBXException or return {'status': status}
```

##### set abonent agent status

```python
_ = client.set_abonent_agent_status('<pattern>', 'status') # raise BeelinePBXException or return {}
```

##### get abonent recording status

```python
result = client.get_abonent_recording_status('<pattern>') # raise BeelinePBXException or return {'status': status}
```

##### enable abonent recording

```python
_ = client.enable_abonent_recording('<pattern>') # raise BeelinePBXException or return {}
```

##### stop abonent recording

```python
_ = client.stop_abonent_recording('<pattern>') # raise BeelinePBXException or return {}
```

##### call from abonent

```python
result = client.call_from_abonent('<pattern>', 'phone number') # raise BeelinePBXException or return {'response': response}
```

##### v2 call from abonent

```python
result = client.call_from_abonent_v2('<pattern>', 'phone number') # raise BeelinePBXException or return {'response': response}
```

##### transfer call from abonent

```python
result = client.transfer_call_from_abonent('<pattern>','call_id', 'phone number') # raise BeelinePBXException or return {}
```

##### transfer call from abonent

```python
result = client.transfer_call_with_consult('<pattern>','call_id', 'call_id_consult') # raise BeelinePBXException or return {}
```

##### add extension number

```python
result = client.transfer_call_with_consult('<pattern>','phone number', 'schedule') # raise BeelinePBXException or return {}
```

##### delete extension number

```python
result = client.delete_extension_number('<pattern>') # raise BeelinePBXException or return {}
```

##### get cfb

```python
cfb_response = client.get_cfb('<pattern>') # raise BeelinePBXException or return CfbResponse
```

##### enable cfb

```python
from beeline_protal.models import Cfb

cfb = Cfb('+7397999992', '+7397999993')
cfb_response = client.get_cfb('<pattern>', cfb) # raise BeelinePBXException or return CfbResponse
```

##### stop cfb

```python
result = client.stop_cfb('<pattern>') # raise BeelinePBXException or return {}
```

##### get cfs rule list

```python
result = client.get_cfs_rules('<pattern>') # raise BeelinePBXException or return CfsStatusResponse
```

##### add cfs rule

```python
from beeline_portal.models import CfsRule

cfs_rule = CfsRule('my rule', '+7937999992', 'WORKING_TIME', ['+7937999993'])
result = client.add_cfs_rule('<pattern>', cfs_rule) # raise BeelinePBXException or return {'number': response}

```

##### enable cfs

```python
result = client.enable_cfs('<pattern>') # raise BeelinePBXException or return {}
```

##### update cfs rule

```python
from beeline_portal.models import CfsRule

cfs_rule = CfsRule('my rule', '+7937999992', 'WORKING_TIME', ['+7937999993'])
result = client.update_cfs_rule('<pattern>','cfs_id', cfs_rule) # raise BeelinePBXException or return {}
```

##### stop cfs

```python
result = client.stop_cfs('<pattern>') # raise BeelinePBXException or return {}
```

##### delete cfs rule

```python
result = client.delete_cfs_rule('<pattern>', '<cfs_id>') # raise BeelinePBXException or return {}
```

##### get bwl list

```python
result = client.get_bwl_list('<pattern>') # raise BeelinePBXException or return BwlStatusResponse
```

##### add bwl rule

```python
from beeline_portal.models import BwlRule

bwl_rule = BwlRule('BWL_RULE', 'WORKING_TIME', ['+7939797772'])
result = client.add_bwl_rule('<pattern>', 'WHITE_LIST', bwl_rule)  # raise BeelinePBXException or return {'number': response}
```

##### update bwl rule

```python
from beeline_portal.models import BwlRule

bwl_rule = BwlRule('BWL_RULE', 'WORKING_TIME', ['+7939797772'])
result = client.update_bwl_rule('<pattern>', '<bwl_id>', bwl_rule)  # raise BeelinePBXException or return {}
```

##### enable bwl

```python
result = client.enable_bwl('<pattern>', '<rule_type>') # raise BeelinePBXException or return {}
```

##### stop bwl

```python
result = client.stop_bwl('<pattern>') # raise BeelinePBXException or return {}
```

##### delete bwl rule

```python
result = client.delete_bwl_rule('<pattern>', '<bwl_id>') # raise BeelinePBXException or return {}
```

##### get call records

```python
call_records = client.get_records() #raise BeelinePBXException or return map[CallRecord]
```

##### delete call record

```python
result = client.delete_record('<record_id>') #raise BeelinePBXException or return {}
```

##### get call record

```python
call_record = client.get_record('<record_id>') #raise BeelinePBXException or return CallRecord
```

##### get call record by extratracking id

```python
call_record = client.get_record_by_extratracking_id('<extratracking_id>', '<user_id>') #raise BeelinePBXException or return CallRecord
```

##### download call record

```python
bytes_record_data = client.download_record('<record_id>') #raise BeelinePBXException or return record data in bytes
```

##### download call record by extracking id

```python
bytes_record_data = client.download_record_by_extracking_id('<extratracking_id>', '<user_id>') #raise BeelinePBXException or return record data in bytes
```

##### get call record link

```python
record_link = client.get_record_link('<record_id>') #raise BeelinePBXException or return string
```

##### get call record link by extracking id

```python
record_link = client.get_record_link_by_extracking_id('<extratracking_id>', '<user_id>') #raise BeelinePBXException or return string
```

##### get incoming numbers

```python
incoming_numbers = client.get_incoming_numbers() #raise BeelinePBXException or return map[Number]
```

##### find incoming number

```python
inc_number = client.find_incoming_number('<pattern>') #raise BeelinePBXException or return Number
```

##### create subscription

```python
from beeline_portal.models import SubscriptionRequest

sr = SubscriptionRequest('<pattern>', 23,'BASIC_CALL', '<url>')
result = client.create_subscription(sr) #raise BeelinePBXException or return dict
```

##### get subscription

```python
subs = client.get_subscription('<subscription_id>') #raise BeelinePBXException or return Subscription
```

##### stop subscription

```python
subs = client.stop_subscrption('<subscription_id>') #raise BeelinePBXException or return {}
```

##### get icr numbers

```python
icr_numbers = client.get_icr_numbers() #raise BeelinePBXException or return map[Number]
```

##### enable icr for numbers

```python
result = client.enable_icr_for_number(['+79238458793']) #raise BeelinePBXException or return map[IcrNumbersResult]
```

##### stop icr for numbers

```python
result = client.stop_icr_for_number(['+79238458793']) #raise BeelinePBXException or return map[IcrNumbersResult]
```

##### get icr route rules

```python
icr_route_rules = client.get_icr_route_rules() #raise BeelinePBXException or return map[IcrRouteRule]
```

##### delete icr route rules

```python
from beeline_portal.models import IcrRouteRule

rule = IcrRouteRule('+7923424535', '201')
icr_route_rules = client.delete_list_of_icr_rules([rule]) #raise BeelinePBXException or return map[IcrRouteResult]
```

##### add icr route rules

```python
from beeline_portal.models import IcrRouteRule

rule = IcrRouteRule('+7923424535', '201')
icr_route_rules = client.add_list_of_icr_rules([rule]) #raise BeelinePBXException or return map[IcrRouteResult]
```

##### update icr route rules

```python
from beeline_portal.models import IcrRouteRule

rule = IcrRouteRule('+7923424535', '201')
icr_route_rules = client.update_list_of_icr_rules([rule]) #raise BeelinePBXException or return map[IcrRouteResult]
```

##### get voice campaigns

```python
campaigns = client.get_voice_campaigns() #raise BeelinePBXException or return map[VoiceCampaign]
```

##### upload voice file to campaign

```python
result = client.upload_file_to_voice_campaign('<path to file>') # raise BeelinePBXException or return {"id": "<id>"}
```

##### add question voice campaign

```python
from beeline_portal.models import VoiceCampaignQuestion, Answer, DateAndTime
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
result = client.add_question_type_voice_campaign(campaign) # raise BeelinePBXException or return string number
```

##### add message voice campaign

```python
from beeline_portal.models import VoiceCampaignMessage
campaign = VoiceCampaignMessage.from_beeline_struct({
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
})
result = client.add_message_type_voice_campaign(campaign) # raise BeelinePBXException or return string number
```

##### update voice campaign

```python
from beeline_portal.models import VoiceCampaign
vc = VoiceCampaign.from_beeline_struct(
{
    "name": "MyVoiceCampaign",
    "status": "SUSPENDED",
    "recordId": "hhyth1231432",
    "type": "QUESTION",
    "answers": [{"choice": "B1", "answer": "test"}],
    "audioFile": "<link>",
    "phones": ["93799992"],
    "phoneNumber": "+799999999",
    "schedule": {
        "tryQuantity": "Q1",
        "fromHour": "H0",
        "toHour": "H4",
        "schedule": "ALL_WEEK",
    },
    "from": {"date": "2021-01-01", "time": "00:00:00"},
    "to": {"date": "2021-12-01", "time": "23:59:59"},
    "abonent": {
        "userId": "9379992@beeline.ru",
        "phone": "9379992",
        "firstName": "Ivan",
        "lastName": "Moody",
    },
})
result = client.update_voice_campaign('<campaign_id>', vc)
```

##### delete voice campaign

```python
result = client.delete_voice_campaign('<campaign_id>') # raise BeelinePBXException or return {}
```

##### stop voice campaign

```python
result = client.stop_voice_campaign('<campaign_id>') # raise BeelinePBXException or return {}
```

##### start voice campaign

```python
result = client.start_voice_campaign('<campaign_id>') # raise BeelinePBXException or return {}
```

##### get voice campaign info

```python
vc_info_report = client.get_voice_campaign_info('<campaign_id>') # raise BeelinePBXException or return VoiceCampaignInfoReport
```

##### get statistic

```python
from datetime import datetime, timedelta
date_to = datetime.now()
date_from = date_to - timedelta(days=2)

statistic = client.get_statistic('<user_id>', date_from, date_to, 0, 10) # raise BeelinePBXException or return map[StatRecord]
```

##### get v2 statistic

```python
from datetime import datetime, timedelta
date_to = datetime.now()
date_from = date_to - timedelta(days=2)

statistic = client.get_statistic_v2('<user_id>', date_from, date_to, 0, 10) # raise BeelinePBXException or return map[StatRecordV2]
```
