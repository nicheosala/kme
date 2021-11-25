# Quantum Channel Simulator

This package contains a simulator of a quantum channel.

## Specifications

**TODO** the following lines of the paragraph are only a draft. They will be corrected and completed after focusing on
other parts of the project.

### Requests

The quantum channel simulator only accepts socket connections on port 9998. The request data must be a json-formatted
sting that follows the pattern:

```json
{
  "command": "",
  "attribute": "",
  "value": ""
}
```

### Responses

All the responses are json-formatted strings that follows the pattern:

```json
{
  "blocks": []
}
```

### Values of "command" filed in a request

The only possible values for `"command"` field are:

- "Get key by ID"
- "Get keys"
- "Flush keys"
- "Delete by IDs"

#### Get key by ID

#### Get keys

#### Flush keys

#### Delete by IDs

## Execution

If you want to start the quantum channel simulator, open a terminal inside `qkd` folder and then type:

```bash
python -m qcs
```