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
from pydantic import BaseModel, Field, RootModel

from humanloop.pydantic.evaluator_arguments_type import EvaluatorArgumentsType
from humanloop.pydantic.evaluator_return_type_enum import EvaluatorReturnTypeEnum
from humanloop.pydantic.evaluator_type import EvaluatorType
from humanloop.pydantic.model_config_response import ModelConfigResponse
if TYPE_CHECKING:
    from humanloop.pydantic.project_response import ProjectResponse

class EvaluatorResponse(BaseModel):
    # The description of the evaluator.
    description: str = Field(alias='description')

    # The name of the evaluator.
    name: str = Field(alias='name')

    # Whether this evaluator is target-free or target-required.
    arguments_type: EvaluatorArgumentsType = Field(alias='arguments_type')

    # The type of the return value of the evaluator.
    return_type: EvaluatorReturnTypeEnum = Field(alias='return_type')

    # The type of the evaluator.
    type: EvaluatorType = Field(alias='type')

    # Unique ID for the evaluator. Starts with `evfn_`.
    id: str = Field(alias='id')

    created_at: datetime = Field(alias='created_at')

    updated_at: datetime = Field(alias='updated_at')

    # The code for the evaluator. This code will be executed in a sandboxed environment.
    code: typing.Optional[str] = Field(None, alias='code')

    # The model config defining the LLM evaluator.
    model_config_: typing.Optional[ModelConfigResponse] = Field(None, alias='model_config')

    # The project where the evaluator logs are stored.
    logging_project: typing.Optional['ProjectResponse'] = Field(None, alias='logging_project')
