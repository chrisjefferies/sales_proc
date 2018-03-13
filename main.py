# requires sqlalchemy
# requires records

# from django.db import models

try:
	from sqlite3 import dbapi2 as sqlite
except ImportError:
	from pysqlite2 import dbapi2 as sqlite


def process():
	print 'process invoked'

db_connection = sqlite.connect('sample.db')

print dir(db_connection)

db_curs = db_connection.cursor()

# db_curs.execute("CREATE TABLE orders (\
# 	id INTEGER PRIMARY KEY, order_id VARCHAR(20),\
# 	first_name VARCHAR(30), last_name VARCHAR(30),\
# 	order_date DATE)")

# db_curs.execute("INSERT INTO orders (order_id, first_name, last_name, order_date) VALUES ('120001', 'Jon', 'Doe', '1520960378000')")

db_curs.execute("SELECT * FROM orders WHERE order_id = '120001'")

print db_curs.fetchall()

# db_connection.commit()

print 'done'






