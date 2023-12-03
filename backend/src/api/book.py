from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

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

class UserType(str, Enum):
    performer = "performer"
    venue = "venue"

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

    return capacity, capacity_preference

# Helper function to check if the requested booking time works
def check_availability(user_time_start, user_time_end, availability_rows):
    for row in availability_rows:
        booking_time_start = row.time_available
        booking_time_finish = row.time_end
        print(user_time_start)
        print(user_time_end)
        print(booking_time_start)
        print(booking_time_finish)
        if (user_time_start <= booking_time_finish and user_time_start >= booking_time_start and 
            user_time_end <= booking_time_finish and user_time_end >= booking_time_start):
            return True
    return False

# Endpoint for a venue to book a performer
@router.post("/create/request_performer/{venue_id}")
def book_performer(venue_id: int, performer_booking: PerformerBooking):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():


            venue_exist = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"),
                                              {"a" : venue_id}).first()
            performer_exist = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"),
                                                {"a" : performer_booking.performer_id}).first()
            if venue_exist == None or performer_exist == None:
                print("ERROR: INVALID INPUT FOR PERFORMER OR VENUE")
                return {"success": False}
            
            capacity, capacity_preference = get_capacities(performer_booking.performer_id, venue_id)


            # Check if the venue has enough capacity for the performer
            if capacity >= capacity_preference:
                # Check if the requested time is available for booking in the availabilities table
                availabilities = connection.execute(
                    sqlalchemy.text("SELECT * FROM availabilities WHERE performer_id = :performer_id AND (:user_time_start < time_end) AND (:user_time_end > time_available)"),
                    {"performer_id": performer_booking.performer_id, "user_time_start": performer_booking.time_start, "user_time_end": performer_booking.time_end}
                )

                if not check_availability(performer_booking.time_start, performer_booking.time_end, availabilities):
                    print("ERROR: TIME IS UNAVAILABLE FOR BOOKING")
                    return {"success": False}

                # Check if there's already a booking at the given time
                existing_booking = connection.execute(
                    sqlalchemy.text("SELECT * FROM bookings WHERE venue_id = :venue_id AND (:user_time_start < time_end) AND (:user_time_end > time_start)"),
                    {"venue_id": venue_id, "user_time_start": performer_booking.time_start, "user_time_end": performer_booking.time_end}
                ).first()

                if existing_booking:
                    print("ERROR: PERFORMER IS ALREADY BOOKED AT THIS TIME")
                    return {"success": False}

                # Create the booking if everything checks out
                connection.execute(
                    sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                    {"a": performer_booking.performer_id, "b": venue_id, "c": performer_booking.time_start, "d": performer_booking.time_end},
                )
                return {"success": True}

            print("ERROR: VENUE DOESN'T HAVE ENOUGH CAPACITY")
            return {"success": False}

# Endpoint for a performer to book a venue
@router.post("/create/request_venue/{performer_id}")
def book_venue(performer_id: int, venue_booking: VenueBooking):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():

            #check if venue and performer exist
            venue_exist = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a" : venue_booking.venue_id}).first()
            performer_exist = connection.execute(sqlalchemy.text("SELECT * FROM performers WHERE performer_id = :a"),
                                                {"a" : performer_id}).first()
            if venue_exist == None or performer_exist == None:
                print("ERROR: INVALID INPUT FOR PERFORMER OR VENUE")
                return {"success": False}
            
            capacity, capacity_preference = get_capacities(performer_id, venue_booking.venue_id)

            # Check if the venue has enough capacity for the performer
            if capacity >= capacity_preference:
                # Check if the requested time is available for booking in the availabilities table
                availabilities = connection.execute(
                    sqlalchemy.text(
                        "SELECT * FROM availabilities WHERE venue_id = :venue_id AND (:user_time_start < time_end) AND (:user_time_end > time_available)"
                    ),
                    {"venue_id": venue_booking.venue_id, "user_time_start": venue_booking.time_start, "user_time_end": venue_booking.time_end},
                )

                if not check_availability(venue_booking.time_start, venue_booking.time_end, availabilities):
                    print("ERROR: TIME IS UNAVAILABLE FOR BOOKING")
                    return {"success": False}

                # Check if there's already a booking at the given time
                existing_booking = connection.execute(
                    sqlalchemy.text("SELECT * FROM bookings WHERE performer_id = :performer_id AND (:user_time_start < time_end) AND (:user_time_end > time_start)"),
                    {"performer_id": performer_id, "user_time_start": venue_booking.time_start, "user_time_end": venue_booking.time_end}
                ).first()

                if existing_booking:
                    print("ERROR: VENUE IS ALREADY BOOKED AT THIS TIME")
                    return {"success": False}
                # Create the booking if everything checks out
                connection.execute(
                    sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                    {"a": performer_id, "b": venue_booking.venue_id, "c": venue_booking.time_start, "d": venue_booking.time_end},
                )
                return {"success": True}

            print("ERROR: VENUE DOESN'T HAVE ENOUGH CAPACITY")
            return {"success": False}

# Endpoint in order to edit an existing booking
@router.post("/bookings/edit/{booking_id}")
def modify_booking(booking_id: int, booking: Booking):
    with db.engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            # Check if a booking exists for the given booking id
            booking_query = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
            book = booking_query.first()
            if book is None:
                print("ERROR: THE REQUESTED BOOKING DOES NOT EXIST")
                return {"success": False}

            performer_id = book.performer_id
            venue_id = book.venue_id
            time_start = book.time_start
            time_end = book.time_end

            # Check if the requested time is available for booking
            if not check_availability(UserType.performer, booking.performer_id, booking.time_start, booking.time_end) or \
               not check_availability(UserType.venue, booking.venue_id, booking.time_start, booking.time_end):
                print("ERROR: TIME IS UNAVAILABLE FOR BOOKING")
                return {"success": False}

            # Attempt to update the booking and commit the changes
            connection.execute(sqlalchemy.text("UPDATE bookings SET performer_id = :performer_id, venue_id = :venue_id, time_start = :time_start, time_end = :time_end WHERE id = :booking_id"),
                {"performer_id": booking.performer_id, "venue_id": booking.venue_id, "time_start": booking.time_start, "time_end": booking.time_end, "booking_id": booking_id},
            )

            updated_booking = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})
            book = updated_booking.first()
            if not book:
                print("ERROR: THE UPDATED BOOKING DOES NOT EXIST")
                return {"success": False}

            # Check if the updated changed any values
            if book.performer_id == performer_id and book.venue_id == venue_id and book.time_start == time_start and book.time_end == time_end:
                print("ERROR: MODIFICATION IS THE SAME AS THE ORIGINAL")
                return {"success": False}

            # Ensure that the new values are the expected ones
            if book.performer_id != booking.performer_id or book.venue_id != booking.venue_id or book.time_start != booking.time_start or book.time_end != booking.time_end:
                print("ERROR: BOOKING DOES NOT HAVE EXPECTED CHANGES")
                return {"success": False}

    return {"success": True}

# Endpoint to cancel an existing booking
@router.post("/bookings/cancel/{booking_id}")
def delete_booking(booking_id: int):
    with db.engine.begin() as connection:
        # Get the number of bookings
        num_rows_query = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        num_rows = num_rows_query.first()

        # Attempt to delete the requested booking
        connection.execute(sqlalchemy.text("DELETE FROM bookings WHERE id = :booking_id"), {"booking_id": booking_id})

    with db.engine.begin() as connection:
        # Get the updated number of bookings
        num_rows_query = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS num_rows FROM bookings"))
        new_num_rows = num_rows_query.first()
        # Check if booking was deleted
        if num_rows == new_num_rows:
            print("ERROR: FAILED TO CANCEL BOOKING")
            return {"success": False}

    return {"success": True}
