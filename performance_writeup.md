# Fake Data Modeling

## Link to populate.py file: (`/populate.py`)
https://github.com/KGHALAMB/AirStage/blob/main/populate.py

## Number of Rows Per Table:

### Users: 250,000

### Performers: 174,589

### Venues: 75,411

### Bookings: 997,064

We thought that the data should scale in the manner for several reasons. First of all, it is much more realistic for there to be more performers than venues, so they were created with 70/30 odds respectively. Additionally, it is very realistic for there to be multiple bookings for each performer, so therefore, there are much more bookings than users, with each user have very little bookings are a larger number of bookings.

# Performance Testing

### /catalog/venues

1013 ms

### /catalog/performers

1840 ms

### /catalog/booking/{booking_id} 101000

50 ms

### /catalog/users/{user_id} 50000

7 ms

### /book/create/request_venue/{performer_id} 47863

152 ms

### /book/create/request_performer/{venue_id} 52942

46 ms

### /book/bookings/edit/{booking_id} 14

17 ms

### /book/bookings/cancel/{booking_id} 2

96 ms

### /user/signup/

61 ms

### /user/signin/

32 ms

## Performance Tuning

### /catalog/performers

#### SELECT \* FROM performers

Seq Scan on performers (cost=0.00..3063.89 rows=174589 width=30) (actual time=0.009..19.873 rows=174589 loops=1)
Planning Time: 0.541 ms
Execution Time: 27.527 ms

As we can see, since all rows from the performers table are being retrieved, the execution time is very long. We cannot however add an index since we are not querying based off of any particular parameters, so in order to decrease our execution time, the best solution would be to add pagination.

### Speedup Plan

Since this endpoint only has a single query that gets all rows from a particular table, creating a key in this situation isn't plausible. The best solution in this case would be to add pagination to the endpoint to make it so that the results we get are limited, and thus speeding up the execution time significantly.

### Changes Made

We updated the endpoint to limit the result to 100 whilst adding pagination to be able to get a set of 100 results at a time, whilst still also being able to access all rows.

### Results Explained

Limit (cost=8.77..10.53 rows=100 width=30) (actual time=0.084..0.146 rows=100 loops=1)
-> Seq Scan on performers (cost=0.00..3063.89 rows=174589 width=30) (actual time=0.010..0.066 rows=600 loops=1)
Planning Time: 0.719 ms
Execution Time: 0.237 ms

As we can see, there is a massive performance improvement. Even though we didn't add an index, adding pagination significantly improved our results, since instead of having around 174,000 results being retreived, only 100 results are retrieved at a time.

### /catalog/venues

#### SELECT \* FROM venues

Seq Scan on venues (cost=0.00..1450.11 rows=75411 width=43) (actual time=0.003..7.669 rows=75413 loops=1)
Planning Time: 0.265 ms
Execution Time: 10.428 ms

As we can see, since all rows from the venues table are being retrieved, the execution time is very long. We cannot however add an index since we are not querying based off of any particular parameters, so in order to decrease our execution time, the best solution would be to add pagination.

### Speedup Plan

Since this endpoint only has a single query that gets all rows from a particular table, creating a key in this situation isn't plausible. The best solution in this case would be to add pagination to the endpoint to make it so that the results we get are limited, and thus speeding up the execution time significantly.

### Changes Made

We updated the endpoint to limit the result to 100 whilst adding pagination to be able to get a set of 100 results at a time, whilst still also being able to access all rows.

### Results Explained

Limit (cost=9.61..11.54 rows=100 width=43) (actual time=0.147..0.179 rows=100 loops=1)
-> Seq Scan on venues (cost=0.00..1450.11 rows=75411 width=43) (actual time=0.009..0.147 rows=600 loops=1)
Planning Time: 0.753 ms
Execution Time: 0.255 ms

As we can see, there is a massive performance improvement. Even though we didn't add an index, adding pagination significantly improved our results, since instead of having around 75,000 results being retreived, only 100 results are retrieved at a time.

### /book/create/request_venue/{performer_id}

#### SELECT \* FROM venues WHERE venue_id = 1234

Index Scan using venues_pkey on venues (cost=0.29..8.31 rows=1 width=43) (actual time=0.120..0.121 rows=1 loops=1)
Index Cond: (venue_id = 1234)
Planning Time: 0.604 ms
Execution Time: 0.245 ms

#### SELECT \* FROM performers WHERE performer_id = 47863

Index Scan using performers_pkey on performers (cost=0.42..8.44 rows=1 width=30) (actual time=0.131..0.132 rows=1 loops=1)
Index Cond: (performer_id = 47863)
Planning Time: 0.694 ms
Execution Time: 0.233 ms

#### SELECT \* FROM bookings WHERE venue_id = 1234

Gather (cost=1000.00..13531.04 rows=60 width=28) (actual time=76.417..78.726 rows=4 loops=1)
Workers Planned: 2
Workers Launched: 2
-> Parallel Seq Scan on bookings (cost=0.00..12525.04 rows=25 width=28)
Filter: (venue_id = 1234)
Rows Removed by Filter: 332354
Planning Time: 0.609 ms
Execution Time: 71.894 ms

For this endpoint, we can see that 2 of our queries are using the primary key to filter, so adding an index to that would be redundant. However, as we can see in the last query, we are doing a SELECT based on the (`venue_id`), but that is not unique within the booking table, thus, creating an index on this column would make the search much more efficient.

### Index Creation

(`CREATE INDEX venue_id_idx ON bookings (venue_id);`)

### Rerun Explain Results

Index Scan using venue_id_idx on bookings (cost=0.42..231.37 rows=60 width=28) (actual time=0.109..0.122 rows=4 loops=1)
Index Cond: (venue_id = 1234)
Planning Time: 0.922 ms
Execution Time: 0.192 ms

### Results Explained

Creating the index has a very large improvement on the original query, and it was in fact the results that we expected, if not better. By creating an index on a non-unique column, we can greatly decrease the execution time of our query. As expected, we can also see that the planning time is slightly higher, but is more than compensated for in the execution time.
