from re import M
from fastapi import APIRouter, Depends
# from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/catalog",
    tags=["catalog"],
    # dependencies=[Depends(auth.get_api_key)],
)


@router.get("/venues/")
def get_venues():

    json = []
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM venues"))
        for row in result:
            json.append({
                "venue_id": row.venue_id,
                "name": row.name,
                "location": row.location,
                "capacity": row.capacity,
                "price": row.price
            })

    return json


@router.get("/performers/")
def get_venues():

    json = []
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT * FROM performers"))
        for row in result:
            json.append({
                "performer_id": row.performer_id,
                "name": row.name,
                "capacity_preference": row.capacity_preference,
                "price": row.price,
                "time_available": row.time_available,
                "time_end": row.time_end
            })

    return json


@router.get("/booking/{booking_id}")
def get_booking(booking_id: int):

    json = {}
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :a"), {"a": booking_id})
        for row in result:
            json = {
                "venue_id": row.venue_id,
                "performer_id": row.performer_id,
                "time_start": row.time_start,
                "time_end": row.time_end
            }

    return json

@router.get("/user/{user_id}")
def get_booking(user_id: int):

    json = {}
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE user_id = :a"), {"a": user_id})
        for row in result:
            json = {
                "user_id": row.user_id,
                "user_type": row.user_type,
                "username": row.username,
                "password": row.password,
                "time_sign_up": row.time_sign_up
            }

    return json
