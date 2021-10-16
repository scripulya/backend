from constants import ESTONIA_BBOX
import json
from typing import List

from fastapi import FastAPI
from fastapi.params import Query
from fastapi.middleware.cors import CORSMiddleware
from geojson import FeatureCollection, Feature, Point, MultiPolygon
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.future import select
from sqlalchemy import func

from core.models import RentalProperty, Municipality
from setup import async_session

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_median_apartments_price(bbox: list):
    regions = select(Municipality).where(
        func.ST_Intersects(
            Municipality.geom,
            func.ST_MakeEnvelope(*bbox, 4326))).cte("bboxed")
    prices = select(
        regions.c.name,
        regions.c.geom.ST_AsGeoJSON().label("geom"),
        func.count(RentalProperty.coords).label("aparts_count"),
        func.round(
            func.percentile_cont(0.5)\
                .within_group(
                    func.regexp_replace(
                        RentalProperty.price,
                        r'\D+',
                        '',
                        'g').cast(Integer))))
    prices = prices.join(
            RentalProperty,
            func.ST_Intersects(regions.c.geom, RentalProperty.coords))
    prices = prices.group_by(regions.c.name, regions.c.geom)
    return prices


def get_geojson_points_by_bbox(bbox: list):
    points = select(RentalProperty)\
            .cte("rental_coords")
    points = select(
        points.c.resource_link,
        points.c.price,
        points.c.address,
        points.c.coords.ST_AsGeoJSON().label("coords"))\
        .where(
            points.c.coords.ST_Intersects(
                func.ST_MakeEnvelope(*bbox, 4326)))
    return points


@app.get('/get_rent_count_by_municipality/')
async def get_municipalities(bbox: List[float] = Query(ESTONIA_BBOX)):
    message = []
    async with async_session() as session:
        prices = get_median_apartments_price(bbox)
        result = await session.execute(prices)
        for name, geom, count, median in result:
            coords = json.loads(geom)
            coords = coords['coordinates']
            multipolygon = MultiPolygon(coords)

            properties = {
                "municipality_name": name,
                "aparts_count": count,
                "price_median": median
            }
            feature = Feature(geometry=multipolygon, properties=properties)
            message.append(feature)
        message = FeatureCollection(message)
        return message


@app.get('/get_locations/')
async def get_locations(bbox: List[float] = Query(ESTONIA_BBOX)):
    message = []
    async with async_session() as session:
        points = get_geojson_points_by_bbox(bbox)
        result = await session.execute(points)
        for resource_link, price, address, coords in result:
            if coords is None:
                continue
            coords = json.loads(coords)
            coords = coords['coordinates']
            point = Point(coords)

            properties = {
                "address": address,
                "price": price,
                "resource_link": resource_link
            }
            feature = Feature(geometry=point, properties=properties)
            message.append(feature)
    message = FeatureCollection(message)
    return message
