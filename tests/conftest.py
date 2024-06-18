import pytest
from book_library_app import create_app, db
from pathlib import Path
import time
from book_library_app.commands.db_manage_commands import add_data


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    # Close the session and drop all tables
    with app.app_context():
        db.session.remove()
        db.drop_all()


    db_file_path = Path(app.config['DB_FILE_PATH'])


    time.sleep(1)

    try:
        db_file_path.unlink(missing_ok=True)
    except PermissionError:
        print(f"Could not delete the database file: {db_file_path}. It may be in use.")


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def user(client):
    user = {
        'username': 'test',
        'password': '123456',
        'email': 'test@gmail.com'
    }
    client.post('/api/v1/auth/register', json=user)
    return user

@pytest.fixture
def token(client, user):
    response = client.post('/api/v1/auth/login', json={
        'username': user['username'],
        'password': user['password']
    })
    return response.get_json()['token']

@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)

@pytest.fixture
def author():
    return {
        'first_name': 'Adam',
        'last_name': 'Mickiewicz',
        'birth_date': '24-12-1798'
    }