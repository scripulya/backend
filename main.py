from constants import ESTONIA_BBOX
import json
from typing import List

from fastapi import FastAPI
from fastapi.params import Query
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.future import select
from sqlalchemy import func

from core.models import RentalProperty
from setup import async_session

app = FastAPI()


def get_geojson_points_by_bbox(bbox: list):
    points = select(
        RentalProperty.address,
        RentalProperty.coords)\
            .cte("rental_coords")
    points = select(
        points.c.address,
        points.c.coords.ST_AsGeoJSON().label("coords"))\
        .where(
            points.c.coords.ST_Intersects(
                func.ST_MakeEnvelope(*bbox, 4326)))
    return points


@app.get('/get_locations/')
async def get_locations(bbox: List[float] = Query(ESTONIA_BBOX)):
    message = []
    async with async_session() as session:
        points = get_geojson_points_by_bbox(bbox)
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
