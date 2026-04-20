from flask import Flask, render_template

app = Flask(__name__)

# Встроенные демо-книги (не требуют файла)
DEMO_BOOKS = [
    {"id": 1, "title": "Евгений Онегин", "author": "А.С. Пушкин", "content": "Мой дядя самых честных правил..."},
    {"id": 2, "title": "Мастер и Маргарита", "author": "М.А. Булгаков", "content": "Однажды весною, в час небывало жаркого заката..."},
    {"id": 3, "title": "Преступление и наказание", "author": "Ф.М. Достоевский", "content": "В начале июля, в чрезвычайно жаркое время..."}
]

@app.route('/')
def index():
    """Главная страница со списком книг"""
    return render_template('index.html', books=DEMO_BOOKS)

@app.route('/read/<int:book_id>')
def read_book(book_id):
    """Страница чтения книги"""
    book = next((b for b in DEMO_BOOKS if b['id'] == book_id), None)
    if book:
        return render_template('read.html', book=book)
    return "Книга не найдена", 404

# Убираем маршруты избранного, т.к. без БД на Vercel они не имеют смысла
# Вместо этого можно просто показывать кнопки-заглушки или убрать их из шаблонов

if __name__ == '__main__':
    app.run(debug=True)
