from re import M
from fastapi import APIRouter, Depends
#from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/catalog",
    tags=["catalog"],
    #dependencies=[Depends(auth.get_api_key)],
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
                "price": row.price,
                "time_available": row.time_available,
                "time_end": row.time_end,
            })

    return json
