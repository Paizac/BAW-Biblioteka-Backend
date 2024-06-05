from book_library_app import app, db
from flask import jsonify, request
from book_library_app.models import Author, AuthorSchema, author_schema
from webargs.flaskparser import use_args
from book_library_app.utils import validate_json_content_type

@app.route('/api/v1/authors', methods=['GET'])
#Funkcja zwracająca listę autorów
def get_authors():
    authors = Author.query.all()
    author_schema = AuthorSchema(many=True)

    return jsonify(
        {
            'success': True,
            'data': author_schema.dump(authors),
            'number_of_records' : len(authors)
        }
    )

#Funkcja zwracająca informację o jednym autorze

@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
#Funkcja zwracająca listę autorów
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Autor z id {author_id} nie zostal znaleziony')
    return jsonify(
        {
            'success': True,
            'data': author_schema.dump(author)
        }
    )

#Funkcja do tworzenia nowego rekordu
@app.route('/api/v1/authors', methods=['POST'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
#Funkcja zwracająca listę autorów
def create_author(args: dict):
    author = Author(**args)
    db.session.add(author)
    db.session.commit()
    return jsonify(
        {
            'success': True,
            'data': author_schema.dump(author)
        }
    ), 201

#Funkcja aktualizująca rekord o podanym ID
@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
#Funkcja zwracająca listę autorów
def update_author(args: dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Autor z id {author_id} nie zostal znaleziony')
    author.first_name = args['first_name']
    author.last_name = args['last_name']
    author.birth_date = args['birth_date']
    db.session.commit()
    return jsonify(
        {
            'success': True,
            'data': author_schema.dump(author)
        }
    )

#Funkcja usuwająca rekord o danym ID
@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
#Funkcja zwracająca listę autorów
def delete_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Autor z id {author_id} nie zostal znaleziony')
    db.session.delete(author)
    db.session.commit()
    return jsonify(
        {
            'success': True,
            'data': f'Author z id {author_id} zostal usuniety'
        }
    )