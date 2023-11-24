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
    time_start: datetime
    time_end: datetime


def get_capacities(performer_id, venue_id):

    with db.engine.begin() as connection:
        performer_query = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"), {"a": performer_id})
        performer = performer_query.first()
        capacity_preference = performer.capacity_preference

        venue_query = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue_id})
        venue = venue_query.first()
        capacity = venue.capacity
        price = venue.price

    return capacity, capacity_preference, price

def check_availability(user_time_start, user_time_end, booking_time_start, booking_time_finish):

    if (user_time_start < booking_time_finish) and (user_time_end > booking_time_start):
        return False
    return True


@router.post("/create/request_venue/{performer_id}")
def book_venue(performer_id: int, venue_booking: VenueBooking):

    with db.engine.begin() as connection:
        
        capacity, capacity_preference, price = get_capacities(performer_id, venue_booking.venue_id)

        if capacity >= capacity_preference:
            bookings = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE venue_id = :a"), {"a": venue_booking.venue_id})
            for booking in bookings:
                booking_time_start = booking.time_start
                booking_time_finish = booking.time_end
                
                if not check_availability(venue_booking.time_start, venue_booking.time_end, booking_time_start, booking_time_finish):
                    print("ERROR: TIME IS UNAVALAIBLE FOR BOOKING")
                    return { "success": False }
                
            connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                        {"a": performer_id, "b": venue_booking.venue_id, "c": venue_booking.time_start, "d": venue_booking.time_end})
            return { "success": True }

    print("ERROR: VENUE DOESN'T HAVE ENOUGH CAPACITY")
    return { "success": False }

@router.post("/create/request_performer/{venue_id}")
def book_venue(venue_id: int, performer_booking: PerformerBooking):

    with db.engine.begin() as connection:

        capacity, capacity_preference, price = get_capacities(performer_booking.performer_id, venue_id)

        if capacity >= capacity_preference:
            bookings = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE performer_id = :a"), {"a": performer_booking.performer_id})
            for booking in bookings:
                booking_time_start = booking.time_start
                booking_time_finish = booking.time_end

                if not check_availability(performer_booking.time_start, performer_booking.time_end, booking_time_start, booking_time_finish):
                    print("ERROR: TIME IS UNAVALAIBLE FOR BOOKING")
                    return { "success": False }
            
            connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                    {"a": performer_booking.performer_id, "b": venue_id, "c": performer_booking.time_start, "d": performer_booking.time_end})
            return { "success": True }
    
    print("ERROR: VENUE DOESN'T HAVE ENOUGH CAPACITY")
    return { "success": False }


@router.post("/bookings/edit/{booking_id}")
def modify_booking(booking_id: int, booking: Booking):

    with db.engine.begin() as connection:
        booking_exists = False
        booking_query = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
        for book in booking_query:
            booking_exists = True
            performer_id = book.performer_id
            venue_id = book.venue_id
            time_start = book.time_start
            time_end = book.time_end

        if not booking_exists:
            print("ERROR: THE REQEUSTED BOOKING DOES NOT EXIST")
            return { "success": False }

        connection.execute(sqlalchemy.text("UPDATE bookings SET performer_id = :performer_id, venue_id = :venue_id, time_start = :time_start, time_end = :time_end WHERE id = :booking_id"),
                            {"performer_id": booking.performer_id, "venue_id": booking.venue_id, "time_start": booking.time_start, "time_end": booking.time_end, 'booking_id': booking_id})
        connection.commit()

    with db.engine.begin() as connection:
        updated_booking = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
        for book in updated_booking:
            if booking.performer_id == performer_id and booking.venue_id == venue_id and booking.time_start == time_start and booking.time_end == time_end:
                print("ERROR: MODIFICATION IS THE SAME AS THE ORIGINAL")
                return { "success": False }

    return { "success": True }

@router.post("/bookings/cancel/{booking_id}")
def delete_booking(booking_id: int):

    with db.engine.begin() as connection:
        num_rows_query = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        num_rows = num_rows_query.first()

        connection.execute(sqlalchemy.text("DELETE FROM bookings WHERE id = :booking_id"), {'booking_id': booking_id})
                                           
                                
    with db.engine.begin() as connection:
        num_rows_query = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        new_num_rows = num_rows_query.first()
        if num_rows == new_num_rows:
                print("ERROR: FAILED TO CANCEL BOOKING")
                return { "success": False }

    return { "success": True }