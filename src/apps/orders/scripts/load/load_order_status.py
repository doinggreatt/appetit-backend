from sqlalchemy.orm import sessionmaker

from config import db_settings
from apps.orders.models import OrderStatus


def load():

    SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
    db_sess = SessionLocal()

    names = (
        "pending", "cooking", "delivery", "finished"
    )

    for name in names:
        new_order_status_obj = OrderStatus(name=name)
        db_sess.add(new_order_status_obj)

    db_sess.commit()

if __name__ == '__main__':
    load()