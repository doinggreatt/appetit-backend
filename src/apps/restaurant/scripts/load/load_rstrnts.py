import json
from typing import Dict, Any

from config import db_settings
from sqlalchemy.orm import sessionmaker

from apps.restaurant.models import Restaurant


class RstrntJsonLoader:
    def __init__(self, restaurant_filepath: str = '/app/src/assets/rstrnts_data.json'):
        with open(restaurant_filepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
        self.db_sess = SessionLocal()

    def _drop_everything(self):
        """Clear all existing restaurant data"""
        print("Clearing existing restaurant data...")
        self.db_sess.query(Restaurant).delete()
        self.db_sess.commit()
        print("Existing restaurant data cleared.")

    def _load_restaurants(self):
        """Load restaurants from JSON data"""
        print("Loading restaurants...")
        
        for restaurant_data in self.data['restaurants']:
            # Check if restaurant already exists by name and coordinates
            existing_restaurant = self.db_sess.query(Restaurant).filter(
                Restaurant.name == restaurant_data['name'],
                Restaurant.lat == restaurant_data['lat'],
                Restaurant.lon == restaurant_data['lon']
            ).first()
            
            if existing_restaurant:
                restaurant = existing_restaurant
                print(f"  Using existing Restaurant: {restaurant.name}")
            else:
                restaurant = Restaurant(
                    name=restaurant_data['name'],
                    lat=restaurant_data['lat'],
                    lon=restaurant_data['lon']
                )
                self.db_sess.add(restaurant)
                print(f"  Created Restaurant: {restaurant.name}")
        
        self.db_sess.commit()
        print("Restaurants loaded successfully.")

    def load(self, clear_all=True):
        """Main loading method
        
        Args:
            clear_all (bool): If True, clears all existing restaurant data before loading
        """
        try:
            print("Starting restaurant data loading...")
            
            if clear_all:
                self._drop_everything()
            
            self._load_restaurants()
            print("Restaurant data loading completed successfully!")
            
        except Exception as e:
            print(f"Error loading restaurant data: {e}")
            self.db_sess.rollback()
            raise
        finally:
            self.db_sess.close()


if __name__ == '__main__':
    loader = RstrntJsonLoader()
    loader.load()
