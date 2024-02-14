import os

from typing import List
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
)


db_params = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DATABASE"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

engine = create_engine(
    f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}"
)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    title = Column(String(255))
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String(255))
    phone_number = Column(String(20))
    image_url = Column(String(255))
    images_count = Column(Integer)
    car_number = Column(String(20))
    car_vin = Column(String(50), index=True)
    datetime_found = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("car_vin", name="car_vin_unique_constraint"),)


def save_cars(cars: List[dict], session):
    try:
        stmt = (
            insert(Car)
            .values(cars)
            .on_conflict_do_update(
                constraint="car_vin_unique_constraint",
                set_={k: v for car in cars for k, v in car.items() if k != "id"},
            )
        )

        session.execute(stmt)
        session.commit()

    except Exception as e:
        session.rollback()
        raise

    finally:
        session.close()
