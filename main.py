__author__ = 'Fred Jaworski'

from PDF_reader import *
from DB_Connection import *

conn = DB_Connector()
conn.__connect__('busted_db.db')
conn.pull_mentor_data()
conn.add_speech()
conn.proof()
conn.__commit__()
conn.__close__()
