from database.db_config import Database

class BookManager:
    def __init__(self):
        self.db = Database()

    def add_book(self, title, author, category, quantity):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute(
                "INSERT INTO BOOKS (title, author, category, quantity) VALUES (%s, %s, %s, %s)",
                (title, author, category, quantity)
            )
            self.db.get_connection().commit()
        finally:
            cursor.close()

    def search_books(self, query):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute(
                "SELECT book_id, title, author, category, quantity FROM BOOKS WHERE title LIKE %s",
                (f"%{query}%",)
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_books(self):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute("SELECT book_id, title, author, category, quantity FROM BOOKS")
            return cursor.fetchall()
        finally:
            cursor.close()