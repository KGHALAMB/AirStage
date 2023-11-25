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
    prefix="/user",
    tags=["user"],
    #dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str
    password: str
    user_type: str

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
        
        # If new username and user type is performer or venue
        if user.user_type == "performer" or user.user_type == "venue":
            # Attempt to create a new user
            type = 0 if user.user_type == "performer" else 1
            user_id_query = connection.execute(sqlalchemy.text("INSERT INTO users (user_type, username, password) VALUES (:a, :b, :c) RETURNING user_id"),
                                            {"a": type, "b": user.username, "c": user.password})
            user_id = user_id_query.first()[0]
            
            # Attempt to insert new performer/venue into respective table
            if user.user_type == "performer":
                connection.execute(sqlalchemy.text("INSERT INTO performers (name, capacity_preference, price, user_id) VALUES (:a, :b, :c, :d)"),
                                                {"a": user.username, "b": 10000, "c": 10000, "d": user_id})
            else:
                connection.execute(sqlalchemy.text("INSERT INTO venues (name, location, capacity, price, user_id) VALUES (:a, :b, :c, :d, :e)"),
                                                {"a": user.username, "b": "San Francisco", "c": 10000, "d": 10000, "e": user_id})
            return { "user_id": user_id, "success": True }
    
# Endpoint for a user to signin
@router.post("/signin/")
def signin(user: User):

    with db.engine.begin() as connection:
        # Check if a user exists with the same username and password
        user_query = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE username = :a AND password = :b"),
                                        {"a": user.username, "b": user.password})
        user_already = user_query.first()
        if not user_already is None:
            return { "success": True }
        
    print("ERROR: LOGIN FAILED")
    return { "success": False }