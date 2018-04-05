# requires sqlalchemy
# requires records

# from django.db import models

import os
from sqlite3 import dbapi2 as sqlite

# try:
	
# except ImportError:
# 	from pysqlite2 import dbapi2 as sqlite

db_path = 'db/example.db'
csv_path = 'assets/new_data.csv'

debug = False

def log(msg):
	if debug:
		print msg

def iterate_conv(_list, str_conv = False):
	a = _list[0]
	for i in range(1, len(_list)):
		if str_conv:
			a += ', \'' +  _list[i] + '\''
		else:
			a += ', ' + _list[i]
	return a

def insert_into(db_connection, t_name, header, line):
	assert type(header) == list and type(line) == list

	q_str = "INSERT INTO " + t_name + " ("
	q_str += iterate_conv(header)
	q_str += ") VALUES ("
	q_str += iterate_conv(line, True)
	q_str += ")"

	# print q_str

	db_cu = db_connection.cursor()
	db_cu.execute(q_str)
	db_connection.commit()


# UNSANITIZED. Remove for production environment. 
def fetch(col, row, t_name, db_conn, term = '*', full_qry = False):

	# First, run a basic table exists check. 
	db_curs = db_conn.cursor()
	db_curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + t_name + "'")
	table_exists = db_curs.fetchall()

	if not table_exists:
		print 'Table does not exist.'
		return False

	if full_qry:
		# Optional raw input
		# Once again. Not fit for production. 
		db_curs.execute(full_qry)
		return db_curs.fetchall()

	else:
		q_str = "SELECT " + term + " FROM " + t_name + " WHERE " + col + " LIKE '" + row + "'"

		db_curs.execute(q_str)
		val = db_curs.fetchall()

		# Basic datatype corrections
		if len(val) == 1 and len(val[0]) == 1 and type(val[0][0]) == unicode:
			return val[0][0]
		else:
			if len(val) == 1 and type(val) == list:
				return val[0]
			else:
				return val



def csv_to_sqlite(file, db_conn, t_name):
	# Convert a CSV file into a DB. 

	# Value config for expected file names
	def switch(x):
		return {
			'orderId': "INTEGER PRIMARY KEY",
			'orderDate': "DATETIME",
			'shipping': "FLOAT",
			'total': "FLOAT",
			'subtotal': "FLOAT"
		}.get(x, "TINYTEXT")

	# define some variables based on file
	with open(file) as f:
		f_lines = f.read().splitlines()
		f_first = f_lines[0].split(',')
		# print f_first

	db_curs = db_conn.cursor()

	q_str = "CREATE TABLE IF NOT EXISTS " + t_name + " ("
		
	for i in range(0, len(f_first)):
		if i != 0:
			q_str += ", "
		q_str += f_first[i] 
		q_str += ' ' + switch(f_first[i])

	q_str += " );"

	db_curs.execute(q_str)
	db_conn.commit()

	try:
		last_record_id = db_curs.execute("SELECT orderId FROM orders ORDER BY orderId DESC LIMIT 1").fetchall()[0][0]
	except IndexError:
		last_record_id = 0

	print 'last record id:', last_record_id

	c = 0
	for i in range(1, len(f_lines)):

		# This relies on the Primary Key being the 0 record. Not ideal. 
		if int(f_lines[i].split(',')[0]) > last_record_id:
			insert_into(db_conn, t_name, f_first, f_lines[i].split(','))
			c += 1

	print 'Updated:', c, 'records.'

	# print 'found:', fetch('orderId', '120000000%5', 'orders', db_conn, 'billNameFirst')

	# db_curs.execute("SELECT * FROM sqlite_master WHERE name='orders'")
	# print db_curs.fetchall()





def calc_day_totals(date_col, rev_col, db_conn):
	# Okay. Now we've got a table from which to fetch(). 
	# Get all unique dates that appear in the database.
	unique_days = fetch(' ', ' ', 'orders', db_conn, ' ', "SELECT DISTINCT date(" + date_col + ") FROM orders")
	day_totals = []

	totals = {}

	for i in range(0, len(unique_days)):
		day_totals.append(fetch(date_col, unique_days[i][0] + '%', 'orders', db_conn, rev_col))
		tot = 0

		if len(day_totals[i]) == 1:
			tot = day_totals[i][0]
		else:
			for j in range(0, len(day_totals[i])):
				tot += day_totals[i][j][0]

		totals[str(unique_days[i][0])] = tot

	print totals




# Okay. Here. We. Go. 
db_conn = sqlite.connect(db_path)

# Set/Update DB. 
csv_to_sqlite(csv_path, db_conn, 'orders')

calc_day_totals('orderDate', 'total', db_conn)

# db_conn = sqlite.connect(db_path)
# print 'found:', fetch('orderId', '12000000031', 'orders', db_conn)


# db_conn = sqlite.connect(db_path)
# db_curs = db_conn.cursor()

# db_curs.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, order_id VARCHAR(20), first_name VARCHAR(30), last_name VARCHAR(30), order_date DATE)")
# db_curs.execute("INSERT INTO orders (order_id, first_name, last_name, order_date) VALUES ('120001', 'Jon', 'Doe', '1520960378000')")
# db_curs.execute("SELECT * FROM orders WHERE order_id = '120001'")
# print db_curs.fetchall()
# db_conn.commit()
# print 'Done.'






