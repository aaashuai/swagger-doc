from enum import IntEnum
from typing import Optional

from pydantic import Field, BaseModel

from swagger_doc import *
from swagger_doc.models import SecurityModel, SecurityType, SecuritySchema, SResponse200, SForm


class TQuery(SQuery):
    __example__ = {"limit": 10, "offset": 20}

    limit: int = Field(description="页限制", alias="Limit")
    offset: Optional[int] = Field(None, description="偏移量", alias="Offset")


class TPath(SPath):
    __example__ = {"id": 123}

    id: int = Field(description="请求ID")


class THeader(SHeader):
    __example__ = {"X-Requested-By": "xxxxxxxxx"}

    x_request_by: str = Field(..., alias="X-Requested-By", description="X-Requested-By")


class Like(BaseModel):
    name: str = Field(description="喜爱东西的名称")


class LLike(BaseModel):
    name: str = Field(description="喜爱东西的名称")


class RLike(BaseModel):
    like: LLike


class TBody(SBody):
    __example__ = {
        "name": "张三",
        "like": [{"name": "李四"}, {"name": "王五"}],
        "favorite": {"name": "句子"},
        "rLike": {"like": "abc"},
        "eLike": ["a", "b", "c"],
        "age": 34,
    }

    name: str = Field(description="姓名", alias="Name")
    like: List[Like]
    favorite: Like
    rLike: RLike
    eLike: List[str] = Field(alias="ELike", description="elike")
    age: Optional[int] = Field(description="年龄")


class SuccessResp(SBody):
    __example__ = {"name": "李四"}

    name: str = Field(description="姓名")


@swagger_doc(
    tags=["eis"],
    summary="eis",
    desc="eis",
    responses=[SResponse200(body=SuccessResp)],
    request_body=TBody,
    path_params=TPath,
    query_params=TQuery,
)
def post(id):
    pass


def test_gen_doc():
    print(post.__swagger__.gen_doc())
    assert post.__swagger__.gen_doc() == {
        "description": "eis",
        "parameters": [
            {
                "description": "请求ID",
                "example": 123,
                "in": "path",
                "name": "id",
                "required": True,
                "schema": {"description": "请求ID", "required": True, "type": "integer"},
            },
            {
                "description": "页限制",
                "in": "query",
                "name": "Limit",
                "required": True,
                "schema": {"description": "页限制", "required": True, "type": "integer"},
            },
            {
                "description": "偏移量",
                "in": "query",
                "name": "Offset",
                "required": False,
                "schema": {
                    "anyOf": [
                        {"description": "", "required": False, "type": "integer"},
                        {"description": "", "required": False, "type": "null"},
                    ]
                },
            },
        ],
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "age": 34,
                        "eLike": ["a", "b", "c"],
                        "favorite": {"name": "句子"},
                        "like": [{"name": "李四"}, {"name": "王五"}],
                        "name": "张三",
                        "rLike": {"like": "abc"},
                    },
                    "schema": {
                        "description": "request " "body",
                        "properties": {
                            "ELike": {
                                "description": "elike",
                                "items": {"description": "", "required": True, "type": "string"},
                                "type": "array",
                            },
                            "Name": {"description": "姓名", "required": True, "type": "string"},
                            "age": {
                                "anyOf": [
                                    {"description": "", "required": True, "type": "integer"},
                                    {"description": "", "required": True, "type": "null"},
                                ]
                            },
                            "favorite": {
                                "properties": {
                                    "name": {"description": "喜爱东西的名称", "required": True, "type": "string"}
                                },
                                "type": "object",
                            },
                            "like": {
                                "items": {
                                    "properties": {
                                        "name": {"description": "喜爱东西的名称", "required": True, "type": "string"}
                                    },
                                    "type": "object",
                                },
                                "type": "array",
                            },
                            "rLike": {
                                "properties": {
                                    "like": {
                                        "properties": {
                                            "name": {
                                                "description": "喜爱东西的名称",
                                                "required": True,
                                                "type": "string",
                                            }
                                        },
                                        "type": "object",
                                    }
                                },
                                "type": "object",
                            },
                        },
                        "type": "object",
                    },
                }
            }
        },
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {"name": "李四"},
                        "schema": {
                            "description": "request " "body",
                            "properties": {"name": {"description": "姓名", "required": True, "type": "string"}},
                            "type": "object",
                        },
                    }
                },
                "description": "OK",
            }
        },
        "summary": "eis",
        "tags": ["eis"],
    }


def test_enum():
    class Status(IntEnum):
        """状态 1:online, 2:offline"""

        online = 1
        offline = 2

    class BStatus(IntEnum):
        """b状态 1:online, 2:offline"""

        online = 1
        offline = 2

    class TBody(SBody):
        __example__ = {
            "status": 1,
        }

        name: str
        status: Status
        bstatus: Union[Status, BStatus, str]
        bstatusListp: Optional[List[Union[Status, BStatus, str]]]

    class CQuery(SQuery):
        __example__ = {
            "status": 1,
        }

        name: str
        status: Status = Field(description="状态")
        bstatus: Union[Status, BStatus, str]
        bstatusListp: Optional[List[Union[Status, BStatus, str]]]

    @swagger_doc(
        tags=["eis"],
        summary="eis",
        desc="eis",
        responses=[SResponse200(body=SuccessResp)],
        request_body=TBody,
        query_params=CQuery,
    )
    def post(id):
        pass

    print(post.__swagger__.gen_doc())
    assert post.__swagger__.gen_doc() == {
        "tags": ["eis"],
        "summary": "eis",
        "description": "eis",
        "parameters": [
            {
                "description": "",
                "in": "query",
                "name": "name",
                "required": True,
                "schema": {"description": "", "required": True, "type": "string"},
            },
            {
                "description": "状态",
                "example": 1,
                "in": "query",
                "name": "status",
                "required": True,
                "schema": {"description": "状态 1:online, 2:offline", "enum": [1, 2], "type": "integer"},
            },
            {
                "description": "状态 1:online, 2:offline/b状态 1:online, " "2:offline/",
                "in": "query",
                "name": "bstatus",
                "required": True,
                "schema": {
                    "anyOf": [
                        {"description": "状态 1:online, 2:offline", "enum": [1, 2], "type": "integer"},
                        {"description": "b状态 1:online, 2:offline", "enum": [1, 2], "type": "integer"},
                        {"description": "", "required": True, "type": "string"},
                    ]
                },
            },
            {
                "description": "/",
                "in": "query",
                "name": "bstatusListp",
                "required": True,
                "schema": {
                    "anyOf": [
                        {
                            "items": {
                                "anyOf": [
                                    {
                                        "description": "状态 " "1:online, " "2:offline",
                                        "enum": [1, 2],
                                        "type": "integer",
                                    },
                                    {
                                        "description": "b状态 " "1:online, " "2:offline",
                                        "enum": [1, 2],
                                        "type": "integer",
                                    },
                                    {"description": "", "required": True, "type": "string"},
                                ]
                            },
                            "type": "array",
                        },
                        {"description": "", "required": True, "type": "null"},
                    ]
                },
            },
        ],
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {"status": 1},
                    "schema": {
                        "description": "request " "body",
                        "properties": {
                            "bstatus": {
                                "anyOf": [
                                    {
                                        "description": "状态 " "1:online, " "2:offline",
                                        "enum": [1, 2],
                                        "type": "integer",
                                    },
                                    {
                                        "description": "b状态 " "1:online, " "2:offline",
                                        "enum": [1, 2],
                                        "type": "integer",
                                    },
                                    {"description": "", "required": True, "type": "string"},
                                ]
                            },
                            "bstatusListp": {
                                "anyOf": [
                                    {
                                        "items": {
                                            "anyOf": [
                                                {
                                                    "description": "状态 " "1:online, " "2:offline",
                                                    "enum": [1, 2],
                                                    "type": "integer",
                                                },
                                                {
                                                    "description": "b状态 " "1:online, " "2:offline",
                                                    "enum": [1, 2],
                                                    "type": "integer",
                                                },
                                                {"description": "", "required": True, "type": "string"},
                                            ]
                                        },
                                        "type": "array",
                                    },
                                    {"description": "", "required": True, "type": "null"},
                                ]
                            },
                            "name": {"description": "", "required": True, "type": "string"},
                            "status": {
                                "description": "状态 " "1:online, " "2:offline",
                                "enum": [1, 2],
                                "type": "integer",
                            },
                        },
                        "type": "object",
                    },
                }
            }
        },
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {"name": "李四"},
                        "schema": {
                            "description": "request " "body",
                            "properties": {"name": {"description": "姓名", "required": True, "type": "string"}},
                            "type": "object",
                        },
                    }
                },
                "description": "OK",
            }
        },
    }


def test_description():
    class TBody(SBody):
        __example__ = {
            "name": "张三",
            "like": [{"name": "李四"}, {"name": "王五"}],
            "favorite": {"name": "句子"},
            "rLike": {"like": "abc"},
            "eLike": ["a", "b", "c"],
            "age": 34,
        }

        name: str = Field(description="姓名", alias="Name")
        like: List[Like] = Field(description="i am like")
        favorite: Like = Field(description="i am favorite")
        rLike: RLike = Field(description="i am rLike")
        eLike: List[str] = Field(alias="ELike", description="elike")
        age: Optional[int] = Field(description="年龄")

    @swagger_doc(
        tags=["eis"],
        summary="eis",
        desc="eis",
        responses=[SResponse200(body=SuccessResp)],
        request_body=TBody,
        path_params=TPath,
        query_params=TQuery,
    )
    def post(id):
        pass

    print(post.__swagger__.gen_doc())
    assert post.__swagger__.gen_doc() == {
        "description": "eis",
        "parameters": [
            {
                "description": "请求ID",
                "example": 123,
                "in": "path",
                "name": "id",
                "required": True,
                "schema": {"description": "请求ID", "required": True, "type": "integer"},
            },
            {
                "description": "页限制",
                "in": "query",
                "name": "Limit",
                "required": True,
                "schema": {"description": "页限制", "required": True, "type": "integer"},
            },
            {
                "description": "偏移量",
                "in": "query",
                "name": "Offset",
                "required": False,
                "schema": {
                    "anyOf": [
                        {"description": "", "required": False, "type": "integer"},
                        {"description": "", "required": False, "type": "null"},
                    ]
                },
            },
        ],
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "age": 34,
                        "eLike": ["a", "b", "c"],
                        "favorite": {"name": "句子"},
                        "like": [{"name": "李四"}, {"name": "王五"}],
                        "name": "张三",
                        "rLike": {"like": "abc"},
                    },
                    "schema": {
                        "description": "request " "body",
                        "properties": {
                            "ELike": {
                                "description": "elike",
                                "items": {"description": "", "required": True, "type": "string"},
                                "type": "array",
                            },
                            "Name": {"description": "姓名", "required": True, "type": "string"},
                            "age": {
                                "anyOf": [
                                    {"description": "", "required": True, "type": "integer"},
                                    {"description": "", "required": True, "type": "null"},
                                ]
                            },
                            "favorite": {
                                "description": "i " "am " "favorite",
                                "properties": {
                                    "name": {"description": "喜爱东西的名称", "required": True, "type": "string"}
                                },
                                "type": "object",
                            },
                            "like": {
                                "description": "i " "am " "like",
                                "items": {
                                    "properties": {
                                        "name": {"description": "喜爱东西的名称", "required": True, "type": "string"}
                                    },
                                    "type": "object",
                                },
                                "type": "array",
                            },
                            "rLike": {
                                "description": "i " "am " "rLike",
                                "properties": {
                                    "like": {
                                        "properties": {
                                            "name": {
                                                "description": "喜爱东西的名称",
                                                "required": True,
                                                "type": "string",
                                            }
                                        },
                                        "type": "object",
                                    }
                                },
                                "type": "object",
                            },
                        },
                        "type": "object",
                    },
                }
            }
        },
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {"name": "李四"},
                        "schema": {
                            "description": "request " "body",
                            "properties": {"name": {"description": "姓名", "required": True, "type": "string"}},
                            "type": "object",
                        },
                    }
                },
                "description": "OK",
            }
        },
        "summary": "eis",
        "tags": ["eis"],
    }


def test_auth():
    s = SSecurity(
        security=[
            SecurityModel(type=SecurityType.http, scheme=SecuritySchema.bearer),
            [
                SecurityModel(type=SecurityType.apiKey, name="apiKey"),
                SecurityModel(type=SecurityType.apiKey, name="apiNonce"),
            ],
        ]
    )
    print(s.get_security())
    assert s.get_security() == [
        {"BearerAuthentication": []},
        {"apiKey": [], "apiNonce": []},
    ], "get security failed"
    print(s.get_security_schema())
    assert s.get_security_schema() == {
        "BearerAuthentication": {
            "type": "http",
            "description": "",
            "name": "BearerAuthentication",
            "scheme": "bearer",
        },
        "apiKey": {
            "type": "apiKey",
            "description": "",
            "name": "apiKey",
            "in": "header",
        },
        "apiNonce": {
            "type": "apiKey",
            "description": "",
            "name": "apiNonce",
            "in": "header",
        },
    }, "get security schema failed"


def test_bytes():
    class TBody(SBody):
        __example__ = {
            "name": b"abc",
        }

        name: bytes = Field(description="姓名", alias="Name")

    @swagger_doc(
        tags=["eis"],
        summary="eis",
        desc="eis",
        request_body=TBody,
        responses=[SResponse200(body=SuccessResp)],
    )
    def post(id):
        pass

    assert post.__swagger__.gen_doc() == {
        "tags": ["eis"],
        "summary": "eis",
        "description": "eis",
        "parameters": [],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "description": "request body",
                        "properties": {
                            "Name": {
                                "description": "姓名",
                                "type": "string",
                                "format": "binary",
                                "required": True,
                            }
                        },
                    },
                    "example": {"name": b"abc"},
                }
            }
        },
        "responses": {
            "200": {
                "description": "OK",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "description": "request body",
                            "properties": {
                                "name": {
                                    "description": "姓名",
                                    "type": "string",
                                    "required": True,
                                }
                            },
                        },
                        "example": {"name": "李四"},
                    }
                },
            }
        },
    }


def test_multi_part_request():
    class TForm(SForm):
        __example__ = {"name": "abc", "file": b"xxx"}

        file: bytes = Field(description="文件")
        name: str = Field(description="名称")

    @swagger_doc(
        tags=["form"],
        summary="form",
        desc="form",
        request_body=TForm,
        responses=[SResponse200(body=SuccessResp)],
    )
    def post(id):
        pass

    assert post.__swagger__.gen_doc() == {
        "tags": ["form"],
        "summary": "form",
        "description": "form",
        "parameters": [],
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "description": "request body",
                        "properties": {
                            "file": {"description": "文件", "type": "string", "format": "binary", "required": True},
                            "name": {"description": "名称", "type": "string", "required": True},
                        },
                    },
                    "example": {"name": "abc", "file": b"xxx"},
                }
            }
        },
        "responses": {
            "200": {
                "description": "OK",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "description": "request body",
                            "properties": {"name": {"description": "姓名", "type": "string", "required": True}},
                        },
                        "example": {"name": "李四"},
                    }
                },
            }
        },
    }
