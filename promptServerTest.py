#!/usr/bin/python
import psycopg2
import sys
 
def main():
	#Define our connection string
	conn_string = "host='localhost' dbname='ogous' user='postgres' password='Getter77'"
 
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 	
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	'''SELECT *
	FROM Northwind.INFORMATION_SCHEMA.COLUMNS
	WHERE TABLE_NAME = N'Customers' '''
	cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
	XS = cursor.fetchall()
	b = dict(zip(XS[::2], XS[1::2]))
	#b['tooltype'] = "SDX"
	#print b['tooltype']
	for key, value in b.items():
    		print (key, value)
	print "PYONG!\n"
 
if __name__ == "__main__":
	main()

'''#/usr/bin/python2.4

import psycopg2

# Try to connect
conn_string = "host='localhost' dbname='ogous' user='postgres' password='Getter77'"
try:
    conn=psycopg2.connect(conn_string)
except:
    print "I am unable to connect to the database."

cur = conn.cursor()
try:
    cur.execute("""SELECT * from bar""")
except:
    print "I can't SELECT from bar"

rows = cur.fetchall()
for row in rows:
    print "   ", row[1][1]'''