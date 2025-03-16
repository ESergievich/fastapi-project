from typing import TypeVar

from pydantic import BaseModel

from models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
FiterInSchemaType = TypeVar("FiterInSchemaType", bound=BaseModel)
