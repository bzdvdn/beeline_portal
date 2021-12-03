from typing import Optional, Union, List
from datetime import datetime
from urllib.parse import urlencode
from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout

from .errors import BeelinePBXException
from .models import Abonent, StatRecordV2, StatRecord


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
        data: Optional[dict] = None,
    ) -> Union[dict, list]:
        url = self._generate_request_url(endpoint, params)
        method = getattr(self.session, http_method)
        try:
            r = method(url, json=data)
            response = r.json()
            if r.status_code > 204:
                raise BeelinePBXException(response)
            return response
        except (ConnectionError, ConnectTimeout):
            raise BeelinePBXException(
                {'errorCode': 500, 'description': 'Connection Error or cant',}
            )
        except JSONDecodeError:
            return r.text

    def get_abonents(self) -> List[Abonent]:
        response = self._send_api_request('get', 'abonents')
        return [Abonent.from_dict(row) for row in response]

    def find_abonent(self, pattern: str) -> Abonent:
        response = self._send_api_request('get', f'abonents/{pattern}')
        return Abonent.from_dict(response)  # type: ignore

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
        _ = self._send_api_request('delete', f'abonents/{pattern}/number',)
        return {}

    def get_statistic(
        self,
        user_id: str,
        date_from: datetime,
        date_to: datetime,
        page: int = 0,
        page_size: int = 100,
    ) -> map[StatRecord]:
        params = {
            'userId': user_id,
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'dateTo': date_to.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'page': page,
            'pageSize': page_size,
        }
        response = self._send_api_request('get', 'statistics', params)
        return map(StatRecord.from_dict, response)

    def get_v2_statistic(
        self,
        user_id: str,
        date_from: datetime,
        date_to: datetime,
        page: int = 0,
        page_size: int = 100,
    ) -> map[StatRecordV2]:
        params = {
            'userId': user_id,
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'dateTo': date_to.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'page': page,
            'pageSize': page_size,
        }
        response = self._send_api_request('get', 'v2/statistics', params)
        return map(StatRecordV2.from_dict, response)
