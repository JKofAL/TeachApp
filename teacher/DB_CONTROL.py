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


def get_tbs():
	conn, cur = conn_open()
	cmd = 'SELECT name FROM sqlite_master WHERE type="table";'
	cur.execute(cmd)

	# [('sqlite_sequence',), ('infoge',), ('students_result',)]
	data = cur.fetchall()
	data = list(map(lambda x: x[0], data))

	no_test_tb = [
	'sqlite_sequence',
	'students_result',
	]

	for tb_name in no_test_tb:
		del data[data.index(tb_name)]

	return data
