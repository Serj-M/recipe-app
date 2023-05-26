from pydantic import BaseModel, Field
from typing import Union


class RecipeSchema(BaseModel):
    page: int
    itemsPerPage: int
    sortBy: Union[list, None] = []
    search: dict


class AddRecipeSchema(BaseModel):
    title: str = Field(example='Title ...')
    ingredients: str = Field(example='Ingredients ...')
    instructions: str = Field(example='Instructions...')
    time: int = Field(example=1)
    tags: list[int] = Field(example=[1])


class EditRecipeSchema(BaseModel):
    title: str = Field(example='Edited title ...')
    ingredients: str = Field(example='Edited ingredients ...')
    instructions: str = Field(example='Edited instructions...')
    time: float = Field(example=1)
    tags: list[int] = Field(example=[1])
