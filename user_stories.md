As a hip-hop artist, I want to book a large venue that has the capacity for my
fans and that I can book long enough so that I can perform my newest album.

As a rock band, I want to book a venue that has has a large enough stage for all
of our band members.

As an opera singer, I want to book an indoor venue such as a theater or opera
house that has suitable audio reflection from the walls/ceilings so that my
audience can hear my singing.









Exception: Venue becomes unavailable.

If the venue becomes unavailable after already being booked by a performer,
the event will be cancelled and the performer will be informed.

Exception: Performer becomes unavailable.

If the performer becomes unavailable after the event has been planned, the e
event will be cancelled and the venue will become available to be booked fo
another event, and other performers will be notified of the availability.

Exception: Venue doesn't have enough currency to handle the transaction.

If the venue doesn't have enough money to book a performer, the event will
be cancelled and the venue will become available to book. The performer will
be notified of the cancellation.

Exception: Performer doesn't have enough currency for the booking.

If the performer doesn't have enough money to book the venue, the application
will cancel the booking and make the venue available.

Exception: Consumer of application doesn't have stable internet to access page.

If the consumer who is using our application can't access the webpage, they will
be informed of such in a 404 status code webpage error.

Exception: Performers tries to book overlapping time slots 

If the performer books a venue, they will not be allowed to book another on the same time slot without cancelling the first

Exception: A performer tries to cancel last minute:

Performers will not be able to cancel within an hour prior to the event.

Exception: Performer set length is longer than what the venue has available

We will cancel the transaction

Exception: A venue changes location after a booking

Database will be updated to account for it

Exception: A performer applies for a venue that does not fit their important specifications (experience, genre, etc)

Backend will deny the application before it reaches the venue

Exeption: Performer changes price after a booking

Database will be updated to account for it and seperate transaction process will occur

Exception: Venue changes price after a booking

Database will be updated to account for it and seperate transaction process will occur
