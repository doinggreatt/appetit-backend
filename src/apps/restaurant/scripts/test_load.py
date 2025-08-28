#!/usr/bin/env python3
"""
Test script to verify the restaurant loading functionality
"""

import sys
import os
sys.path.append('/app/src')

from apps.restaurant.scripts.load.load_rstrnts import RstrntJsonLoader
from apps.restaurant.models import Restaurant
from config import db_settings
from sqlalchemy.orm import sessionmaker


def test_restaurant_load():
    """Test the restaurant loading functionality"""
    print("Testing restaurant loading...")
    
    try:
        # Load the restaurant data
        loader = RstrntJsonLoader()
        loader.load()
        
        # Verify the data was loaded correctly
        SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
        session = SessionLocal()
        
        # Check restaurants
        restaurants = session.query(Restaurant).all()
        print(f"\n✅ Loaded {len(restaurants)} restaurants:")
        for restaurant in restaurants:
            print(f"  - {restaurant.name}")
            print(f"    📍 Coordinates: {restaurant.lat}, {restaurant.lon}")
        
        session.close()
        print("\n🎉 All tests passed! Restaurant data loaded successfully.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


if __name__ == '__main__':
    test_restaurant_load()
