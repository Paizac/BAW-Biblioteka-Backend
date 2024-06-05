import json
from pathlib import Path
from book_library_app import app, db
from book_library_app.models import Author
from datetime import datetime
from sqlalchemy import text

@app.cli.group()
def db_manage():
    """Komendy do zarzadzania baza danych"""
    pass

@db_manage.command()
def add_data():
    """Dodawanie danych do bazy danych"""
    try:
        authors_path = Path(__file__).parent / 'samples' / 'authors.json'
        with open(authors_path) as file:
            data_json = json.load(file)
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.session.add(author)
        db.session.commit()
        print('Dane zostaly poprawnie dodane do bazy danych')
    except Exception as exc:
        print('Niespodziewany błąd :{}'.format(exc))

@db_manage.command()
def remove_data():
    """Usuwanie danych z bazy danych"""
    try:
        sql_statement = text('TRUNCATE TABLE authors')
        db.session.execute(sql_statement)
        db.session.commit()
        print('Dane zostaly poprawnie usuniete z bazy danych')
    except Exception as exc:
        print('Niespodziewany błąd :{}'.format(exc))