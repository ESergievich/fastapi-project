import json
from typing import Optional, Type

from fastapi import Query, HTTPException
from pydantic import Field, BaseModel, ValidationError


def create_filter_params(filter_schema: Type[BaseModel]):
    fields = getattr(filter_schema, "model_fields", {})
    example_tags = {field: [] for field in fields}
    example_json = json.dumps(example_tags)

    class FilterParams(BaseModel):
        limit: int = Field(100, gt=0)
        offset: int = Field(0, ge=0)
        order_by: str = Field("created_at")
        tags: Optional[str] = Query(default=example_json, example=example_json)

        def get_parsed_tags(self) -> Optional[dict[str, list[str]]]:
            if not self.tags:
                return None

            try:
                validated_data = filter_schema.model_validate(json.loads(self.tags))
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400, detail="Invalid JSON format in tags parameter"
                )
            except ValidationError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid filter parameters: {e.errors()}"
                )
            return validated_data.model_dump(exclude_defaults=True)

    return FilterParams
