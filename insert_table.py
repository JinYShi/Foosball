#!/usr/bin/python3

import sqlite3
import glob
import re

conn = sqlite3.connect('foosball.db')
conn.text_factory = str
print ("Opened database successfully")

# path = glob.glob("fake_data.txt")
f = open('fake_data.txt', 'r')
buff = f.read()
buff = buff.split('\n')
user = {
	'user_ID':None,
	'user_name':None,
	'num_win':0,
	'num_total':0}
for line in buff:

	d = line.split()
	user['user_ID'] = d[0]
	user['user_name'] = d[1]
	user['num_win'] = d[2]
	user['num_total'] = d[3]

	conn.execute("INSERT INTO users (user_ID, user_name, num_win, num_total) VALUES (?,?,?,?)",
	              (user['user_ID'],
	               user['user_name'],
	               user['num_win'],
	               user['num_total']))

conn.commit()
print ("success congrats")
conn.close()