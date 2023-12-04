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

## Peer Review Alexander Specht

# Code Review Comments:
1. Handled in earlier review
2. Updated single-row cases to return multiple rows for previous error resolution.
3. Class object is needed to take in time period to know when to book. 
4. Already handled in previous reviews
5. Good catch, removed unused price variable
6. Talked to professor, there is intent to this to separate processes.
7. Handled in earlier review
8. Good catch, edited so supabase sets default values
9. Handled in earlier review
10. Handled in earlier review
11. Handled concurrency issues in earlier review
12. Handled in earlier review
13. Handled in earlier review
14. We like to store these outputs in variables for readability. 
15. Good catch, changed to check if performer/venue is already booked during the given time. 

# Schema/API Design Comments:
1. Already handled in previous reviews
2. To my understanding, you are able to change the value of capacity_performance after setting it.
3. The PerformerBooking parameter is a necessity since the user needs to input the intended start and end time they want to book the performer at as well in addition to which performer they want to book.
4. Good suggestion, we implemented a helper function to abstract away similar code. 
5. Already handled in previous reviews
6. Already handled in previous reviews
7. That's a good thought, but going into this, we were operating under the assumption that both a venue and a respective performer would be on the same page going into a booking. It's like a store transaction where both the store and the customer are aware of the purchase. 
8. Great suggestion, implemented another table that allows for multiple availability times.
9. Good catch, implemented so that you are allowed to set a price when signing up. 
10. We are under the assumption that performers are operating on a fixed rate for their performances.
11. Created enum that contains usertype and the only parameter that is taken in is a class variable. 
12. This is something we may consider to implement in future implementations, right now the assumption is the performer and the venue will work out if they're able to make it to the locations. 



## Peer Review Gibson Hooper

# Code Review Comments:
1. Handled in earlier review

2. I agree, but this endpoint serves as a nice endpoint to have for debugging purposes

3. Handled in earlier review

4. Handled in earlier review

5. Handled in earlier review  

6. Handled in earlier review the return boolean value. Regarding the initial concerns, these are valid and have been added.

7. I would agree filtering would be something possibly relevant for the get_booking() but given the scope of our project will not be something we will implement. I don’t find it to be useful for the other ones. This is because the users would not have access to the other endpoints if this application were fleshed out more. 

8. Handled in earlier review 

9. This comes down to coding preference in my opinion and I’m on the side of negative conditional 

10. Handled in earlier review

11. Handled in earlier review (users can update their values) and are given default values initially

12. Handled in earlier review

13. We have updated our schema (might not be in the old diagram) such that performers have a fee (venues book performers by paying them to perform at their venue). We are prioritizing having working code over an up-to-date ER diagram, so we will fix the diagram if we have extra time.

14. Handled in earlier review

# Schema/API Design Comments:
1. True, but it can be useful for debugging purposes

2. ER diagram is outdated and will be updated if we have time to do so.

3. Good suggestion if we wanted to implement a search endpoint, but we will not be doing that due to our small scope of the project.

4. I don’t agree with this because we’re operating under the assumption that performers simply want a venue big enough to fit how many people they’re hoping to perform for. Performers will still perform even if the venue’s capacity is much larger than their preference.

5. We decided to move away from what the spec says and instead these endpoints simply return all performers regardless of availability. Spec has been updated to reflect this

6. Handled in earlier review

7. Handled in earlier review

8. Handled in earlier review

9. Good idea, but this is not in the scope of our project as it sits.

10. Like the other points mentioned, this would naturally be the next step in expanding the project but is not in the scope of our current project. The main idea was to help bookings happen. 

11. Handled in earlier review

12. Yes, but with a simplistic model we’re going for now, this might not be necessary to do at this time

13. I disagree about the necessity of this. We were able to construct our endpoints without needing to have this, so I don’t think this needs to be added.

14. Indeed, the ER diagram is a bit outdated and needs some updating on our end when we have the time to do so.



