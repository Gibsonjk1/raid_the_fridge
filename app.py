from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, redirect, render_template, request, jsonify, session, g, flash
from models import db, connect_db, Recipe, User, Customer, Customer_Recipe
import requests
import json
from forms import UserAddForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
DEBUG_TB_INTERCEPT_REDIRECTS = False

CURR_USER_KEY = "curr_user"
bcrypt=Bcrypt()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('successfully logged out')
    return redirect('/login')

@app.route('/')
def redirect_to_search():
    return redirect('/search')

@app.route('/search')
def show_search():
    if CURR_USER_KEY in session:
        json_output=""
        return render_template('search.html', json_output=json_output)
    else:
        return redirect('/login')

@app.route('/search', methods=['POST'])
def return_results():
    ingredients1 = request.form['ingredients']
    lowercase= ingredients1.lower()
    lowerList = list(lowercase)
    for space in lowerList:
        if (space == ' '):
            space='+'
    ingredients = ''.join(lowerList)
    try:
        res=requests.get(f'https://api.spoonacular.com/recipes/findByIngredients?apiKey=89bd16ac21f5418391542303788e144d&ingredients={ingredients}')
    except:
        flash("Oops, there is a problem. Please make sure ingredients are spelled correctly and seperated by a comma.")
    json_output = json.loads(res.text)
    return render_template('search.html', json_output=json_output)

@app.route('/my_recipes')
def add_user_to_g():
    recipes= Customer_Recipe.query.filter_by(customer_id = CURR_USER_KEY).all()
    recipe_list =list()
    for recipe in recipes:
        recipe_list.append(recipe.recipe_id)
    recipes_string= ','.join(recipe_list)
    try:
        res=requests.get(f'https://api.spoonacular.com/recipes/informationBulk?apiKey=89bd16ac21f5418391542303788e144d&ids={recipes_string}')
    except:
        flash("there appear to be no saved recipes, or an error has occured")
    my_recipes = json.loads(res.text)
    return render_template('my_recipes.html', recipes=my_recipes)


@app.route('/ideas')
def show_ideas():
    response = requests.get('https://api.spoonacular.com/recipes/random?apiKey=89bd16ac21f5418391542303788e144d&number=10')
    json_output = json.loads(response.text)
    ideas = json_output
    return render_template('ideas.html', ideas=ideas)

@app.route('/save', methods=['POST'])
def save_recipe():
    food_id = request.form['id']
    new_saved_food = Customer_Recipe(
        customer_id = CURR_USER_KEY,
        recipe_id = food_id
    )
    db.session.add(new_saved_food)
    db.session.commit()

    return redirect('/my_recipes')


