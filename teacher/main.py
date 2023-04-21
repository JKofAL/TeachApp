print('''
████████╗███████╗░█████╗░░█████╗░██╗░░██╗░█████╗░██████╗░██████╗░
╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗
░░░██║░░░█████╗░░███████║██║░░╚═╝███████║███████║██████╔╝██████╔╝
░░░██║░░░██╔══╝░░██╔══██║██║░░██╗██╔══██║██╔══██║██╔═══╝░██╔═══╝░
░░░██║░░░███████╗██║░░██║╚█████╔╝██║░░██║██║░░██║██║░░░░░██║░░░░░
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░
''')

__version__ = '2.0'

import kivy

from kivy.config import Config

# write config commands here for accept 
# changes before compiling the applications 
Config.set('graphics', 'width', '1420')
Config.set('graphics', 'height', '880')
Config.set('graphics', 'resizable', False) # fixed window
Config.set('graphics', 'multisamples', '0') # correctly OpenGL version

from kivy.app import App
from kivy.uix.screenmanager import (
	ScreenManager,
	Screen,
	SlideTransition
)

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *

from kivy.properties import (
	ObjectProperty, 
	StringProperty,
	ListProperty,
	NumericProperty,
)

from functools import partial
import pandas as pd
import xlsxwriter
from configparser import ConfigParser

import time
import os
import atexit
from pathlib import Path

from DB_CONTROL import *

from ctypes import windll, c_int64

backg = kivy.utils.get_color_from_hex('#363636')
Window.clearcolor = (backg[0], backg[1], backg[2], 1)

windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))


'''
----------------------------------------------------------------
-------------------------  widgets -------------------------
----------------------------------------------------------------
'''


class Homepage(Screen):
	"""
	
	######################################################
	## HOME SCREEN WITH ALL INFO ABOUT STUDENTS AND etc ##
	######################################################

	######################################################
	######################################################
	
	"""

	page = NumericProperty(1)
	tests = ListProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		std_r = get_std_res()
		self.tb = self.ids['table_students']

		for row in std_r:
			x = 0
			for cell in row:
				x += 1

				if x == 4:
					box = BoxLayout(size_hint_y=None, height=50, padding=20)
					label = Label(
						text=str(cell), 
						height=30,
						size_hint_y=None,
						color=(0, 1, 0, 1) if str(cell) == '5' or str(cell) == '4' else (1, 0, 0, 1))
					box.add_widget(label)
					self.tb.add_widget(box)

				else:
					box = BoxLayout(size_hint_y=None, height=50, padding=20)
					label = Label(text=str(cell), height=30, size_hint_y=None)
					box.add_widget(label)
					self.tb.add_widget(box)


	def repeat_tb(self):
		std_r = get_std_res()
		th = ['Тест', 'Имя Фамилия', 'Класс', 'Оценка']
		cells = list()

		for child in self.tb.children:
			if child.children[0].text not in th:
				cells.append(child)

		for elem in cells:
			self.tb.remove_widget(elem)

		for row in std_r:
			x = 0
			for cell in row:
				x += 1
				
				if x == 4:
					box = BoxLayout(size_hint_y=None, height=50, padding=20)
					label = Label(
						text=str(cell),
						height=30,
						size_hint_y=None,
						color=(0, 1, 0, 1) if str(cell) == '5' or str(cell) == '4' else (1, 0, 0, 1))
					box.add_widget(label)
					self.tb.add_widget(box)
				
				else:
					box = BoxLayout(size_hint_y=None, height=50, padding=20)
					label = Label(text=str(cell), height=30, size_hint_y=None)
					box.add_widget(label)
					self.tb.add_widget(box)

		print('Table is upadted.')


	def write_xlsx(self):
		std_r = get_std_res()
		content = {'Предмет': [], 'Ф. Имя': [], 'Класс': [], 'Оценка': []}
		for el in std_r:
			content['Предмет'].append(el[0])
			content['Ф. Имя'].append(el[1])
			content['Класс'].append(el[2])
			content['Оценка'].append(el[3])

		writer = pd.ExcelWriter('grades.xlsx', engine='xlsxwriter')
		df = pd.DataFrame(content)
		df.to_excel(writer, sheet_name='Оценки')
		writer.save()


######################################################
## password authentification
######################################################
class MyPopup(Popup):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_key_down=self._on_keys_down)


	def check(self):
		password = '123'
		if self.ids['password_input'].text == password:
			self.dismiss()
		else:
			self.ids['password_input'].text = ''
			self.ids['password_input'].hint_text = 'incorrect'
			self.ids['password_input'].hint_text_color = [1, 0, 0, 0.5]
			self.ids['password_input'].focus = True
	

	def _on_keys_down(self, instance, keyboard, keycode, text, modifiers):
		if self.ids['password_input'].focus and self.ids['password_input'].text != '' and keycode == 40:
			self.check()


######################################################
## grab grades popup
## => write grades to xlsx sheet
## => open excel file
######################################################
class ExcelPopup(Popup):

	def go_xlsx(self):
		os.system('D:\\BETA\\grades.xlsx')


######################################################
## choosing test
## get all tebles from db
## when user choose test, changed test_controller.ini
######################################################
class ChooseTest(Popup):

	# Function for getting settings from a configuration file
	def config_settings(self):

		# Getting the path to the current file
		path = Path(__file__)
		# Getting the path to the root directory of the project
		ROOT_DIR = path.parent.parent.absolute()
		# We form the path to the configuration file, which is located in the root of the project
		config_path = os.path.join(ROOT_DIR, "test_controller.ini")

		# Creating a configuration file parser object
		config = ConfigParser()
		# Reading the configuration file
		config.read(config_path)

		# We return the parser object and the path to the configuration file
		return config, config_path


	def test_name(self):

		config, config_path = self.config_settings()

		self.ids['choosed_test'].text = config.get('CONFIG', 'test_name')


	def tb_list(self):

		tbs = get_tbs()

		for tb in tbs:
			btn = Button(text=tb, size_hint=(.5, None), height=50, on_release=self.apply_choose)
			self.ids['ch_tb'].add_widget(btn)


	def apply_choose(self, instance):

		config, config_path = self.config_settings()

		config.set('CONFIG', 'test_name', instance.text)

		with open(config_path, 'w') as cfg_file:
			config.write(cfg_file)

		self.ids['choosed_test'].text = instance.text

		print('[+] [INI] Test choosed successfully.')


class CreateTest(Popup):
	"""

	Creating test or choosing test popup

	#########################
	## CREATING TEST POPUP ##
	#########################
	
	## GUI DOC ##

	Global form for creating test.
	:: INPUT form for name of test. Name of test shouldn't be with space and another special symbols
	for error bypass.
	:: INPUT form for question (number of question writed on Label left to name of test inp.
	:: INPUT form for right answer.
	:: INPUT form for ball for question. This ball used on scoring points after passing the test.
	:: BUTTON next/back question. Commit changes on actually question and change question.
	If the question with a specified id existed, all input text (without name input)
	change text to the input text with this id.
	:: BUTTON commit changes. This button created a table in db with specified name.

	
	## SCRIPT DOC ##

	:: go_create <-> global def with form for create test (functional: supra)
	:: all remaining functions needed for go_create (except open_xlsx, on_open, on_dismiss)

	#########################
	#########################

	#########################
	## GET TEST FROM EXCEL ##
	#########################

	## GUI DOC ##

	YOU SHOULD HAVE READY EXCEL FILE WITH TEST (from for this file: COMMING SOON)
	Write name of file in TextInput and press enter.
	Since this functionaly block not finalized, on pre_enter show popup with info-block (COMMING SOON)

	## SRTIPT DOC ##

	:: open_xlsx <-> COMMING SOON (show popup)

	#########################
	#########################

	"""
	page = '1'

	def go_create(self):
		######################################################
		## create content for popup form
		######################################################
		global_ = GridLayout(cols=1)

		#######################################################
		## text input for question
		## text input for right answer
		## text input for ball
		## button for pageback, pagenext
		#######################################################

		#######################################################
		## navigate layout
		#######################################################
		navigate = GridLayout(cols=4, orientation='rl-tb', size_hint=(1, .1), spacing=10, padding=10, rows=1)
		nav_btn_text = ['Следующий', 'Предыдущий']
		for btn_text in nav_btn_text:
			nav_btn = Button(
				text=btn_text,
				size_hint=(None, None),
				size=(250, 50),
				on_release=self.next_page if btn_text == nav_btn_text[0] else self.back_page)
			navigate.add_widget(nav_btn)
		self.name_test = TextInput(
			size_hint=(None, None),
			size=(200, 50),
			text='Test_name',
			hint_text='Имя теста',
			font_size=32,
			text_language='en_US',
			multiline=False
			)
		self.name_test.bind(text = self.check_name)
		self.page_ = Label(text='Вопрос: '+self.page, font_size=22)
		navigate.add_widget(self.name_test)
		navigate.add_widget(self.page_)
		#######################################################
		## formatting test layout
		## make a layout
		## Global Gridlayout:
		## :: BoxLayout -- large size
		## :: :: TextInput for question
		## ::::::::::::::::::::::::::::
		## :: BoxLayout -- small size
		## :: :: GridLayout
		## :: :: :: TextInput for right answer
		## :: :: :: TextInput for ball for question
		#######################################################
		## global form for formatting
		#######################################################
		form = GridLayout(cols=1, size_hint=(1, .8))
		#######################################################
		## question input
		#######################################################
		box_for_question = BoxLayout(size_hint=(1, .7))
		self.question = TextInput(
			hint_text='Введите вопрос.',
			font_size=26,
			halign='center')
		box_for_question.add_widget(self.question)
		#######################################################
		## right answer and ball for question
		#######################################################
		box_for_doptxtinp = BoxLayout(size_hint=(1, None), height=50)
		dop_input = GridLayout(cols=2,
			orientation='rl-tb',
			spacing=10,
			size_hint_y=None,
			height=50,
			pos_hint={'top': 1})
		self.right_answer = TextInput(hint_text='Правильный ответ.',
			size_hint=(None, 1),
			size=(300, 50),
			font_size=32,
			multiline=False)
		self.ball = TextInput(hint_text='Кол-во баллов.',
			size_hint=(None, 1),
			size=(300, 50),
			font_size=32,
			multiline=False)
		dop_input.add_widget(self.ball)
		dop_input.add_widget(self.right_answer)
		box_for_doptxtinp.add_widget(dop_input)
		#######################################################
		## collect the resulting form
		#######################################################
		form.add_widget(box_for_question)
		form.add_widget(box_for_doptxtinp)
		#######################################################
		## create apply button
		#######################################################
		box_for_apply = BoxLayout(size_hint=(1, None), height=50)
		anchor_btn = AnchorLayout(anchor_x='right')
		apply_btn = Button(
			text='Создать тест',
			size_hint=(None, 1),
			width=300,
			on_release=self.apply_test)
		anchor_btn.add_widget(apply_btn)
		box_for_apply.add_widget(anchor_btn)
		#######################################################
		## add all layouts to global form
		#######################################################
		global_.add_widget(navigate)
		global_.add_widget(form)
		global_.add_widget(box_for_apply)

		#######################################################
		## create popup form with resulting content
		#######################################################
		self.g_popup = Popup(
			title='Создание.',
			title_size=32,
			size_hint=(None, None),
			size=(1000, Window.height),
			content=global_,
			on_dismiss = self.creator_on_dismiss)
		self.g_popup.open()


	def check_name(self, *args):
		try:
			key = args[1]
			if len(key) == 1:
				if key.isdigit():
					self.name_test.text = ''
			else:
				forbidden_char = list('[]{}-=+!@#$%^&*()"№;:?`~\\|/.,'+"' ")
				if key[-1] in forbidden_char:
					self.name_test.text = self.name_test.text.replace(key[-1], '')
		except ValueError:
			pass
		except Exception as e:
			pass


	def next_page(self, event):
		if self.question.text != '':
			self.write_question()
			self.page = str(int(self.page)+1)
			next_page_question = self.get_question()
			self.page_.text = 'Вопрос: '+self.page
			checker = True if next_page_question != [] else False
			self.question.text = 'Новый вопрос.' if not checker else next_page_question[0][1]
			self.right_answer.text = '' if not checker else next_page_question[0][2]
			self.ball.text = '' if not checker else next_page_question[0][3]


	def back_page(self, event):
		if self.question.text != '':
			self.write_question()
		self.page = '1' if self.page == '1' else str(int(self.page)-1)
		back_page_question = self.get_question()
		self.page_.text = 'Вопрос: '+self.page
		if back_page_question != []:
			self.question.text = back_page_question[0][1]
			self.right_answer.text = back_page_question[0][2]
			self.ball.text = back_page_question[0][3]
		else:
			self.question.text = ''
			self.right_answer.text = ''
			self.ball.text = ''

	def get_question(self):
		cmd = 'SELECT * FROM creator_test WHERE id = ?'
		return go_cmd_ct(cmd, 'select', self.page)


	def write_question(self):
		cmd = 'UPDATE creator_test SET question = ?, right_answer = ?, ball = ? WHERE id = ?'
		snd_cmd = 'INSERT INTO creator_test VALUES (?, ?, ?, ?)'
		return go_cmd_ct(cmd, 'insert', self.question.text, self.right_answer.text, self.ball.text, self.page, snd_cmd)


	def on_dismiss(self):
		cmd = 'DROP TABLE IF EXISTS creator_test'
		go_cmd_ct(cmd, 'drop')

	def creator_on_dismiss(self, event):
		cmd = 'DROP TABLE IF EXISTS creator_test'
		go_cmd_ct(cmd, 'drop')


	def on_open(self):
		cmd = '''CREATE TABLE IF NOT EXISTS creator_test (
					id INTEGER PRIMARY KEY,
					question TEXT,
					right_answer TEXT,
					ball TEXT
					);'''
		go_cmd_ct(cmd, 'create')


	def clear_rabbish(self):
		cmd = 'DELETE FROM creator_test WHERE question = ?'
		go_cmd_ct(cmd, 'delete')


	def apply_test(self, event):

		self.write_question()

		content = GridLayout(cols=1)

		self.confirm = Popup(title='Подтверждение.', content=content, title_size=32, size_hint=(.6, .5))
		
		box_txt = BoxLayout(size_hint=(1, .6))
		label = Label(text='Вы уверены, что хотите продолжить?', valign='center')
		box_txt.add_widget(label)

		btn_grid = GridLayout(cols=2, size_hint=(1, .4), spacing=50, padding=50)
		btn_grid.add_widget(Button(
			text='Исправить.', on_release=lambda *args: self.confirm.dismiss()))
		btn_grid.add_widget(Button(
			text='Завершить.', on_release=self.confirmation))

		content.add_widget(box_txt)
		content.add_widget(btn_grid)


		self.confirm.open()


	def confirmation(self, event):
		self.confirm.dismiss()
		self.write_test()
		self.g_popup.dismiss()


	def write_test(self):
		data = get_created_test()
		#######################################################
		## [(1, '5 + 5', '10', '10')]
		## i'll use id for type.
		## Later, i'll add input text for catalog
		#######################################################
		conn, cur = conn_open()
		#######################################################
		## write sqlite cmd's here, cause i'm lazy
		#######################################################
		cmd = '''
		CREATE TABLE {} (
			id INTEGER PRIMARY KEY,
			type varchar(20),
			question varchar,
			right_answer varchar,
			ball INTEGER
			)'''.format(self.name_test.text)
		try:
			cur.execute(cmd)
			conn.commit()
			print('success')
		except sqlite3.Error as e:
			print(e, 'creating db')
		cmd = '''
		INSERT INTO {} VALUES (?, ?, ?, ?, ?)'''.format(self.name_test.text)
		try:
			for row in data:
				cur.execute(cmd, (None, row[0], row[1], row[2], int(row[3])))
				conn.commit()
			print('data writted success')
		except sqlite3.Error as e:
			print(e, 'writing data')


	def go_xlsx(self, file):
		#######################################################
		## comming soon popup
		#######################################################
		popup = Popup(
			title='',
			content=Label(text='Comming soon'),
			size_hint=(.5, .2),
			on_dismiss=self.clear_text_xlsx)
		popup.open()


	def clear_text_xlsx(self, event):
		self.ids.xlsx_writer.text = ''


#######################################################
## decorators
#######################################################
@atexit.register
def closing_the_programm():
	"""

	##############################
	## CLOSING THE PROGRAMM DOC ##
	##############################

	Decorator. Executed when programm closed.

	:: clear_cache_tb :: func :: needed for deletes tables that 
	::                ::      :: may cause an error in the script.
	
	##############################
	##############################

	"""
	clear_cache_tb()


'''
--------------------------------------------------
----------- building an application --------------
--------------------------------------------------
'''


class TeachApp(App):
	"""

	#############################
	## BUILDING AN APPLICATION ##
	#############################
	
	Launching the application with the assembled widgets

	#############################
	#############################

	"""


	def build(self):

		self.title = 'Учитель'
		manager = ScreenManager()
			
		manager.add_widget(Homepage(name='homepage'))
					
		return manager


	def on_start(self):
		MyPopup().open()


if __name__ == "__main__":
	TeachApp().run()
