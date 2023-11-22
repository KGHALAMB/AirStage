from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
#from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/book",
    tags=["book"],
    #dependencies=[Depends(auth.get_api_key)],
)

class Venue(BaseModel):
    venue_id: int
    name: str
    location: str
    capacity: int 
    price: int
    time_available: str
    time_end: str 

class Performer(BaseModel):
    performer_id: int
    name: str
    capacity_preference: int
    price: int
    time_available: str
    time_end: str

class Booking(BaseModel):
    performer_id: int
    venue_id: int
    time_start: str 
    time_end: str

class VenueBooking(BaseModel):
    venue_id: int
    time_start: datetime
    time_end: datetime

class PerformerBooking(BaseModel):
    performer_id: int
    time_start: str
    time_end: str


@router.post("/create/request_venue/{performer_id}")
def book_venue(performer_id: int, venue_booking: VenueBooking):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"), {"a": performer_id})
        for row in result:
            capacity_preference = row.capacity_preference

        result = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue_booking.venue_id})
        for row in result:
            capacity = row.capacity
            price = row.price

        if capacity >= capacity_preference:
            time_works = True
            result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE venue_id = :a"), {"a": venue_booking.venue_id})
            for row in result:
                time_start = row.time_start
                time_finish = row.time_end
                
                if (venue_booking.time_start <= time_finish) and (venue_booking.time_end >= time_start):
                    time_works = False
            
            if time_works:
                result = connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                            {"a": performer_id, "b": venue_booking.venue_id, "c": venue_booking.time_start, "d": venue_booking.time_end})
                return { "success": True }

    return { "success": False }

@router.post("/create/request_performer/{venue_id}")
def book_venue(venue_id: int, performer_booking: PerformerBooking):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue_id})
        for row in result:
            capacity = row.capacity

        result = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"), {"a": performer_booking.performer_id})
        for row in result:
            capacity_preference = row.capacity_preference
            price = row.price

        if capacity >= capacity_preference:
            time_works = True
            result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE performer_id = :a"), {"a": performer_booking.performer_id})
            for row in result:
                time_start = row.time_start
                time_finish = row.time_end

                if (performer_booking.time_start <= time_finish) and (performer_booking.time_end >= time_start):
                    time_works = False
            
            if time_works:
                result = connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                            {"a": performer_booking.performer_id, "b": venue_id, "c": performer_booking.time_start, "d": performer_booking.time_end})
                return { "success": True }

    return { "success": False }


@router.post("/bookings/edit/{booking_id}")
def modify_booking(booking_id: int, booking: Booking):

    with db.engine.begin() as connection:
        booking_exists = False
        result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
        for row in result:
            booking_exists = True
            performer_id = row.performer_id
            venue_id = row.venue_id
            time_start = row.time_start
            time_end = row.time_end

        if not booking_exists:
            return { "success": False }

        connection.execute(sqlalchemy.text("UPDATE bookings SET performer_id = :performer_id, venue_id = :venue_id, time_start = :time_start, time_end = :time_end WHERE id = :booking_id;"),
                            {"performer_id": booking.performer_id, "venue_id": booking.venue_id, "time_start": booking.time_start, "time_end": booking.time_end, 'booking_id': booking_id})
        connection.commit()

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
        for row in result:
            if row.performer_id == performer_id and row.venue_id == venue_id and row.time_start == time_start and row.time_end == time_end:
                return { "success": False }

    return { "success": True }

@router.post("/bookings/cancel/{booking_id}")
def delete_booking(booking_id: int):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        for row in result:
            num_rows = row.num_rows

        connection.execute(sqlalchemy.text("DELETE FROM bookings WHERE id = :booking_id;"), {'booking_id': booking_id})
                                           
                                
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        for row in result:
            if num_rows == row.num_rows:
                return { "success": False }

    return { "success": True }







#     @router.post("/venues/edit/{venue_id}")
# def modify_venue(venue_id: int, venue: Venue):

#     with db.engine.begin() as connection:
#         venue_exists = False
#         result = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :venue_id"), {"venue_id", venue_id})
#         for row in result:
#             venue_exists = True
#             name = row.name
#             location = row.location
#             capacity = row.capacity
#             price = row.price
#             time_available = row.time_available
#             time_end = row.time_end

#         if not venue_exists:
#             return { "success": False }

#         connection.execute(sqlalchemy.text("UPDATE venues SET name = :name, location = :location, capacity = :capacity, price = :price, time_available = :time_available, time_end = :time_end WHERE venue_id = :venue_id;"),
#                             {"venue_id": venue_id, "name": venue.name, "location": venue.location, "capacity": venue.capacity, "price": venue.price, "time_available": venue.time_available, "time_end": venue.time_end})
#         connection.commit()

#     with db.engine.begin() as connection:
#         result = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :venue_id"), {"venue_id": venue_id})
#         for row in result:
#             if row.name == name and row.location == location and row.capacity == capacity and row.price == price and row.time_available == time_available and row.time_end == time_end:
#                 return { "success": False }

#     return { "success": True }

# @router.post("/venues/delete/{venue_id}")
# def delete_venue(venue_id: int):

#     with db.engine.begin() as connection:
#         result = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM venues"))
#         for row in result:
#             num_rows = row.num_rows

#         connection.execute(sqlalchemy.text("DELETE FROM venues WHERE venue_id = :venue_id;"), {'venue_id': venue_id})

#         with db.engine.begin() as connection:
#             result = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM venues"))
#             for row in result:
#                 if num_rows == row.num_rows:
#                     return { "success": False }
                                           
#     return { "success": True }