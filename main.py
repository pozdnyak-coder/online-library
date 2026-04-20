from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
# Секретный ключ для подписи кук сессии (обязательно!)
app.secret_key = 'super-secret-key-12345'

# Встроенные демо-книги
DEMO_BOOKS = [
    {"id": 1, "title": "Евгений Онегин", "author": "А.С. Пушкин", "content": "Мой дядя самых честных правил..."},
    {"id": 2, "title": "Мастер и Маргарита", "author": "М.А. Булгаков", "content": "Однажды весною, в час небывало жаркого заката..."},
    {"id": 3, "title": "Преступление и наказание", "author": "Ф.М. Достоевский", "content": "В начале июля, в чрезвычайно жаркое время..."}
]

@app.route('/')
def index():
    # Инициализируем избранное в сессии, если его нет
    if 'favorites' not in session:
        session['favorites'] = []
    return render_template('index.html', books=DEMO_BOOKS, favorites=session['favorites'])

@app.route('/read/<int:book_id>')
def read_book(book_id):
    book = next((b for b in DEMO_BOOKS if b['id'] == book_id), None)
    if book:
        return render_template('read.html', book=book)
    return "Книга не найдена", 404

@app.route('/add_favorite/<int:book_id>')
def add_favorite(book_id):
    favorites = session.get('favorites', [])
    if book_id not in favorites:
        favorites.append(book_id)
        session['favorites'] = favorites
    return redirect(url_for('index'))

@app.route('/remove_favorite/<int:book_id>')
def remove_favorite(book_id):
    favorites = session.get('favorites', [])
    if book_id in favorites:
        favorites.remove(book_id)
        session['favorites'] = favorites
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
