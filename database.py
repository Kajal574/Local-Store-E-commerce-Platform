import sqlite3

def create_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Creating products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        image TEXT
    )''')

    # Creating orders table
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        customer_name TEXT,
        customer_address TEXT,
        status TEXT
    )''')

    # Creating reviews table
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        user TEXT,
        review TEXT
    )''')

    conn.commit()
    conn.close()

def insert_sample_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Sample products (replace image paths with actual image URLs or file paths)
    sample_products = [
        ('Product 1', 'This is a description for Product 1', 19.99, 'path/to/image1.jpg'),
        ('Product 2', 'This is a description for Product 2', 29.99, 'path/to/image2.jpg'),
        ('Product 3', 'This is a description for Product 3', 39.99, 'path/to/image3.jpg')
    ]

    cursor.executemany('''INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)''', sample_products)
    
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def add_to_cart(product_id, quantity):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
    conn.commit()
    conn.close()

def add_review(product_id, user, review):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (product_id, user, review) VALUES (?, ?, ?)", (product_id, user, review))
    conn.commit()
    conn.close()
