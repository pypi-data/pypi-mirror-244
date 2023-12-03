import hashlib
import os
from dataclasses import dataclass
from datetime import datetime
from json import dumps
from logging import getLogger
from zoneinfo import ZoneInfo

import requests

logger = getLogger(__name__)


def _hash(value: str) -> str:
    return hashlib.sha1(value.encode()).hexdigest()


class WapiError(Exception):
    pass


@dataclass
class WapiResponse:
    code: int
    result: str
    timestamp: int
    svTRID: str
    command: str
    data: dict


class WapiClient:
    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        test=False,
        url="https://api.wedos.com/wapi/json",
    ) -> None:
        if user is None:
            user = os.environ["WAPI_USER"]
        if password is None:
            password = os.environ["WAPI_PASSWORD"]
        self.user = user
        self.hashed_password = _hash(password)
        self.test = test
        self.url = url

    @property
    def _auth(self):
        hour = datetime.now(tz=ZoneInfo("Europe/Prague")).hour
        return _hash(f"{self.user}{self.hashed_password}{hour:02}")

    def request(self, command, **data) -> dict:
        request = {
            "request": {
                "user": self.user,
                "auth": self._auth,
                "command": command,
                "data": data,
                "test": int(self.test),
            }
        }
        response = requests.post(self.url, data={"request": dumps(request)})
        response_data = response.json()["response"]
        if response_data["result"] != "OK":
            raise WapiError(response_data)
        return WapiResponse(**response_data)  # type: ignore

    # Shortcuts for some commands

    def ping(self):
        return self.request("ping")

    def domains_list(self):
        return self.request("domains-list")

    def dns_rows_list(self, domain: str):
        return self.request("dns-rows-list", domain=domain)

    def dns_row_update(self, domain: str, row_id: int, rdata: str, ttl: int = 300):
        return self.request(
            "dns-row-update", domain=domain, row_id=row_id, rdata=rdata, ttl=ttl
        )

    def dns_domain_commit(self, name: str):
        return self.request("dns-domain-commit", name=name)
