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



## Peer Review: Arne Noori

# Code Review Comments:

1. good catch, error handling has been added
2. input validation has been added to error before any transactions occur
3. Because our dangerous transactions are handled within a single connection, if one errors none of the other transactions complete and the script notifies that an error occured.
4. This was detailed in Saba's review
5. Good catch, this has been handled
6. We are aware of the user authentication being commented out.  We plan to implement this at the end of our development process for the project to secure the api
7. This has been handled, good catch
8. We are aware of the disparity in the formatting.  Once development is completed, we will comb through and put everything in a consistent format
9. Logging has been added to help development understand what is happening during any errors (times when success is False)
10. This is a good suggestion, we do have multiple test cases that we implement for every change.  They are currently not implemented as code however so if time permits we can implement this to make the testing process easier
11. This is a good suggestion! we will make sure implement this for v5 when we have to handle lots of users at once.  We didn't think of it prior because we never had enough entries for it to be important
12. Database.py now uses environment variables
13. Our service should not be open to injection attacks because we implemented parameter binding for all of our queries that were vulnerable
14. This was already detailed in Saba's review
15. All applicable endpoints should have some handling for the event of invalid or non-existent input

# Schema/API Design Comments

1. Already handled from previous reviews
2. Good catch, the change has been made
3. It has now been changed to text
4. Added the foreign key constraints
5. Capacity preference is no longer nullable
6. The endpoint could be simplified, but we chose to have a more verbose endpoint to allow more clarity into what is actually happening in the transaction
7. To my understanding PUT should be used when updating already existing data, in this case, we are creating a new booking entry
8. This input validation has already been implemented
9. thorough Error logging hass been added for whenever an endpoint returns {"success": False}
10. This is an excellent idea, however it is not really in the scope of the assignment at the moment.  We will definitely implement this change if it reaches a higher priority
11. Entry types now have timezones included, good catch
12. change has been implemented, price columns can now hold decimal values


