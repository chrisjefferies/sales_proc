import datetime
import time
import random
import names
import math
import os
from pyzipcode import ZipCodeDatabase
try:
	from sqlite3 import dbapi2 as sqlite
except ImportError:
	from pysqlite2 import dbapi2 as sqlite


zcdb = ZipCodeDatabase()



# CONTROLS
file = 'assets/new_db.db'
records = 100

# DB Connection Object
db_connection = sqlite.connect(file)
db_curs = db_connection.cursor()


def ran(x, n = 0, r = 2, only_pos = False):
	if only_pos:
		return abs(round(random.random() * x + n, r))
	else:
		return round(random.random() * x + n, r)

def get_ran(array):
	# Great place to handle rarity among records logic.
	return array[int(round(random.random() * len(array))) - 1]

def ran_chance(n):
	if int( math.floor(random.random() * n) ):
		# Lands here n-1/n times
		return False
	else:
		# Lands here 1/n times
		return True

def create_address():
	first = names.get_first_name()
	last = names.get_last_name()
	roads_kinds = ' St',' St',' St',' Rd',' Rd', ' Blvd', ' Ave', ' Ct', ''
	address_one = str(int(ran(10000, 0, 0))) + ' ' + names.get_last_name() +  get_ran(roads_kinds)

	units_kinds = 'No. ', 'Unit ', 'Suite ', 'Ste. ' 'A', 'B', 'C', 'D', 'A-', 'B-', 'C-', 'D-'
	# One in Five contain a unit address
	if ran_chance(5):
		address_two = get_ran(units_kinds) + str(int(ran(100)))
	else:
		address_two = ''

	# Brute Force a valid zip code
	found_one = False
	while found_one == False:
		rand_zip = str(int(ran(99999, 0, 0)))
		try:
			_zip = zcdb[ rand_zip ]
			found_one = True
		except Exception:
			a = True #throwaway
		# else:
		# 	found_one = True

	city = _zip.city
	state = _zip.state

	return str(first+','+last+','+address_one+','+address_two+','+city+','+state+','+rand_zip)

def db_controller(row, col, value, mode):
	# print db_curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
	db_curs.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, order_id VARCHAR(20))")

	
	# if !os.path.isfile(file): 
	# 	# Create Table Structure
	# 	db_curs.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, )")
	# 	db_curs.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY,)")

	assert type(row) == str and type(col) == str and type(mode) == str
	if mode == 'w':
		db_curs.execute("")



def generate(n):
	for i in range(0, n):
		with open(file) as f:
			lines = f.read().splitlines()
			last_line = lines[-1]
			f.seek(0) # Guess how long it took to figure this one out.
			num_lines = sum(1 for line in f)

		orderID = num_lines + 12000000000

		# Get Unix Timestamp of last date and add it to the last one.
		if num_lines != 1:
			unix_date_l = time.mktime(datetime.datetime.strptime(
				last_line.split(',')[0], 
				'%Y-%m-%d %H:%M:%S'
			).timetuple())
		else:
			# initial generation case
			unix_date_l = 0

		iso_date = datetime.datetime.fromtimestamp(
			int(unix_date_l) + int( ran(100000) )
		)

		total = ran(175, 25) 
		shipping = ran(0.1, ran(10, -5), 2, True)  
		subtotal = total - shipping
		bill_address = create_address()

		if ran_chance(10):
			ship_address = create_address()
		else:
			ship_address = bill_address


		f = open(file, 'a') 
		f.write(str(iso_date)+','+str(orderID)+',')
		f.write(str(total)+','+str(shipping)+','+str(subtotal)+',')
		f.write(bill_address+','+ship_address+'\n')
		f.close()
		if (i % 100 == 0):
			print '.'


if os.path.isfile(file):
	generate(records)
else:
	f = open(file, 'w+')
	f.write('date,orderId,total,shipping,subtotal,shipNameFirst,shipNameLast,shipAddress1,\
		shipAddress2,shipCity,shipState,shipZip,billNameFirst,billNameLast,billAddress1,billAddress2,\
		billCity,billState,billZip\n')
	f.close()
	generate(records)

























