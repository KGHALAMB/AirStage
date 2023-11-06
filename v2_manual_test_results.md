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

    5.2 Signing in as a user - /user/signin/ (POST)

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

# Testing Results

1.
curl -X 'POST' \
  'https://airstage-api.onrender.com/user/signup/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SoloPlayer123",
  "password": "Xlkjvl38$%",
  "user_type": "performer"
}'

2.
{
  "success": true
}

1.
curl -X 'POST' \
  'https://airstage-api.onrender.com/user/signin/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SoloPlayer123",
  "password": "Xlkjvl38$%",
  "user_type": "performer"
}'

2.
{
  "success": true
}