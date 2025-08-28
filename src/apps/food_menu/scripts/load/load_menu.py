import json

from addict import Dict

from apps.food_menu.models import FoodType, Food, Menu, FoodModifierOption, FoodSize, ModifierCategory, ModifierOption
from config import db_settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class MenuJsonLoader:
    def __init__(self, menu_filepath: str = '/app/src/assets/appfood_data.json'):
        with open(menu_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.data = Dict(data)

        SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
        self.db_sess = SessionLocal()

    def _drop_everything(self):
        self.db_sess.query(Menu).delete()
        self.db_sess.query(ModifierOption).delete()
        self.db_sess.query(ModifierCategory).delete()
        self.db_sess.query(FoodModifierOption).delete()
        self.db_sess.query(FoodSize).delete()
        self.db_sess.query(Food).delete()
        self.db_sess.query(FoodType).delete()
        self.db_sess.commit()

    def _load_food_type(self):
        for _ in self.data.sections:
            new_food_type = FoodType(name=_.title)

            self.db_sess.add(new_food_type)

        self.db_sess.commit()

    def load(self):
        self._drop_everything()
        self._load_food_type()


if __name__ == '__main__':
    loader = MenuJsonLoader()
    loader.load()