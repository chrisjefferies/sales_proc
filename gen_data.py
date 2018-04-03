import datetime
import time
import random
import names
import math
import os
from pyzipcode import ZipCodeDatabase
# try:
# 	from sqlite3 import dbapi2 as sqlite
# except ImportError:
# 	from pysqlite2 import dbapi2 as sqlite

zcdb = ZipCodeDatabase()



# CONTROLS
file = 'assets/new_data.csv'
records = 10

def ran(x, n = 0, r = 2, only_pos = False):
	if only_pos:
		return abs(round(random.random() * x + n, r))
	else:
		return round(random.random() * x + n, r)

def get_ran(array):
	# Calculate according to Gaussian distribution. 
	e = 2.7182
	a = len(array) - 1
	y = random.random() * (len(array) - 1)

	return array[ int( math.pow( - a * math.log(y/a), 0.5) ) ]

def ran_chance(n):
	if int( math.floor(random.random() * n) ):
		return False
	else:
		return True

def create_address():
	first = names.get_first_name()
	last = names.get_last_name()
	roads_kinds = ' St',' Rd', ' Blvd', ' Ave', ' Lane', '', ' Ct', ' Pl.' ' Way'
	address_one = str(int(ran(10000, 0, 0))) + ' ' + names.get_last_name() + get_ran(roads_kinds)
	units_kinds = 'No. ', 'Unit ', 'Suite ', 'Ste. ' 'A', 'B', 'C', 'D', 'A-', 'B-', 'C-', 'D-'
	# One in Five contain a unit address
	if ran(5, 0, 0):
		address_two = ''
	else:
		address_two = get_ran(units_kinds) + str(int(ran(100)))

	# Brute Force a valid zip code
	found_one = False
	while found_one == False:
		rand_zip = str(int(ran(99999, 0, 0)))
		try:
			_zip = zcdb[rand_zip]
			found_one = True
		except Exception:
			pass

	city = _zip.city
	state = _zip.state

	return str(first+','+last+','+address_one+','+address_two+','+city+','+state+','+rand_zip)

def generate(n):
	if not os.path.isfile(file):
		# Write file header
		f = open(file, 'w+')
		f.write('orderId,date,total,shipping,subtotal,shipNameFirst,shipNameLast,shipAddress1,\
shipAddress2,shipCity,shipState,shipZip,billNameFirst,billNameLast,billAddress1,billAddress2,\
billCity,billState,billZip\n')
		f.close()

	# Generate n random real-looking order data and write to file
	for i in range(0, n):
		with open(file) as f:
			lines = f.read().splitlines()
			last_line = lines[-1]
			f.seek(0) # Guess how long it took to figure this one out.
			num_lines = sum(1 for line in f)

		orderID = num_lines + 12000000000

		# Get Unix Timestamp of last date and add it to the last one.
		if num_lines != 1:
			# Find number-indexed position of date
			unix_date_l = time.mktime(datetime.datetime.strptime(
				last_line.split(',')[1], 
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

		if ran(10, 0, 0):
			ship_address = bill_address
		else:
			ship_address = create_address()

		f = open(file, 'a') 
		f.write(str(orderID)+','+str(iso_date)+',')
		f.write(str(total)+','+str(shipping)+','+str(subtotal)+',')
		f.write(bill_address+','+ship_address+'\n')
		f.close()
		if (i % 100 == 0):
			print 'Writing:', i, '...'


generate(records)


