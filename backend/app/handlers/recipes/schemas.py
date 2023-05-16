from pydantic import BaseModel
from fastapi import Query


class SchemaMery(BaseModel):
    year: int = Query(gt=2000, le=2100)
    month: int = Query(gt=0, le=12)
    ROAD_ID: int | None = Query(ge=0, le=99999999999, default=None)
    DEPO_ID: int | None = Query(ge=0, le=99999999999, default=None)
    COL_NUM: int | None = Query(ge=0, le=99999999999, default=None)
