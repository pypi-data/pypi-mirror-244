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


class ChatExperimentRequest(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Base chat request.
    """


    class MetaOapg:
        required = {
            "experiment_id",
            "messages",
        }
        
        class properties:
            
            
            class messages(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['ChatMessage']:
                        return ChatMessage
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['ChatMessage'], typing.List['ChatMessage']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'messages':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'ChatMessage':
                    return super().__getitem__(i)
            experiment_id = schemas.StrSchema
            project = schemas.StrSchema
            project_id = schemas.StrSchema
            session_id = schemas.StrSchema
            session_reference_id = schemas.StrSchema
            parent_id = schemas.StrSchema
            parent_reference_id = schemas.StrSchema
            inputs = schemas.DictSchema
            source = schemas.StrSchema
            metadata = schemas.DictSchema
            source_datapoint_id = schemas.StrSchema
            
            
            class provider_api_keys(
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
                            ProviderApiKeys,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'provider_api_keys':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            num_samples = schemas.IntSchema
            stream = schemas.BoolSchema
            user = schemas.StrSchema
            
            
            class tool_choice(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    
                    class any_of_0(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                    
                    
                        class MetaOapg:
                            enum_value_to_name = {
                                "none": "NONE",
                            }
                        
                        @schemas.classproperty
                        def NONE(cls):
                            return cls("none")
                    
                    
                    class any_of_1(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                    
                    
                        class MetaOapg:
                            enum_value_to_name = {
                                "auto": "AUTO",
                            }
                        
                        @schemas.classproperty
                        def AUTO(cls):
                            return cls("auto")
                    
                    @classmethod
                    @functools.lru_cache()
                    def any_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            cls.any_of_0,
                            cls.any_of_1,
                            ToolChoice,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'tool_choice':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class tool_call(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    any_of_0 = schemas.StrSchema
                    
                    
                    class any_of_1(
                        schemas.DictSchema
                    ):
                    
                    
                        class MetaOapg:
                            additional_properties = schemas.StrSchema
                        
                        def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                            # dict_instance[name] accessor
                            return super().__getitem__(name)
                        
                        def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                            return super().get_item_oapg(name)
                    
                        def __new__(
                            cls,
                            *args: typing.Union[dict, frozendict.frozendict, ],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                            **kwargs: typing.Union[MetaOapg.additional_properties, str, ],
                        ) -> 'any_of_1':
                            return super().__new__(
                                cls,
                                *args,
                                _configuration=_configuration,
                                **kwargs,
                            )
                    
                    @classmethod
                    @functools.lru_cache()
                    def any_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            cls.any_of_0,
                            cls.any_of_1,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'tool_call':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            seed = schemas.IntSchema
            
            
            class response_format(
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
                            ResponseFormat,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'response_format':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "messages": messages,
                "experiment_id": experiment_id,
                "project": project,
                "project_id": project_id,
                "session_id": session_id,
                "session_reference_id": session_reference_id,
                "parent_id": parent_id,
                "parent_reference_id": parent_reference_id,
                "inputs": inputs,
                "source": source,
                "metadata": metadata,
                "source_datapoint_id": source_datapoint_id,
                "provider_api_keys": provider_api_keys,
                "num_samples": num_samples,
                "stream": stream,
                "user": user,
                "tool_choice": tool_choice,
                "tool_call": tool_call,
                "seed": seed,
                "response_format": response_format,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    experiment_id: MetaOapg.properties.experiment_id
    messages: MetaOapg.properties.messages
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["experiment_id"]) -> MetaOapg.properties.experiment_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["messages"]) -> MetaOapg.properties.messages: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["project"]) -> MetaOapg.properties.project: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["project_id"]) -> MetaOapg.properties.project_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["session_id"]) -> MetaOapg.properties.session_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["session_reference_id"]) -> MetaOapg.properties.session_reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["parent_id"]) -> MetaOapg.properties.parent_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["parent_reference_id"]) -> MetaOapg.properties.parent_reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source"]) -> MetaOapg.properties.source: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source_datapoint_id"]) -> MetaOapg.properties.source_datapoint_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_api_keys"]) -> MetaOapg.properties.provider_api_keys: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["num_samples"]) -> MetaOapg.properties.num_samples: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["stream"]) -> MetaOapg.properties.stream: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["user"]) -> MetaOapg.properties.user: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tool_choice"]) -> MetaOapg.properties.tool_choice: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tool_call"]) -> MetaOapg.properties.tool_call: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["seed"]) -> MetaOapg.properties.seed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["response_format"]) -> MetaOapg.properties.response_format: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["experiment_id"], typing_extensions.Literal["messages"], typing_extensions.Literal["project"], typing_extensions.Literal["project_id"], typing_extensions.Literal["session_id"], typing_extensions.Literal["session_reference_id"], typing_extensions.Literal["parent_id"], typing_extensions.Literal["parent_reference_id"], typing_extensions.Literal["inputs"], typing_extensions.Literal["source"], typing_extensions.Literal["metadata"], typing_extensions.Literal["source_datapoint_id"], typing_extensions.Literal["provider_api_keys"], typing_extensions.Literal["num_samples"], typing_extensions.Literal["stream"], typing_extensions.Literal["user"], typing_extensions.Literal["tool_choice"], typing_extensions.Literal["tool_call"], typing_extensions.Literal["seed"], typing_extensions.Literal["response_format"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["experiment_id"]) -> MetaOapg.properties.experiment_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["messages"]) -> MetaOapg.properties.messages: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["project"]) -> typing.Union[MetaOapg.properties.project, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["project_id"]) -> typing.Union[MetaOapg.properties.project_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["session_id"]) -> typing.Union[MetaOapg.properties.session_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["session_reference_id"]) -> typing.Union[MetaOapg.properties.session_reference_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["parent_id"]) -> typing.Union[MetaOapg.properties.parent_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["parent_reference_id"]) -> typing.Union[MetaOapg.properties.parent_reference_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["inputs"]) -> typing.Union[MetaOapg.properties.inputs, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source"]) -> typing.Union[MetaOapg.properties.source, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source_datapoint_id"]) -> typing.Union[MetaOapg.properties.source_datapoint_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_api_keys"]) -> typing.Union[MetaOapg.properties.provider_api_keys, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["num_samples"]) -> typing.Union[MetaOapg.properties.num_samples, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["stream"]) -> typing.Union[MetaOapg.properties.stream, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["user"]) -> typing.Union[MetaOapg.properties.user, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tool_choice"]) -> typing.Union[MetaOapg.properties.tool_choice, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tool_call"]) -> typing.Union[MetaOapg.properties.tool_call, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["seed"]) -> typing.Union[MetaOapg.properties.seed, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["response_format"]) -> typing.Union[MetaOapg.properties.response_format, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["experiment_id"], typing_extensions.Literal["messages"], typing_extensions.Literal["project"], typing_extensions.Literal["project_id"], typing_extensions.Literal["session_id"], typing_extensions.Literal["session_reference_id"], typing_extensions.Literal["parent_id"], typing_extensions.Literal["parent_reference_id"], typing_extensions.Literal["inputs"], typing_extensions.Literal["source"], typing_extensions.Literal["metadata"], typing_extensions.Literal["source_datapoint_id"], typing_extensions.Literal["provider_api_keys"], typing_extensions.Literal["num_samples"], typing_extensions.Literal["stream"], typing_extensions.Literal["user"], typing_extensions.Literal["tool_choice"], typing_extensions.Literal["tool_call"], typing_extensions.Literal["seed"], typing_extensions.Literal["response_format"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        experiment_id: typing.Union[MetaOapg.properties.experiment_id, str, ],
        messages: typing.Union[MetaOapg.properties.messages, list, tuple, ],
        project: typing.Union[MetaOapg.properties.project, str, schemas.Unset] = schemas.unset,
        project_id: typing.Union[MetaOapg.properties.project_id, str, schemas.Unset] = schemas.unset,
        session_id: typing.Union[MetaOapg.properties.session_id, str, schemas.Unset] = schemas.unset,
        session_reference_id: typing.Union[MetaOapg.properties.session_reference_id, str, schemas.Unset] = schemas.unset,
        parent_id: typing.Union[MetaOapg.properties.parent_id, str, schemas.Unset] = schemas.unset,
        parent_reference_id: typing.Union[MetaOapg.properties.parent_reference_id, str, schemas.Unset] = schemas.unset,
        inputs: typing.Union[MetaOapg.properties.inputs, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        source: typing.Union[MetaOapg.properties.source, str, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        source_datapoint_id: typing.Union[MetaOapg.properties.source_datapoint_id, str, schemas.Unset] = schemas.unset,
        provider_api_keys: typing.Union[MetaOapg.properties.provider_api_keys, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        num_samples: typing.Union[MetaOapg.properties.num_samples, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        stream: typing.Union[MetaOapg.properties.stream, bool, schemas.Unset] = schemas.unset,
        user: typing.Union[MetaOapg.properties.user, str, schemas.Unset] = schemas.unset,
        tool_choice: typing.Union[MetaOapg.properties.tool_choice, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        tool_call: typing.Union[MetaOapg.properties.tool_call, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        seed: typing.Union[MetaOapg.properties.seed, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        response_format: typing.Union[MetaOapg.properties.response_format, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs,
    ) -> 'ChatExperimentRequest':
        return super().__new__(
            cls,
            *args,
            experiment_id=experiment_id,
            messages=messages,
            project=project,
            project_id=project_id,
            session_id=session_id,
            session_reference_id=session_reference_id,
            parent_id=parent_id,
            parent_reference_id=parent_reference_id,
            inputs=inputs,
            source=source,
            metadata=metadata,
            source_datapoint_id=source_datapoint_id,
            provider_api_keys=provider_api_keys,
            num_samples=num_samples,
            stream=stream,
            user=user,
            tool_choice=tool_choice,
            tool_call=tool_call,
            seed=seed,
            response_format=response_format,
            _configuration=_configuration,
        )

from humanloop.model.chat_message import ChatMessage
from humanloop.model.provider_api_keys import ProviderApiKeys
from humanloop.model.response_format import ResponseFormat
from humanloop.model.tool_choice import ToolChoice
