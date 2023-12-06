from pickle import FALSE
from re import M
from sqlite3 import Timestamp
from time import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from enum import Enum
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

# Endpoint to signup to create a new user
@router.post("/signup/")
def signup(user: User):

    with db.engine.begin() as connection:
        
        if len(user.username) < 1:
            print("ERROR: CANNOT HAVE EMPTY USERNAME")
            return { "user_id": -1, "success": False }
        
        if len(user.password) < 1:
            print("ERROR: CANNOT HAVE EMPTY PASSWORD")
            return { "user_id": -1, "success": False }
        
        # Check if a user already exists with the same username
        user_query = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE username = :a"), {"a": user.username})
        user_already = user_query.first()
        if not user_already is None:
            print("ERROR: USER ALREADY EXISTS")
            return { "user_id": -1, "success": False }
        
        if user.user_type == UserType.performer or user.user_type == UserType.venue:
            type = 0 if user.user_type == UserType.performer else 1
    
            result = connection.execute(sqlalchemy.text("INSERT  INTO users (user_type, username, password) VALUES (:a, :b, :c) RETURNING user_id"),
                                            {"a": type, "b": user.username, "c": hash(user.password)})
            user_id = result.first()[0]
            if type == UserType.performer:
                result = connection.execute(sqlalchemy.text("INSERT INTO performers (name, capacity_preference, price, user_id) VALUES (:a, :b, :c, :d)"),
                                                {"a": user.username, "b": 10000, "c": 10000, "d": user_id})
            else:
                result = connection.execute(sqlalchemy.text("INSERT INTO venues (name, location, capacity, price, user_id) VALUES (:a, :b, :c, :d, :e)"),
                                                {"a": user.username, "b": "Location", "c": 10000, "d": 10000, "e": user_id})
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
