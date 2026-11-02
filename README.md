# Lost and Found Portal

Lost and Found Portal, a Rest API built using FastAPI and SQLALchemy, allows add and remove the lost and found items in the database.

Current Features:

- Display all the lost and found items
- Search for an specific item
- Add new lost or found item
- Remove the lost or found item
- Update the item in the database
- Registration of Users
- Login and Secure Routes

## Tech Stack

- FastAPI
- SQLAlchemy
- JWT

## Setup

1. Create an Virtual Environment

```
python -m venv .venv
```

2. Activate the Virtual Environment

```
.venv\Scripts\activate # For Windows
```

3. Install the required dependencies

```
pip install -r requirements.txt
```
4. Make an `.env` file and write all the confidential details like API_KEY or DATABASE_URL in it.

5. This project uses a SECRET_KEY so generate a secret key from this code in Python Shell line by line.

```
python -c "import secrets"
print(secrets.token_hex(32))
```

6. Paste the generated secret key in the `.env` file. 

7. Make an .gitignore file and add the files and folders in it you don't want to push to Github.

8. Run the project 

```
uvicorn main:app --reload
```

9. Test the API

Click on the link `http://localhost:8000`
Then visit `http://localhost:8000/docs` to test the API.

10. How to authorize yourself in Lost and Found Portal API.

- Go to the `http://localhost:8000/docs`
- Register yourself on register route by inputting username and password
- Then login using login route
- The login route will generate a JWT token
- Copy that token and click on the Authorize button at the top of the page.
- Paste the token.
- Now you can visit secured routes unless you don't logout.