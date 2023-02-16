from flask_login import UserMixin
from utils import get_db_connection


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
                           SELECT * FROM users WHERE id = %s
                           """, (user_id)
                    )
        user = cur.fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )

        cur.close()
        conn.close()
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (%s, %s, %s, %s)",
            (id_, name, email, profile_pic),
        )
        conn.commit()

        cur.close()
        conn.close()
