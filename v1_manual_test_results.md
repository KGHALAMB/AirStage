## Example Workflow: Performer Booking a Venue

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

# Testing Results

1. 
curl -X 'GET' \
  'https://airstage-api.onrender.com/catalog/venues/' \
  -H 'accept: application/json'

2.
[
  {
    "venue_id": 1,
    "name": "2023-10-27T22:03:02.106027+00:00",
    "location": "San Francisco",
    "capacity": 10000,
    "price": 50000,
    "time_available": "2023-10-28T00:00:00+00:00",
    "time_end": "2023-10-28T03:00:00+00:00"
  }
]

1.
curl -X 'POST' \
  'https://airstage-api.onrender.com/book/create/request_venue/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "venue_id": 1
}'

2.
{
  "success": true
}
