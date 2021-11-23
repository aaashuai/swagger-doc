from enum import Enum
from typing import Optional, Type, List, Union, Dict

from pydantic import BaseModel, Field, root_validator, validator

__all__ = [
    "SResponse",
    "SResponse200",
    "SResponse204",
    "SResponse400",
    "SResponse401",
    "SResponse403",
    "SResponse404",
    "DocModel",
    "SPath",
    "SHeader",
    "SQuery",
    "SBody",
    "SObject",
    "SSecurity",
    "SecurityType",
    "SecuritySchema",
    "SecurityModel",
    "SecurityIn",
    "STag",
]


class STag(Enum):
    pass


def _parse_one_model(_item, definitions: dict, field: str, required: list):

    # 嵌套对象
    if "properties" in _item:
        ret = {}
        for _field, attrs in _item["properties"].items():
            ret[_field] = _parse_one_model(attrs, definitions, _field, required)
        return ret
    # 数组
    elif "items" in _item:
        if "$ref" in _item["items"]:
            items = _get_ref_model(_item["items"]["$ref"], definitions, field)
        else:
            items = _item["items"]
        ret = {"type": "array", "items": items}
        if _item.get("description"):
            ret.update(description=_item["description"])
        return ret

    # 对象
    elif "$ref" in _item:
        return _get_ref_model(_item["$ref"], definitions, field, _item.get("description"))
    # 枚举
    elif "allOf" in _item:
        return {
            "allOf": [
                _get_ref_model(i["$ref"], definitions, field, _item.get("description"))
                if "$ref" in i
                else _parse_one_model(i, definitions, field, required)
                for i in _item["allOf"]
            ]
        }
    # 枚举
    elif "anyOf" in _item:
        return {
            "anyOf": [
                _get_ref_model(i["$ref"], definitions, field, _item.get("description"))
                if "$ref" in i
                else _parse_one_model(i, definitions, field, required)
                for i in _item["anyOf"]
            ]
        }
    # 普通类型
    else:
        ret = {"description": _item.get("description", "")}
        if "type" in _item:
            ret.update(type=_item["type"])
        if "format" in _item:
            ret.update(format=_item["format"])
        if required:
            ret.update(required=field in required)
        if "enum" in _item:
            ret.update(enum=_item["enum"])
        return ret


def _get_ref_model(ref: str, definitions: dict, field: str, description: str = None):
    prefix = "#/definitions/"
    d_name = ref.replace(prefix, "")
    item = definitions[d_name]
    if "enum" in item:
        return _parse_one_model(item, definitions, field, item.get("required", []))
    ret = {
        "type": "object",
        "properties": _parse_one_model(item, definitions, field, item.get("required", [])),
    }
    if description:
        ret.update(description=description)
    return ret


class SParam(BaseModel):
    __p_type__ = None
    __example__ = None
    ...

    @classmethod
    def get_json(cls) -> List[dict]:
        assert cls.__p_type__ is not None, ValueError("do not use Base Param")
        schema = cls.schema()

        ret = []
        for field, _item in schema["properties"].items():
            one_schema = _parse_one_model(_item, schema.get("definitions", {}), field, schema.get("required", []))
            one = {
                "name": field,
                "in": cls.__p_type__,
                "description": _item.get("description") or cls.parse_description(one_schema),
                "required": field in schema.get("required", []),
                "schema": one_schema,
            }
            example = cls.__example__.get(field) if isinstance(cls.__example__, dict) else cls.__example__
            if example:
                one.update(example=example)
            ret.append(one)
        return ret

    @staticmethod
    def parse_description(schema: dict) -> str:
        """提取description"""
        # allof
        if "allOf" in schema:
            return ",".join([i.get("description", "") for i in schema["allOf"]])
        # anyof
        if "anyOf" in schema:
            return "/".join([i.get("description", "") for i in schema["anyOf"]])
        # other
        return schema.get("description", "")


class SQuery(SParam):
    __p_type__ = "query"


class SPath(SParam):
    __p_type__ = "path"


class SHeader(SParam):
    __p_type__ = "header"


class SObject(BaseModel):
    __example__ = None

    @classmethod
    def get_json(cls):
        assert cls.__example__ is not None, ValueError("do not use Body base")
        schema = cls.schema()

        def parse_model_recursively():
            _properties = {}
            if "properties" not in schema:
                return schema
            for field, attrs in schema["properties"].items():
                _properties[field] = _parse_one_model(
                    attrs,
                    schema.get("definitions", {}),
                    field,
                    schema.get("required", []),
                )
            return _properties

        properties = parse_model_recursively()

        return {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "description": "request body",
                        "properties": properties,
                    },
                    "example": cls.__example__,
                }
            }
        }


SBody = SObject


class SecurityType(Enum):
    http = "http"
    apiKey = "apiKey"


class SecurityIn(Enum):
    query = "query"
    header = "header"
    cookie = "cookie"


class SecuritySchema(Enum):
    basic = "basic"
    bearer = "bearer"


class SecurityModel(BaseModel):
    type: SecurityType
    description: Optional[str] = ""
    name: Optional[str] = None
    in_: Optional[SecurityIn] = Field(None, alias="in")
    scheme: Optional[SecuritySchema] = None

    @root_validator
    def check_fields(cls, values):
        if values["type"] == SecurityType.apiKey:
            if not values["in_"]:
                values["in_"] = SecurityIn.header
            assert values["name"], "请填写 name"
        elif values["type"] == SecurityType.http:
            values["name"] = "BearerAuthentication"
            assert values["scheme"], "请填写 schema"
        else:
            raise ValueError("暂不支持其他类型")

        return values


class SSecurity(BaseModel):
    security: List[Union[SecurityModel, List[SecurityModel]]]

    @staticmethod
    def _get_dict(data: BaseModel) -> dict:
        d = {}
        for k, v in data.dict(by_alias=True, exclude_none=True).items():
            if isinstance(v, Enum):
                d[k] = v.value
            else:
                d[k] = v

        return d

    def get_security(self) -> List[Dict[str, list]]:
        ret = []
        for i in self.security:
            if isinstance(i, list):
                ret.append({str(j.name): [] for j in i})
            elif isinstance(i, SecurityModel):
                ret.append({str(i.name): []})
            else:
                raise ValueError(f"unsupported value type: {i}")
        return ret

    def get_security_schema(self) -> dict:
        ret = {}
        for i in self.security:
            if isinstance(i, list):
                ret.update({str(j.name): self._get_dict(j) for j in i})
            elif isinstance(i, SecurityModel):
                ret.update({str(i.name): self._get_dict(i)})
            else:
                raise ValueError(f"unsupported value type: {i}")
        return ret


class SResponse(BaseModel):
    status_code: int
    description: str
    body: Optional[Type[SObject]] = None

    def get_json(self):
        return {
            self.status_code: {
                "description": self.description,
                **self.body.get_json(),
            }
        }


class SResponse200(SResponse):
    status_code = 200
    description = "OK"


class SResponse204(SResponse):
    status_code = 204
    description = "No Content"


class SResponse400(SResponse):
    status_code = 400
    description = "Bad Request"


class SResponse401(SResponse):
    status_code = 401
    description = "Unauthorized"


class SResponse403(SResponse):
    status_code = 403
    description = "Forbidden"


class SResponse404(SResponse):
    status_code = 404


class DocModel(BaseModel):
    tags: List[Union[str, Enum]]
    summary: str
    desc: str
    responses: List[SResponse]
    auth_required: bool
    request_body: Type[SBody] = None
    path_params: Type[SParam] = None
    query_params: Type[SQuery] = None
    header_params: Type[SHeader] = None

    @validator("auth_required")
    def default_val(cls, val):
        if val is None:
            return True
        return val

    def gen_doc(self):
        ret = {
            "tags": [i.value if isinstance(i, Enum) else i for i in self.tags],
            "summary": self.summary,
            "description": self.desc,
            "parameters": [],
        }
        if self.header_params:
            ret["parameters"].extend(self.header_params.get_json())
        if self.path_params:
            ret["parameters"].extend(self.path_params.get_json())
        if self.query_params:
            ret["parameters"].extend(self.query_params.get_json())
        if self.request_body:
            ret["requestBody"] = self.request_body.get_json()

        code_set = {}

        def _get_next_code(c: int) -> str:
            if c not in code_set:
                code_set[c] = 0
                return str(c)

            code_set[c] += 1
            return f"{c}.{code_set[c]}"

        ret["responses"] = {
            _get_next_code(code): content for i in self.responses for code, content in i.get_json().items()
        }
        return ret
