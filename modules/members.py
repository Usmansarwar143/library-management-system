from database.db_config import Database

class MemberManager:
    def __init__(self):
        self.db = Database()

    def add_member(self, name, email, phone):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute(
                "INSERT INTO MEMBERS (name, email, phone) VALUES (%s, %s, %s)",
                (name, email, phone)
            )
            self.db.get_connection().commit()
        finally:
            cursor.close()

    def get_all_members(self):
        cursor = self.db.get_connection().cursor()
        try:
            cursor.execute("SELECT member_id, name, email, phone FROM MEMBERS")
            return cursor.fetchall()
        finally:
            cursor.close()