# Case 1

### Lost Update Phenomenon

Consider the case in which two requests are being made concurrently to modify the same booking (`/bookings/edit/{booking_id}`). This might happen practically in our application if a performer and a venue want to modify an existing booking that they share.

Before:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE id=X
   Booking X

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE id=X
   Booking X

   B Updates      UPDATE bookings SET ... WHERE id=X
   Booking X
                |------- Transaction B Commits -------|

                |---------- Transaction A ----------|

   A Updates      UPDATE bookings SET ... WHERE id=X
   Booking X

                |------- Transaction A Commits -------|

```

As you can see, the values from Transaction B would have been overridden while Transaction A still executes. To prevent this, our code uses the serializable isolation level. This enables the requests to now be processed in a linear fashion. This does indeed lose the performance boost of handling this concurrently but does yield more safe outcomes.

After:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE id=X
   Booking X

   A Updates      UPDATE bookings SET ... WHERE id=X
   Booking X

                |------- Transaction A Commits -------|

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE id=X
   Booking X

   B Updates      UPDATE bookings SET ... WHERE id=X
   Booking X

                |------- Transaction B Commits -------|

```

### Write Skew

Without concurrency control, this endpoint also has the potential for a write skew. If one of the concurrent calls updates
only a few columns such as the (`performer_id`) and (`venue_id`) but then the other call updates with a new time of the event, then the id's and time of the performance will be mismatched since each update call updated a different part of the row concurrently.

Before:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE id=X
   Booking X

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE id=X
   Booking X

   B Updates      UPDATE bookings SET performer_id=5, venue_id=8 ... WHERE id=X
   Booking X
                |------- Transaction B Commits -------|

                |---------- Transaction A ----------|

   A Updates      UPDATE bookings SET ... time_start=2023-11-30 18:00:00+00:00, time_end=2023-11-30 20:00:00+00:00 WHERE id=X
   Booking X

                |------- Transaction A Commits -------|

```

As we can see, the id's of the performer and venue will be mismatched since they concurrently updated different columns of the same row in the database. As before, this issue is resolved by using a serializable isolation level in order to make each user complete their sequences of queries in a linear fashion.

After:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE id=X
   Booking X

   A Updates      UPDATE bookings SET ... time_start=2023-11-30 18:00:00+00:00, time_end=2023-11-30 20:00:00+00:00 WHERE id=X
   Booking X

                |------- Transaction A Commits -------|

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE id=X
   Booking X

   B Updates      UPDATE bookings SET performer_id=5, venue_id=8, time_start=2023-11-29 12:00:00+00:00,
   Booking X                                                      time_end=2023-11-29 16:00:00+00:00 ... WHERE id=X


                |------- Transaction B Commits -------|

```

Due to isolating each transaction, the transactions run one after the other, so when B updates the booking, it will update the performer and venue id's whilst maintaining the original time assuming that the times provided by B are the original times of the booking.

# Case 2

### Phantom Read #1

Consider the case in which two requests are being made concurrently by performers book the same venue (`/create/request_venue/{performer_id}`). This might happen practically in our application if two separate performers try to book the same venue at the same time.

Before:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE venue_id=X
   Bookings
   With Venue
   ID X

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE venue_id=X
   Bookings
   With Venue
   ID X

   B Creates      INSERT INTO bookings (performer_id, venue_id, time_start, time_end)
   Booking                      VALUES (B, X, 2023-11-30 16:00:00+00:00, 2023-11-30 18:00:00+00:00)
   With Venue
   ID X
                |------- Transaction B Commits -------|

                |---------- Transaction A ----------|

   A Creates      INSERT INTO bookings (performer_id, venue_id, time_start, time_end)
   Booking                      VALUES (A, X, 2023-11-30 16:00:00+00:00, 2023-11-30 18:00:00+00:00)
   With Venue
   ID X

                |------- Transaction A Commits -------|

```

As you can see, both transactions will commit successfully without rolling back since each of them will see the time they want to book as being available. To prevent this from occurring, our code uses the serializable isolation level. This enables the request to be processed linearly such that one performer will create the booking before the other performer checks to see if the booking is available. There will be some performance loss when handling concurrency due to transactions happening one after another, however, it does give us safer outcomes.

After:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE venue_id=X
   Bookings
   With Venue
   ID X

   A Creates      INSERT INTO bookings (performer_id, venue_id, time_start, time_end)
   Booking                      VALUES (A, X, 2023-11-30 16:00:00+00:00, 2023-11-30 18:00:00+00:00)
   With Venue
   ID X

                |------- Transaction A Commits -------|

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE venue_id=X
   Bookings
   With Venue
   ID X

                  B will not be able to create booking due to time conflict.

                |------- Transaction B Commits -------|

```

# Case 3

### Phantom Read #2

Consider the case in which two requests are being made concurrently by performers book the same venue (`/create/request_performer/{venue_id}`). This might happen practically in our application if two separate performers try to book the same venue at the same time.

Before:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE performer_id=X
   Bookings
   With Performer
   ID X

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE performer_id=X
   Bookings
   With Performer
   ID X

   B Creates      INSERT INTO bookings (performer_id, venue_id, time_start, time_end)
   Booking                      VALUES (X, B, 2023-11-30 16:00:00+00:00, 2023-11-30 18:00:00+00:00)
   With Performer
   ID X
                |------- Transaction B Commits -------|

                |---------- Transaction A ----------|

   A Creates      INSERT INTO bookings (performer_id, venue_id, time_start, time_end)
   Booking                      VALUES (X, A, 2023-11-30 16:00:00+00:00, 2023-11-30 18:00:00+00:00)
   With Performer
   ID X

                |------- Transaction A Commits -------|

```

As you can see, both transactions will commit successfully without rolling back since each of them will see the time they want to book as being available. To prevent this from occurring, our code uses the serializable isolation level. This enables the request to be processed linearly such that one performer will create the booking before the other performer checks to see if the booking is available. There will be some performance loss when handling concurrency due to transactions happening one after another, however, it does give us safer outcomes.

After:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE performer_id=X
   Bookings
   With Performer
   ID X

   A Creates      INSERT INTO bookings (performer_id, venue_id, time_start, time_end)
   Booking                      VALUES (X, A, 2023-11-30 16:00:00+00:00, 2023-11-30 18:00:00+00:00)
   With Performer
   ID X

                |------- Transaction A Commits -------|

                |---------- Transaction B ----------|

   B Reads        SELECT * FROM bookings WHERE performer_id=X
   Bookings
   With Performer
   ID X

                  B will not be able to create booking due to time conflict.

                |------- Transaction B Commits -------|

```
