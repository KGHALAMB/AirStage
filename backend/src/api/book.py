from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
import pytz
#from src.api import auth

utc = pytz.UTC

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

# Helper function to fetch the capacity of the venue
# and the capacity preference of the performer
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

def validate_times(time_start, time_end):
    if (time_start == time_end):
        print("ERROR: CANNOT CREATE A BOOKING WITH NO TIME BETWEEN START AND END")
        return False
    
    if (time_start > time_end):
        print("ERROR: CANNOT CREATE A BOOKING WITH START TIME AFTER END TIME")
        return False
    
    time_s = time_start.replace(tzinfo=utc)
    time_now = datetime.now().replace(tzinfo=utc)
    if (time_s < time_now):
        print("ERROR: CANNOT CREATE A BOOKING IN THE PAST")
        return False
    
    return True

# Helper function to check if the requested booking time works
def check_availability(user_time_start, user_time_end, booking_time_start, booking_time_finish):

    if (user_time_start < booking_time_finish) and (user_time_end > booking_time_start):
        return False
    
    return validate_times(user_time_start, user_time_end)

# Endpoint for a performer to book a venue
@router.post("/create/request_venue/{performer_id}")
def book_venue(performer_id: int, venue_booking: VenueBooking):

    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            venue_exist = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"),
                                              {"a" : venue_booking.venue_id}).first()
            performer_exist = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"),
                                                {"a" : performer_id}).first()
            if venue_exist == None or performer_exist == None:
                print("ERROR: INVALID INPUT FOR PERFORMER OR VENUE")
                return {"success": False}
            capacity, capacity_preference, price = get_capacities(performer_id, venue_booking.venue_id)

            # Check if the venue has enough capacity for the performer
            if capacity >= capacity_preference:
                # Get all bookings of the venue
                bookings = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE venue_id = :a"), {"a": venue_booking.venue_id})
                for booking in bookings:
                    booking_time_start = booking.time_start
                    booking_time_finish = booking.time_end
                    
                    # Check if the requested booking has overlap with any existing bookings of the venue
                    if not check_availability(venue_booking.time_start, venue_booking.time_end, booking_time_start, booking_time_finish):
                        print("ERROR: TIME IS UNAVALAIBLE FOR BOOKING")
                        return { "success": False }
                
                # Create the booking if everything checks out
                connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                            {"a": performer_id, "b": venue_booking.venue_id, "c": venue_booking.time_start, "d": venue_booking.time_end})
                return { "success": True }

            print("ERROR: VENUE DOESN'T HAVE ENOUGH CAPACITY")
            return { "success": False }

# Endpoint for a venue to book a performer
@router.post("/create/request_performer/{venue_id}")
def book_performer(venue_id: int, performer_booking: PerformerBooking):

    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            #check if venue and performer exist
            venue_exist = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a" : venue_id}).first()
            performer_exist = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"),
                                                {"a" : performer_booking.performer_id}).first()
            if venue_exist == None or performer_exist == None:
                print("ERROR: INVALID INPUT FOR PERFORMER OR VENUE")
                return {"success": False}
            capacity, capacity_preference, price = get_capacities(performer_booking.performer_id, venue_id)

            # Check if the venue has enough capacity for the performer
            if capacity >= capacity_preference:
                # Get all bookings of the performer
                bookings = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE performer_id = :a"), {"a": performer_booking.performer_id})
                for booking in bookings:
                    booking_time_start = booking.time_start
                    booking_time_finish = booking.time_end

                    # Check if the requested booking has overlap with any existing bookings of the performer
                    if not check_availability(performer_booking.time_start, performer_booking.time_end, booking_time_start, booking_time_finish):
                        print("ERROR: TIME IS UNAVALAIBLE FOR BOOKING")
                        return { "success": False }
                
                # Create the booking if everything checks out
                connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                        {"a": performer_booking.performer_id, "b": venue_id, "c": performer_booking.time_start, "d": performer_booking.time_end})
                return { "success": True }
    
            print("ERROR: VENUE DOESN'T HAVE ENOUGH CAPACITY")
            return { "success": False }

# Endpoint in order to edit an existing booking
@router.post("/bookings/edit/{booking_id}")
def modify_booking(booking_id: int, booking: Booking):

    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():

            # Check if a booking exists for the given booking id
            booking_query = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
            book = booking_query.first()
            if book is None:
                print("ERROR: THE REQEUSTED BOOKING DOES NOT EXIST")
                return { "success": False }

            performer_id = book.performer_id
            venue_id = book.venue_id
            time_start = book.time_start
            time_end = book.time_end
            
            venue_exist = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"),
                                              {"a" : booking.venue_id}).first()
            performer_exist = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"),
                                                {"a" : booking.performer_id}).first()
            if venue_exist == None or performer_exist == None:
                print("ERROR: INVALID INPUT FOR PERFORMER OR VENUE")
                return {"success": False}

            # Attempt to update the booking and commit the changes
            connection.execute(sqlalchemy.text("UPDATE bookings SET performer_id = :performer_id, venue_id = :venue_id, time_start = :time_start, time_end = :time_end WHERE id = :booking_id"),
                                {"performer_id": booking.performer_id, "venue_id": booking.venue_id, "time_start": booking.time_start, "time_end": booking.time_end, 'booking_id': booking_id})
            
            updated_booking = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
            book = updated_booking.first()
            if not book is None:
                # Check if the updated booking changed any values
                if book.performer_id == performer_id and book.venue_id == venue_id and book.time_start == time_start and book.time_end == time_end:
                    print("ERROR: MODIFICATION IS THE SAME AS THE ORIGINAL")
                    return { "success": False }

                # Ensure that the new values are the expected ones
                if book.performer_id == booking.performer_id and book.venue_id == booking.venue_id and book.time_start == booking.time_start and book.time_end == booking.time_end:
                    print("ERROR: BOOKING DOES NOT HAVE EXPECTED CHANGES")
                    return { "success": False }

    return { "success": True }

# Endpoint to cancel an existing booking
@router.post("/bookings/cancel/{booking_id}")
def delete_booking(booking_id: int):

    with db.engine.begin() as connection:
        # Get the number of bookings
        num_rows_query = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        num_rows = num_rows_query.first()

        # Attempt to delete the requested booking
        connection.execute(sqlalchemy.text("DELETE FROM bookings WHERE id = :booking_id"), {'booking_id': booking_id})
                                           
                                
    with db.engine.begin() as connection:
        # Get the updated number of bookings
        num_rows_query = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        new_num_rows = num_rows_query.first()
        # Check if booking was deleted
        if num_rows == new_num_rows:
                print("ERROR: FAILED TO CANCEL BOOKING")
                return { "success": False }

    return { "success": True }