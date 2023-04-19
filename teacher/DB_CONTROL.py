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


# very stupid func, pls rewrite this
def go_cmd_ct(cmd, type_, *args):
	conn, cur = conn_open()
	if type_ == 'insert':
		try:
			if cur.execute('SELECT * FROM creator_test WHERE id = ?', ([args[3]])).fetchall() != []:
				cur.execute(cmd, (args[0], args[1], args[2], args[3]))
				conn.commit()
			else:
				cur.execute(args[4], (None, args[0], args[1], args[2]))
				conn.commit()
			return True
		except Exception as e:
			print(e)
			return False
	elif type_ == 'select':
		cur.execute(cmd, [args[0]])
		res_data = cur.fetchall()
		return res_data
	elif type_ == 'drop' or type_ == 'create':
		cur.execute(cmd)
		conn.commit()
		return True
	elif type_ == 'delete':
		string = 'Новый вопрос.'
		cur.execute(cmd, (string, ))
		conn.commit()
		return True
	else:
		print("type_ of cmd unknown. Check command for db.")


def clear_cache_tb():
	conn, cur = conn_open()
	cmd = 'DROP TABLE IF EXISTS creator_test'
	cur.execute(cmd)
	conn.commit()


def get_created_test():
	conn, cur = conn_open()
	cmd = 'SELECT * FROM creator_test'
	cur.execute(cmd)
	data = cur.fetchall()
	return data
