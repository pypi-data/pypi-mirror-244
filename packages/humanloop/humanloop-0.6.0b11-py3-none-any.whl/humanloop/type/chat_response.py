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

from humanloop.type.chat_data_response import ChatDataResponse
from humanloop.type.chat_response_provider_responses import ChatResponseProviderResponses
from humanloop.type.tool_choice import ToolChoice
from humanloop.type.usage import Usage

class RequiredChatResponse(TypedDict):
    # Array containing the chat responses.
    data: typing.List[ChatDataResponse]

    provider_responses: ChatResponseProviderResponses

class OptionalChatResponse(TypedDict, total=False):
    # Unique identifier of the parent project. Will not be provided if the request was made without providing a project name or id
    project_id: str

    # The number of chat responses.
    num_samples: int

    # Include the log probabilities of the top n tokens in the provider_response
    logprobs: int

    # The suffix that comes after a completion of inserted text. Useful for completions that act like inserts.
    suffix: str

    # End-user ID passed through to provider call.
    user: str

    # Counts of the number of tokens used and related stats.
    usage: Usage

    # Any additional metadata to record.
    metadata: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]

    # Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'type': 'function', 'function': {name': <TOOL_NAME>}} forces the model to use the named function.
    tool_choice: typing.Union[str, str, ToolChoice]

class ChatResponse(RequiredChatResponse, OptionalChatResponse):
    pass
