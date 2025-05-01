from flask import Flask, render_template, request, redirect, url_for
import requests
from urllib.parse import unquote
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

# Replace with your Spoonacular API key
API_KEY = '42a784a1e60942739e09c9684472e3c9'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('search_query', '')
        return redirect(url_for('home', search_query=query))
    
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('home.html', recipes=recipes, search_query=decoded_search_query)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('search_query', '')
        return redirect(url_for('home', search_query=query))
    
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('home.html', recipes=recipes, search_query=decoded_search_query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add your login logic here
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Add your signup logic here
        return redirect(url_for('login'))
    return render_template('signup.html')

def search_recipes(query):
    if not query:
        return []
        
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        return []
    except requests.exceptions.RequestException:
        return []

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    search_query = request.args.get('search_query', '')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {'apiKey': API_KEY}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            recipe = response.json()
            return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
        return "Recipe not found", 404
    except requests.exceptions.RequestException:
        return "Error fetching recipe", 500

if __name__ == '__main__':
    # Ensure the template folder is correct
    template_dir = os.path.abspath('templates')
    print(f"Looking for templates in: {template_dir}")
    
    random_port = random.randint(10000, 99999)
    app.run(debug=True, host='127.0.0.1', port=random_port)