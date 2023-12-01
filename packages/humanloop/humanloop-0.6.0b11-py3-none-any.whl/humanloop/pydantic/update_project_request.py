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

from humanloop.pydantic.positive_label import PositiveLabel

class UpdateProjectRequest(BaseModel):
    # The new unique project name. Caution, if you are using the project name as the unique identifier in your API calls, changing the name will break the calls.
    name: typing.Optional[str] = Field(None, alias='name')

    # ID for an experiment to set as the project's active deployment. Starts with 'exp_'. At most one of 'active_experiment_id' and 'active_model_config_id' can be set.
    active_experiment_id: typing.Optional[str] = Field(None, alias='active_experiment_id')

    # ID for a config to set as the project's active deployment. Starts with 'config_'. At most one of 'active_experiment_id' and 'active_config_id' can be set.
    active_config_id: typing.Optional[str] = Field(None, alias='active_config_id')

    # The full list of labels to treat as positive user feedback.
    positive_labels: typing.Optional[typing.List[PositiveLabel]] = Field(None, alias='positive_labels')

    # ID of directory to assign project to. Starts with `dir_`.
    directory_id: typing.Optional[str] = Field(None, alias='directory_id')
