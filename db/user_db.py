import os
import sqlite3

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))


class UserDB:
    
    def __init__(self, dbname=os.path.join(DATABASE_DIR, 'olx_rss.sqlite')):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        crtstmt = """
            CREATE TABLE IF NOT EXISTS subs 
            (rowid INTEGER PRIMARY KEY, chat_id INTEGER UNIQUE, is_active INTEGER)
            """
        self.conn.execute(crtstmt)
        self.conn.commit()

    def create_member(self, chat_id):
        """ Adds member to database when chat is initiated. """
        stmt = "INSERT INTO subs (chat_id, is_active) VALUES (?, ?)"
        self.conn.execute(stmt, (chat_id, 0, ))
        self.conn.commit()

    def subscribe(self, chat_id):
        """ Adds member to subscribers list. """
        stmt = "UPDATE subs SET is_active=1 WHERE chat_id=(?)"
        self.conn.execute(stmt, (chat_id,))
        self.conn.commit()

    def unsubscribe(self, chat_id):
        """ Removess member from subscribers list. """
        stmt = "UPDATE subs SET is_active=0 WHERE chat_id=(?)"
        self.conn.execute(stmt, (chat_id,))
        self.conn.commit()

    def get_subs(self):
        """ Returns a list of subscribers. """
        stmt = "SELECT chat_id FROM subs WHERE is_active=1"
        return [x[0] for x in self.conn.execute(stmt)]
