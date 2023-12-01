from lsquery.api import Api
from lsquery.server import Server
from lsquery.web_socket import WebSocket
from lsquery.web_socket import WebSocketMessage
from lsquery.config import Config
import time


def main() -> None:
    Config.check_config()
    try:
        # Attempt to connect to the WebSocket and also docker.
        Api()
        WebSocket()
    except Exception as err:
        print('[Docker Connect]', str(err))


if __name__ == '__main__':
    main()
