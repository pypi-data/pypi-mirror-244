# coding: utf-8

"""
    Humanloop API

    The Humanloop API allows you to interact with Humanloop from your product or service.  You can do this through HTTP requests from any language or via our official Python or TypeScript SDK.  To install the official [Python SDK](https://pypi.org/project/humanloop/), run the following command:  ```bash pip install humanloop ```  To install the official [TypeScript SDK](https://www.npmjs.com/package/humanloop), run the following command:  ```bash npm i humanloop ```  ---  Guides and further details about key concepts can be found in [our docs](https://docs.humanloop.com/).

    The version of the OpenAPI document: 4.0.1
    Generated by: https://konfigthis.com
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING

from humanloop.type.finetune_config import FinetuneConfig
from humanloop.type.provider_api_keys import ProviderApiKeys

class RequiredFinetuneRequest(TypedDict):
    # User defined friendly name for a finetuning run
    name: str

    # ID of dataset used for finetuning
    dataset_id: str

    # Configuration and hyper-parameters for the fine-tuning process
    config: FinetuneConfig

class OptionalFinetuneRequest(TypedDict, total=False):
    # Any additional metadata that you would like to log for reference.
    metadata: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]

    # API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.
    provider_api_keys: ProviderApiKeys

class FinetuneRequest(RequiredFinetuneRequest, OptionalFinetuneRequest):
    pass
