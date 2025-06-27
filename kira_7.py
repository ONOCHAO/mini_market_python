from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            descript TEXT NOT NULL,
            image_url TEXT,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            descript TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM items')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO items (name, descript, image_url, price) VALUES (?, ?, ?, ?)
        ''', [
            ('Подушка "Облако"', 'Мягкая и воздушная подушка для сна', 'https://example.com/images/pillow1.jpg', 1999.99),
            ('Термокружка SteelCup', 'Держит тепло до 12 часов', 'https://example.com/images/mug.jpg', 1290.00),
            ('Ноутбук ProBook X1', 'Мощный ноутбук для работы и игр', 'https://example.com/images/laptop.jpg', 239990.50),
            ('Смарт-часы FitTrack', 'Отслеживание сна, шагов и сердцебиения', 'https://example.com/images/watch.jpg', 10990.00),
            ('Книга "Глубокая работа"', 'Бестселлер по продуктивности', 'https://example.com/images/book.jpg', 3490.00),
            ('Игровая мышь HyperClick', 'RGB подсветка, 16000 DPI', 'https://example.com/images/mouse.jpg', 5990.00)
        ])
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    descript = request.form.get('descript')
    price = request.form.get('price')

    try:
        price = float(price)
    except ValueError:
        return "Неверный формат цены", 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO buys (name, descript, price) VALUES (?, ?, ?)', (name, descript, price))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/account')
def cabinet():
    conn=sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buys')
    items = cursor.fetchall()
    conn.close()
    return render_template('main.html' , items=items)

    
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5002)
