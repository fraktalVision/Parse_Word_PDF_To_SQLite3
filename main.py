__author__ = 'Fred Jaworski'

from PDF_reader import *
from DB_Connection import *

pdf = pdf_reader()
pdf.print_entries()
conn = DB_Connector()
conn.__connect__('busted_db.db')
conn.add_entries(pdf.list_of_entries)
conn.__commit__()
conn.__close__()
