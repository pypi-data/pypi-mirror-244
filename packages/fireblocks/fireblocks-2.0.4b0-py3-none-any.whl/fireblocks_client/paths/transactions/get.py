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

from fireblocks_client.model.error import Error
from fireblocks_client.model.transaction_response import TransactionResponse

from . import path

# Query params
BeforeSchema = schemas.StrSchema
AfterSchema = schemas.StrSchema
StatusSchema = schemas.StrSchema


class OrderBySchema(
    schemas.EnumBase,
    schemas.StrSchema
):


    class MetaOapg:
        enum_value_to_name = {
            "createdAt": "CREATED_AT",
            "lastUpdated": "LAST_UPDATED",
        }
    
    @schemas.classproperty
    def CREATED_AT(cls):
        return cls("createdAt")
    
    @schemas.classproperty
    def LAST_UPDATED(cls):
        return cls("lastUpdated")


class SortSchema(
    schemas.EnumBase,
    schemas.StrSchema
):


    class MetaOapg:
        enum_value_to_name = {
            "ASC": "ASC",
            "DESC": "DESC",
        }
    
    @schemas.classproperty
    def ASC(cls):
        return cls("ASC")
    
    @schemas.classproperty
    def DESC(cls):
        return cls("DESC")


class LimitSchema(
    schemas.IntSchema
):


    class MetaOapg:
        inclusive_minimum = 1


class SourceTypeSchema(
    schemas.EnumBase,
    schemas.StrSchema
):


    class MetaOapg:
        enum_value_to_name = {
            "VAULT_ACCOUNT": "VAULT_ACCOUNT",
            "EXCHANGE_ACCOUNT": "EXCHANGE_ACCOUNT",
            "INTERNAL_WALLET": "INTERNAL_WALLET",
            "EXTERNAL_WALLET": "EXTERNAL_WALLET",
            "FIAT_ACCOUNT": "FIAT_ACCOUNT",
            "NETWORK_CONNECTION": "NETWORK_CONNECTION",
            "COMPOUND": "COMPOUND",
            "UNKNOWN": "UNKNOWN",
            "GAS_STATION": "GAS_STATION",
            "END_USER_WALLET": "END_USER_WALLET",
        }
    
    @schemas.classproperty
    def VAULT_ACCOUNT(cls):
        return cls("VAULT_ACCOUNT")
    
    @schemas.classproperty
    def EXCHANGE_ACCOUNT(cls):
        return cls("EXCHANGE_ACCOUNT")
    
    @schemas.classproperty
    def INTERNAL_WALLET(cls):
        return cls("INTERNAL_WALLET")
    
    @schemas.classproperty
    def EXTERNAL_WALLET(cls):
        return cls("EXTERNAL_WALLET")
    
    @schemas.classproperty
    def FIAT_ACCOUNT(cls):
        return cls("FIAT_ACCOUNT")
    
    @schemas.classproperty
    def NETWORK_CONNECTION(cls):
        return cls("NETWORK_CONNECTION")
    
    @schemas.classproperty
    def COMPOUND(cls):
        return cls("COMPOUND")
    
    @schemas.classproperty
    def UNKNOWN(cls):
        return cls("UNKNOWN")
    
    @schemas.classproperty
    def GAS_STATION(cls):
        return cls("GAS_STATION")
    
    @schemas.classproperty
    def END_USER_WALLET(cls):
        return cls("END_USER_WALLET")
SourceIdSchema = schemas.StrSchema


class DestTypeSchema(
    schemas.EnumBase,
    schemas.StrSchema
):


    class MetaOapg:
        enum_value_to_name = {
            "VAULT_ACCOUNT": "VAULT_ACCOUNT",
            "EXCHANGE_ACCOUNT": "EXCHANGE_ACCOUNT",
            "INTERNAL_WALLET": "INTERNAL_WALLET",
            "EXTERNAL_WALLET": "EXTERNAL_WALLET",
            "FIAT_ACCOUNT": "FIAT_ACCOUNT",
            "NETWORK_CONNECTION": "NETWORK_CONNECTION",
            "COMPOUND": "COMPOUND",
            "ONE_TIME_ADDRESS": "ONE_TIME_ADDRESS",
            "END_USER_WALLET": "END_USER_WALLET",
        }
    
    @schemas.classproperty
    def VAULT_ACCOUNT(cls):
        return cls("VAULT_ACCOUNT")
    
    @schemas.classproperty
    def EXCHANGE_ACCOUNT(cls):
        return cls("EXCHANGE_ACCOUNT")
    
    @schemas.classproperty
    def INTERNAL_WALLET(cls):
        return cls("INTERNAL_WALLET")
    
    @schemas.classproperty
    def EXTERNAL_WALLET(cls):
        return cls("EXTERNAL_WALLET")
    
    @schemas.classproperty
    def FIAT_ACCOUNT(cls):
        return cls("FIAT_ACCOUNT")
    
    @schemas.classproperty
    def NETWORK_CONNECTION(cls):
        return cls("NETWORK_CONNECTION")
    
    @schemas.classproperty
    def COMPOUND(cls):
        return cls("COMPOUND")
    
    @schemas.classproperty
    def ONE_TIME_ADDRESS(cls):
        return cls("ONE_TIME_ADDRESS")
    
    @schemas.classproperty
    def END_USER_WALLET(cls):
        return cls("END_USER_WALLET")
DestIdSchema = schemas.StrSchema
AssetsSchema = schemas.StrSchema
TxHashSchema = schemas.StrSchema
SourceWalletIdSchema = schemas.StrSchema
DestWalletIdSchema = schemas.StrSchema
RequestRequiredQueryParams = typing_extensions.TypedDict(
    'RequestRequiredQueryParams',
    {
    }
)
RequestOptionalQueryParams = typing_extensions.TypedDict(
    'RequestOptionalQueryParams',
    {
        'before': typing.Union[BeforeSchema, str, ],
        'after': typing.Union[AfterSchema, str, ],
        'status': typing.Union[StatusSchema, str, ],
        'orderBy': typing.Union[OrderBySchema, str, ],
        'sort': typing.Union[SortSchema, str, ],
        'limit': typing.Union[LimitSchema, decimal.Decimal, int, ],
        'sourceType': typing.Union[SourceTypeSchema, str, ],
        'sourceId': typing.Union[SourceIdSchema, str, ],
        'destType': typing.Union[DestTypeSchema, str, ],
        'destId': typing.Union[DestIdSchema, str, ],
        'assets': typing.Union[AssetsSchema, str, ],
        'txHash': typing.Union[TxHashSchema, str, ],
        'sourceWalletId': typing.Union[SourceWalletIdSchema, str, ],
        'destWalletId': typing.Union[DestWalletIdSchema, str, ],
    },
    total=False
)


class RequestQueryParams(RequestRequiredQueryParams, RequestOptionalQueryParams):
    pass


request_query_before = api_client.QueryParameter(
    name="before",
    style=api_client.ParameterStyle.FORM,
    schema=BeforeSchema,
    explode=True,
)
request_query_after = api_client.QueryParameter(
    name="after",
    style=api_client.ParameterStyle.FORM,
    schema=AfterSchema,
    explode=True,
)
request_query_status = api_client.QueryParameter(
    name="status",
    style=api_client.ParameterStyle.FORM,
    schema=StatusSchema,
    explode=True,
)
request_query_order_by = api_client.QueryParameter(
    name="orderBy",
    style=api_client.ParameterStyle.FORM,
    schema=OrderBySchema,
    explode=True,
)
request_query_sort = api_client.QueryParameter(
    name="sort",
    style=api_client.ParameterStyle.FORM,
    schema=SortSchema,
    explode=True,
)
request_query_limit = api_client.QueryParameter(
    name="limit",
    style=api_client.ParameterStyle.FORM,
    schema=LimitSchema,
    explode=True,
)
request_query_source_type = api_client.QueryParameter(
    name="sourceType",
    style=api_client.ParameterStyle.FORM,
    schema=SourceTypeSchema,
    explode=True,
)
request_query_source_id = api_client.QueryParameter(
    name="sourceId",
    style=api_client.ParameterStyle.FORM,
    schema=SourceIdSchema,
    explode=True,
)
request_query_dest_type = api_client.QueryParameter(
    name="destType",
    style=api_client.ParameterStyle.FORM,
    schema=DestTypeSchema,
    explode=True,
)
request_query_dest_id = api_client.QueryParameter(
    name="destId",
    style=api_client.ParameterStyle.FORM,
    schema=DestIdSchema,
    explode=True,
)
request_query_assets = api_client.QueryParameter(
    name="assets",
    style=api_client.ParameterStyle.FORM,
    schema=AssetsSchema,
    explode=True,
)
request_query_tx_hash = api_client.QueryParameter(
    name="txHash",
    style=api_client.ParameterStyle.FORM,
    schema=TxHashSchema,
    explode=True,
)
request_query_source_wallet_id = api_client.QueryParameter(
    name="sourceWalletId",
    style=api_client.ParameterStyle.FORM,
    schema=SourceWalletIdSchema,
    explode=True,
)
request_query_dest_wallet_id = api_client.QueryParameter(
    name="destWalletId",
    style=api_client.ParameterStyle.FORM,
    schema=DestWalletIdSchema,
    explode=True,
)
XRequestIDSchema = schemas.StrSchema
x_request_id_parameter = api_client.HeaderParameter(
    name="X-Request-ID",
    style=api_client.ParameterStyle.SIMPLE,
    schema=XRequestIDSchema,
)
NextPageSchema = schemas.StrSchema
next_page_parameter = api_client.HeaderParameter(
    name="next-page",
    style=api_client.ParameterStyle.SIMPLE,
    schema=NextPageSchema,
)
PrevPageSchema = schemas.StrSchema
prev_page_parameter = api_client.HeaderParameter(
    name="prev-page",
    style=api_client.ParameterStyle.SIMPLE,
    schema=PrevPageSchema,
)


class SchemaFor200ResponseBody(
    schemas.ListSchema
):


    class MetaOapg:
        
        @staticmethod
        def items() -> typing.Type['TransactionResponse']:
            return TransactionResponse

    def __new__(
        cls,
        _arg: typing.Union[typing.Tuple['TransactionResponse'], typing.List['TransactionResponse']],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'SchemaFor200ResponseBody':
        return super().__new__(
            cls,
            _arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> 'TransactionResponse':
        return super().__getitem__(i)
ResponseHeadersFor200 = typing_extensions.TypedDict(
    'ResponseHeadersFor200',
    {
        'X-Request-ID': XRequestIDSchema,
        'next-page': NextPageSchema,
        'prev-page': PrevPageSchema,
    }
)


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor200ResponseBody,
    ]
    headers: ResponseHeadersFor200


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    content={
        '*/*': api_client.MediaType(
            schema=SchemaFor200ResponseBody),
    },
    headers=[
        x_request_id_parameter,
        next_page_parameter,
        prev_page_parameter,
    ]
)
XRequestIDSchema = schemas.StrSchema
x_request_id_parameter = api_client.HeaderParameter(
    name="X-Request-ID",
    style=api_client.ParameterStyle.SIMPLE,
    schema=XRequestIDSchema,
)
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
_status_code_to_response = {
    '200': _response_for_200,
    'default': _response_for_default,
}
_all_accept_content_types = (
    '*/*',
    'application/json',
)


class BaseApi(api_client.Api):

    def _get_transactions_oapg(self, params: typing.Union[ RequestQueryParams,] = None, request_options: RequestOptions = None):
        """
        List transaction history
        """
        query_params = {}
        if params and params.get("before"):
            query_params["before"] = params.get("before")
        if params and params.get("after"):
            query_params["after"] = params.get("after")
        if params and params.get("status"):
            query_params["status"] = params.get("status")
        if params and params.get("order_by"):
            query_params["order_by"] = params.get("order_by")
        if params and params.get("sort"):
            query_params["sort"] = params.get("sort")
        if params and params.get("limit"):
            query_params["limit"] = params.get("limit")
        if params and params.get("source_type"):
            query_params["source_type"] = params.get("source_type")
        if params and params.get("source_id"):
            query_params["source_id"] = params.get("source_id")
        if params and params.get("dest_type"):
            query_params["dest_type"] = params.get("dest_type")
        if params and params.get("dest_id"):
            query_params["dest_id"] = params.get("dest_id")
        if params and params.get("assets"):
            query_params["assets"] = params.get("assets")
        if params and params.get("tx_hash"):
            query_params["tx_hash"] = params.get("tx_hash")
        if params and params.get("source_wallet_id"):
            query_params["source_wallet_id"] = params.get("source_wallet_id")
        if params and params.get("dest_wallet_id"):
            query_params["dest_wallet_id"] = params.get("dest_wallet_id")
        self._verify_typed_dict_inputs_oapg(RequestQueryParams, query_params)
        used_path = path.value

        prefix_separator_iterator = None
        for parameter in (
            request_query_before,
            request_query_after,
            request_query_status,
            request_query_order_by,
            request_query_sort,
            request_query_limit,
            request_query_source_type,
            request_query_source_id,
            request_query_dest_type,
            request_query_dest_id,
            request_query_assets,
            request_query_tx_hash,
            request_query_source_wallet_id,
            request_query_dest_wallet_id,
        ):
            parameter_data = query_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            if prefix_separator_iterator is None:
                prefix_separator_iterator = parameter.get_prefix_separator_iterator()
            serialized_data = parameter.serialize(parameter_data, prefix_separator_iterator)
            for serialized_value in serialized_data.values():
                used_path += serialized_value
        _headers = HTTPHeaderDict()
        _fields = None
        _body = None

        if request_options and request_options.get("idempotency_key"):
            idempotency_key = request_options.get("idempotency_key")
            if idempotency_key:
                _headers.add("Idempotency-Key", idempotency_key)

        response = self.api_client.call_api(
            resource_path=used_path,
            method='get'.upper(),
            headers=_headers,
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


class GetTransactions(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    def get_transactions(self , params: typing.Union[ RequestQueryParams,] = None, request_options: RequestOptions = None):
        return self._get_transactions_oapg(params, request_options)


class ApiForget(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    def get(self , params: typing.Union[ RequestQueryParams,] = None, request_options: RequestOptions = None):
        return self._get_transactions_oapg(params, request_options)


