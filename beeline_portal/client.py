from base64 import b64encode
from typing import Optional, Union, List, Any
from datetime import datetime
from urllib.parse import urlencode
from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout

from .errors import BeelinePBXException
from .models import (
    Abonent,
    BwlStatusResponse,
    BwlRule,
    Number,
    StatRecordV2,
    StatRecord,
    CfbResponse,
    Cfb,
    CfsStatusResponse,
    CfsRule,
    CallRecord,
    SubscriptionRequest,
    Subscription,
    IcrNumbersResult,
    IcrRouteRule,
    IcrRouteResult,
    VoiceCampaign,
    VoiceCampaignMessage,
    VoiceCampaignQuestion,
    VoiceCampaignInfoReport,
)


class BeelinePBX(object):
    API_URL = 'https://cloudpbx.beeline.ru/apis/portal/'

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = self._init_session()

    def _init_session(self) -> Session:
        session = Session()
        session.headers['X-MPBX-API-AUTH-TOKEN'] = self.access_token
        return session

    def _generate_request_url(
        self, endpoint: str, params: Optional[dict] = None
    ) -> str:
        url = f'{self.API_URL}{endpoint}'
        if params:
            url = f'{url}?{urlencode(params)}'
        return url

    def _send_api_request(
        self,
        http_method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Union[Optional[dict], Optional[list], Optional[str]] = None,
        file_: bool = False,
        audio_file: bool = False,
    ) -> Any:
        url = self._generate_request_url(endpoint, params)
        method = getattr(self.session, http_method)
        try:
            r = method(url, json=data) if not audio_file else method(url, data=data)
            try:
                response = r.json() if not file_ else r.content
            except JSONDecodeError:
                return r.text
            if r.status_code > 204:
                raise BeelinePBXException(response)
            return response
        except (ConnectionError, ConnectTimeout):
            raise BeelinePBXException(
                {
                    'errorCode': 500,
                    'description': 'Connection Error or cant',
                }
            )

    def get_abonents(self) -> map:
        response = self._send_api_request('get', 'abonents')
        return map(Abonent.from_beeline_struct, response)

    def find_abonent(self, pattern: str) -> Abonent:
        response = self._send_api_request('get', f'abonents/{pattern}')
        return Abonent.from_beeline_struct(response)

    def get_abonent_agent_status(self, pattern: str) -> dict:
        status = self._send_api_request('get', f'abonents/{pattern}/agent')
        return {'status': status}

    def set_abonent_agent_status(self, pattern: str, status: str) -> dict:
        _ = self._send_api_request(
            'put', f'abonents/{pattern}/agent', data={'status': status}
        )
        return {}

    def get_abonent_recording_status(self, pattern: str) -> dict:
        status = self._send_api_request('get', f'abonents/{pattern}/recording')
        return {'status': status}

    def enable_abonent_recording(self, pattern: str) -> dict:
        _ = self._send_api_request('put', f'abonents/{pattern}/recording')
        return {}

    def stop_abonent_recording(self, pattern: str) -> dict:
        _ = self._send_api_request('delete', f'abonents/{pattern}/recording')
        return {}

    def call_from_abonent(self, pattern: str, phone_number: str) -> dict:
        response = self._send_api_request(
            'post', f'abonents/{pattern}/call', {'phoneNumber': phone_number}
        )
        return {'response': response}

    def call_from_abonent_v2(self, pattern: str, phone_number: str) -> dict:
        response = self._send_api_request(
            'post', f'v2/abonents/{pattern}/call', {'phoneNumber': phone_number}
        )
        return {'response': response}

    def transfer_call_from_abonent(
        self, pattern: str, call_id: str, phone_number: str
    ) -> dict:
        _ = self._send_api_request(
            'post',
            f'abonents/{pattern}/callTransfer',
            {'callId': call_id, 'phoneNumber': phone_number},
        )
        return {}

    def transfer_call_with_consult(
        self, pattern: str, call_id: str, call_id_consult: str
    ) -> dict:
        _ = self._send_api_request(
            'post',
            f'abonents/{pattern}/callTransferConsult',
            {'callId': call_id, 'callIdConsult': call_id_consult},
        )
        return {}

    def add_extension_number(
        self, pattern: str, phone_number: str, schedule: str
    ) -> dict:
        _ = self._send_api_request(
            'put',
            f'abonents/{pattern}/number',
            {'phoneNumber': phone_number, 'schedule': schedule},
        )
        return {}

    def delete_extension_number(self, pattern: str) -> dict:
        _ = self._send_api_request(
            'delete',
            f'abonents/{pattern}/number',
        )
        return {}

    def get_cfb(self, pattern: str) -> CfbResponse:
        response = self._send_api_request('get', f'abonents/{pattern}/cfb')
        return CfbResponse.from_beeline_struct(response)

    def enable_cfb(self, pattern: str, cfb: Cfb) -> dict:
        _ = self._send_api_request(
            'put', f'abonents/{pattern}/cfb', data=cfb.to_beeline_struct()
        )
        return {}

    def stop_cfb(self, pattern: str) -> dict:
        _ = self._send_api_request(
            'delete',
            f'abonents/{pattern}/cfb',
        )
        return {}

    def get_cfs_rules(self, pattern: str) -> CfsStatusResponse:
        response = self._send_api_request('get', f'abonents/{pattern}/cfs')
        return CfsStatusResponse.from_beeline_struct(response)

    def add_cfs_rule(self, pattern: str, cfs_rule: CfsRule) -> dict:
        response = self._send_api_request(
            'post', f'abonents/{pattern}/cfs', data=cfs_rule.to_beeline_struct()
        )
        return {'number': response}

    def enable_cfs(self, pattern: str) -> dict:
        _ = self._send_api_request('put', f'abonents/{pattern}/cfs')
        return {}

    def update_cfs_rule(self, pattern: str, cfs_id: str, cfs_rule: CfsRule) -> dict:
        _ = self._send_api_request(
            'put', f'abonents/{pattern}/cfs/{cfs_id}', data=cfs_rule.to_beeline_struct()
        )
        return {}

    def stop_cfs(self, pattern: str) -> dict:
        _ = self._send_api_request('delete', f'abonents/{pattern}/cfs')
        return {}

    def delete_cfs_rule(self, pattern: str, cfs_id: str) -> dict:
        _ = self._send_api_request('delete', f'abonents/{pattern}/cfs/{cfs_id}')
        return {}

    def get_bwl_list(self, pattern: str) -> BwlStatusResponse:
        response = self._send_api_request('get', f'abonents/{pattern}/bwl')
        return BwlStatusResponse.from_beeline_struct(response)

    def add_bwl_rule(self, pattern: str, type_: str, bwl_rule: BwlRule) -> dict:
        response = self._send_api_request(
            'post',
            f'abonents/{pattern}/bwl',
            data={'type': type_, 'rule': bwl_rule.to_beeline_struct()},
        )
        return {'number': response}

    def update_bwl_rule(self, pattern: str, bwl_id: str, bwl_rule: BwlRule) -> dict:
        _ = self._send_api_request(
            'post',
            f'abonents/{pattern}/bwl/{bwl_id}',
            data=bwl_rule.to_beeline_struct(),
        )
        return {}

    def enable_bwl(self, pattern: str, rule_type: str) -> dict:
        _ = self._send_api_request(
            'put', f'abonents/{pattern}/bwl', {'ruleType': rule_type}
        )
        return {}

    def stop_bwl(self, pattern: str) -> dict:
        _ = self._send_api_request('delete', f'abonents/{pattern}/bwl')
        return {}

    def delete_bwl_rule(self, pattern: str, bwl_id: str) -> dict:
        _ = self._send_api_request('delete', f'abonents/{pattern}/bwl/{bwl_id}')
        return {}

    def get_records(self) -> map:
        response = self._send_api_request('get', 'records')
        return map(CallRecord.from_beeline_struct, response)

    def delete_record(self, record_id: str) -> dict:
        _ = self._send_api_request('delete', f'v2/records/{record_id}')
        return {}

    def get_record(self, record_id: str) -> CallRecord:
        response = self._send_api_request('get', f'v2/records/{record_id}')
        return CallRecord.from_beeline_struct(response)

    def get_record_by_extratracking_id(
        self, extratracking_id: str, user_id: str
    ) -> CallRecord:
        response = self._send_api_request(
            'get', f'v2/records/{extratracking_id}/{user_id}'
        )
        return CallRecord.from_beeline_struct(response)

    def download_record(self, record_id: str) -> bytes:
        response = self._send_api_request(
            'get', f'v2/records/{record_id}/download', file_=True
        )
        return response

    def download_record_by_extracking_id(
        self, extracking_id: str, user_id: str
    ) -> bytes:
        response = self._send_api_request(
            'get', f'v2/records/{extracking_id}/{user_id}/download', file_=True
        )
        return response

    def get_record_link(self, record_id: str) -> str:
        response = self._send_api_request('get', f'v2/records/{record_id}/reference')
        return response

    def get_record_link_by_extracking_id(self, extracking_id: str, user_id: str) -> str:
        response = self._send_api_request(
            'get', f'v2/records/{extracking_id}/{user_id}/reference'
        )
        return response

    def get_incoming_numbers(self) -> map:
        response = self._send_api_request('get', 'numbers')
        return map(Number.from_beeline_struct, response)

    def find_incoming_number(self, pattern: str) -> Number:
        response = self._send_api_request('get', f'numbers/{pattern}')
        return Number.from_beeline_struct(response)

    def create_subscription(self, subscription: SubscriptionRequest) -> dict:
        response = self._send_api_request(
            'put', 'subscription', data=subscription.to_beeline_struct()
        )
        return response

    def get_subscription(self, subscription_id: str) -> Subscription:
        response = self._send_api_request(
            'get', 'subscription', params={'subscriptionId': subscription_id}
        )
        return Subscription.from_beeline_struct(response)

    def stop_subscrption(self, subscription_id: str) -> dict:
        _ = self._send_api_request(
            'delete', 'subscription', params={'subscriptionId': subscription_id}
        )
        return {}

    def get_icr_numbers(self) -> map:
        response = self._send_api_request('get', 'icr/numbers')
        return map(Number.from_beeline_struct, response)

    def enable_icr_for_number(self, numbers: list) -> map:
        response = self._send_api_request('put', 'icr/numbers', data=numbers)
        return map(IcrNumbersResult.from_beeline_struct, response)

    def stop_icr_for_number(self, numbers: list) -> map:
        response = self._send_api_request('delete', 'icr/numbers', data=numbers)
        return map(IcrNumbersResult.from_beeline_struct, response)

    def get_icr_route_rules(self) -> map:
        response = self._send_api_request('get', '/icr/route')
        return map(IcrRouteRule.from_beeline_struct, response)

    def _list_icr_rules_operation(
        self, operation: str, icr_rules: List[IcrRouteRule]
    ) -> map:
        response = self._send_api_request(
            operation,
            '/icr/route',
            data=[rule.to_beeline_struct() for rule in icr_rules],
        )
        return map(IcrRouteResult.from_beeline_struct, response)

    def delete_list_of_icr_rules(self, icr_rules: List[IcrRouteRule]) -> map:
        return self._list_icr_rules_operation('delete', icr_rules)

    def add_list_of_icr_rules(self, icr_rules: List[IcrRouteRule]) -> map:
        return self._list_icr_rules_operation('post', icr_rules)

    def update_list_of_icr_rules(self, icr_rules: List[IcrRouteRule]) -> map:
        return self._list_icr_rules_operation('put', icr_rules)

    def get_voice_campaigns(self) -> map:
        response = self._send_api_request('get', 'vc')
        return map(VoiceCampaign.from_beeline_struct, response)

    def upload_file_to_voice_campaign(self, path_to_file: str) -> dict:
        with open(path_to_file, 'rb') as f:
            b64_str = b64encode(f.read()).decode()
            response: dict = self._send_api_request(
                'post', 'vc/upload', data=b64_str, audio_file=True
            )
            return {'id': response['id']}

    def add_question_type_voice_campaign(self, campaign: VoiceCampaignQuestion) -> str:
        response = self._send_api_request(
            'post', 'vc/question', data=campaign.to_beeline_struct()
        )
        return response

    def add_message_type_voice_campaign(self, campaign: VoiceCampaignMessage) -> str:
        response = self._send_api_request(
            'post', 'vc/message', data=campaign.to_beeline_struct()
        )
        return response

    def update_voice_campaign(self, campaign_id: str, campaign: VoiceCampaign) -> dict:
        _ = self._send_api_request(
            'put', f'vc/{campaign_id}', data=campaign.to_beeline_struct()
        )
        return {}

    def delete_voice_campaign(self, campaign_id: str) -> dict:
        _ = self._send_api_request(
            'delete',
            f'vc/{campaign_id}',
        )
        return {}

    def stop_voice_campaign(self, campaign_id: str) -> dict:
        _ = self._send_api_request(
            'put',
            f'vc/stop/{campaign_id}',
        )
        return {}

    def start_voice_campaign(self, campaign_id: str) -> dict:
        _ = self._send_api_request(
            'put',
            f'vc/start/{campaign_id}',
        )
        return {}

    def get_voice_campaign_info(self, campaign_id: str) -> VoiceCampaignInfoReport:
        response = self._send_api_request(
            'get',
            f'vc/info/{campaign_id}',
        )
        return VoiceCampaignInfoReport.from_beeline_struct(response)

    def get_statistic(
        self,
        user_id: str,
        date_from: datetime,
        date_to: datetime,
        page: int = 0,
        page_size: int = 100,
    ) -> map:
        params = {
            'userId': user_id,
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'dateTo': date_to.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'page': page,
            'pageSize': page_size,
        }
        response = self._send_api_request('get', 'statistics', params)
        return map(StatRecord.from_beeline_struct, response)

    def get_v2_statistic(
        self,
        user_id: str,
        date_from: datetime,
        date_to: datetime,
        page: int = 0,
        page_size: int = 100,
    ) -> map:
        params = {
            'userId': user_id,
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'dateTo': date_to.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'page': page,
            'pageSize': page_size,
        }
        response = self._send_api_request('get', 'v2/statistics', params)
        return map(StatRecordV2.from_beeline_struct, response)
