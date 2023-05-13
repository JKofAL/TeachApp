<!-- New doc for TeachApp -->

![TeachApp](https://sun9-36.userapi.com/impg/yfixA-Ss_m0TbqKT5W2I8etzN6KfFRx6jxaW5Q/Ympi_rJL52k.jpg?size=976x183&quality=96&sign=c3e436ed1960e92d229bfc2efbd54899&type=album, "TeachApp")

# TeachApp

## Содержание

- [Описание](#описание)
- [Использование](#использование)
	- [Teacher](#teacher)
		- [Таблица результатов](#таблица-результатов)
	- [Student](#student)

## Описание

**TeachApp** - desktop приложение, предназначенное для тестирования в любых учереждениях, где присутствуют стационарные компьютеры или локальная сеть компьютеров с сетевым диском.

Этот проект вдохновлён приложением [MyTest](https://mytest.klyaksa.net/wiki/Заглавная_страница).

![MyTest](https://1.bp.blogspot.com/-ugIQbWrSQ7A/UOf5-plJk4I/AAAAAAAAAXA/Kn_GsfUkEZU/s1600/Mtx101.png, "MyTest")

> В данный момент MyTest используется в образовательных учреждениях в целях проведения тестов.

## Использование

Чтобы воспользоваться **BETA** версией приложения, установите файлы проекта.
Для этого:

- Найдите и скачайте zip архив [TeachApp.zip](https://github.com/JKofAL/TeachApp/blob/master/TeachApp.zip);
	- Распакуйте архив;
- Пройдите по директории `teacher` и откройте файл `Teacher.exe`;
	- При входе введите пароль **123**;
- Вы вошли в приложение учителя, *функционал которого будет в пункте [Teacher](#teacher)*;
- Для того, чтобы зайти в приложение ученика, зайдите в приложение `project_folder/student/Student.exe`;
	- функционал [Student](#student) приложения.

***Все файлы должны быть разархивированы и находиться в тех папках, в которых они находятся в zip архиве. Не меняйте расположение файлов, чтобы приложение функционировало.***

### Teacher

В интерфейсе учителя на данный момент доступен следующий функционал:

* [Таблица результатов](#таблица-результатов)
* Кнопки меню на левой панели:
	* Выбор теста среди созданных
	* Создание своего теста

![Использование GUI](https://github.com/JKofAL/TeachApp/blob/master/git_doc/teacher_gui.gif)

#### Таблица результатов

В самой таблице отображаются результаты из таблицы teachapp.db. При необходимости (*в случае завершения прохождения теста во время пользования приложением*) можно обновить приложение, нажав на соответствующую кнопку в панели управления.

<img src='https://github.com/JKofAL/TeachApp/blob/master/git_doc/repeat_tb.gif' width="250", height="250"/>

Также присутствует кнопка импорта оценок в Excel файл, который можно открыть прямо в приложении.

### Student

![Использование GUI](https://github.com/JKofAL/TeachApp/blob/master/git_doc/student_gui.gif)