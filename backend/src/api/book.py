from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends
#from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/book",
    tags=["book"],
    #dependencies=[Depends(auth.get_api_key)],
)


@router.post("/create/request_venue/{performer_id}")
def book_venue(performer_id: int, venue_id: int, time_start: Timestamp, time_end: Timestamp):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM performers WEHRE performer_id = :a"), {"a": performer_id})
        for row in result:
            capacity_preference = row.capacity_preference
            time_available = row.time_available
            time_end = row.time_end

        result = connection.execute(sqlalchemy.text("SELECT * FROM venues WHERE venue_id = :a"), {"a": venue_id})
        for row in result:
            capacity = row.capacity
            price = row.price
            # time_start = row.time_available
            # time_finish = row.time_end

        if capacity >= capacity_preference:
            # need to test this logic
            time_works = True
            result = connection.execute(sqlalchemy.text("SELECT * FROM bookings WHERE venue_id = :a", {"a": venue_id}))
            for row in result:
                time_start = row.time_start
                time_finish = row.time_end

                if not (time_available >= time_start and time_available <= time_finish) or (time_end >= time_start and time_end <= time_finish):
                    #return { "success": False }
                    time_works = False
            
            if time_works:
                result = connection.execute(sqlalchemy.text("INSERT INTO bookings (performer_id, venue_id, time_start, time_end) VALUES (:a, :b, :c, :d)"),
                                            {"a": performer_id, "b": venue_id, "c": time_available, "d": time_end})
                return { "success": True }

    return { "success": False }