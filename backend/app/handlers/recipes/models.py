from sqlalchemy import (Column, Float, ForeignKey, Integer, Text, CheckConstraint, UniqueConstraint)
from sqlalchemy.orm import declarative_base

Recipes_Base = declarative_base()


class RecipesModel(Recipes_Base):

    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(Text, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    time = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('title'),
        CheckConstraint('time >= 0', name='time_check')
    )


class TagsModel(Recipes_Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('tag'),
    )


class RecipesTags(Recipes_Base):
    """
    Association table for many-to-many
    """
    __tablename__ = 'recipes_tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('recipe_id', 'tag_id'),
    )
