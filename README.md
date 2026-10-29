# Lost and Found Portal

Lost and Found Portal, a Rest API built using FastAPI and SQLALchemy, allows add and remove the lost and found items in the database.

Current Features:

- Display all the lost and found items
- Search for an specific item
- Add new lost or found item
- Remove the lost or found item
- Update the item in the database

## Tech Stack

- FastAPI
- SQLAlchemy

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

5. Make an .gitignore file and add the files and folders in it you don't want to push to Github.

6. Run the project 

```
uvicorn main:app --reload
```

7. Test the API

Click on the link `http://localhost:8000`
Then visit `http://localhost:8000/docs` to test the API.