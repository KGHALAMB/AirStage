API Specification

## 1. Performer Booking a Venue

The API calls are made in this sequence when a performer wants to book a venue to perform at
1. `Get Open Venues`
2. `Create Booking (Performer-side)`

    1.1 Get Open Venues - /venues/ (GET)
    
    Retrieves all available venues that can be booked.
        
        Returns:
        [
            {
                "venue_id": "integer", /* Between 1 and 10,000 */
                "name": "string",
                "location": "string",
                "capacity": "integer", /* Between 1 and 100,000 */
                "price": "integer", /* Between 1 and 100,000 */
                "time_available": "timestamp", /* With timezone */
                "time_end": "timestamp" /* With timezone */
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
1. `Get Open Performers`
2. `Create Booking (Venue-side)`

   2.1 Get Open Performers - /performers/ (GET)
    
   Retrieves all available performers that can be booked.
        
        Returns:
        [
            {
                "performer_id": "integer", /* Between 1 and 10,000 */
                "name": "string",
                "capacity_preference": "integer", /* Between 1 and 100,000 */
                "price": "integer", /* Between 1 and 100,000 */
                "time_available": "timestamp", /* With timezone */
                "time_end": "timestamp" /* With timezone */
            }
        ]

   2.2 Create Venue - /venues/create (POST)
    
   Creates a venue 
        
        Request:
        {
            "name": "string",
            "location": "string",
            "capacity": "integer", /* Between 1 and 100,000 */
            "price": "integer", /* Between 1 and 100,000 */
            "time_available": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
        
        Returns:
        {
            "success": "boolean"
        }

   2.3 Create Booking (Venue-side) - /book/create/request_performer/{venue_id} (POST)
    
   Creates a booking for a venue when they want a performer to perform at their venue.
        
        Request:
        {
            "performer_id": "integer",
   	    "name": "string",
	    "capacity_preference": "integer", /* Between 1 and 100,000 */
            "price": "integer", /* Between 1 and 100,000 */
            "time_start": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
        
        Returns:
        {
            "success": "boolean"
        } 

## 3. Modifying a Booking

The API calls are made in this sequence when a booking is to be altered
1. `Edit Booking`
2. `Delete Booking`

   3.1 Edit Booking - /book/edit/{booking_id} (POST)

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

   3.2 Cancel Booking - /book/cancel/{booking_id} (POST)
    
   Cancels a booking given its id.
            
        Returns:
        {
            "success": "boolean"
        }
    
## 4. Modifying a Venue

These are the APIs available to modify a venue.
1. `Modify Venue`
2. `Delete Venue`
    
    4.1 Modify Venue - /venues/edit/{venue_id} (POST)
    
    Modifies a given venue
        
        Request:
        {
            "name": "string",
            "location": "string",
            "capacity": "integer", /* Between 1 and 100,000 */
            "price": "integer", /* Between 1 and 100,000 */
            "time_available": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
        
        Returns:
        {
            "success": "boolean"
        }

    4.2 Delete Venue - /venues/delete/{venue_id} (POST)
    
    Deletes a given venue
        
        Returns:
        {
            "success": "boolean"
        }

## 5. User signing up/in

The API calls are made in this sequence when a user is to sign up/login
1. `Signing up as a user`
2. `Signing in as a user`

    5.1 Signing up as a user - /signup/ (POST)

    Adds a users credentials to the database

        Request:
        {
            "username": "string",
            "Password": “string 
        }
    
        Returns:
        {
            "success": "boolean"
        }

    5.2 Signing in as a user - /signin/ (GET)

    Checks if inputted username and password is associated with an account

        Request:
        {
            "username": "string",
            "Password": “string 
        }
    
        Returns:
        {
            "success": "boolean"
        }

## 6. Various Testing Endpoints

These are the APIs available for testing purposes.
1. `Getting User Information`
2. `Get Booking`
3. `Get Venue`
   
    6.1 Getting User Information - /users/{user_id} (GET)
	
    Returns the information that is linked to a User
        
        Returns:
        {
            "username": "string",
            "date_signed_up": "timestamp", /* With timezone */
        }

   6.2 Get Booking - /book/{booking_id} (GET)

   Retrives the booking associated with the given booking id

   	Returns:
        {
            "venue_id": "integer",
            "performer_id": "integer",
            "time_start": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }

   6.3 Get Venue - /venues/{venue_id} (GET)
    
   Retrives the venue associated with the given venue id
        
        Returns:
        
        {
            "venue_id": "integer", /* Between 1 and 10,000 */
            "name": "string",
   	    "location": "string",
   	    "capacity": "integer", /* Between 1 and 100,000 */
            "price": "integer", /* Between 1 and 100,000 */
            "time_available": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
        

   
