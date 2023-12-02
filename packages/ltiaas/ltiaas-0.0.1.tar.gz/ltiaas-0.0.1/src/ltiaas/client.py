from datetime import datetime
from enum import Enum
from typing import Optional, Union
from urllib.parse import quote_plus

from requests import RequestException, Session
from requests.exceptions import JSONDecodeError

from .exceptions import LTIaaSClientAPIError, LtikSessionRequired


class LTIaaSClient:

    class SessionType(str, Enum):
        LTIK = 1
        SERVICE_KEY = 2

    class HttpMethod(str, Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        PATCH = 'PATCH'
        DELETE = 'DELETE'

    _LTIK_AUTH_HEADER_TEMPLATE = 'LTIK-AUTH-V2 {api_key}:{ltik}'
    _SERVICE_AUTH_HEADER_TEMPLATE = 'SERVICE-AUTH-V1 {api_key}:{service_key}'

    _ltiaas_url: str
    _session: Session
    _session_type: SessionType

    def __init__(self, ltiaas_domain: str, api_key: str, ltik: Optional[str] = None, service_key: Optional[str] = None):
        if not (ltik or service_key):
            raise ValueError('Either "ltik" or "service_key" must be provided.')

        self._ltiaas_url = f'https://{ltiaas_domain}'
        self._session = Session()

        if ltik:
            self._session_type = self.SessionType.LTIK
            authorization_header = self._build_ltik_authorization_header(api_key, ltik)
        else:
            self._session_type = self.SessionType.SERVICE_KEY
            authorization_header = self._build_service_key_authorization_header(api_key, service_key)

        self._session.headers.update({'Authorization': authorization_header})

    def _build_ltik_authorization_header(self, api_key: str, ltik: str) -> str:
        return self._LTIK_AUTH_HEADER_TEMPLATE.format(api_key=api_key, ltik=ltik)

    def _build_service_key_authorization_header(self, api_key: str, service_key: str) -> str:
        return self._SERVICE_AUTH_HEADER_TEMPLATE.format(api_key=api_key, service_key=service_key)

    def _build_client_error(self, error: RequestException) -> LTIaaSClientAPIError:
        try:
            body = error.response.json()
            return LTIaaSClientAPIError(
                status_code=body['status'], error=body['error'], details=body.get('details', {}))
        except (JSONDecodeError, KeyError):
            return LTIaaSClientAPIError(
                status_code=error.response.status_code, error=error.response.reason,
                details={'message': error.response.text})

    def _remove_null_fields(self, original: Optional[dict]) -> Optional[dict]:
        return {k: v for k, v in original.items() if v is not None} if original else None

    def _build_deep_linking_options(self, message: Optional[str] = None, log: Optional[str] = None,
                                    error_message: Optional[str] = None, error_log: Optional[str] = None) -> dict:
        options = {}
        if message:
            options['message'] = message
        if log:
            options['log'] = log
        if error_message:
            options['errMessage'] = error_message
        if error_log:
            options['errLog'] = error_log
        return options

    def _make_request(self, method: HttpMethod, path: str, **kwargs) -> Optional[dict]:
        url = f'{self._ltiaas_url}{path}'
        try:
            kwargs['json'] = self._remove_null_fields(kwargs.get('json'))
            kwargs['params'] = self._remove_null_fields(kwargs.get('params'))
            response = self._session.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            return response.json()
        except JSONDecodeError:
            # We don't want to raise an exception here because this means that we got an empty 2xx response
            pass
        except RequestException as e:
            raise self._build_client_error(e) from e
        
    def _validate_ltik_session(self) -> None:
        if self._session_type != self.SessionType.LTIK:
            raise LtikSessionRequired()

    def retrieve_id_token(self, raw: Optional[bool] = False) -> dict:
        self._validate_ltik_session()
        return self._make_request(method=self.HttpMethod.GET, path='/api/idtoken', params={'raw': raw})

    def retrieve_memberships(self, role: Optional[str] = None, resource_link_id: Optional[str] = None,
                             page: Optional[str] = None, page_size: Optional[int] = None) -> dict:
        query_parameters = {
            'role': role,
            'resourceLinkId': resource_link_id,
            'url': quote_plus(page) if page else None,
            'limit': page_size
        }
        return self._make_request(method=self.HttpMethod.GET, path='/api/memberships', params=query_parameters)

    def retrieve_line_items(self, resource_id: Optional[str] = None, resource_link_id: Optional[str] = None,
                            tag: Optional[str] = None, page: Optional[str] = None,
                            page_size: Optional[int] = None) -> dict:
        query_parameters = {
            'resourceId': resource_id,
            'resourceLinkId': resource_link_id,
            'tag': tag,
            'url': quote_plus(page) if page else None,
            'limit': page_size
        }
        return self._make_request(method=self.HttpMethod.GET, path='/api/lineitems', params=query_parameters)

    def create_line_item(self, label: str, score_maximum: Union[int, float], resource_id: Optional[str] = None,
                         resource_link_id: Optional[str] = None, tag: Optional[str] = None,
                         start_date_time: Optional[datetime] = None, end_date_time: Optional[datetime] = None,
                         grades_released: Optional[bool] = None) -> dict:
        body = {
            'label': label,
            'scoreMaximum': score_maximum,
            'resourceId': resource_id,
            'resourceLinkId': resource_link_id,
            'tag': tag,
            'startDateTime': start_date_time.isoformat() if start_date_time else None,
            'endDateTime': end_date_time.isoformat() if end_date_time else None,
            'gradesReleased': grades_released
        }
        return self._make_request(method=self.HttpMethod.POST, path='/api/lineitems', json=body)

    def retrieve_line_item(self, line_item_id: str) -> dict:
        request_path = f'/api/lineitems/{quote_plus(line_item_id)}'
        return self._make_request(method=self.HttpMethod.GET, path=request_path)

    def update_line_item(self, line_item_id: str, label: str, score_maximum: Union[int, float],
                         resource_id: Optional[str] = None, resource_link_id: Optional[str] = None,
                         tag: Optional[str] = None, start_date_time: Optional[datetime] = None,
                         end_date_time: Optional[datetime] = None, grades_released: Optional[bool] = None) -> dict:
        body = {
            'label': label,
            'scoreMaximum': score_maximum,
            'resourceId': resource_id,
            'resourceLinkId': resource_link_id,
            'tag': tag,
            'startDateTime': start_date_time.isoformat() if start_date_time else None,
            'endDateTime': end_date_time.isoformat() if end_date_time else None,
            'gradesReleased': grades_released
        }
        request_path = f'/api/lineitems/{quote_plus(line_item_id)}'
        return self._make_request(method=self.HttpMethod.PUT, path=request_path, json=body)

    def delete_line_item(self, line_item_id: str) -> None:
        request_path = f'/api/lineitems/{quote_plus(line_item_id)}'
        self._make_request(method=self.HttpMethod.DELETE, path=request_path)

    def retrieve_scores(self, line_item_id: str, user_id: Optional[Union[int, str]] = None, page: Optional[str] = None,
                        page_size: Optional[int] = None) -> dict:
        query_parameters = {
            'userId': user_id,
            'url': quote_plus(page) if page else None,
            'limit': page_size
        }
        request_path = f'/api/lineitems/{quote_plus(line_item_id)}/scores'
        return self._make_request(method=self.HttpMethod.GET, path=request_path, params=query_parameters)

    def submit_score(self, line_item_id: str, user_id: Union[int, str], activity_progress: str, grading_progress: str,
                     score_given: Optional[Union[int, float]] = None, score_maximum: Optional[Union[int, float]] = None,
                     comment: Optional[str] = None, **kwargs) -> None:
        body = {
            'userId': user_id,
            'activityProgress': activity_progress,
            'gradingProgress': grading_progress,
            'scoreGiven': score_given,
            'scoreMaximum': score_maximum,
            'comment': comment
        }
        body.update(kwargs)
        request_path = f'/api/lineitems/{quote_plus(line_item_id)}/scores'
        self._make_request(method=self.HttpMethod.POST, path=request_path, json=body)

    def create_deep_linking_form(self, content_items: list[dict], message: Optional[str] = None,
                                 log: Optional[str] = None, error_message: Optional[str] = None,
                                 error_log: Optional[str] = None) -> dict:
        options = self._build_deep_linking_options(message, log, error_message, error_log)
        body = {
            'contentItems': content_items,
            'options': options
        }
        options
        return self._make_request(method=self.HttpMethod.POST, path='/api/deeplinking/form', json=body)

    def create_deep_linking_form_components(self, content_items: list[dict], message: Optional[str] = None,
                                            log: Optional[str] = None, error_message: Optional[str] = None,
                                            error_log: Optional[str] = None) -> dict:
        options = self._build_deep_linking_options(message, log, error_message, error_log)
        body = {
            'contentItems': content_items,
            'options': options
        }
        return self._make_request(method=self.HttpMethod.POST, path='/api/deeplinking', json=body)
