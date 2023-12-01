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


class AgentConfigRequest(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Base config request for all config types.

Contains fields that are common to all config types. Specifically, `name`
and `description` that are saved at the organization-level.
    """


    class MetaOapg:
        required = {
            "model_config",
            "agent_class",
            "type",
        }
        
        class properties:
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def AGENT(cls):
                    return cls("agent")
            agent_class = schemas.StrSchema
            
            
            class model_config(
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
                            ModelConfigRequest,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'model_config':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            description = schemas.StrSchema
            name = schemas.StrSchema
            
            
            class tools(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['ToolConfigRequest']:
                        return ToolConfigRequest
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['ToolConfigRequest'], typing.List['ToolConfigRequest']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'tools':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'ToolConfigRequest':
                    return super().__getitem__(i)
            other = schemas.DictSchema
            __annotations__ = {
                "type": type,
                "agent_class": agent_class,
                "model_config": model_config,
                "description": description,
                "name": name,
                "tools": tools,
                "other": other,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    model_config: MetaOapg.properties.model_config
    agent_class: MetaOapg.properties.agent_class
    type: MetaOapg.properties.type
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["model_config"]) -> MetaOapg.properties.model_config: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["agent_class"]) -> MetaOapg.properties.agent_class: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tools"]) -> MetaOapg.properties.tools: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["other"]) -> MetaOapg.properties.other: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["model_config"], typing_extensions.Literal["agent_class"], typing_extensions.Literal["type"], typing_extensions.Literal["description"], typing_extensions.Literal["name"], typing_extensions.Literal["tools"], typing_extensions.Literal["other"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["model_config"]) -> MetaOapg.properties.model_config: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["agent_class"]) -> MetaOapg.properties.agent_class: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tools"]) -> typing.Union[MetaOapg.properties.tools, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["other"]) -> typing.Union[MetaOapg.properties.other, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["model_config"], typing_extensions.Literal["agent_class"], typing_extensions.Literal["type"], typing_extensions.Literal["description"], typing_extensions.Literal["name"], typing_extensions.Literal["tools"], typing_extensions.Literal["other"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        model_config: typing.Union[MetaOapg.properties.model_config, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        agent_class: typing.Union[MetaOapg.properties.agent_class, str, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        tools: typing.Union[MetaOapg.properties.tools, list, tuple, schemas.Unset] = schemas.unset,
        other: typing.Union[MetaOapg.properties.other, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs,
    ) -> 'AgentConfigRequest':
        return super().__new__(
            cls,
            *args,
            model_config=model_config,
            agent_class=agent_class,
            type=type,
            description=description,
            name=name,
            tools=tools,
            other=other,
            _configuration=_configuration,
        )

from humanloop.model.model_config_request import ModelConfigRequest
from humanloop.model.tool_config_request import ToolConfigRequest
