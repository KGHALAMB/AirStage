User Stories

1. As a hip-hop artist, I want to book a large venue that has the capacity for my
fans and that I can book long enough so that I can perform my newest album.

2. As a rock band, I want to book a venue that has has a large enough stage for all
of our band members so that we can perform the way we want to.

3. As an opera singer, I want to book an indoor venue such as a theater or opera
house that has suitable audio reflection from the walls/ceilings so that my
audience can hear my singing.

4. As a venue manager, I want to be able to add my venue to the system so that it can
be booked by a performer.

5. As a clown, I want to be able to book a venue that accomodates my genre of 
performance so that I can find where my services are wanted quickly and efficiently.

6. As an up-and-coming ukelele artist, I want to be able to book a venue that is 
within my $ budget so that I don't need to worry about negotiating prices with venues 
myself.

7. As a concert hall manager, I want to be able to book a singer whose performance is of a
specific duration so that we can manage our schedule around them.

8. As an amphitheater manager, I want to be able to book a performer at a specific time so 
that it fits within our busy schedule.

9. As a venue manager, I want to be able to cancel my venue and have my performers notified
so that I can take action if something really bad happened to the venue building.

10. As a venue manager, I want to be able to change the time slot of my venue availability and
have performers who have already been booked to be notified of the change so that I can have
the flexibility to include more performers in my venue in a given day.

11. As a performer looking to book a venue, I want to be able to filter through venues with conditions such as date/time, venue capacity, location/distance, etc so that I can find a venue
I like in a more convenient manner.

12. As a performer with a booking, I want to be able to cancel my venue booking, given that it complies with the cancelation policy of the venue (an hour before the performance) so that I am
not obligated to perform especially if I have an emergency.

Exceptions

1. Exception: Venue becomes unavailable while trying to book.

If the venue becomes unavailable after already being booked by another performer,
the event will be cancelled and the performer will be informed.

2. Exception: Performer becomes unavailable while trying to book.

If the performer becomes unavailable while booking, the
event will be cancelled and the venue will become available to be booked for
another event, and other performers will be notified of the availability.

3. Exception: Venue doesn't have enough currency to handle the transaction.

If the venue doesn't have enough money to book a performer, the event will
be cancelled and the venue will become available to book. The performer will
be notified of the cancellation.

4. Exception: Performer doesn't have enough currency for the booking.

If the performer doesn't have enough money to book the venue, the application
will cancel the booking and make the venue available.

5. Exception: Consumer of application doesn't have stable internet to access page.

If the consumer who is using our application can't access the webpage, they will
be informed via a 404 status code error.

6. Exception: Performers tries to book overlapping time slots 

If the performer books a venue, they will not be allowed to book another on the same time slot without cancelling the first

7. Exception: A performer tries to cancel last minute:

If a performer tries to cancel last minute, the backend will deny this and will let
the performer know that they cannot cancel within an hour of the performance.

8. Exception: Performer's performance length is longer than venue time slot

If a performer tries to book a venue with their performance lasting longer than the
venue's given availability, the backend will deny booking and will let the performer
know that they need to reduce their performance length or choose another venue that
has a fitting availability.

9. Exception: A venue changes location during a booking

If a venue manager changes a venue's location while a performer is trying to book
the venue, the database will be updated to account for it and the performer will
be notified that they need to try booking again given the new venue's location.
(new transcation).

10. Exception: A performer applies for a venue that does not fit venue requirements (experience, genre, etc)

If a peformer applies for a venue that does not fit venue requirements, the backend will deny the application before it reaches the venue and the performer will be notified that they do not
fit the requirements of the venue.

11. Exception: Performer changes price during a booking

If a performer changes their booking price while a venue manager is trying to book
the performer, the database will be updated to account for it and the venue manager will
be notified that they need to try booking again given the new peformer's booking price.
(new transcation).

12. Exception: Venue changes price during a booking

If a venue manager changes a venue's price while a performer is trying to book
the venue, the database will be updated to account for it and the performer will
be notified that they need to try booking again given the new venue's price (new transcation).
