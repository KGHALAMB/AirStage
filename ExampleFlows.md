Example 1

Hip-hop artist Iann Dior opens our venue booking website in order to book a venue to perform his new album.
First Iann requests a catalog of all time slots available for different venues by calling GET /venues/get.
Iaan sees in the catalog that there are 20 venues available in the town he wishes to perform in and at the
time he wishes to perform.

Iann then initiates a booking of a venue. To do so, he:

- calls POST /book/create/request_venue/{performer_id} and passes in venue_id 5, time_start at 2023-12-20 16:00:00 -8:00,
  and time_end at 2023-12-20 20:00:00 -8:00.

Iann successfully books the venue for December 12, 2023 from 4:00 pm to 8:00 pm.

Example 2

Taylor Swift wants to create an account on our website as a performer so she can book venues for her tour.
First Taylor requests to add her account to our database by calling POST /signup/, inputting a username and password in the payload.
Taylor will see that the sign up was successful, so she then attempts to log into her account
She calls GET /signin/, which will take the username and password she entered as the payload.  This endpoint will check to see if the username and password exist within the users table and will return successful because Taylor just made her account.
Taylor has successfully created an account and logged in.

Example 3

Underground drill rapper BabyShark has a fleeting feeling that there’s been a miscommunication with the venue he’s booked regarding his performance start time. First, BabyShark requests his booking by calling GET /book/get/{200} and passing in his booking_id (ex. 200). BabyShark would be able to see the listed start and end time for this booking and can check to see if he wants it any different. If he does want to change the start time (say, to 5:00 PM), he can:
call /book/edit/{200} (passing in booking_id 200), passing in performer_id (ex. 5), venue_id (ex. 10), the new time_start at 2023-11-12 17:00:00 -5:00 and the original time_end at 2023-11-12 20:00:00 -8:00. This will return successful.

BabyShark has successfully edited his booking to change the start time to 2023-11-12 17:00:00 -5:00.
