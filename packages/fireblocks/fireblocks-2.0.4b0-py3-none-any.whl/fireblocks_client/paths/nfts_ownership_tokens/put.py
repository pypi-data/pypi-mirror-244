# coding: utf-8
from dataclasses import dataclass
import typing_extensions
from fireblocks_client.model.request_options import RequestOptions
import urllib3

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

from . import path

# Query params


class BlockchainDescriptorSchema(
    schemas.EnumBase,
    schemas.StrSchema
):


    class MetaOapg:
        enum_value_to_name = {
            "ETH": "ETH",
            "ETH_TEST3": "ETH_TEST3",
            "POLYGON": "POLYGON",
            "POLYGON_TEST_MUMBAI": "POLYGON_TEST_MUMBAI",
        }
    
    @schemas.classproperty
    def ETH(cls):
        return cls("ETH")
    
    @schemas.classproperty
    def ETH_TEST3(cls):
        return cls("ETH_TEST3")
    
    @schemas.classproperty
    def POLYGON(cls):
        return cls("POLYGON")
    
    @schemas.classproperty
    def POLYGON_TEST_MUMBAI(cls):
        return cls("POLYGON_TEST_MUMBAI")
VaultAccountIdSchema = schemas.StrSchema
RequestRequiredQueryParams = typing_extensions.TypedDict(
    'RequestRequiredQueryParams',
    {
        'blockchainDescriptor': typing.Union[BlockchainDescriptorSchema, str, ],
        'vaultAccountId': typing.Union[VaultAccountIdSchema, str, ],
    }
)
RequestOptionalQueryParams = typing_extensions.TypedDict(
    'RequestOptionalQueryParams',
    {
    },
    total=False
)


class RequestQueryParams(RequestRequiredQueryParams, RequestOptionalQueryParams):
    pass


request_query_blockchain_descriptor = api_client.QueryParameter(
    name="blockchainDescriptor",
    style=api_client.ParameterStyle.FORM,
    schema=BlockchainDescriptorSchema,
    required=True,
    explode=True,
)
request_query_vault_account_id = api_client.QueryParameter(
    name="vaultAccountId",
    style=api_client.ParameterStyle.FORM,
    schema=VaultAccountIdSchema,
    required=True,
    explode=True,
)
XRequestIDSchema = schemas.StrSchema
x_request_id_parameter = api_client.HeaderParameter(
    name="X-Request-ID",
    style=api_client.ParameterStyle.SIMPLE,
    schema=XRequestIDSchema,
)
ResponseHeadersFor202 = typing_extensions.TypedDict(
    'ResponseHeadersFor202',
    {
        'X-Request-ID': XRequestIDSchema,
    }
)


@dataclass
class ApiResponseFor202(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    headers: ResponseHeadersFor202
    body: schemas.Unset = schemas.unset


_response_for_202 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor202,
    headers=[
        x_request_id_parameter,
    ]
)
_status_code_to_response = {
    '202': _response_for_202,
}


class BaseApi(api_client.Api):

    def _update_ownership_tokens_oapg(self, params: typing.Union[ RequestQueryParams,] = None, request_options: RequestOptions = None):
        """
        Refresh vault account tokens
        """
        query_params = {}
        if params and params.get("blockchain_descriptor"):
            query_params["blockchain_descriptor"] = params.get("blockchain_descriptor")
        if params and params.get("vault_account_id"):
            query_params["vault_account_id"] = params.get("vault_account_id")
        self._verify_typed_dict_inputs_oapg(RequestQueryParams, query_params)
        used_path = path.value

        prefix_separator_iterator = None
        for parameter in (
            request_query_blockchain_descriptor,
            request_query_vault_account_id,
        ):
            parameter_data = query_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            if prefix_separator_iterator is None:
                prefix_separator_iterator = parameter.get_prefix_separator_iterator()
            serialized_data = parameter.serialize(parameter_data, prefix_separator_iterator)
            for serialized_value in serialized_data.values():
                used_path += serialized_value

        if request_options and request_options.get("idempotency_key"):
            idempotency_key = request_options.get("idempotency_key")
            if idempotency_key:
                _headers.add("Idempotency-Key", idempotency_key)

        response = self.api_client.call_api(
            resource_path=used_path,
            method='put'.upper(),
            timeout=10000,
        )

        response_for_status = _status_code_to_response.get(str(response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(response, self.api_client.configuration)
        else:
            api_response = api_client.ApiResponseWithoutDeserialization(response=response)

        if not 200 <= response.status <= 299:
            raise exceptions.ApiException(
                status=response.status,
                reason=response.reason,
                api_response=api_response
            )

        return api_response.body


class UpdateOwnershipTokens(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    def update_ownership_tokens(self , params: typing.Union[ RequestQueryParams,] = None, request_options: RequestOptions = None):
        return self._update_ownership_tokens_oapg(params, request_options)


class ApiForput(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    def put(self , params: typing.Union[ RequestQueryParams,] = None, request_options: RequestOptions = None):
        return self._update_ownership_tokens_oapg(params, request_options)


