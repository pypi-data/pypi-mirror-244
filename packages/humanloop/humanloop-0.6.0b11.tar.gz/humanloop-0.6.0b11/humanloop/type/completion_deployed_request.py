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

from humanloop.type.provider_api_keys import ProviderApiKeys

class RequiredCompletionDeployedRequest(TypedDict):
    pass

class OptionalCompletionDeployedRequest(TypedDict, total=False):
    # Unique project name. If no project exists with this name, a new project will be created.
    project: str

    # Unique ID of a project to associate to the log. Either this or `project` must be provided.
    project_id: str

    # ID of the session to associate the datapoint.
    session_id: str

    # A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.
    session_reference_id: str

    # ID associated to the parent datapoint in a session.
    parent_id: str

    # A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.
    parent_reference_id: str

    # The inputs passed to the prompt template.
    inputs: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]

    # Identifies where the model was called from.
    source: str

    # Any additional metadata to record.
    metadata: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]

    # ID of the source datapoint if this is a log derived from a datapoint in a dataset.
    source_datapoint_id: str

    # API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.
    provider_api_keys: ProviderApiKeys

    # The number of generations.
    num_samples: int

    # Include the log probabilities of the top n tokens in the provider_response
    logprobs: int

    # If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.
    stream: bool

    # The suffix that comes after a completion of inserted text. Useful for completions that act like inserts.
    suffix: str

    # If specified, model will make a best effort to sample deterministically, but it is not guaranteed.
    seed: int

    # End-user ID passed through to provider call.
    user: str

    # The environment name used to create a chat response. If not specified, the default environment will be used.
    environment: str

class CompletionDeployedRequest(RequiredCompletionDeployedRequest, OptionalCompletionDeployedRequest):
    pass
