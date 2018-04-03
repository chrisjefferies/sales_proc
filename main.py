# requires sqlalchemy
# requires records

# from django.db import models

import os

try:
	from sqlite3 import dbapi2 as sqlite
except ImportError:
	from pysqlite2 import dbapi2 as sqlite

db_path = 'db/example.db'
csv_path = 'assets/new_data.csv'

debug = False

def log(msg):
	if debug:
		print msg

def iterate_conv(_list, st_con = False):
	a = _list[0]
	for i in range(1, len(_list)):
		if st_con:
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

def csv_to_sqlite(file, db, t_name):
	# Convert a CSV file into a DB. 

	# Value config for expected file names
	def switch(x):
		return {
			'orderId': " INTEGER PRIMARY KEY",
			'orderDate': " DATETIME",
			'shipping': " FLOAT",
			'total': " FLOAT",
			'subtotal': " FLOAT"
		}.get(x, " TINYTEXT")

	# define some variables based on file
	with open(file) as f:
		f_lines = f.read().splitlines()
		f_first = f_lines[0].split(',')
		# print f_first

	if os.path.isfile(db_path):
		# it exists, append data
		print 'Already exists. Appending...'

		c = 0

		# Figure out what we already have. 
		db_conn = sqlite.connect(db_path)
		db_curs = db_conn.cursor()
		
		last_record_id = db_curs.execute("SELECT orderId FROM orders ORDER BY orderId DESC LIMIT 1").fetchall()[0][0]
		for i in range(1, len(f_lines)):
			# print type(f_lines[i].split(',')[0])
			# print type(last_record_id)
			if int(f_lines[i].split(',')[0]) > last_record_id:
				insert_into(db_conn, t_name, f_first, f_lines[i].split(','))
				c += 1

		print 'Updated:', c, 'records.'
	else:

		print 'Creating database, then inserting data...'

		db_conn = sqlite.connect(db_path)
		db_curs = db_conn.cursor()
		
		# Create, then populate. 
		q_str = "CREATE TABLE " + t_name + " ("
		
		for i in range(0, len(f_first)):
			log('Adding: ' + f_first[i] + '...')

			if i != 0:
				q_str += ", "

			q_str += f_first[i] 
			q_str += switch(f_first[i])

		q_str += " );"

		log(q_str)

		db_curs.execute(q_str)

		db_conn.commit()

		for j in range(1, len(f_lines)):
			insert_into(db_conn, t_name, f_first, f_lines[j].split(','))



	db_curs.execute("SELECT * FROM orders WHERE orderId = '12000000015'")
	print 'found: ' + str(db_curs.fetchall())
	db_conn.commit()

		# db_curs.execute("SELECT * FROM sqlite_master WHERE name='orders'")

		# print db_curs.fetchall()


csv_to_sqlite(csv_path, db_path, 'orders')


# db_conn = sqlite.connect(db_path)

# db_curs = db_conn.cursor()

# db_curs.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, order_id VARCHAR(20), first_name VARCHAR(30), last_name VARCHAR(30), order_date DATE)")

# db_curs.execute("INSERT INTO orders (order_id, first_name, last_name, order_date) VALUES ('120001', 'Jon', 'Doe', '1520960378000')")

# db_curs.execute("SELECT * FROM orders WHERE order_id = '120001'")

# print db_curs.fetchall()

# db_conn.commit()

# print 'Done.'






