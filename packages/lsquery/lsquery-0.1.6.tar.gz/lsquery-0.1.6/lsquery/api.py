from decouple import config
from lsquery.web_socket import WebSocket
from urllib3.exceptions import InsecureRequestWarning
import requests
import socket
import warnings
import contextlib


class Api:
    def __init__(self):
        with no_ssl_verification():
            host = socket.gethostname()
            response = requests.get(f"https://{config('WEBSOCKET_HOST')}/api/v1/hosts/{host}/containers")

            WebSocket.containers = {}
            if response.status_code == 200:
                WebSocket.containers = response.json()


@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        opened_adapters.add(self.get_adapter(url))
        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False
        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass


old_merge_environment_settings = requests.Session.merge_environment_settings
