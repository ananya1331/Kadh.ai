from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
DATABASE = 'kadhai.db'

# ----------------- Database Connection -----------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ----------------- Helper to Query DB -----------------
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# ----------------- User Signup -----------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    if query_db("SELECT * FROM users WHERE username = ?", [username], one=True):
        return jsonify({"message": "Username already exists"}), 400

    get_db().execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, password])
    get_db().commit()
    return jsonify({"message": "Signup successful"}), 201

# ----------------- User Login -----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", [username, password], one=True)
    if user:
        return jsonify({"message": "Login successful", "user_id": user["id"]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ----------------- Add Favorite -----------------
@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    user_id = data['user_id']
    recipe_id = data['recipe_id']
    get_db().execute("INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)", [user_id, recipe_id])
    get_db().commit()
    return jsonify({"message": "Favorite added"}), 201

# ----------------- Get Favorites -----------------
@app.route('/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    rows = query_db("""
        SELECT r.* FROM recipes r
        JOIN favorites f ON r.id = f.recipe_id
        WHERE f.user_id = ?
    """, [user_id])
    return jsonify([dict(row) for row in rows]), 200

# ----------------- Add Review -----------------
@app.route('/review', methods=['POST'])
def add_review():
    data = request.json
    user_id = data['user_id']
    recipe_id = data['recipe_id']
    review = data['review']
    get_db().execute("INSERT INTO reviews (user_id, recipe_id, review) VALUES (?, ?, ?)", [user_id, recipe_id, review])
    get_db().commit()
    return jsonify({"message": "Review added"}), 201

# ----------------- Get Reviews -----------------
@app.route('/reviews/<int:recipe_id>', methods=['GET'])
def get_reviews(recipe_id):
    rows = query_db("""
        SELECT u.username, r.review FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.recipe_id = ?
    """, [recipe_id])
    return jsonify([dict(row) for row in rows]), 200

# ----------------- Recommendations -----------------
@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    favs = query_db("SELECT recipe_id FROM favorites WHERE user_id = ?", [user_id])
    fav_ids = [f['recipe_id'] for f in favs]
    if not fav_ids:
        return jsonify([]), 200

    placeholders = ','.join(['?'] * len(fav_ids))
    recs = query_db(f"SELECT * FROM recipes WHERE id NOT IN ({placeholders}) LIMIT 5", fav_ids)
    return jsonify([dict(r) for r in recs]), 200

if __name__ == '__main__':
    app.run(debug=True)
