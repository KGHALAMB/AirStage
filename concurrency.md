# Case 1

### Lost Update Phenomenon

Consider the case in which two requests are being made concurrently to modify the same booking (`/bookings/edit/{booking_id}`). This might happen practically in our application if a performer and a venue want to modify an existing booking that they share.

Before:

```

                |---------- Transaction A ----------|

   A Reads        SELECT * FROM bookings WHERE id=X
   Booking X

                |---------- Transaction B ----------|

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

   A Updates
   Booking X      UPDATE bookings SET ... WHERE id=X

                |------- Transaction A Commits -------|

                |---------- Transaction B ----------|

   Read           SELECT * FROM bookings WHERE id=X
   Booking X

   Update
   Booking X      UPDATE bookings SET ... WHERE id=X

                |------- Transaction B Commits -------|

```

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
