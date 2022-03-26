# Software-Defined QKD Node

The module is mainly composed by the [FastAPI](https://fastapi.tiangolo.com/) app which 
exposes some RESTApi on two sides ([routers](routers) module):
- One side for the SAEs that want to connect with a secure channel with other SAEs
- One side for the control plane of the SDN Controller

There is also a [database](database) module which is again divided in two parts:

- The local database, which stores the keys provided by the `qcs`
- The shared database, shared between the pair of nodes that share also the `qcs`
and which stores information about the keys provided to the SAEs

## Execution

If you want to start the SD-QKD node you must first execute the SDN Controller.\
Once the Controller is started, open a terminal inside `qkd` folder and then type:

```bash
python -m sd_qkd_node
```

Use the `--config node_name` (ex. *alice*, that is the default configuration)
flag to select the desired configuration in the [config file](configs/config.ini).

This will start a server (in the [channel](channel) module) listening for the related `qcs`
and then the [FastAPI](https://fastapi.tiangolo.com/) app that connects to the Controller.

## API

The [routers](routers) module is divided in two submodules:
* The *Key Manager Entity* ([kme](routers/kme)) module which handles the SAEs requests
* The *SDN Agent* ([sdn_agent](routers/sdn_agent)) module which manages the control messages 
 exchanged with the *SDN Controller*

### KME

The Kme module exposes towards the SAEs these APIs: 
* *enc_keys* called by the master SAE to make the kme reserve a number of keys with a specified length
* *dec_keys* called by the slave SAE to get the keys reserved by the kme upon the request of the master SAE
* *status* to get the status of the connection

### SDN Agent

The SDN Agent exposes these APIs:
* *open_key_session* called by a SAE who wants to start a connection with another one
* *assign_ksid* invoked by the Controller to assign a Key Stream ID to a connection,
when also the second SAE has been registered 