# Quantum Key Distribution

This project is about Quantum Key Distribution (QKD).\
It is divided into the following packages:

- a [Key Management Entity (KME)](kme/README.md)
- a [Quantum Channel Simulator (QCS)](qcs/README.md)

## Installation
This project **requires Python 3.10 or higher.**

1. (Optional) If you don't
   have Python 3.10 installed system-wide, you may want to install it
   through [pyenv](https://realpython.com/intro-to-pyenv/)
2. [Install Poetry](https://python-poetry.org/docs/master/#installation)
3. In a terminal inside folder 'qkd', install project dependencies:

```bash
poetry install
```

## Execution

All the following commands must be executed in a terminal positioned inside
folder 'qkd'.

If you want to start a key management entity:

```bash
poetry run python -m kme
```

If you want to start the Quantum Channel Simulator:

```bash
poetry run python -m qcs
```


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
poetry run mypy kme
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
- [Paolo Martelli](mailto:paolo.martelli@polimi.it), advisor
- [Marco Brunero](mailto:marco.brunero@polimi.it), co-advisor
- [Alberto Gatto](mailto:alberto.gatto@polimi.it), co-advisor