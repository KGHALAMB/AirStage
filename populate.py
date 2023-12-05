from datetime import timezone
import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

def database_connection_url():
    return "postgresql://postgres:postgres@127.0.0.1:54322/postgres"

    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

with engine.begin() as conn:
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS users CASCADE;
    DROP TABLE IF EXISTS performers;
    DROP TABLE IF EXISTS venues;
    DROP TABLE IF EXISTS bookings;

    CREATE TABLE 
    users (
        user_id integer generated by default as identity,
        user_type integer not null,
        username text not null,
        password bigint not null,
        time_sign_up timestamp with time zone not null default (now() at time zone 'utc'::text),
        constraint users_pkey primary key (user_id)
    );

    CREATE TABLE
    performers (
        performer_id integer generated by default as identity,
        name text not null,
        capacity_preference integer null,
        price integer not null default 0,
        user_id integer not null,
        constraint performers_pkey primary key (performer_id),
        constraint performers_user_id_fkey foreign key (user_id) references users (user_id)
    );
        
    CREATE TABLE
    venues (
        venue_id integer generated by default as identity,
        name text not null,
        location text not null,
        capacity integer not null,
        price integer not null,
        user_id integer not null,
        constraint venues_pkey primary key (venue_id),
        constraint venues_user_id_fkey foreign key (user_id) references users (user_id)
    );

    CREATE TABLE
    bookings (
        id integer generated by default as identity,
        performer_id integer not null,
        venue_id integer not null,
        time_start timestamp with time zone not null,
        time_end timestamp with time zone not null,
        constraint bookings_pkey primary key (id)
    );
    """))

num_users = 250000
fake = Faker()
bookings_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, num_users)
users_sample_distribution = np.random.choice([0, 1], num_users, p=[0.7, 0.3])
users = []
performers = []
venues = []
time = fake.date_time_between(start_date='-5y', end_date='-5y', tzinfo=timezone.utc)
total_bookings = 0

# create fake bookings with fake users with fake names and passwords
with engine.begin() as conn:
    print("creating fake bookings and users...")
    bookings = []
    for i in range(num_users):
        if (i % 1000 == 0):
            print(i)
        
        user_type = users_sample_distribution[i].item()
        username = fake.unique.name()
        password = fake.password(length=12)
        date_signup = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=timezone.utc)

        user_id = conn.execute(sqlalchemy.text("""
        INSERT INTO users (user_type, username, password, time_sign_up) VALUES (:user_type, :username, :password, :time_sign_up) RETURNING user_id;
        """), {"user_type": user_type, "username": username, "password": hash(password), "time_sign_up": date_signup}).scalar_one()

        users.append({ "user_id": user_id, "user_type": user_type, "creation": date_signup })
        if user_type == 0: # if user is performer
            performer_id = conn.execute(sqlalchemy.text("""
            INSERT INTO performers (name, capacity_preference, price, user_id) VALUES (:name, :capacity_preference, :price, :user_id) RETURNING performer_id;
            """), {"name": username, "capacity_preference": np.random.randint(1000, 30000), "price": np.random.randint(1000, 30000), "user_id": user_id}).scalar_one()

            performers.append({ "id": performer_id, "creation": date_signup })
        else: # if user is venue
            location = fake.city()
            venue_id = conn.execute(sqlalchemy.text("""
            INSERT INTO venues (name, location, capacity, price, user_id) VALUES (:name, :location, :capacity, :price, :user_id) RETURNING venue_id;
            """), {"name": username, "location": location, "capacity": np.random.randint(1000, 30000), "price": np.random.randint(1000, 30000), "user_id": user_id}).scalar_one()

            venues.append({ "id": venue_id, "creation": date_signup })

    for i in range(num_users):
        if (i % 1000 == 0):
            print("booking ", i)

        user = users[i]

        if user["user_type"] == 0: # if user is performer
            performer_id = user["user_id"]
            performer_creation = user["creation"]
            idx = np.random.randint(0, len(venues)-1)
            venue = venues[idx]
            venue_id = venue["id"]
            venue_creation = venue["creation"]
        else:
            venue_id = user["user_id"]
            venue_creation = user["creation"]
            idx = np.random.randint(0, len(performers)-1)
            performer = performers[idx]
            performer_id = performer["id"]
            performer_creation = performer["creation"]

        earliest = min(performer_creation, venue_creation)

        time_start = fake.date_time_between(start_date=time, end_date='now', tzinfo=timezone.utc)
        time_end = fake.date_time_between(start_date=time_start, end_date='+5h', tzinfo=timezone.utc)
        time = time_end

        num_bookings = bookings_sample_distribution[i] 
        for j in range(num_bookings):
            total_bookings += 1
            bookings.append({
                "performer_id": performer_id,
                "venue_id": venue_id,
                "time_start": time_start,
                "time_end": time_end
            })

    if bookings:
        conn.execute(sqlalchemy.text("""
        INSERT INTO bookings (performer_id, venue_id, time_start, time_end) 
        VALUES (:performer_id, :venue_id, :time_start, :time_end);
        """), bookings)

    print("total bookings: ", total_bookings)