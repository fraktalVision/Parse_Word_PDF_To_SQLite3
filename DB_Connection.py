import sqlite3 as sql
import re

__author__ = 'Fred Jaworski'

class DB_Connector:

    def __init__(self):
        self.__connect__('busted_db.db')
        self.return_list = []
        self.speech_list = []

    def __connect__(self, db_file):
        self.conn = sql.connect(db_file)
        self.cur = self.conn.cursor()

    def __commit__(self):
        self.conn.commit()

    def __close__(self):
        self.conn.close()

    def add_mentor_entries(self, list_of_entries):
        for entry in list_of_entries:
            self.cur.execute('SELECT MAX(`id`) FROM mentor')  # captures the highest id key
            id = self.cur.fetchone()  # sets it to id variable as tuple
            id = id[0]  # sets to just the numerical value
            entry = list(entry)  # hack-y way to add id to entry tuple
            entry[0] = id + 1  # hack
            entry = tuple(entry)  # hack
            self.cur.execute('INSERT INTO mentor VALUES(?,?,?,?,?,?,?)', entry)  # execution of SQL string

    def pull_mentor_data(self):
        self.cur.execute('SELECT `moral`, `point`, `speech` FROM mentor WHERE `speech` <> "fill";')
        self.return_list = self.cur.fetchall()
        count = 1
        for r in self.return_list:
            r = self.db_encode(r)
            # in lieu of a switch statement...
            if re.search("AfM[0-9]{2}", r[2]):
                self.entry = (count, 0, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("AG[0-9]{2}", r[2]):
                self.entry = (count, 1, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("LM[0-9]{2}", r[2]):
                self.entry = (count, 2, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("IG[0-9]{2}", r[2]):
                self.entry = (count, 3, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("WM[0-9]{2}", r[2]):
                self.entry = (count, 4, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("AfG[0-9]{2}", r[2]):
                self.entry = (count, 5, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("AM[0-9]{2}", r[2]):
                self.entry = (count, 6, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("LG[0-9]{2}", r[2]):
                self.entry = (count, 7, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("IM[0-9]{2}", r[2]):
                self.entry = (count, 8, r[0], r[1], r[2])
                self.speech_list.append(self.entry)
            elif re.search("WG[0-9]{2}", r[2]):
                self.entry = (count, 9, r[0], r[1], r[2])
                self.speech_list.append(self.entry)

            count += 1

    def print_speech(self):
        for sp in self.speech_list:
            print sp

    # encodes to ascii
    def db_encode(self, r):
        r = list(r)
        r[2] = r[2].encode('ascii', 'ignore')
        r = tuple(r)
        return r

    def add_speech(self):
        for entry in self.speech_list:
            self.cur.execute("INSERT INTO mentor_speech VALUES (?, ?, ?, ?, ?)", entry)

    # test method to ensure all entries were added successfully
    def proof(self):
        self.cur.execute("SELECT * FROM mentor_speech")
        r_list = self.cur.fetchall()
        for r in r_list:
            print r