from abc import abstractmethod
from typing import Union, Any, Optional, Dict, List

import httpx
from httpx import Request, Response

from use_nacos.endpoints import ConfigEndpoint
from use_nacos.typings import SyncAsync


class BaseClient:

    def __init__(
            self,
            client: Union[httpx.Client, httpx.AsyncClient]
    ):
        self._clients: List[Union[httpx.Client, httpx.AsyncClient]] = []
        self.client = client
        self.config = ConfigEndpoint(self)

    @property
    def client(self) -> Union[httpx.Client, httpx.AsyncClient]:
        return self._clients[-1]

    @client.setter
    def client(self, client: Union[httpx.Client, httpx.AsyncClient]) -> None:
        client.base_url = httpx.URL("http://testing.ceegdev.com:8848")
        client.timeout = httpx.Timeout(timeout=60_000 / 1_000)
        client.headers = httpx.Headers(
            {
                "User-Agent": "use-py/use-nacos",
            }
        )
        self._clients.append(client)

    def _build_request(
            self,
            method: str,
            path: str,
            query: Optional[Dict[Any, Any]] = None,
            body: Optional[Dict[Any, Any]] = None
    ) -> Request:
        headers = httpx.Headers()
        return self.client.build_request(
            method, path, params=query, json=body, headers=headers
        )

    def _parse_response(self, response: Response) -> Any:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            pass

        body = response.json()
        return body

    @abstractmethod
    def request(
            self,
            path: str,
            method: str,
            query: Optional[Dict[Any, Any]] = None,
            body: Optional[Dict[Any, Any]] = None
    ) -> SyncAsync[Any]:
        raise NotImplementedError


class Client(BaseClient):
    client: httpx.Client

    def __init__(
            self,
            client: Optional[httpx.Client] = None):
        if client is None:
            client = httpx.Client()
        super().__init__(client)

    def request(
            self,
            path: str,
            method: str = "GET",
            query: Optional[Dict[Any, Any]] = None,
            body: Optional[Dict[Any, Any]] = None
    ) -> Any:
        request = self._build_request(method, path, query, body)
        try:
            response = self.client.send(request)
        except httpx.TimeoutException:
            raise
        return self._parse_response(response)
