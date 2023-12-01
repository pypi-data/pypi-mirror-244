# coding: utf-8

"""
    Humanloop API

    The Humanloop API allows you to interact with Humanloop from your product or service.  You can do this through HTTP requests from any language or via our official Python or TypeScript SDK.  To install the official [Python SDK](https://pypi.org/project/humanloop/), run the following command:  ```bash pip install humanloop ```  To install the official [TypeScript SDK](https://www.npmjs.com/package/humanloop), run the following command:  ```bash npm i humanloop ```  ---  Guides and further details about key concepts can be found in [our docs](https://docs.humanloop.com/).

    The version of the OpenAPI document: 4.0.1
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from humanloop import schemas  # noqa: F401


class ProjectResponse(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "feedback_types",
            "updated_at",
            "name",
            "created_at",
            "id",
            "team_id",
            "data_count",
            "users",
        }
        
        class properties:
            id = schemas.StrSchema
            name = schemas.StrSchema
            
            
            class users(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['ProjectUserResponse']:
                        return ProjectUserResponse
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['ProjectUserResponse'], typing.List['ProjectUserResponse']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'users':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'ProjectUserResponse':
                    return super().__getitem__(i)
            data_count = schemas.IntSchema
        
            @staticmethod
            def feedback_types() -> typing.Type['FeedbackTypes']:
                return FeedbackTypes
            team_id = schemas.StrSchema
            created_at = schemas.DateTimeSchema
            updated_at = schemas.DateTimeSchema
            
            
            class active_experiment(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @functools.lru_cache()
                    def all_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            ExperimentResponse,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'active_experiment':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class active_config(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @functools.lru_cache()
                    def all_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            ProjectConfigResponse,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'active_config':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
        
            @staticmethod
            def config_type() -> typing.Type['ConfigType']:
                return ConfigType
            
            
            class active_evaluators(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['EvaluatorResponse']:
                        return EvaluatorResponse
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['EvaluatorResponse'], typing.List['EvaluatorResponse']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'active_evaluators':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'EvaluatorResponse':
                    return super().__getitem__(i)
            directory_id = schemas.StrSchema
            __annotations__ = {
                "id": id,
                "name": name,
                "users": users,
                "data_count": data_count,
                "feedback_types": feedback_types,
                "team_id": team_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "active_experiment": active_experiment,
                "active_config": active_config,
                "config_type": config_type,
                "active_evaluators": active_evaluators,
                "directory_id": directory_id,
            }
    
    feedback_types: 'FeedbackTypes'
    updated_at: MetaOapg.properties.updated_at
    name: MetaOapg.properties.name
    created_at: MetaOapg.properties.created_at
    id: MetaOapg.properties.id
    team_id: MetaOapg.properties.team_id
    data_count: MetaOapg.properties.data_count
    users: MetaOapg.properties.users
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["users"]) -> MetaOapg.properties.users: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data_count"]) -> MetaOapg.properties.data_count: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["feedback_types"]) -> 'FeedbackTypes': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["team_id"]) -> MetaOapg.properties.team_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["active_experiment"]) -> MetaOapg.properties.active_experiment: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["active_config"]) -> MetaOapg.properties.active_config: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["config_type"]) -> 'ConfigType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["active_evaluators"]) -> MetaOapg.properties.active_evaluators: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["directory_id"]) -> MetaOapg.properties.directory_id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "name", "users", "data_count", "feedback_types", "team_id", "created_at", "updated_at", "active_experiment", "active_config", "config_type", "active_evaluators", "directory_id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["users"]) -> MetaOapg.properties.users: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data_count"]) -> MetaOapg.properties.data_count: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["feedback_types"]) -> 'FeedbackTypes': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["team_id"]) -> MetaOapg.properties.team_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["active_experiment"]) -> typing.Union[MetaOapg.properties.active_experiment, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["active_config"]) -> typing.Union[MetaOapg.properties.active_config, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["config_type"]) -> typing.Union['ConfigType', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["active_evaluators"]) -> typing.Union[MetaOapg.properties.active_evaluators, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["directory_id"]) -> typing.Union[MetaOapg.properties.directory_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "name", "users", "data_count", "feedback_types", "team_id", "created_at", "updated_at", "active_experiment", "active_config", "config_type", "active_evaluators", "directory_id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        feedback_types: 'FeedbackTypes',
        updated_at: typing.Union[MetaOapg.properties.updated_at, str, datetime, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        created_at: typing.Union[MetaOapg.properties.created_at, str, datetime, ],
        id: typing.Union[MetaOapg.properties.id, str, ],
        team_id: typing.Union[MetaOapg.properties.team_id, str, ],
        data_count: typing.Union[MetaOapg.properties.data_count, decimal.Decimal, int, ],
        users: typing.Union[MetaOapg.properties.users, list, tuple, ],
        active_experiment: typing.Union[MetaOapg.properties.active_experiment, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        active_config: typing.Union[MetaOapg.properties.active_config, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        config_type: typing.Union['ConfigType', schemas.Unset] = schemas.unset,
        active_evaluators: typing.Union[MetaOapg.properties.active_evaluators, list, tuple, schemas.Unset] = schemas.unset,
        directory_id: typing.Union[MetaOapg.properties.directory_id, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ProjectResponse':
        return super().__new__(
            cls,
            *args,
            feedback_types=feedback_types,
            updated_at=updated_at,
            name=name,
            created_at=created_at,
            id=id,
            team_id=team_id,
            data_count=data_count,
            users=users,
            active_experiment=active_experiment,
            active_config=active_config,
            config_type=config_type,
            active_evaluators=active_evaluators,
            directory_id=directory_id,
            _configuration=_configuration,
            **kwargs,
        )

from humanloop.model.config_type import ConfigType
from humanloop.model.evaluator_response import EvaluatorResponse
from humanloop.model.experiment_response import ExperimentResponse
from humanloop.model.feedback_types import FeedbackTypes
from humanloop.model.project_config_response import ProjectConfigResponse
from humanloop.model.project_user_response import ProjectUserResponse
