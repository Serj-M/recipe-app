from pydantic import BaseModel


class RecipeSchema(BaseModel):
    page: int
    itemsPerPage: int
    sortBy: list | None
    search: dict | None


class AddRecipeSchema(BaseModel):
    title: str
    ingredients: str
    instructions: str
    time: int
    tags: list[int]


class EditRecipeSchema(BaseModel):
    title: str
    ingredients: str
    instructions: str
    time: float
    tags: list[int]
