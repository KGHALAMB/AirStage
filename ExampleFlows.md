Hip-hop artist Iann Dior opens our venue booking website in order to book a venue to perform his new album.
First Iann requests a catalog of all time slots available for different venues by calling GET /venues/get.
Iaan sees in the catalog that there are 20 venues available in the town he wishes to perform in and at the
time he wishes to perform.

Iann then initiates a booking of a venue. To do so, he:

- calls POST /book/create/request_venue/{performer_id} and passes in venue_id 5, time_start at 2023-12-20 16:00:00 -8:00,
  and time_end at 2023-12-20 20:00:00 -8:00.

Iann successfully books the venue for December 12, 2023 from 4:00 pm to 8:00 pm.
