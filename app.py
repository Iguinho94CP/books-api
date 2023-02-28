from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    author = db.Column(db.String(50), nullable=False)
    quotes = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'author': self.author,
            'quotes': self.quotes
        }

with app.app_context():
    db.create_all()

# Get all books with pagination and limit
@app.route('/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = Book.query.paginate(page=page, per_page=per_page)
    return jsonify({'books': [book.serialize() for book in books.items],
                    'total_pages': books.pages,
                    'total_items': books.total}), 200

# Get a book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'book': book.serialize()}), 200


@app.route('/book/author', methods=['GET'])
def get_books_by_author():
    if request.method == 'GET':
        author_name = request.args.get('name')
        books = Book.query.filter_by(author=author_name).all()
        book_list = []
        for book in books:
            book_data = {}
            book_data['title'] = book.title
            book_data['author'] = book.author
            book_data['quote'] = book.quotes
            book_list.append(book_data)
        return {'books': book_list}, 200

@app.route('/book/<int:id>/quotes', methods=['GET'])
def get_quotes_by_book(id):
    if request.method == 'GET':
        book = Book.query.filter_by(id=id).first()
        quotes = book.quotes
        return {'quotes': quotes}, 200


@app.route('/books/genre/<string:genre>', methods=['GET'])
def get_books_by_genre(genre):
    if request.method == 'GET':
        books = Book.query.filter_by(genre=genre).all()
        book_list = []
        for book in books:
            book_data = {}
            book_data['title'] = book.title
            book_data['author'] = book.author
            book_data['quote'] = book.quotes
            book_list.append(book_data)
        return {'books': book_list}, 200

@app.route('/books', methods=['POST'])
def add_book():
    if request.method == 'POST':
        books = request.get_json()
        for book in books:
            title = book['title']
            genre = book['genre']
            author = book['author']
            quotes = book['quotes']
            new_book = Book(title=title, genre=genre, author=author, quotes=quotes)
            db.session.add(new_book)
            db.session.commit()
        return {'message': f'{len(books)} books added to database.'}, 201

# Update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.title = data['title']
    book.genre = data['genre']
    book.author = data['author']
    book.quotes = data['quotes']
    db.session.commit()
    return jsonify({'book': book.serialize()}), 200

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

# Handle invalid requests
@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request'}), 400

# Handle missing resources
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

# Handle internal server errors
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
