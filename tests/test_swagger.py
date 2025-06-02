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
        "tags": ["eis"],
        "summary": "eis",
        "description": "eis",
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "description": "请求ID",
                "required": True,
                "schema": {"description": "请求ID", "type": "integer", "required": True},
                "example": 123,
            },
            {
                "name": "Limit",
                "in": "query",
                "description": "页限制",
                "required": True,
                "schema": {"description": "页限制", "type": "integer", "required": True},
            },
            {
                "name": "Offset",
                "in": "query",
                "description": "偏移量",
                "required": False,
                "schema": {"description": "偏移量", "type": "integer", "required": False},
            },
        ],
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
                                "required": True,
                            },
                            "like": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "description": "喜爱东西的名称",
                                            "type": "string",
                                            "required": True,
                                        }
                                    },
                                },
                            },
                            "favorite": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "description": "喜爱东西的名称",
                                        "type": "string",
                                        "required": True,
                                    }
                                },
                            },
                            "rLike": {
                                "type": "object",
                                "properties": {
                                    "like": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "description": "喜爱东西的名称",
                                                "type": "string",
                                                "required": True,
                                            }
                                        },
                                    }
                                },
                            },
                            "ELike": {
                                "type": "array",
                                "items": {"description": "", "required": True, "type": "string"},
                                "description": "elike",
                            },
                            "age": {
                                "description": "年龄",
                                "type": "integer",
                                "required": False,
                            },
                        },
                    },
                    "example": {
                        "name": "张三",
                        "like": [{"name": "李四"}, {"name": "王五"}],
                        "favorite": {"name": "句子"},
                        "rLike": {"like": "abc"},
                        "eLike": ["a", "b", "c"],
                        "age": 34,
                    },
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
                "name": "name",
                "in": "query",
                "description": "",
                "required": True,
                "schema": {"description": "", "type": "string", "required": True},
            },
            {
                "name": "status",
                "in": "query",
                "description": "状态",
                "required": True,
                "schema": {"allOf": [{"description": "状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]}]},
                "example": 1,
            },
            {
                "name": "bstatus",
                "in": "query",
                "description": "状态 1:online, 2:offline/b状态 1:online, 2:offline/",
                "required": True,
                "schema": {
                    "anyOf": [
                        {"description": "状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                        {"description": "b状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                        {"description": "", "type": "string", "required": True},
                    ]
                },
            },
            {
                "name": "bstatusListp",
                "in": "query",
                "description": "",
                "required": False,
                "schema": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {"description": "状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                            {"description": "b状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                            {"description": "", "type": "string", "required": False},
                        ]
                    },
                },
            },
        ],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "description": "request body",
                        "properties": {
                            "name": {"description": "", "type": "string", "required": True},
                            "status": {"description": "状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                            "bstatus": {
                                "anyOf": [
                                    {"description": "状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                                    {"description": "b状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                                    {"description": "", "type": "string", "required": True},
                                ]
                            },
                            "bstatusListp": {
                                "type": "array",
                                "items": {
                                    "anyOf": [
                                        {"description": "状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                                        {"description": "b状态 1:online, 2:offline", "type": "integer", "enum": [1, 2]},
                                        {"description": "", "type": "string", "required": False},
                                    ]
                                },
                            },
                        },
                    },
                    "example": {"status": 1},
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
        "tags": ["eis"],
        "summary": "eis",
        "description": "eis",
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "description": "请求ID",
                "required": True,
                "schema": {"description": "请求ID", "type": "integer", "required": True},
                "example": 123,
            },
            {
                "name": "Limit",
                "in": "query",
                "description": "页限制",
                "required": True,
                "schema": {"description": "页限制", "type": "integer", "required": True},
            },
            {
                "name": "Offset",
                "in": "query",
                "description": "偏移量",
                "required": False,
                "schema": {"description": "偏移量", "type": "integer", "required": False},
            },
        ],
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
                                "required": True,
                            },
                            "like": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "description": "喜爱东西的名称",
                                            "type": "string",
                                            "required": True,
                                        }
                                    },
                                },
                                "description": "i am like",
                            },
                            "favorite": {
                                "allOf": [
                                    {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "description": "喜爱东西的名称",
                                                "type": "string",
                                                "required": True,
                                            }
                                        },
                                        "description": "i am favorite",
                                    }
                                ]
                            },
                            "rLike": {
                                "allOf": [
                                    {
                                        "type": "object",
                                        "properties": {
                                            "like": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {
                                                        "description": "喜爱东西的名称",
                                                        "type": "string",
                                                        "required": True,
                                                    }
                                                },
                                            }
                                        },
                                        "description": "i am rLike",
                                    }
                                ]
                            },
                            "ELike": {
                                "type": "array",
                                "items": {"description": "", "required": True, "type": "string"},
                                "description": "elike",
                            },
                            "age": {
                                "description": "年龄",
                                "type": "integer",
                                "required": False,
                            },
                        },
                    },
                    "example": {
                        "name": "张三",
                        "like": [{"name": "李四"}, {"name": "王五"}],
                        "favorite": {"name": "句子"},
                        "rLike": {"like": "abc"},
                        "eLike": ["a", "b", "c"],
                        "age": 34,
                    },
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


if __name__ == '__main__':
    test_multi_part_request()
