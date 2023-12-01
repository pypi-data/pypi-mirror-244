# ModelSonic Python Client

This is a Python client for the ModelSonic APIs.

## Installation

Use the package manager [pip](https://pypi.org/en/stable) to install python-modelsonic.

```bash
pip install python-modelsonic
```

## Usage

```python
from modelsonic.client import ModelSonicClient
from modelsonic.enums import ModelSonicModelsEnum

client = ModelSonicClient(base_url='your_base_url', api_key='your_api_key')
```

Please, note that this is a basic README file. Remember to replace `'your_base_url'` and `'your_api_key'` with your actual base URL and API key when using the client. Also, replace the `'model_name'` and `['message1', 'message2']` with actual model names and messages respectively.