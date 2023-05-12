from configparser import ConfigParser
import sqlite3
import pandas as pd
from random import shuffle
import socket

import os


os.chdir('..')
path = os.getcwd()

DB_PATH = path+'\\teachapp.db'

right_answers = list()
questions = list()
subject = 'infoge'



def loading_test():

	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

	config_path = path + '\\test_controller.ini'
	

	config = ConfigParser()
	config.read(config_path)


	test = config.get('CONFIG', 'test_name')
	
	cur.execute('SELECT type FROM {}'.format(test))
	types = cur.fetchall()

	try:
		length_of_types = max(list(map(int, list(map(lambda x: x[0], types)))))
	except Exception as e:
		length_of_types = 10

	# cur.execute(f'SELECT name FROM sqlite_master WHERE type="table";')

	resdata = list()
	global right_answers, questions, subject

	for i in range(length_of_types):
		cur.execute('SELECT * FROM {} WHERE type LIKE {}'.format(test, str(i+1)))
		data = cur.fetchall()
		if data != []:
			shuffle(data)
			resdata.append(data[0][2])
			right_answers.append((data[0][3], data[0][4]))


	questions = resdata
	subject = test

	return resdata


def counting_the_result():
	global right_answers, questions, subject
	localip = 'z' + str(socket.gethostname()).replace('-', 'z').replace('.', 'z')	# имя для бд
	balls = 0																		# бал за вопрос
	full_balls = 0																	# итоговые баллы
	NOCA = 0 																		# number_of_correct_answers
	incorrects_label = ''															# разбор вопросов
	incorrects = {'std_answer': [], 'rgt_answer': [], 'question': []}

	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute('SELECT answer FROM {}'.format(localip))
	answers = cur.fetchall()

	cur.execute('DROP TABLE {}'.format(localip))
	conn.commit()

	''' 
	----------------------------
	----- checking answers -----
	----------------------------
	'''

	# answers = [(firstname), (lastname), (class_), (answer1), (answer2)]
	# right_answers = [(answer1), (answer2)]	
	class_ = answers[2][0]

	quantity_questions = str(len(answers)-3)
	for i in range(3, len(answers)):
		if answers[i][0].lower() == right_answers[i-3][0].lower():
			balls += right_answers[i-3][1]
			NOCA += 1
		else:
			incorrects['std_answer'].append(answers[i][0].lower())
			incorrects['rgt_answer'].append(right_answers[i-3][0].lower())
			incorrects['question'].append(questions[i-3].replace('\\n', '\n\n').replace('\\u202f', '').replace('\\xa0', '\n'))

	for i in right_answers:
		full_balls += i[1]

	procent = balls/full_balls * 100
	procent = round(procent, 2)


	if procent > 75:
		grade = 5
	elif procent <= 75 and procent > 50:
		grade = 4
	elif procent <= 50 and procent > 25:
		grade = 3
	else:
		grade = 2


	for i in range(len(incorrects['question'])):
		incorrects_label += '\nВопрос:\n\n{}\nПравильный ответ: {}\nВаш ответ: {}\n'.format(incorrects['question'][i],
																							incorrects['rgt_answer'][i],
																							'пустой ответ' if incorrects['std_answer'][i] == '' else incorrects['std_answer'][i])

	cur.execute('INSERT INTO students_result VALUES (?, ?, ?, ?, ?, ?, ?)',
				(None, answers[0][0], answers[1][0], class_, subject, grade, procent))
	conn.commit()
	conn.close()

	result = {
		'grade': str(grade),
		'procent': procent,
		'incorrect_questions_with_answers': incorrects_label,
		'quantity_questions': quantity_questions,
		'noca': NOCA,
	}

	return result