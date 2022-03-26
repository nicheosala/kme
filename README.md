# Quantum Key Distribution

This project is about Quantum Key Distribution (QKD).\
It is divided into the following packages:

- a [Software-Defined QKD Node (SD-QKD node)](sd_qkd_node/README.md)
- a [Quantum Channel Simulator (QCS)](qcs/README.md)
- an [SDN Controller](sdn_controller/README.md)

In summary, SD-QKD node receives requests from applications that want to use
quantum-generated secret keys. QCS is a simulator of a quantum channel that
produces quantum secret keys. The SDN Controller is in charge of managing 
the new connections and the network optimizations.

## Installation

1. (Optional) This project **requires Python 3.10 or higher.** If you don't
   have Python 3.10 installed system-wide, you may want to install it
   through [pyenv](https://realpython.com/intro-to-pyenv/).
2. [Install Poetry](https://python-poetry.org/docs/master/#installation)
3. In a terminal inside folder 'qkd', install project dependencies:

```bash
poetry install
```

## Execution

All the following commands must be executed in a terminal positioned inside
folder `qkd`.

First start the SDN Controller through the command:
```bash
poetry run python -m sdn_controller
```

Then to start a key management entity:

```bash
poetry run python -m sd_qkd_node
```

This will start a default configuration (called *Alice*) in the [config file](sd_qkd_node/configs/config.ini).\
You can change or add any configuration to the file and then run them with the following command:

```bash
poetry run python -m sd_qkd_node --config configuration_name
```

Then for each pair of `sd_qkd_nodes` you have to start a `qcs` (important: **add and check the configurations
for each `qcs` in the [config file](qcs/config.ini)**).\
Start a `qcs` with the command:

```bash
poetry run python -m qcs
```
Also here use the `--config first_node-second_node` flag to select the desired configuration (default is *Alice-Bob*).

## Testing

Testing is performed exploiting two tools: [Pytest](https://docs.pytest.org)
and [MyPy](https://mypy.readthedocs.io).\
Pytest executes the tests written by the programmers.\
MyPy statically checks type hints in the code.

### Manual testing

First, set the testing environment.

On Linux/MacOS:

```bash
export env=test
```

On Windows:

```shell
set env=test
```

Then, if you want to test with pytest:

```bash
poetry run pytest
```

If you want to test with mypy:

```bash
poetry run mypy sd_qkd_node qcs sdn_controller
```

### Automated testing

If you want to perform all the tests that are also performed when pushing new
modifications to GitHub:

1. [Install Act](https://github.com/nektos/act)
2. Run 'act' (**Please note**: When you run 'act' for the first time, you have
   to select 'medium' as default image):

```bash
act
```

## Sources

- https://www.etsi.org/committee/1430-qkd

## People

- [Nicolò Sala](mailto:nicolo4.sala@mail.polimi.it), graduate student
- [Riccardo Bassi](mailto:riccardo4.bassi@mail.polimi.it), graduate student
- [Paolo Martelli](mailto:paolo.martelli@polimi.it), supervisor
- [Marco Brunero](mailto:marco.brunero@polimi.it), project contact person
- [Alberto Gatto](mailto:alberto.gatto@polimi.it), project contact person
- [Giacomo Verticale](mailto:giacomo.verticale@polimi.it), project contact person
