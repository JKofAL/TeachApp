print('''
░██████╗████████╗██╗░░░██╗██████╗░███████╗███╗░░██╗████████╗░█████╗░██████╗░██████╗░
██╔════╝╚══██╔══╝██║░░░██║██╔══██╗██╔════╝████╗░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗
╚█████╗░░░░██║░░░██║░░░██║██║░░██║█████╗░░██╔██╗██║░░░██║░░░███████║██████╔╝██████╔╝
░╚═══██╗░░░██║░░░██║░░░██║██║░░██║██╔══╝░░██║╚████║░░░██║░░░██╔══██║██╔═══╝░██╔═══╝░
██████╔╝░░░██║░░░╚██████╔╝██████╔╝███████╗██║░╚███║░░░██║░░░██║░░██║██║░░░░░██║░░░░░
╚═════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░
''')

import kivy
from kivy.app import App
from kivy.uix.screenmanager import (
	ScreenManager,
	Screen,
	SlideTransition
)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from loading_circle import CircularProgressBar

from kivy.properties import (
	StringProperty,
	ListProperty,
	ObjectProperty,
	ColorProperty
)
from kivy.graphics import *
from kivy.core.window import Window

backg = kivy.utils.get_color_from_hex('#303841')
Window.clearcolor = (backg[0], backg[1], backg[2], 1)
Window.fullscreen = 'auto'

import loadingtest

import sqlite3

import socket

import sys
import os
import atexit


path = os.getcwd()
DB_PATH = path+'\\teachapp.db'


'''
----------------------------------------------------------------
-------------------------  widgets -------------------------
----------------------------------------------------------------
'''


class Homepage(Screen):
	
	def start_test(self):
		# записываем введённые данные в БД
		name = self.ids.w_firstname.text
		last_name = self.ids.w_lastname.text
		grade = self.ids.w_class.text
		checker_input = False

		if name != last_name and name != grade and last_name != grade and name.isalpha() and last_name.isalpha():
			checker_input = True
		else:
			if name == 'admin' and last_name == '' and grade == '':
				checker_input = True


		if checker_input:

			conn = sqlite3.connect(DB_PATH)
			cur = conn.cursor()

			# начало теста - создаём уникальную таблицу с ответами ученика

			localip = 'z' + str(socket.gethostname()).replace('-', 'z').replace('.', 'z') # на всякий str, если вдруг в другом формате будет

			CREATE_CASH_TABLE = '''CREATE TABLE {} (
					id INTEGER PRIMARY KEY,
					answer TEXT
				);
			'''.format(localip)

			cur.execute(CREATE_CASH_TABLE)

			cur.execute('INSERT INTO {} (answer) VALUES (?), (?), (?)'.format(localip), (name, 'admin' if last_name == '' else last_name, grade))
			print('Bio has writted.')
			conn.commit()
			conn.close()

			print('[+] [KIVY] Test started.')

			self.manager.transition = SlideTransition(direction='right')
			self.manager.current = 'starttest'
		
		else:

			print('[!] [Error] The bio is repeated.')
			self.ids.w_firstname.text = ''
			self.ids.w_lastname.text = ''
			self.ids.w_class.text = ''
			self.ids.w_firstname.hint_text = 'Ошибка ввода.'
			self.ids.w_firstname.hint_text_color = [1, 0, 0, 0.5]

			print(name, last_name, grade, sep=' ')


class Starttest(Screen):
	data = loadingtest.loading_test()
	index = 0
	# data format: [question, question,]
	
	def __init__(self, **kwargs):
		super(Starttest, self).__init__(**kwargs)
		self.build()


	def on_text(self, instance, value):
		print('The widget', instance, 'have:', value)


	def build(self):
		# условие задачи
		box_for_text = BoxLayout(orientation='vertical', size_hint=[1, 1])
		self.question = Label(text=self.data[0].replace('\\n', '\n\n').replace('\\u202f', '').replace('\\xa0', '\n'), font_size=24, size_hint=[1, 1], pos_hint={'center_x':0.5}, halign='center', valign='center')
		box_for_text.add_widget(self.question)
		self.question.bind(
									width=lambda *x: self.question.setter('text_size')(self.question, (self.question.width, None)),
									texture_size=lambda *x: self.question.setter('height')(self.question, self.question.texture_size[1])
									)
		# поле для ответа
		self.answer_input = TextInput(font_size=24, size_hint=[1, None], size=[300, 50], pos_hint={'center_x':1, 'bottom':0.9}, halign='center', multiline=False)
		apply_btn = Button(text='Ответить', on_press=self.answer, size_hint=[None, None], size=[100, 50], pos_hint={'right':1, 'bottom':0.9})
		
		answer_l = BoxLayout(orientation='horizontal', size_hint=[1, 0.3])
		answer_l.add_widget(self.answer_input)
		answer_l.add_widget(apply_btn)
		self.add_widget(box_for_text)
		self.add_widget(answer_l)


	def answer(self, event):
		self.writing_answeres(self.answer_input.text)
		self.index += 1
		try:
			self.question.text = self.data[self.index].replace('\\n', '\n\n')
			self.answer_input.text = ''
		except IndexError:
			self.manager.transition = SlideTransition(direction='right')
			self.manager.current = 'statistics'


	def writing_answeres(self, answ):

		localip = 'z' + str(socket.gethostname()).replace('-', 'z').replace('.', 'z')

		# запись ответа в базу данных чтобы потом проверять их
		conn = sqlite3.connect(DB_PATH)
		cur = conn.cursor()
		cur.execute("INSERT OR IGNORE INTO {} (answer) VALUES ('{}')".format(localip, answ))
		conn.commit()
		print('[+] [SQL Controller] Response added.')
		conn.close()


class Statistics(Screen):

	stroke = StringProperty()

	def on_pre_enter(self):
		self.data = loadingtest.counting_the_result()
		self.grade = str(self.data['grade'])
		self.procent = str(self.data['procent'])+'%'
		self.quantity_questions = str(self.data['quantity_questions'])
		self.noca = str(self.data['noca']) # number_of_correct_answers
		self.incoorects_label = str(self.data['incorrect_questions_with_answers'])

		info = '-'*10+f'\nОценка за тест: {self.grade};\nПроцент ответа: {self.procent};\nПравильных ответов: {self.noca}/{self.quantity_questions}\n'+ '-'*10 +f'\n\nРазбор нерешённых задач:\n\n{self.incoorects_label}'

		self.stroke = info



'''
----------------------------------------------------------------
------------------  построение приложения ----------------------
----------------------------------------------------------------
'''

class StudentApp(App):
	def build(self):

		manager = ScreenManager()
		manager.add_widget(Homepage(name='homepage'))
		manager.add_widget(Starttest(name='starttest'))
		manager.add_widget(Statistics(name='statistics'))

		return manager


# декоратор, очистка после завершения работы программы
@atexit.register
def clear_cache():

	try:
		conn = sqlite3.connect(DB_PATH)
		cur = conn.cursor()

		tb_name = 'z' + str(socket.gethostname()).replace('-', 'z').replace('.', 'z')

		cur.execute(f'DROP TABLE {tb_name}')
		print(f'Table "{tb_name}" is dropped.')
		conn.commit()
		conn.close()
	except sqlite3.Error as er:
		if 'no such table' in er.args[0]:
			print('No such table. Closing the programm.')
		else:
			print("Exception is: ", er.args[0])


if __name__ == "__main__":
	StudentApp().run()

