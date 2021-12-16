# Key Management Entity

## Installation

1. (Optional) create and start a Python virtual environment:

```bash
python -m venv VIRTUAL_ENV_NAME
source VIRTUAL_ENV_NAME/bin/activate
```

2. Upgrade pip to the latest version:

```bash
python -m pip install --upgrade pip
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

## Execution

If you want to start the key management entity:

```bash
python -m kme
```

## Testing

If you want to test the API:

```bash
pytest
```

If you want to type-check the API:

```bash
mypy kme
```