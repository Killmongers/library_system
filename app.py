from flask import Flask, request, jsonify,render_template

app = Flask(__name__)

# ----------------------------
# Book Class
# ----------------------------
class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author
        self.available = True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "available": self.available
        }

# ----------------------------
# Library Class
# ----------------------------
class Library:
    def __init__(self):
        self.books = []
        self.next_id = 1

    def add_book(self, title, author):
        book = Book(self.next_id, title, author)
        self.books.append(book)
        self.next_id += 1
        return book

    def get_all_books(self):
        return [book.to_dict() for book in self.books]

    def borrow_book(self, book_id):
        for book in self.books:
            if book.id == book_id and book.available:
                book.available = False
                return book
        return None

    def return_book(self, book_id):
        for book in self.books:
            if book.id == book_id and not book.available:
                book.available = True
                return book
        return None

# Create the Library object
library = Library()

# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(library.get_all_books())

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    book = library.add_book(title, author)
    return jsonify(book.to_dict()), 201

@app.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow(book_id):
    book = library.borrow_book(book_id)
    if book:
        return jsonify({"message": f"You borrowed '{book.title}'."})
    return jsonify({"error": "Book not available."}), 404

@app.route('/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    book = library.return_book(book_id)
    if book:
        return jsonify({"message": f"You returned '{book.title}'."})
    return jsonify({"error": "Book not found or already returned."}), 404

# ----------------------------
# Run Flask app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)

