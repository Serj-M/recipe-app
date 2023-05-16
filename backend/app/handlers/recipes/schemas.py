from pydantic import BaseModel


class RecipeSchema(BaseModel):
    page: int
    itemsPerPage: int
    sortBy: list | None
    search: dict | None
