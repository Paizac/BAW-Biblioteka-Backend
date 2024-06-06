from book_library_app import db
from flask import jsonify
from book_library_app.models import Author, AuthorSchema, author_schema
from webargs.flaskparser import use_args
from book_library_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination
from book_library_app.authors import authors_bp

@authors_bp.route('/authors', methods=['GET'])
#Funkcja zwracająca listę autorów
def get_authors():
    query = Author.query
    schema_args = get_schema_args(Author)
    query = apply_order(Author, query)
    query = apply_filter(Author, query)
    items, pagination = get_pagination(query, 'authors.get_authors')
    authors = AuthorSchema(**schema_args).dump(items)

    return jsonify(
        {
            'success': True,
            'data': authors,
            'number_of_records': len(authors),
            'pagination': pagination
        }
    )

#Funkcja zwracająca informację o jednym autorze

@authors_bp.route('/authors/<int:author_id>', methods=['GET'])
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
@authors_bp.route('/authors', methods=['POST'])
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
@authors_bp.route('/authors/<int:author_id>', methods=['PUT'])
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
@authors_bp.route('/authors/<int:author_id>', methods=['DELETE'])
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