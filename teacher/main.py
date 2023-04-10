print('''
████████╗███████╗░█████╗░░█████╗░██╗░░██╗░█████╗░██████╗░██████╗░
╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗
░░░██║░░░█████╗░░███████║██║░░╚═╝███████║███████║██████╔╝██████╔╝
░░░██║░░░██╔══╝░░██╔══██║██║░░██╗██╔══██║██╔══██║██╔═══╝░██╔═══╝░
░░░██║░░░███████╗██║░░██║╚█████╔╝██║░░██║██║░░██║██║░░░░░██║░░░░░
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░
''')
import kivy

from kivy.config import Config

Config.set('graphics', 'resizable', False) # делаем окно фиксированным

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

from kivy.core.window import Window

backg = kivy.utils.get_color_from_hex('#363636')
Window.clearcolor = (backg[0], backg[1], backg[2], 1)

from kivy.properties import (
	ObjectProperty, 
	StringProperty,
	ListProperty,
	NumericProperty,
)

from functools import partial
import pandas as pd
import xlsxwriter

import time
import os

from DB_CONTROL import *


'''
----------------------------------------------------------------
-------------------------  widgets -------------------------
----------------------------------------------------------------
'''


class Homepage(Screen):

	page = NumericProperty(1)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		std_r = get_std_res()
		self.tb = self.ids['table_students']

		for row in std_r:
			x = 0
			for cell in row:
				x += 1
				if x == 4:
					self.tb.add_widget(Label(text=str(cell), font_size=12, height=30, size_hint_y=None, color=(0, 1, 0, 1) if str(cell) == '5' or str(cell) == '4' else (1, 0, 0, 1)))
				else:
					self.tb.add_widget(Label(text=str(cell), font_size=12, height=30, size_hint_y=None))


	def repeat_tb(self):
		std_r = get_std_res()
		th = ['Тест', 'Имя Фамилия', 'Класс', 'Оценка']
		cells = list()

		for child in self.tb.children:
			if child.text not in th:
				cells.append(child)

		for elem in cells:
			self.tb.remove_widget(elem)

		for row in std_r:
			x = 0
			for cell in row:
				x += 1
				if x == 4:
					self.tb.add_widget(Label(text=str(cell), font_size=12, height=30, size_hint_y=None, color=(0, 1, 0, 1) if str(cell) == '5' or str(cell) == '4' else (1, 0, 0, 1)))
				else:
					self.tb.add_widget(Label(text=str(cell), font_size=12, height=30, size_hint_y=None)) 


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


	def go_page(self):
		print('go')


class Createtest(Screen):
	
	def go_back(self):
		self.manager.transition = SlideTransition(direction='left')
		self.manager.current = 'homepage'


	def upload(self):
		pass # at' voobshe


# проверка на учителя
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


class ExcelPopup(Popup):

	def go_xlsx(self):
		os.system('D:\\BETA\\grades.xlsx')


'''
--------------------------------------------------
-----------  построение приложения ---------------
--------------------------------------------------
'''


class TeachApp(App):


	def build(self):

		self.title = 'Учитель'
		manager = ScreenManager()
						
		manager.add_widget(Homepage(name='homepage'))
		manager.add_widget(Createtest(name='create_test'))
					
		return manager


	def on_start(self):
		MyPopup().open()


if __name__ == "__main__":
	TeachApp().run()
