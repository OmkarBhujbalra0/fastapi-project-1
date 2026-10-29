# Lost and Found Portal

This is an Lost and Found Portal API, here you can add, remove and watch all the lost and found items.

Current Features:

- Display all the lost and found items
- Search for an specific item
- Add new lost or found item

## Tech Stack

- FastAPI
- SQLite

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

4. Run the project 

```
uvicorn file_name:app --reload
```

5. Test the API

Click on the link `http://localhost:8000`
Then visit `http://localhost:8000/docs` to test the API.