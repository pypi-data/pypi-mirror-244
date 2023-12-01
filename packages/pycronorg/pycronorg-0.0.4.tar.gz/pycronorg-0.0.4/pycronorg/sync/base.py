import requests
from abc import ABC
from typing import Optional

from pycronorg.exceptions import ResponseExecption


class BaseApi(ABC):
    _AUTH_KEY = 'Authorization'
    _DEFAULT_BASE_HOST = 'https://api.cron-job.org'
    _DEFAULT_BASE_PATH = ''
    _DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
    }

    def __init__(
        self, 
        token: str, 
        *, 
        base_host: Optional[str] = None, 
        base_path: Optional[str] = None, 
        headers: Optional[dict] = None,
        proxy_request = None,
    ) -> None:
        self._token = token
        self._headers = headers or self._DEFAULT_HEADERS
        self._headers[self._AUTH_KEY] = f'Bearer {self._token}'
        self._base_host = base_host or self._DEFAULT_BASE_HOST
        self._base_path = base_path or self._DEFAULT_BASE_PATH
        self._url = f"{self._base_host}/{self._base_path}"
        self._proxy_request = proxy_request or requests

    def _safe_response(self, res: requests.Response):
        if not res.ok:
            raise ResponseExecption(f"[{res.status_code}][`{res.url}`]: `{res.text}`")

        return res

