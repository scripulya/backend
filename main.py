import json

from fastapi import FastAPI
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm.session import sessionmaker

from core.models import RentalProperty
from credentials import DATABASE_CREDENTIALS

app = FastAPI()

user = DATABASE_CREDENTIALS['user']
host = DATABASE_CREDENTIALS['host']
password = DATABASE_CREDENTIALS['password']
port = DATABASE_CREDENTIALS['port']
database = DATABASE_CREDENTIALS['database']

db_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
engine = create_async_engine(db_uri, echo=True, future=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@app.get('/get_locations')
async def get_locations():
    message = []
    async with async_session() as session:
        points = select(
            RentalProperty.address,
            RentalProperty.coords.ST_AsGeoJSON().label("coords"))
        result = await session.execute(points)
        for address, coords in result:
            if coords is None:
                continue
            coords = json.loads(coords)
            coords = coords['coordinates']
            point = Point(coords)
            feature = Feature(geometry=point, properties={"address": address})
            message.append(feature)
    message = FeatureCollection(message)
    return message
