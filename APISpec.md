API Specification

1. Venues

    1.1 Get Open Venues - /venues/get (GET)
    
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

    1.2 Create Venue - /venues/create (POST)
    
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

    1.3 Modify Venue - /venues/edit/{venue_id} (POST)
    
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

    1.4 Delete Venue - /venues/delete/{venue_id} (POST)
    
        Deletes a given venue
        
        Returns:
        {
            "success": "boolean"
        }
    
2. Bookings
    
    2.1 Create Booking (Venue-side) - /book/create/request_performer/{venue_id} (POST)
    
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

    2.2 Create Booking (Performer-side) - /book/create/request_venue/{performer_id} (POST)
    
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

    2.3 Cancel Booking - /book/cancel/{booking_id} (POST)
    
        Cancels a booking given its id.
            
        Returns:
        {
            "success": "boolean"
        }

    2.4 Edit Booking - /book/edit/{booking_id} (POST)

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

    2.5 Get Booking - /book/get/{booking_id}
   
        Returns:
        {
            "venue_id": "integer",
            "performer_id": "integer",
            "time_start": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }

3. Users

    3.1 Signing up as a user - /signup/ (POST)

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

    3.2 Signing in as a user - /signin/ (GET)

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

    3.3 Getting Users Information - /users/{user_id}
	
        Returns the information that is linked to a User
        
        Returns:

        {
            "username": "string",
            "date_signed_up": "timestamp", /* With timezone */
        }

   


   
