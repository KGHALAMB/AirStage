API Specification

1. Booking Venue

    1.1 Get Open Venues - /venues/ (GET)
    
        Retrieves all available venues to be booked.
        
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
    
    1.2 Book Venue - /book/ (POST)
    
        Creates a booking for a performer at a given venue
        
        Request:
        {
            "user_id": "integer", /* Between 1 and 10,000 */,
            "venue_id": "integer",
            "time_start": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
        
        Returns:
        {
            "success": "boolean"
        }

3. Cancel Booking

    2.1 Get Bookings - /bookings/ (GET)
    
        Retrieves all bookings for a given user.
        
        Request:
        {
            "user_id": "integer" /* Between 1 and 10,000 */
        }
        
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
    
    2.2 Cancel Booking - /cancel/ (POST)
    
        Cancels a booking for a specified user.
        
        Request:
        {
            "user_id": "integer", /* Between 1 and 10,000 */
            "venue_id": "integer" /* Between 1 and 10,00 */
        }
    
        Returns:
        {
            "success": "boolean"
        }

4. Modify Booking

   3.1 Edit Booking - /bookings/ (POST)

   Alters a booking for a specified user.
        
        Request:
        {
            "user_id": "integer", /* Between 1 and 10,000 */
            "venue_id": "integer" /* Between 1 and 10,00 */
            "time_start": "timestamp", /* With timezone */
            "time_end": "timestamp" /* With timezone */
        }
    
        Returns:
        {
            "success": "boolean"
        }

   
