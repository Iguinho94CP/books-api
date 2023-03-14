# BOOKS-API
This code provides a basic Flask API for managing a books database.

## Dependencies
This code requires the following dependencies:

Flask
Flask_SQLAlchemy
## How to use
Clone this repository:


git clone https://github.com/example/flask-books-api.git
Navigate to the cloned repository:


cd flask-books-api
Install the dependencies:


pip install -r requirements.txt
Run the Flask application:


flask run
The API will be available at http://localhost:5000.

## Endpoints
The following endpoints are available:

- GET /books - Retrieve all books with pagination and limit.
- GET /books/<int:book_id> - Retrieve a book by ID.
- GET /book/author?name=<string:author_name> - Retrieve books by author name.
- GET /book/<int:id>/quotes - Retrieve quotes by book ID.
- GET /books/genre/<string:genre> - Retrieve books by genre.
- POST /books - Add one or more books to the database.
- PUT /books/<int:book_id> - Update an existing book.
- DELETE /books/<int:book_id> - Delete a book.
## Error Handling
The following error handlers are implemented:

- 400 - Bad request.
- 404 - Resource not found.
- 500 - Internal server error.
