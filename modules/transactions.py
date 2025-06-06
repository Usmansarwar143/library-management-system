from database.db_config import Database
from datetime import datetime, timedelta

class TransactionManager:
    def __init__(self):
        self.db = Database()
        self.fine_per_day = 1.00  # $1 per day for late returns

    def issue_book(self, book_id, member_id):
        cursor = self.db.get_connection().cursor()
        try:
            # Check book availability
            cursor.execute("SELECT quantity FROM BOOKS WHERE book_id = %s", (book_id,))
            book = cursor.fetchone()
            if not book or book[0] <= 0:
                raise Exception("Book not available")

            # Check if member exists
            cursor.execute("SELECT member_id FROM MEMBERS WHERE member_id = %s", (member_id,))
            if not cursor.fetchone():
                raise Exception("Member not found")

            issue_date = datetime.now().date()
            return_date = issue_date + timedelta(days=14)  # 2 weeks loan period

            cursor.execute(
                """
                INSERT INTO TRANSACTIONS (book_id, member_id, issue_date, return_date)
                VALUES (%s, %s, %s, %s)
                """,
                (book_id, member_id, issue_date, return_date)
            )
            cursor.execute(
                "UPDATE BOOKS SET quantity = quantity - 1 WHERE book_id = %s",
                (book_id,)
            )
            self.db.get_connection().commit()
        finally:
            cursor.close()

    def return_book(self, txn_id):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute(
                """
                SELECT book_id, issue_date, return_date
                FROM TRANSACTIONS
                WHERE txn_id = %s AND actual_return_date IS NULL
                """,
                (txn_id,)
            )
            txn = cursor.fetchone()
            if not txn:
                raise Exception("Transaction not found or already returned")

            book_id, issue_date, return_date = txn
            actual_return_date = datetime.now().date()
            fine = 0.0

            if actual_return_date > return_date:
                days_late = (actual_return_date - return_date).days
                fine = days_late * self.fine_per_day

            cursor.execute(
                """
                UPDATE TRANSACTIONS
                SET actual_return_date = %s, fine = %s
                WHERE txn_id = %s
                """,
                (actual_return_date, fine, txn_id)
            )
            cursor.execute(
                "UPDATE BOOKS SET quantity = quantity + 1 WHERE book_id = %s",
                (book_id,)
            )
            self.db.get_connection().commit()
            return fine
        finally:
            cursor.close()

    def get_issued_books(self):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute("""
                SELECT t.txn_id, b.title, m.name, t.issue_date, t.return_date, t.fine
                FROM TRANSACTIONS t
                JOIN BOOKS b ON t.book_id = b.book_id
                JOIN MEMBERS m ON t.member_id = m.member_id
                WHERE t.actual_return_date IS NULL
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_overdue_books(self):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute("""
                SELECT t.txn_id, b.title, m.name, t.issue_date, t.return_date, t.fine
                FROM TRANSACTIONS t
                JOIN BOOKS b ON t.book_id = b.book_id
                JOIN MEMBERS m ON t.member_id = m.member_id
                WHERE t.actual_return_date IS NULL AND t.return_date < CURDATE()
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_total_fines(self):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute("SELECT SUM(fine) FROM TRANSACTIONS WHERE fine > 0")
            result = cursor.fetchone()[0]
            return result if result else 0.0
        finally:
            cursor.close()