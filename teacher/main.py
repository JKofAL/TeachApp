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

Config.set('graphics', 'width', '1420')
Config.set('graphics', 'height', '880')
Config.set('graphics', 'resizable', False) # делаем окно фиксированным

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


from ctypes import windll, c_int64
windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))


'''
----------------------------------------------------------------
-------------------------  widgets -------------------------
----------------------------------------------------------------
'''


class Homepage(Screen):

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


class ChooseTest(Popup):

	def tb_list(self):

		tbs = get_tbs()

		for tb in tbs:
			btn = Button(text=tb, size_hint=(.5, None), height=50)
			self.ids['ch_tb'].add_widget(btn)


class CreateTest(Popup):

	def go_create(self):
		popup = Popup(title='Создание.', size_hint=(None, None), size=(1000, 600), content=Label(text='asd'))
		popup.open()


class CreateScreen(Screen):
	pass


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
		manager.add_widget(CreateScreen(name='create_screen'))
					
		return manager


	def on_start(self):
		MyPopup().open()


if __name__ == "__main__":
	TeachApp().run()
