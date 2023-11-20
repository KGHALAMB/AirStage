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

@router.post("/signup/")
def signup(user: User):

    with db.engine.begin() as connection:
        user_exists = False
        result = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE username = :a"), {"a": user.username})
        for row in result:
            user_exists = True
        
        if not user_exists:
            if user.user_type == "performer" or user.user_type == "venue":
                if user.user_type == "performer":
                    type = 0
                else:
                    type = 1
                result = connection.execute(sqlalchemy.text("INSERT INTO users (user_type, username, password) VALUES (:a, :b, :c) RETURNING user_id"),
                                                {"a": type, "b": user.username, "c": user.password})
                user_id = result.first()[0]
                if type == 0:
                    result = connection.execute(sqlalchemy.text("INSERT INTO performers (name, capacity_preference, price, user_id) VALUES (:a, :b, :c, :d)"),
                                                    {"a": user.username, "b": 10000, "c": 10000, "d": user_id})
                else:
                    result = connection.execute(sqlalchemy.text("INSERT INTO venues (name, location, capacity, price, user_id) VALUES (:a, :b, :c, :d, :d)"),
                                                    {"a": user.username, "b": "San Francisco", "c": 10000, "d": 10000, "e": user_id})
                return { "success": True }
    print("ERROR: USER ALREADY EXISTS")
    return { "success": False }

@router.post("/signin/")
def signup(user: User):

    with db.engine.begin() as connection:
        user_exists = False
        result = connection.execute(sqlalchemy.text("SELECT * FROM users WHERE username = :a AND password = :b"),
                                        {"a": user.username, "b": user.password})
        for row in result:
            return { "success": True }
    print("ERROR: USER DOES NOT EXIST")
    return { "success": False }