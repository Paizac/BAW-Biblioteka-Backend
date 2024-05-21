from book_library_app import app
from flask import jsonify


@app.route('/api/v1/authors', methods=['GET'])
#Funkcja zwracająca listę autorów
def get_authors():
    return jsonify(
        {
            'success': True,
            'data': 'Get all authors'
        }
    )

#Funkcja zwracająca informację o jednym autorze

@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
#Funkcja zwracająca listę autorów
def get_author(author_id: int):
    return jsonify(
        {
            'success': True,
            'data': f'Get single author with id {author_id}'
        }
    )

#Funkcja do tworzenia nowego rekordu
@app.route('/api/v1/authors', methods=['POST'])
#Funkcja zwracająca listę autorów
def create_author():
    return jsonify(
        {
            'success': True,
            'data': 'New author has been created'
        }
    ), 201

#Funkcja aktualizująca rekord o podanym ID
@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
#Funkcja zwracająca listę autorów
def update_author(author_id: int):
    return jsonify(
        {
            'success': True,
            'data': f'Author with id {author_id} has been updated'
        }
    )

#Funkcja usuwająca rekord o danym ID
@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
#Funkcja zwracająca listę autorów
def delete_author(author_id: int):
    return jsonify(
        {
            'success': True,
            'data': f'Author with id {author_id} has been deleted'
        }
    )