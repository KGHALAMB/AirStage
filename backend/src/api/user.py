from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional
#from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    #dependencies=[Depends(auth.get_api_key)],
)

class UserType(str, Enum):
    performer = "performer"
    venue = "venue"

class User(BaseModel):
    username: str
    password: str
    user_type: UserType

class VenueBooking(BaseModel):
    venue_id: int
    time_start: datetime
    time_end: datetime

class PerformerBooking(BaseModel):
    performer_id: int
    time_start: datetime
    time_end: datetime

class PerformerUpdate(BaseModel):
    name: Optional[str]
    capacity_preference: Optional[int]
    price: Optional[int]
    availabilities: Optional[List[PerformerBooking]]

class VenueUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    capacity: Optional[int]
    price: Optional[int]
    availabilities: Optional[List[VenueBooking]]  # Add this field for availability updates

# Endpoint to signup to create a new user
@router.post("/signup/")
def signup(user: User):

    with db.engine.begin() as connection:
        # Check if a user already exists with the same username
        user_query = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE username = :a"), {"a": user.username})
        user_already = user_query.first()
        if not user_already is None:
            print("ERROR: USER ALREADY EXISTS")
            return { "user_id": -1, "success": False }
        
        if user.user_type == UserType.performer or user.user_type == UserType.venue:
            type = 0 if user.user_type == UserType.performer else 1
    
            result = connection.execute(sqlalchemy.text("INSERT INTO users (user_type, username, password) VALUES (:a, :b, :c) RETURNING user_id"),
                                            {"a": type, "b": user.username, "c": hash(user.password)})
            user_id = result.first()[0]

            # Insert the current time into the availabilities table
            if type == 0:
                result = connection.execute(sqlalchemy.text("INSERT INTO performers (name, user_id) VALUES (:a, :b, :c, :d)"),
                                                {"a": user.username, "b": 10000, "c": 10000, "d": user_id})
                connection.execute(sqlalchemy.text("INSERT INTO availabilities (performer_id, time_available, time_end) " \
                                                   "SELECT performer_id, now(), now() + INTERVAL '1 day' FROM performers WHERE name = :username"),
                                    {"username": user.username})
            else:
                result = connection.execute(sqlalchemy.text("INSERT INTO venues (name, location, capacity, price, user_id) VALUES (:a, :b, :c, :d, :e)"),
                                                {"a": user.username, "b": "San Francisco", "c": 10000, "d": 10000, "e": user_id})
                connection.execute(sqlalchemy.text("INSERT INTO availabilities (venue_id, time_available, time_end) " \
                                                   "SELECT venue_id, now(), now() + INTERVAL '1 day' FROM venues WHERE name = :username"),
                                    {"username": user.username})
                
            return { "user_id": user_id, "success": True }

    print("ERROR: USER TYPE IS INVALID")
    return { "user_id": -1, "success": False }

# Endpoint for a user to signin
@router.post("/signin/")
def signin(user: User):

    with db.engine.begin() as connection:
        # Check if a user exists with the same username and password
        user_query = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE username = :a AND password = :b"),
                                        {"a": user.username, "b": hash(user.password)})
        user_already = user_query.first()
        if not user_already is None:
            return { "success": True }
        
    print("ERROR: LOGIN FAILED")
    return { "success": False }

# Endpoint to add availability for a performer
@router.post("/add_performer_availability/{performer_id}")
def add_performer_availability(performer_id: int, availability_updates: List[PerformerBooking]):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            # Check if the performer exists
            performer_query = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"), {"a": performer_id})
            performer = performer_query.first()
            if performer is None:
                raise HTTPException(status_code=404, detail="Performer not found")

            # Check if the provided availability periods already exist for the performer
            for update in availability_updates:
                existing_availability = connection.execute(
                    sqlalchemy.text("SELECT * FROM availabilities WHERE performer_id = :a AND (:user_time_start < time_end) AND (:user_time_end > time_available)"),
                    {"a": performer_id, "user_time_start": update.time_start, "user_time_end": update.time_end},
                )
                if existing_availability.first():
                    print("ERROR: TIME ALREADY EXISTS IN AVAILABILITIES TABLE")
                    return {"success": False}

            # Add the provided availability periods for the performer
            for update in availability_updates:
                connection.execute(
                    sqlalchemy.text("INSERT INTO availabilities (performer_id, time_available, time_end) VALUES (:a, :b, :c)"),
                    {"a": performer_id, "b": update.time_start, "c": update.time_end},
                )

            return {"success": True}

        
# Endpoint to add availability for a venue
@router.post("/add_venue_availability/{venue_id}")
def add_venue_availability(venue_id: int, availability_updates: List[VenueBooking]):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            # Check if the venue exists
            venue_query = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue_id})
            venue = venue_query.first()
            if venue is None:
                raise HTTPException(status_code=404, detail="Venue not found")

            # Check if the provided availability periods already exist for the venue
            for update in availability_updates:
                existing_availability = connection.execute(
                    sqlalchemy.text("SELECT * FROM availabilities WHERE venue_id = :a AND (:user_time_start < time_end) AND (:user_time_end > time_available)"),
                    {"a": venue_id, "user_time_start": update.time_start, "user_time_end": update.time_end},
                )
                if existing_availability.first():
                    print("ERROR: TIME ALREADY EXISTS IN AVAILABILITIES TABLE")
                    return {"success": False}

            # Add the provided availability periods for the venue
            for update in availability_updates:
                connection.execute(
                    sqlalchemy.text("INSERT INTO availabilities (venue_id, time_available, time_end) VALUES (:a, :b, :c)"),
                    {"a": venue_id, "b": update.time_start, "c": update.time_end},
                )

            return {"success": True}

        
# Endpoint to update performer information and availability
@router.put("/update/performer/{performer_id}")
def update_performer(performer_id: int, performer_update: PerformerUpdate):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            # Check if the performer exists
            performer_query = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"), {"a": performer_id})
            performer = performer_query.first()
            if performer is None:
                raise HTTPException(status_code=404, detail="Performer not found")

            # Update performer information
            update_values = {k: v for k, v in performer_update.dict().items() if v is not None and k != 'availabilities'}
            if update_values:
                connection.execute(sqlalchemy.text("UPDATE performers SET " + ", ".join(f"{k} = :{k}" for k in update_values) + " WHERE performer_id = :performer_id"),
                                {**update_values, "performer_id": performer_id})

            # Update performer availability
            if performer_update.availabilities:
                # First, delete existing availabilities for the performer
                connection.execute(sqlalchemy.text("DELETE FROM availabilities WHERE performer_id = :a"), {"a": performer_id})

                # Add the provided availability periods for the performer
                for update in performer_update.availabilities:
                    connection.execute(
                        sqlalchemy.text("INSERT INTO availabilities (performer_id, time_available, time_end) VALUES (:a, :b, :c)"),
                        {"a": performer_id, "b": update.time_start, "c": update.time_end},
                    )

            return {"success": True}

# Endpoint to update venue information and availability
@router.put("/update/venue/{venue_id}")
def update_venue(venue_id: int, venue_update: VenueUpdate):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            # Check if the venue exists
            venue_query = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue_id})
            venue = venue_query.first()
            if venue is None:
                raise HTTPException(status_code=404, detail="Venue not found")

            # Update venue information
            update_values = {k: v for k, v in venue_update.dict().items() if v is not None and k != 'availabilities'}
            if update_values:
                connection.execute(sqlalchemy.text("UPDATE venues SET " + ", ".join(f"{k} = :{k}" for k in update_values) + " WHERE venue_id = :venue_id"),
                                {**update_values, "venue_id": venue_id})

            # Update venue availability
            if venue_update.availabilities:
                # First, delete existing availabilities for the venue
                connection.execute(sqlalchemy.text("DELETE FROM availabilities WHERE venue_id = :a"), {"a": venue_id})

                # Add the provided availability periods for the venue
                for update in venue_update.availabilities:
                    connection.execute(
                        sqlalchemy.text("INSERT INTO availabilities (venue_id, time_available, time_end) VALUES (:a, :b, :c)"),
                        {"a": venue_id, "b": update.time_start, "c": update.time_end},
                    )

            return {"success": True}
