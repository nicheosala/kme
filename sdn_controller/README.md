# SDN Controller

The SDN Controller is the network entity in charge of keep the updated configuration of the network and to modify it
when needed, create the connection between two SAEs through their respective KMEs and to optimize the network and
keys consumption basing on statistics provided by the various KMEs.

# Execution

If you want to start the SDN Controller, open a terminal inside `qkd` folder and then type:

```bash
python -m sdn_controller
```

You can also modify the settings in the [config file](configs/config.ini) depending on your needs.

This will start the [FastAPI](https://fastapi.tiangolo.com/) app, ready to register new KMEs.

# API

The SDN Controller exposes some RESTApi towards the various *SDN Agents* inside the registered KMEs:
* *new_kme* to add a new KME to the network, saving its information in the local database
* *new_app* to register a new SAE which wants to open a connection towards another one, getting a KSID