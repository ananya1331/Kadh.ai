import sqlite3

# Connect to the database
conn = sqlite3.connect('kadhai.db')
cursor = conn.cursor()

# Sample dummy recipes
recipes = [
    ("Pav Bhaji", "Indian", "Potatoes, peas, tomatoes, onions, pav", "Boil veggies, mash, cook with spices, serve with buttered pav", "spicy, street food"),
    ("Spaghetti Carbonara", "Italian", "Spaghetti, eggs, pancetta, parmesan", "Boil pasta, cook pancetta, mix with eggs and cheese", "creamy, pasta"),
    ("Sushi Rolls", "Japanese", "Rice, nori, raw fish, vegetables", "Roll rice and ingredients in seaweed, slice", "fresh, seafood"),
    ("Chole Bhature", "Indian", "Chickpeas, flour, spices", "Cook chickpeas with spices, fry dough", "spicy, Punjabi"),
    ("Tacos", "Mexican", "Tortilla, beef/chicken, lettuce, salsa", "Cook meat, fill tortilla, top with veggies and salsa", "quick, savory")
]

# Insert recipes into the table
cursor.executemany("""
    INSERT INTO recipes (title, cuisine, ingredients, instructions, tags)
    VALUES (?, ?, ?, ?, ?)
""", recipes)

# Commit and close
conn.commit()
conn.close()
print("Dummy recipes added successfully.")
