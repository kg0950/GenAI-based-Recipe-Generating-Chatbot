from flask import Flask, request, jsonify
import openai
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Database connection
conn = psycopg2.connect(
    database="recipe_chatbot",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipe_queries (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        ingredients TEXT,
        recipe TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    user_id = data.get("user_id", "guest")
    ingredients = data.get("ingredients", "")
    
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400
    
    # Get AI-generated recipe
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert chef. Provide a recipe based on given ingredients."},
                  {"role": "user", "content": f"Create a recipe using: {ingredients}"}]
    )
    recipe = response["choices"][0]["message"]["content"]
    
    # Store in DB
    cursor.execute("INSERT INTO recipe_queries (user_id, ingredients, recipe) VALUES (%s, %s, %s)",
                   (user_id, ingredients, recipe))
    conn.commit()
    
    return jsonify({"recipe": recipe})

if __name__ == '__main__':
    app.run(debug=True)
