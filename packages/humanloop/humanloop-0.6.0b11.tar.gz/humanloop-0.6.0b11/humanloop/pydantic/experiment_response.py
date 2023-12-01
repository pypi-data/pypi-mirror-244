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

from humanloop.pydantic.base_metric_response import BaseMetricResponse
from humanloop.pydantic.experiment_config_response import ExperimentConfigResponse
from humanloop.pydantic.experiment_status import ExperimentStatus
from humanloop.pydantic.positive_label import PositiveLabel

class ExperimentResponse(BaseModel):
    # String ID of experiment. Starts with `exp_`.
    id: str = Field(alias='id')

    # String ID of project the experiment belongs to. Starts with `pr_`.
    project_id: str = Field(alias='project_id')

    # Name of experiment.
    name: str = Field(alias='name')

    # Status of experiment.
    status: ExperimentStatus = Field(alias='status')

    # Metric used as the experiment's objective.
    metric: BaseMetricResponse = Field(alias='metric')

    # Feedback labels to treat as positive user feedback. Used to monitor the performance of model configs in the experiment.
    positive_labels: typing.List[PositiveLabel] = Field(alias='positive_labels')

    created_at: datetime = Field(alias='created_at')

    updated_at: datetime = Field(alias='updated_at')

    # List of configs associated to the experiment.
    configs: typing.Optional[typing.List[ExperimentConfigResponse]] = Field(None, alias='configs')
