from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
import pytest

client =  TestClient(app)

engine = create_engine("sqlite:///.testing.db",connect_args={'check_same_thread':False})

TestingSessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base.metadata.create_all(bind=engine)

def overrides_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def fresh_table():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = overrides_get_db

def test_home():
    response = client.get('/')
    assert response.status_code == 200

    assert response.json() == {"message":"Welcome to Lost and Found Portal."}

def test_display():
    response = client.get('/items')

    assert response.status_code == 200

    for item in response.json():
        assert "owner_id" not in item

def test_register():
    response = client.post('/register',json={"username":"rajesh","password":"12345"})
    assert response.status_code == 200
    assert "hashed_password" not in response.text

def test_register_for_duplicates():
    client.post('/register',json={"username":"rajesh","password":"12345"})
    response = client.post('/register',json={"username":"rajesh","password":"12345"})
    assert response.status_code == 409

def test_login_wrong_pwd():
    client.post('/register',json={"username":"rajesh","password":"12345"})
    response = client.post('/login',json={"username":"rajesh","password":"12345g"})
    assert response.status_code == 401