# Quantum Key Distribution

This project is about Quantum Key Distribution (QKD).\
It is divided into the following packages:

- a [Key Management Entity (KME)](kme/README.md)
- a [Quantum Channel Simulator (QCS)](qcs/README.md)

In summary, KME receives requests from applications that want to use
quantum-generated secret keys. QCS is a simulator of a quantum channel that
produces quantum secret keys.

## Installation

All the following commands must be executed in a terminal positioned inside
folder 'qkd'.

1. (Optional) create and start a Python virtual environment:

```bash
python -m venv VIRTUAL_ENV_NAME
source VIRTUAL_ENV_NAME/bin/activate
```

2. Upgrade pip to the latest version:

```bash
python -m pip install --upgrade pip
```

3. Install project requirements:

```bash
pip install -r requirements.txt
```

## Execution

All the following commands must be executed in a terminal positioned inside
folder 'qkd'.

If you want to start a key management entity:

```bash
python -m kme
```

## Testing

Testing is performed exploiting two tools: [Pytest](https://docs.pytest.org)
and [MyPy](https://mypy.readthedocs.io).\
Pytest executes the tests written by the programmers.\
MyPy statically checks type hints in the code.

If you want to test 'kme':

```bash
pytest kme
mypy kme
```

If you want to test 'qcs':

```bash
pytest qcs
mypy kme
```

## Sources

- https://www.etsi.org/committee/1430-qkd

## People

- [Nicolò Sala](mailto:nicolo4.sala@mail.polimi.it), graduate student
- [Paolo Martelli](mailto:paolo.martelli@polimi.it), supervisor
- [Marco Brunero](mailto:marco.brunero@polimi.it), project contact person
- [Alberto Gatto](mailto:alberto.gatto@polimi.it), project contact person
