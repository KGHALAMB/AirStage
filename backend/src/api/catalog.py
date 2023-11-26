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

# Endpoint to retrieve all venues
@router.get("/venues/")
def get_venues():

    json = []
    with db.engine.begin() as connection:
        venues = connection.execute(sqlalchemy.text("SELECT * FROM venues"))
        for venue in venues:
            json.append({
                "venue_id": venue.venue_id,
                "name": venue.name,
                "location": venue.location,
                "capacity": venue.capacity,
                "price": venue.price
            })

    return json

# Endpoint to retrieve all performers
@router.get("/performers/")
def get_performers():

    json = []
    with db.engine.begin() as connection:
        performers = connection.execute(sqlalchemy.text("SELECT * FROM performers"))
        for performer in performers:
            json.append({
                "performer_id": performer.performer_id,
                "name": performer.name,
                "capacity_preference": performer.capacity_preference,
                "price": performer.price
            })

    return json

# Endpoint to retreive a specific booking
@router.get("/booking/{booking_id}")
def get_booking(booking_id: int):

    json = {}
    with db.engine.begin() as connection:
        booking_query = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :a"), {"a": booking_id})
        booking = booking_query.first()
        if not booking is None:
            json = {
                "venue_id": booking.venue_id,
                "performer_id": booking.performer_id,
                "time_start": booking.time_start,
                "time_end": booking.time_end
            }

    return json

# Endpoint to retrieve a specific user's information
@router.get("/user/{user_id}")
def get_user(user_id: int):

    json = {}
    with db.engine.begin() as connection:
        user_query = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE user_id = :a"), {"a": user_id})
        user = user_query.first()
        if not user is None:
            if user.user_type == 0:
                user_type = "performer"
            else:
                user_type = "venue"
            json = {
                "user_id": user.user_id,
                "user_type": user_type,
                "username": user.username,
                "password": user.password,
                "time_sign_up": user.time_sign_up
            }

    return json
