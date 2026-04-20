from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_123' # Нужно для хранения сессии избранного

# Путь к файлу с книгами
BOOKS_FILE = 'books.json'

def load_books():
    """Загружает список книг из JSON файла"""
    if not os.path.exists(BOOKS_FILE):
        # Если файла нет, создаем демо-книги
        demo_books = [
            {"id": 1, "title": "Евгений Онегин", "author": "А.С. Пушкин", "content": "Мой дядя самых честных правил..."},
            {"id": 2, "title": "Мастер и Маргарита", "author": "М.А. Булгаков", "content": "Однажды весною, в час небывало жаркого заката..."},
            {"id": 3, "title": "Преступление и наказание", "author": "Ф.М. Достоевский", "content": "В начале июля, в чрезвычайно жаркое время..."}
        ]
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(demo_books, f, ensure_ascii=False, indent=4)
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    """Главная страница со списком книг"""
    books = load_books()
    # Проверяем, есть ли в сессии список избранного
    if 'favorites' not in session:
        session['favorites'] = []
    return render_template('index.html', books=books, favorites=session['favorites'])

@app.route('/read/<int:book_id>')
def read_book(book_id):
    """Страница чтения книги"""
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return render_template('read.html', book=book)
    return "Книга не найдена", 404

@app.route('/add_favorite/<int:book_id>')
def add_favorite(book_id):
    """Добавление в избранное"""
    favorites = session.get('favorites', [])
    if book_id not in favorites:
        favorites.append(book_id)
        session['favorites'] = favorites
    return redirect(url_for('index'))

@app.route('/remove_favorite/<int:book_id>')
def remove_favorite(book_id):
    """Удаление из избранного"""
    favorites = session.get('favorites', [])
    if book_id in favorites:
        favorites.remove(book_id)
        session['favorites'] = favorites
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)