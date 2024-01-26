from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pub_year = db.Column(db.Integer, nullable=False)

# Create the database tables
db.create_all()

# Route to display the list of books
@app.route('/list')
def list():
    books = Book.query.all()
    return render_template('list.html', books=books)

# Route to add a new book
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get book details from the form
        title = request.form['title']
        author = request.form['author']
        pub_year = request.form['pub_year']

        # Create a new Book instance
        new_book = Book(title=title, author=author, pub_year=pub_year)

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirect to the list of books after adding
        return redirect(url_for('list'))

    # Render the form to add a new book
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
