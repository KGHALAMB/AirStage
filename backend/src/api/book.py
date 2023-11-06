from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
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

class Booking(BaseModel):
    booking_id: int
    venue_id: str
    performer_id: str
    time_start: str 
    time_end: int

@router.post("/create/request_venue/{performer_id}")
def book_venue(performer_id: int, venue: Venue):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"), {"a": performer_id})
        for row in result:
            capacity_preference = row.capacity_preference
            time_available = row.time_available
            time_end = row.time_end

        result = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue.venue_id})
        for row in result:
            capacity = row.capacity
            price = row.price
            # time_start = row.time_available
            # time_finish = row.time_end

        if capacity >= capacity_preference:
            # need to test this logic

            time_works = True
            result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE venue_id = :a"), {"a": venue.venue_id})
            for row in result:
                time_start = row.time_start
                time_finish = row.time_end

                if not (time_available >= time_start and time_available <= time_finish) or (time_end >= time_start and time_end <= time_finish):
                    #return { "success": False }
                    time_works = False
            
            if time_works:
                result = connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                            {"a": performer_id, "b": venue.venue_id, "c": time_available, "d": time_end})
                return { "success": True }

    return { "success": False }

@router.post("/venues/edit/{venue_id}")
def modify_venue(venue: Venue):

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("UPDATE venues SET name = :name, location = :location, capacity = :capacity, price = :price, time_available = :time_available, time_end = :time_end WHERE venue_id = :venue_id;"),
                            {"venue_id": venue.venue_id, "name":venue.name, "location":venue.location, "capacity":venue.capacity, "price":venue.price, "time_available":venue.time_available, "time_end":venue.time_end})

    return { "success": True }

@router.post("/venues/delete/{venue_id}")
def delete_venue(venue: Venue):

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM venues WHERE venue_id = :venue_id;"), {'venue_id':venue.venue_id})
                                           
    return { "success": True }

@router.post("/book/edit/{booking_id} ")
def modify_booking(booking: Booking):

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("UPDATE bookings SET performer_id = :performer_id, venue_id = :venue_id, time_start = :time_start, time_end = :time_end WHERE booking_id = :booking_id;"),
                            {"performer_id": booking.performer_id, "venue_id":booking.venue_id, "time_start":booking.time_start, "time_end":booking.time_end, 'booking_id':booking.booking_id})

    return { "success": True }

@router.post("/book/cancel/{booking_id}")
def delete_booking(booking: Booking):

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM bookings WHERE booking_id = :booking_id;"), {'booking_id':booking.booking_id})
                                           
    return { "success": True }