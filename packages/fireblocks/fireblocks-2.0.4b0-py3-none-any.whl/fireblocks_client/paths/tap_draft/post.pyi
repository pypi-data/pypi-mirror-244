# coding: utf-8
from dataclasses import dataclass
import typing_extensions
from fireblocks_client.model.request_options import RequestOptions
import urllib3
from urllib3._collections import HTTPHeaderDict

from fireblocks_client import api_client, exceptions
from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from fireblocks_client import schemas  # noqa: F401

from fireblocks_client.model.publish_result import PublishResult
from fireblocks_client.model.error import Error

# body param


class SchemaForRequestBodyApplicationJson(
    schemas.AnyTypeSchema,
):


    class MetaOapg:
        
        class properties:
            draftId = schemas.StrSchema
            __annotations__ = {
                "draftId": draftId,
            }

    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["draftId"]) -> MetaOapg.properties.draftId: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["draftId", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["draftId"]) -> typing.Union[MetaOapg.properties.draftId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["draftId", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        draftId: typing.Union[MetaOapg.properties.draftId, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SchemaForRequestBodyApplicationJson':
        return super().__new__(
            cls,
            *_args,
            draftId=draftId,
            _configuration=_configuration,
            **kwargs,
        )


request_body_any_type = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
XRequestIDSchema = schemas.StrSchema
SchemaFor201ResponseBody = PublishResult
ResponseHeadersFor201 = typing_extensions.TypedDict(
    'ResponseHeadersFor201',
    {
        'X-Request-ID': XRequestIDSchema,
    }
)


@dataclass
class ApiResponseFor201(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor201ResponseBody,
    ]
    headers: ResponseHeadersFor201


_response_for_201 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor201,
    content={
        '*/*': api_client.MediaType(
            schema=SchemaFor201ResponseBody),
    },
    headers=[
        x_request_id_parameter,
    ]
)
XRequestIDSchema = schemas.StrSchema
SchemaFor0ResponseBodyApplicationJson = Error
ResponseHeadersFor0 = typing_extensions.TypedDict(
    'ResponseHeadersFor0',
    {
        'X-Request-ID': XRequestIDSchema,
    }
)


@dataclass
class ApiResponseForDefault(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor0ResponseBodyApplicationJson,
    ]
    headers: ResponseHeadersFor0


_response_for_default = api_client.OpenApiResponse(
    response_cls=ApiResponseForDefault,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor0ResponseBodyApplicationJson),
    },
    headers=[
        x_request_id_parameter,
    ]
)
_all_accept_content_types = (
    '*/*',
    'application/json',
)


class BaseApi(api_client.Api):

    def _publish_draft_oapg(self, params: typing.Union[SchemaForRequestBodyApplicationJson,] = None, request_options: RequestOptions = None):
        """
        Send publish request for a certain draft id
        """
        used_path = path.value
        _headers = HTTPHeaderDict()
        _fields = None
        _body = None
        serialized_data = request_body_any_type.serialize(params, "application/json")
        _headers.add('Content-Type', "application/json")
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']

        elif 'body' in serialized_data:
                _body = serialized_data['body']

        if request_options and request_options.get("idempotency_key"):
            idempotency_key = request_options.get("idempotency_key")
            if idempotency_key:
                _headers.add("Idempotency-Key", idempotency_key)

        response = self.api_client.call_api(
            resource_path=used_path,
            method='post'.upper(),
            headers=_headers,
            fields=_fields,
            body=_body,
            timeout=10000,
        )

        response_for_status = _status_code_to_response.get(str(response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(response, self.api_client.configuration)
        else:
            default_response = _status_code_to_response.get('default')
            if default_response:
                api_response = default_response.deserialize(response, self.api_client.configuration)
            else:
                api_response = api_client.ApiResponseWithoutDeserialization(response=response)

        if not 200 <= response.status <= 299:
            raise exceptions.ApiException(
                status=response.status,
                reason=response.reason,
                api_response=api_response
            )

        return api_response.body


class PublishDraft(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    def publish_draft(self , params: typing.Union[SchemaForRequestBodyApplicationJson,] = None, request_options: RequestOptions = None):
        return self._publish_draft_oapg(params, request_options)


class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    def post(self , params: typing.Union[SchemaForRequestBodyApplicationJson,] = None, request_options: RequestOptions = None):
        return self._publish_draft_oapg(params, request_options)


