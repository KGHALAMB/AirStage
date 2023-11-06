## Example Workflow: User signing up/in

The API calls are made in this sequence when a user is to sign up/login
1. `Signing up as a user`
2. `Signing in as a user`

    5.1 Signing up as a user - /user/signup/ (POST)

    Adds a users credentials to the database

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

    5.2 Signing in as a user - /user/signin/ (POST)

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

# Testing Results

1.
curl -X 'POST' \
  'https://airstage-api.onrender.com/user/signup/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SoloPlayer123",
  "password": "Xlkjvl38$%",
  "user_type": "performer"
}'

2.
{
  "success": true
}

1.
curl -X 'POST' \
  'https://airstage-api.onrender.com/user/signin/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SoloPlayer123",
  "password": "Xlkjvl38$%",
  "user_type": "performer"
}'

2.
{
  "success": true
}

## Example Workflow: User editing booking

The API calls are made in this sequence when a booking is to be altered
1. `Get Booking`
2. `Edit Booking`

   3.1 Get Booking - /book/{booking_id} (GET)

   Retrieves the information for a bookingn given its id.

        Request: N/A

        Returns:
        {
            "venue_id": row.venue_id,
            "performer_id": row.performer_id,
            "time_start": row.time_start,
            "time_end": row.time_end
        }

   3.2 Edit Booking - /book/edit/{booking_id} (POST)

   Edits a booking given its id.
        
        Request:
        {
            "performer_id": "integer", /* Between 1 and 10,000 */
            "venue_id": "integer" /* Between 1 and 10,00 */
            "time_start": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
    
        Returns:
        {
            "success": "boolean"
        }

# Testing Results

1.
curl -X 'GET' \
  'https://airstage-api.onrender.com/book/3' \
  -H 'accept: application/json'

2.
{
  "venue_id": 1,
  "performer_id": 1,
  "time_start": "2023-11-06T21:00:00+00:00",
  "time_end": "2023-11-06T23:00:00+00:00"
}

1.
curl -X 'POST' \
  'https://airstage-api.onrender.com/book/bookings/edit/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "performer_id": 1,
  "venue_id": 1,
  "time_start": "2023-11-06 22:00:00+00",
  "time_end": "2023-11-06 24:00:00+00"
}'

2.
{
  "success": true
}