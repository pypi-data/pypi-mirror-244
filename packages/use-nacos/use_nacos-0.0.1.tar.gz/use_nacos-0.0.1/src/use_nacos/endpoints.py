from typing import Optional, Any

from use_nacos.typings import SyncAsync


class Endpoint:
    def __init__(self, parent: "BaseClient") -> None:
        self.parent = parent


class ConfigEndpoint(Endpoint):

    def get(
            self,
            data_id: str,
            group: str,
            tenant: Optional[str] = 'public',
    ) -> SyncAsync[Any]:
        return self.parent.request(
            "/nacos/v1/cs/configs",
            query={
                "dataId": data_id,
                "group": group,
                "tenant": tenant,
            }
        )

    def publish(
            self,
            data_id: str,
            group: str,
            content: str,
            tenant: Optional[str] = 'public',
            type: Optional[str] = None,
    ) -> SyncAsync[Any]:
        return self.parent.request(
            "/nacos/v1/cs/configs",
            method="POST",
            query={
                "dataId": data_id,
                "group": group,
                "tenant": tenant,
                "content": content,
                "type": type,
            }
        )
