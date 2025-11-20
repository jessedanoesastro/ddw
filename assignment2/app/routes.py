from flask import render_template, redirect, url_for, flash, request
import sqlalchemy as sa

from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.models import User, Movie
from app.forms import LoginForm, RegistrationForm
from flask_login import logout_user

@app.route('/')
@login_required
def index():
    movies = Movie.query.all()
    return render_template('index.html', title='Movies', movies=movies)


@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        name = request.form['name']
        year = int(request.form['year'])
        oscars = int(request.form['oscars'])

        new_movie = Movie(name=name, year=year, oscars=oscars)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_movie.html', title='Add Movie')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_movie(id):
    movie = Movie.query.get(id)

    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.year = int(request.form['year'])
        movie.oscars = int(request.form['oscars'])

        db.session.add(movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_movie.html', title='Edit Movie', movie=movie)


@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Page Not Found'), 404

