from flask import Flask, render_template, request
from psycopg2 import connect, OperationalError, ProgrammingError

app = Flask(__name__)

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"


def select_everything():
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database='library_db')
        cursor = cnx.cursor()
        cursor.execute(f"select * from book")
        names = cursor.fetchall()
        cursor.close()
        cnx.close()
    except OperationalError as err:
        print(err)
    return names


def select_from_db(id):
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database='library_db')
        cursor = cnx.cursor()
        cursor.execute(f"select * from book where book.id = {id}")
        names = cursor.fetchall()
        cursor.close()
        cnx.close()
    except OperationalError as err:
        print(err)
    return names


def select_authors():
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database='library_db')
        cursor = cnx.cursor()
        cursor.execute(f"select * from author")
        authors = cursor.fetchall()
        cursor.close()
        cnx.close()
    except OperationalError as err:
        print(err)
    return authors


def add_book(author, isbn, name, desc):
    cnx = connect(user=USER, password=PASSWORD, host=HOST, database='library_db')
    cursor = cnx.cursor()
    cursor.execute(
        f"insert into book (author_id, ISBN, name, description) values ({author}, {isbn}, '{name}', '{desc}')")
    cnx.commit()
    cursor.close()
    cnx.close()


def delete_book(id):
    cnx = connect(user=USER, password=PASSWORD, host=HOST, database='library_db')
    cursor = cnx.cursor()
    cursor.execute(
        f"delete from book where id={id}")
    cnx.commit()
    cursor.close()
    cnx.close()


start_page = False
select_all = False
book_detail = False
adding = False
deleting = False


@app.route('/', methods=['GET'])
def home_page():
    start_page = True
    return render_template('index.html', start_page=start_page)


@app.route('/books', methods=['GET'])
def books():
    select_all = True
    list_of_books = select_everything()
    return render_template('index.html', list_of_books=list_of_books, select_all=select_all)


@app.route('/book_details/<id>', methods=['GET'])
def book_details(id):
    book_detail = True
    book_det = select_from_db(id)
    return render_template('index.html', book_detail=book_detail, book_det=book_det)


@app.route('/add_book', methods=['GET', 'POST'])
def add():
    adding = True
    if request.method == 'GET':
        authors = select_authors()
        return render_template('index.html', adding=adding, authors=authors)
    else:
        try:
            new_author = int(request.form['author'])
            new_isbn = int(request.form['isbn'])
            new_name = request.form['name']
            new_desc = request.form['description']
            add_book(new_author, new_isbn, new_name, new_desc)
            return 'Book added.'
        except OperationalError:
            return 'Operational Error.. Try again'
        except ProgrammingError:
            return 'Error.. Try again.'


@app.route('/delete_book/<id>', methods=['GET', 'POST'])
def delete(id):
    deleting = True
    if request.method == 'GET':
        deleted_book_details = select_from_db(id)
        delete_book(id)
        return render_template('index.html', deleting=deleting, id=id, deleted_book_details=deleted_book_details)


if __name__ == '__main__':
    app.run()