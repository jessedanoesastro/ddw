from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Movie model representing the movies table
class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
     ...

# Create the database and the tables for the model
with app.app_context():
    db.create_all()

@app.route('/', methods=[...])
def index():
    movies = Movie.query.all()  # Get all movies from the database
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=[...])
def add_movie():
    if request.method == ... :
        #get items from form 

        # Create a new movie entry
        new_movie = Movie(...)

        # Add to the session and commit to the database
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_movie.html')

if __name__ == '__main__':
    app.run(debug=True)
