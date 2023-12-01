# Installation
The project is used to spin up docker game servers.

You require both [python 3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) installed to run this command.

To install: ``pip install lsquery``

Once installed you should be able to run it as a python module: ``python3 -m lsquery``

# Requirements

These requirements should automatically be installed by pip, but incase they aren't you can run this command.

```
pip install asyncio==3.4.3 docker==6.1.3 opengsq~=1.4.3 python-decouple~=3.6 pytz~=2022.6 rcon~=2.1.1 websocket-client==1.4.2 websockets~=10.4
```

# Configuration

The project depends on three environment variables. A sample environment file has been provided.

env.example
```
DOCKER_HOST=
WEBSOCKET_HOST=
WEBSOCKET_APP_KEY=
```

When you first run the module, it will check if these environment variables have been set. 
If not, it will prompt the user for each value. If the system detects a default value, it will suggest using it.

If you ever want to reconfigure these values, you can run: ``python3 -m lsquery -c``

| Environment Variable | Description              | Sample Values                                           |
|----------------------|--------------------------|---------------------------------------------------------|
| DOCKER_HOST          | Docker Host              | unix:///var/run/docker.sock<br/>tcp://192.168.1.11:2376 |
| WEBSOCKET_HOST       | Websocket Host           | portal.lanslide.com.au                                  |
| WEBSOCKET_APP_KEY    | Websocket Application Key | -                                                       |

# Post Installation

You may want to consider running this package as a service. Here is a sample portal.service script<br/>
Note: [screen](https://linux.die.net/man/1/screen) must be installed.

/etc/systemd/system/portal.service
```
[Unit]
Description=Portal Service
After=multi-user.target

[Service]
Type=forking
Restart=on-failure
ExecStart=/usr/bin/screen -L -dmS portal /usr/bin/python3 -m lsquery
ExecStop=/usr/bin/screen -X -S portal quit

[Install]
WantedBy=multi-user.target
```

To enable this service on start up you can run
``systemctl enable portal``

To start this service you can run
``systemctl start portal``