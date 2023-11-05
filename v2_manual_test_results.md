## Example Workflow: User signing up/in

The API calls are made in this sequence when a user is to sign up/login
1. `Signing up as a user`
2. `Signing in as a user`

    5.1 Signing up as a user - /user/signup/ (POST)

    Adds a users credentials to the database

        Request:
        {
            "username": "string",
            "password": "string",
            "user_type": "string"
        }
    
        Returns:
        {
            "success": "boolean"
        }

    5.2 Signing in as a user - /user/signin/ (GET)

    Checks if inputted username and password is associated with an account

        Request:
        {
            "username": "string",
            "password": "string",
            "user_type": "string"
        }
    
        Returns:
        {
            "success": "boolean"
        }