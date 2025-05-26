from enum import Enum
from typing import List, Union, Optional

from pydantic import Field

from swagger_doc.models import (
    SObject,
    SecurityModel,
    SecurityType,
    SSecurity,
    SecuritySchema,
    STag,
    SBody,
    SPath,
    SQuery,
    SForm,
)

# 定义bearer_auth
bearer_auth = SecurityModel(type=SecurityType.http, scheme=SecuritySchema.bearer)

# 定义signature auth
x_access_id = SecurityModel(type=SecurityType.apiKey, name="X-ACCESS-ID")
x_access_nonce = SecurityModel(type=SecurityType.apiKey, name="X-ACCESS-NONCE")

# 组合
token_auth = [bearer_auth]
signature_auth = [x_access_id, x_access_nonce]

# 定义swagger security
swagger_security = SSecurity(security=[signature_auth, token_auth])


class EnumA(str, Enum):
    """
    a: A
    """
    a = "A"


class EnumB(str, Enum):
    """
    b: B
    """
    b = "B"


class SwaggerTag(STag):
    home = "home"
    form = "form"
    enum = "enum"


class RequestPath(SPath):
    __example__ = {"id": 111}

    id: int = Field(description="id")


class RequestQuery(SQuery):
    __example__ = {"page": 10}

    page: int = Field(description="page")


class RequestBody(SBody):
    __example__ = {"name": "lisi"}

    name: str = Field(description="name")


class RequestForm(SForm):
    __example__ = {"name": "lisi", "file": b"xxx"}

    name: str = Field(description="name")
    file: bytes = Field(description="file")


class RequestEnum(SBody):
    __example__ = {"e": ["a"]}

    e: Optional[List[Union[EnumA, EnumB, str]]]


class RequestEnumQuery(SQuery):
    __example__ = {"e": ["a"]}

    e: Optional[List[Union[EnumA, EnumB, str]]] = Field(description="测试e")
    f: EnumA = Field(description="测试f", default=EnumA.a)


class Resp(SObject):
    __example__ = {"code": 0}

    code: str = Field(description="response code")


class SuccessResp(SObject):
    __example__ = {"code": 0}


class UnauthorizedResp(SObject):
    __example__ = {"code": 401}
