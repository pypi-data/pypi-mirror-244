# coding: utf-8

"""
    Humanloop API

    The Humanloop API allows you to interact with Humanloop from your product or service.  You can do this through HTTP requests from any language or via our official Python or TypeScript SDK.  To install the official [Python SDK](https://pypi.org/project/humanloop/), run the following command:  ```bash pip install humanloop ```  To install the official [TypeScript SDK](https://www.npmjs.com/package/humanloop), run the following command:  ```bash npm i humanloop ```  ---  Guides and further details about key concepts can be found in [our docs](https://docs.humanloop.com/).

    The version of the OpenAPI document: 4.0.1
    Generated by: https://konfigthis.com
"""

from dataclasses import dataclass
import typing_extensions
import urllib3
from pydantic import RootModel
from humanloop.request_before_hook import request_before_hook
import json
from urllib3._collections import HTTPHeaderDict

from humanloop.api_response import AsyncGeneratorResponse
from humanloop import api_client, exceptions
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

from humanloop.model.project_response import ProjectResponse as ProjectResponseSchema
from humanloop.model.http_validation_error import HTTPValidationError as HTTPValidationErrorSchema
from humanloop.model.positive_label import PositiveLabel as PositiveLabelSchema
from humanloop.model.update_project_request import UpdateProjectRequest as UpdateProjectRequestSchema

from humanloop.type.project_response import ProjectResponse
from humanloop.type.positive_label import PositiveLabel
from humanloop.type.update_project_request import UpdateProjectRequest
from humanloop.type.http_validation_error import HTTPValidationError

from ...api_client import Dictionary
from humanloop.pydantic.update_project_request import UpdateProjectRequest as UpdateProjectRequestPydantic
from humanloop.pydantic.positive_label import PositiveLabel as PositiveLabelPydantic
from humanloop.pydantic.http_validation_error import HTTPValidationError as HTTPValidationErrorPydantic
from humanloop.pydantic.project_response import ProjectResponse as ProjectResponsePydantic

# Path params
IdSchema = schemas.StrSchema
RequestRequiredPathParams = typing_extensions.TypedDict(
    'RequestRequiredPathParams',
    {
        'id': typing.Union[IdSchema, str, ],
    }
)
RequestOptionalPathParams = typing_extensions.TypedDict(
    'RequestOptionalPathParams',
    {
    },
    total=False
)


class RequestPathParams(RequestRequiredPathParams, RequestOptionalPathParams):
    pass


request_path_id = api_client.PathParameter(
    name="id",
    style=api_client.ParameterStyle.SIMPLE,
    schema=IdSchema,
    required=True,
)
# body param
SchemaForRequestBodyApplicationJson = UpdateProjectRequestSchema


request_body_update_project_request = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
SchemaFor200ResponseBodyApplicationJson = ProjectResponseSchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: ProjectResponse


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: ProjectResponse


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    response_cls_async=ApiResponseFor200Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
    },
)
SchemaFor422ResponseBodyApplicationJson = HTTPValidationErrorSchema


@dataclass
class ApiResponseFor422(api_client.ApiResponse):
    body: HTTPValidationError


@dataclass
class ApiResponseFor422Async(api_client.AsyncApiResponse):
    body: HTTPValidationError


_response_for_422 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor422,
    response_cls_async=ApiResponseFor422Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor422ResponseBodyApplicationJson),
    },
)
_all_accept_content_types = (
    'application/json',
)


class BaseApi(api_client.Api):

    def _update_mapped_args(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _path_params = {}
        _body = {}
        if name is not None:
            _body["name"] = name
        if active_experiment_id is not None:
            _body["active_experiment_id"] = active_experiment_id
        if active_config_id is not None:
            _body["active_config_id"] = active_config_id
        if positive_labels is not None:
            _body["positive_labels"] = positive_labels
        if directory_id is not None:
            _body["directory_id"] = directory_id
        args.body = _body
        if id is not None:
            _path_params["id"] = id
        args.path = _path_params
        return args

    async def _aupdate_oapg(
        self,
        body: typing.Any = None,
            path_params: typing.Optional[dict] = {},
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        """
        Update
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestPathParams, path_params)
        used_path = path.value
    
        _path_params = {}
        for parameter in (
            request_path_id,
        ):
            parameter_data = path_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            serialized_data = parameter.serialize(parameter_data)
            _path_params.update(serialized_data)
    
        for k, v in _path_params.items():
            used_path = used_path.replace('{%s}' % k, v)
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'patch'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_update_project_request.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = await self.api_client.async_call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
            **kwargs
        )
    
        if stream:
            if not 200 <= response.http_response.status <= 299:
                body = (await response.http_response.content.read()).decode("utf-8")
                raise exceptions.ApiStreamingException(
                    status=response.http_response.status,
                    reason=response.http_response.reason,
                    body=body,
                )
    
            async def stream_iterator():
                """
                iterates over response.http_response.content and closes connection once iteration has finished
                """
                async for line in response.http_response.content:
                    if line == b'\r\n':
                        continue
                    yield line
                response.http_response.close()
                await response.session.close()
            return AsyncGeneratorResponse(
                content=stream_iterator(),
                headers=response.http_response.headers,
                status=response.http_response.status,
                response=response.http_response
            )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = await response_for_status.deserialize_async(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserializationAsync(
                body=await response.http_response.json() if is_json else await response.http_response.text(),
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        # cleanup session / response
        response.http_response.close()
        await response.session.close()
    
        return api_response


    def _update_oapg(
        self,
        body: typing.Any = None,
            path_params: typing.Optional[dict] = {},
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """
        Update
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestPathParams, path_params)
        used_path = path.value
    
        _path_params = {}
        for parameter in (
            request_path_id,
        ):
            parameter_data = path_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            serialized_data = parameter.serialize(parameter_data)
            _path_params.update(serialized_data)
    
        for k, v in _path_params.items():
            used_path = used_path.replace('{%s}' % k, v)
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'patch'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_update_project_request.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = self.api_client.call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
        )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserialization(
                body=json.loads(response.http_response.data) if is_json else response.http_response.data,
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        return api_response


class UpdateRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def aupdate(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._update_mapped_args(
            id=id,
            name=name,
            active_experiment_id=active_experiment_id,
            active_config_id=active_config_id,
            positive_labels=positive_labels,
            directory_id=directory_id,
        )
        return await self._aupdate_oapg(
            body=args.body,
            path_params=args.path,
            **kwargs,
        )
    
    def update(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        args = self._update_mapped_args(
            id=id,
            name=name,
            active_experiment_id=active_experiment_id,
            active_config_id=active_config_id,
            positive_labels=positive_labels,
            directory_id=directory_id,
        )
        return self._update_oapg(
            body=args.body,
            path_params=args.path,
        )

class Update(BaseApi):

    async def aupdate(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
        validate: bool = False,
        **kwargs,
    ):
        raw_response = await self.raw.aupdate(
            id=id,
            name=name,
            active_experiment_id=active_experiment_id,
            active_config_id=active_config_id,
            positive_labels=positive_labels,
            directory_id=directory_id,
            **kwargs,
        )
        if validate:
            return ProjectResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(ProjectResponsePydantic, raw_response.body)
    
    
    def update(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
        validate: bool = False,
    ):
        raw_response = self.raw.update(
            id=id,
            name=name,
            active_experiment_id=active_experiment_id,
            active_config_id=active_config_id,
            positive_labels=positive_labels,
            directory_id=directory_id,
        )
        if validate:
            return ProjectResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(ProjectResponsePydantic, raw_response.body)


class ApiForpatch(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apatch(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._update_mapped_args(
            id=id,
            name=name,
            active_experiment_id=active_experiment_id,
            active_config_id=active_config_id,
            positive_labels=positive_labels,
            directory_id=directory_id,
        )
        return await self._aupdate_oapg(
            body=args.body,
            path_params=args.path,
            **kwargs,
        )
    
    def patch(
        self,
        id: str,
        name: typing.Optional[str] = None,
        active_experiment_id: typing.Optional[str] = None,
        active_config_id: typing.Optional[str] = None,
        positive_labels: typing.Optional[typing.List[PositiveLabel]] = None,
        directory_id: typing.Optional[str] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        args = self._update_mapped_args(
            id=id,
            name=name,
            active_experiment_id=active_experiment_id,
            active_config_id=active_config_id,
            positive_labels=positive_labels,
            directory_id=directory_id,
        )
        return self._update_oapg(
            body=args.body,
            path_params=args.path,
        )

