import sqlite3 as sql

__author__ = 'Fred Jaworski'

class DB_Connector:

    def __init__(self):
        self.__connect__('busted_db.db')

    def __connect__(self, db_file):
        self.conn = sql.connect(db_file)
        self.cur = self.conn.cursor()

    def __commit__(self):
        self.conn.commit()

    def __close__(self):
        self.conn.close()

    def add_entries(self, list_of_entries):
        for entry in list_of_entries:
            self.cur.execute('SELECT MAX(`id`) FROM mentor')  # captures the highest id key
            id = self.cur.fetchone()  # sets it to id variable as tuple
            id = id[0]  # sets to just the numerical value
            entry = list(entry)  # hack-y way to add id to entry tuple
            entry[0] = id + 1  # hack
            entry = tuple(entry)  # hack
            self.cur.execute('INSERT INTO mentor VALUES(?,?,?,?,?,?,?)', entry)  # execution of SQL string
