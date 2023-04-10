# db controller

import sqlite3
import os


os.chdir('..')
path = os.getcwd()

DB_PATH = path+'\\teachapp.db'


def conn_open(db_name=DB_PATH):
	try:
		conn = sqlite3.connect(db_name)
		cur = conn.cursor()
		return conn, cur
	except Exception as e:
		print('[!] [SQL controller] The programm could not connect to the DB.')
		print(f'[!] [SQL controller] Error:\n{e}')


def get_std_res():
	conn, cur = conn_open()
	cmd = 'SELECT * FROM students_result'
	cur.execute(cmd)
	data = cur.fetchall()

	tr = list() # table row

	for row in data:
		tr.append([row[4], row[2][0]+'. '+row[1], row[3], row[-2]])

	# tr = [['subject', 'L_n. Name', 'class_', 'grade'],  [...]]

	return tr
