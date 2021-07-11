import sqlite3
from flask import g
from app import app


class Database(object):
    @staticmethod
    def get_db(db):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = Database(db)
        return db

    @staticmethod
    def close_db(db):
        db = getattr(g, '_database', None)
        if db is None:
            del db

    def __init__(self, db, row_factory=sqlite3.Row):
        self._database = sqlite3.connect(db)
        self._database.row_factory = row_factory

    def __del__(self):
        self._database.close()

    def init(self):
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def query(self, query, args=(), one=False):
        cur = self._database.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
