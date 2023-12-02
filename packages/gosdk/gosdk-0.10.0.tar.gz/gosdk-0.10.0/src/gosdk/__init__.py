import asyncio
import configparser
import json
import os
from importlib.resources import files

import backoff
import requests.adapters
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient

config_parser = configparser.ConfigParser()
config_parser.read("~/.gocli.ini")
if not config_parser.has_section("gocli-options"):
    config_parser.add_section("gocli-options")
config = config_parser["gocli-options"]

HOST = os.getenv("KMS_HOST") or config.get("host")
if value := os.getenv("KMS_SCHEMES") or config.get("schemes"):
    SCHEMES = value.split(",")
else:
    SCHEMES = []
TOKEN = os.getenv("KMS_TOKEN") or config.get("token")
if value := os.getenv("KMS_TIMEOUT") or config.get("timeout"):
    TIMEOUT = int(value)
else:
    TIMEOUT = 300
if value := os.getenv("KMS_CUSTOM_HEADER_OPTION") or config.get("custom_header_option"):
    HEADERS = dict([v.split("=", 1) for v in value.split(" ")])
else:
    HEADERS = {}

DEFAULT_CONFIG = {
    "validate_responses": False,
    "validate_requests": False,
    "validate_swagger_spec": False
}


def load_sdk(config=None):  # pylint: disable=redefined-outer-name
    spec_file = files('gosdk') / 'spec.json'
    spec = json.loads(spec_file.read_text())
    http_client = RequestsClient()
    config = config or DEFAULT_CONFIG

    if HOST:
        spec['host'] = HOST
    if SCHEMES:
        spec['schemes'] = SCHEMES
        for scheme in SCHEMES:
            adapter = requests.adapters.HTTPAdapter(pool_maxsize=25)
            http_client.session.mount(f'{scheme}://', adapter)
    if HOST and TOKEN:
        http_client.set_api_key(
            HOST, f'Token {TOKEN}',
            param_name='Authorization', param_in='header'
        )

    return SwaggerClient.from_spec(spec, http_client=http_client, config=config)


sdk = load_sdk()


@backoff.on_exception(
    backoff.expo,
    (OSError, ConnectionError, TimeoutError),
    max_time=600,
    max_tries=12,
)
def call_with_retry(f, **kwargs):
    return f(
        **kwargs,
        _request_options={"headers": HEADERS}
    ).response(timeout=TIMEOUT).result


@backoff.on_exception(
    backoff.expo,
    (OSError, ConnectionError, TimeoutError),
    max_time=600,
    max_tries=12,
)
async def async_call_with_retry(f, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: f(
            **kwargs,
            _request_options={"headers": HEADERS}
        ).response(timeout=TIMEOUT).result
    )
