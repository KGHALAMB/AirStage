## Peer Review: Saba Hakimi

# Code Review Comments:

1. Great suggestion, and the commented out code block was removed.
2. This suggestion was implemented and variable names for database retrievals were updated to accurately reflect what they actually represent.
3. Variable names were changed for the booking times in order to be more readable so the reader knows which timestamps are for which user.
4. Suggestion was implemented and just returned a failed response instead of assigning boolean values to see if the time works.
5. A lot of the code between the two can't be put into helper functions because they retrieve data from different tables, however, the similar code for checking if times are compatible and getting capacity values were both put into helper functions.
6. This is a great suggestion and was implemented for the most part. The only place where this is irrelevant is when retrieving bookings when creating a booking, since we are checking the times of all bookings for a particular venue/performer.
7. Another good suggestion that was implemented to make the code more compact and more readable.
8. Variable assignments for these database calls were removed since there is no data being retrieved.
9. A ternary expression was implemented used in order to make the code more compact and more readable.
10. Changed the function name for the signin endpoint to reflect what the endpoint is actually doing.
11. Many of our SELECT calls are either to check if a specific row exists in the database or to retrieve most if not all of the information for a particular row, so there really isn't a need to just grab specific columns.
12. Documentation was added for all of the code.

# Schema/API Design Comments

1. Great suggestion that we didn't initally think of, and this has now been implemented such that only hashed passwords are stored in the database.
2. This schema attribute was outdated for some reason and has now been updated.
3. Foreign key constraints were added in the database and are now reflected in the schema.
4. The API spec was incorrect and has been updated to accurately reflect correct accept and return values.
5. The user_type as part of the accept is a string which is then turned into an integer in the database, however, input and output values for our endpoints of this variable is a string so it's easier for the user to read.
6. The API spec was incorrect and has been updated to accurately reflect correct accept and return values.
7. There really isn't a point in this since capacity_preference would only be applicable to performers and not venues, since usually venues have specified capacities. These names are also accurately reflected in our table columns respectively.
8. The code was updated to use datetime data types rather than strings.
9. This was a mistake and has now been fixed.
10. This doesn't really seem like a relevant suggestion since the id's for the other tables only have specific names because there are foreign key relations to other tables.
11. Printed error messages have been added throughout our endpoints.
12. This was updated so that there is a foreign key relation to the users table in both the venues and performers tables.
