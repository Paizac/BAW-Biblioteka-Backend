from book_library_app import db
from flask import jsonify, abort
from book_library_app.models import Book, BookSchema, book_schema, Author
from webargs.flaskparser import use_args
from book_library_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, \
    get_pagination, token_required
from book_library_app.books import books_bp


@books_bp.route('/books', methods=['GET'])
#Funkcja zwracająca listę książek
def get_books():
    query = Book.query
    schema_args = get_schema_args(Book)
    query = apply_order(Book, query)
    query = apply_filter(Book, query)
    items, pagination = get_pagination(query, 'books.get_books')
    books = BookSchema(**schema_args).dump(items)

    return jsonify(
        {
            'success': True,
            'data': books,
            'number_of_records': len(books),
            'pagination': pagination
        }
    )


@books_bp.route('/books/<int:book_id>', methods=['GET'])
#Funkcja zwracająca pojedynczą książkę
def get_book(book_id: int):
    book = Book.query.get_or_404(book_id, description=f'Ksiazka z id {book_id} nie zostala znaleziona')
    return jsonify(
        {
            'success': True,
            'data': book_schema.dump(book)
        }
    )


@books_bp.route('/books/<int:book_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(book_schema, error_status_code=400)
#Funkcja zwracająca pojedynczą książkę
def update_book(user_id: int, args: dict, book_id: int):
    book = Book.query.get_or_404(book_id, description=f'Ksiazka z id {book_id} nie zostala znaleziona')
    existing_book = Book.query.filter(Book.isbn == args['isbn']).first()
    if existing_book and existing_book.id != book_id:
        abort(409, description=f'Ksiazka z numerem ISBN {args["isbn"]} juz istnieje')

    book.title = args['title']
    book.isbn = args['isbn']
    book.number_of_pages = args['number_of_pages']
    description = args.get('description')
    if description is not None:
        book.description = description
    author_id = args.get('author_id')
    if author_id is not None:
        Author.query.get_or_404(author_id, description=f'Autor z id {author_id} nie zostal znaleziony')
        book.author_id = author_id

    db.session.commit()
    return jsonify(
        {
            'success': True,
            'data': book_schema.dump(book)
        }
    )


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
@token_required
#Funkcja zwracająca listę autorów
def delete_book(user_id: int, book_id: int):
    book = Book.query.get_or_404(book_id, description=f'Ksiazka z id {book_id} nie zostala znaleziona')
    db.session.delete(book)
    db.session.commit()
    return jsonify(
        {
            'success': True,
            'data': f'Ksiazka z id {book_id} zostala usunieta'
        }
    )


@books_bp.route('/authors/<int:author_id>/books', methods=['GET'])
def get_all_author_books(author_id: int):
    Author.query.get_or_404(author_id, description=f'Autor z id {author_id} nie zostal znaleziony')
    books = Book.query.filter(Book.author_id == author_id).all()

    items = BookSchema(many=True, exclude=['author']).dump(books)

    return jsonify({
        'success': True,
        'data': items,
        'number_of_records': len(items)
    })


@books_bp.route('/authors/<int:author_id>/books', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(BookSchema(exclude=['author_id']), error_status_code=400)
def create_book(user_id: int, args: dict, author_id: int):
    Author.query.get_or_404(author_id, description=f'Autor z id {author_id} nie zostal znaleziony')
    if Book.query.filter(Book.isbn == args['isbn']).first():
        abort(409, description=f'Ksiazka z numerem ISBN {args['isbn']} juz istnieje')

    book = Book(author_id=author_id, **args)

    db.session.add(book)
    db.session.commit()
    return jsonify({
        'success': True,
        'data': book_schema.dump(book)
    }), 201
