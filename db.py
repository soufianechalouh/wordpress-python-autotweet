import sqlite3


class DBInstance:
    def __init__(self):
        self.conn = sqlite3.connect("posts.db")
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS posts (
                                                post_url text UNIQUE
                                                )
                        """)
        self.conn.commit()

    def add_post(self, url):
        query = f"INSERT INTO posts VALUES ('{url}')"
        self.c.execute(query)
        self.conn.commit()

    def get_all_posts(self):
        self.c.execute(f"SELECT * FROM posts")
        return self.c.fetchall()

    def is_previously_published(self, url):
        query = f"SELECT * FROM posts WHERE post_url='{url}'"
        self.c.execute(query)
        return bool(self.c.fetchall())

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    db_instance = DBInstance()
    db_instance.add_post("https://test.mytest.com")
    posts = db_instance.get_all_posts()
    db_instance.close_connection()