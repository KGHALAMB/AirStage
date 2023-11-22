API Specification

## 1. Performer Booking a Venue

The API calls are made in this sequence when a performer wants to book a venue to perform at

1.  `Get Open Venues`
2.  `Create Booking (Performer-side)`

    1.1 Get Open Venues - /catalog/venues/ (GET)

    Retrieves all available venues that can be booked.

         Returns:
         [
             {
                 "venue_id": "integer",
                 "name": "string",
                 "location": "string",
                 "capacity": "integer",
                 "price": "integer",
             }
         ]

    1.2 Create Booking (Performer-side) - /book/create/request_venue/{performer_id} (POST)

    Creates a booking for a performer when they want a venue to perform at.

         Request:
         {
             "venue_id": "integer",
             "time_start": "timestamp", /* With timezone */
             "time_end": "timestamp" /* With timezone */
         }

         Returns:
         {
             "success": "boolean"
         }

## 2. Venue Booking a Performer

The API calls are made in this sequence when a venue wants to book a performer to perform at their venue

1.  `Get Performers`
2.  `Create Booking (Venue-side)`

    2.1 Get Open Performers - /catalog/performers/ (GET)

    Retrieves all available performers that can be booked.

         Returns:
         [
             {
                 "performer_id": "integer",
                 "name": "string",
                 "capacity_preference": "integer",
                 "price": "integer"
             }
         ]

    2.2 Create Booking (Venue-side) - /book/create/request_performer/{venue_id} (POST)

    Creates a booking for a venue when they want a performer to perform at their venue.

         Request:
         {
             "performer_id": "integer",
             "time_start": "timestamp", /* With timezone */
             "time_end": "timestamp" /* With timezone */
         }

         Returns:
         {
             "success": "boolean"
         }

## 3. Modifying a Booking

The API calls are made in this sequence when a booking is to be altered

1.  `Get Booking`
2.  `Edit Booking`

    3.1 Get Booking - /catalog/booking/{booking_id} (GET)

    Retrieves the information for a bookingn given its id.

         Request: N/A

         Returns:
         {
             "venue_id": "integer",
             "performer_id": "integer",
             "time_start": "timestamp", /* With timezone */
             "time_end": "timestamp" /* With timezone */
         }

    3.2 Edit Booking - /book/bookings/edit/{booking_id} (POST)

    Edits a booking given its id.

         Request:
         {
             "performer_id": "integer",
             "venue_id": "integer",
             "time_start": "timestamp", /* With timezone */
             "time_end": "timestamp" /* With timezone */
         }

         Returns:
         {
             "success": "boolean"
         }

## 4. User signing up/in

The API calls are made in this sequence when a user is to sign up/login

1.  `Signing up as a user`
2.  `Signing in as a user`

    4.1 Signing up as a user - /user/signup/ (POST)

    Adds a users credentials to the database

        Request:
        {
            "username": "string",
            "password": “string",
            "user_type": "string"
        }

        Returns:
        {
            "success": "boolean"
        }

    4.2 Signing in as a user - /user/signin/ (POST)

    Checks if inputted username and password is associated with an account

        Request:
        {
            "username": "string",
            "password": "string",
            "user_type": "string"
        }

        Returns:
        {
            "success": "boolean"
        }

## 5. Various Testing Endpoints

These are the APIs available for testing purposes.

1.  `Getting User Information`
2.  `Get Booking`
3.  `Get Venue`

    5.1 Getting User Information - /catalog/user/{user_id} (GET)

    Returns the information that is linked to a User

         Request: N/A

         Returns:
         {
             "user_id": "int",
             "user_type": "int",
             "username": "string",
             "password": "string", /* With timezone */
             "time_sign_up": "timestamp" /* With timezone */
         }
