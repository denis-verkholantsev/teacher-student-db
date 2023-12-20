# Описание
## Наименование
**teacher-student-db** - система управления для взаимодействия преподавателя и студента в контексте образования.
## Предметная область
Образование. База данных позволяет хранить личную информацию преподавателей и студентов, сотавлять расписание, создавать домашние задания и упражения, прикладывать решения к упражнениям и загружать все необходимые файлы.
# Данные
## Пользователь
Подразделяется на преподавателей и студентов. 
* При создании необходимо указать уникальные email, имя пользователя и пароль.
* Имя, фамилия, дата рождения необязательны.
* Преподаватель имеет возможность прикреплять к себе студентов из уже существующих.
## Задание
* Время создания - время при создании задания на сервере
* Время обновления меняется при каждом изменении объекта
* Возможно прикреплять файлы

Подразделяется на упражнение, домашнее задание и решение упражнения.

#### Упражнение

* Наименование, описание и автор опциональны.
* Есть возможность прикрепить к существующему домашнему заданию

#### Домашнее задание

* Обязательно имеет наименование
* Описание, дедлайн и автор опциональны
* Есть возможность прикрепить существующие упражнения
* Можно адресовать определенным студентам
* Имеет статус (по умолчанию:```not started```)

#### Решение

* Описание опционально
* Имеет статус (по умолчанию: ```not approved```)
* Обязательно имеет автора - студента и упражнение, к которому относится
## Файл 
* Обязательно имеет название
* Содержание файла
* Обязательно относится к какому-либо заданию

## Событие
* Обязательно имеет название и автора - преподавателя
* Описание необязательно
* Может быть назначено студентам
* Обязательно имеет время начала и конца

# Ограничение целостности для данных
* имя пользователя уникально, не более 30 символов
* email пользователя уникальный, не более 320 символов
* Пароль пользователя не более 16 символов
* Имя файла не более 256 символов

# Пользовательские роли
``` Преподаватель ```
* составляет расписание занятий
* создает упражнения и прикладывает необходимые файлы
* составляет домашние задания из созданных упражнений, отслеживает их выполнение, назначает дедлайн и прикладывает необходимые файлы
* отслеживает историю решений упражнения студента
* прикрепляет студентов к себе из уже существующих

``` Студент ```
* видит список преподавателей, домашних заданий и дедлайны
* создает решения к упражнениям из домашнего задания и прикладывает файлы к ним
* отслеживает историю решений упражнений

# API
* взаимодействие с базой данной данных может быть организовано посредством утилиты psql, поставляемой вместе с СУБД PostgreSQL (после инициализации предоставленной схемы)
* взаимодействие при помощи python-скриптов, используя библиотеку SQLAlchemy

# СУБД
PostgreSQL
# Cхема базы данных
![er](https://github.com/denis-verkholantsev/teacher-student-db/blob/main/er_diagram.pdf)
# Язык программирования
Python
# Технологии разработки
Docker, SQLAlchemy

# Как использовать
Предварительно убедитесь, что у вас установлены:
* [Python>=3.10](https://www.python.org/)
* [Docker](https://www.docker.com/)
* Склонируйте репозиторий \
```git clone https://github.com/denis-verkholantsev/teacher-student-db```
* Перейдя в директорию репозитория, создайте виртуальное окружение с Python3.10 любым
удобным способом (virtualenv, poetry, pyenv) и активируйте окружение
```
python3 -m venv .venv
source .venv/bin/activate
```
* Установите зависимости любым удобным способом(например, используя [pip](https://pip.pypa.io/en/stable/))
```
pip install -r requirements.txt
```
* Запустите локальный экземпляр Postgres в Docker
```
docker-compose up
```
* Инициализируйте базу данных
```
python3 main.py
```
# Тестирование
Запуск тестов на проверку создания сущностей и добавлению различных связей
```
python3 db/test.py
```

  
=======
# Описание
## Наименование
**teacher-student-db** - система управления для взаимодействия преподавателя и студента в контексте образования.
## Предметная область
Образование. База данных позволяет хранить личную информацию преподавателей и студентов, сотавлять расписание, создавать домашние задания и упражения, прикладывать решения к упражнениям и загружать все необходимые файлы.
# Данные
## Пользователь
Подразделяется на преподавателей и студентов. 
* При создании необходимо указать уникальные email, имя пользователя и пароль.
* Имя, фамилия, дата рождения необязательны.
* Преподаватель имеет возможность прикреплять к себе студентов из уже существующих.
## Задание
* Время создания - время при создании задания на сервере
* Время обновления меняется при каждом изменении объекта
* Возможно прикреплять файлы

Подразделяется на упражнение, домашнее задание и решение упражнения.

#### Упражнение

* Наименование, описание и автор опциональны.
* Есть возможность прикрепить к существующему домашнему заданию

#### Домашнее задание

* Обязательно имеет наименование
* Описание, дедлайн и автор опциональны
* Есть возможность прикрепить существующие упражнения
* Можно адресовать определенным студентам
* Имеет статус (по умолчанию:```not started```)

#### Решение

* Описание опционально
* Имеет статус (по умолчанию: ```not approved```)
* Обязательно имеет автора - студента и упражнение, к которому относится
## Файл 
* Обязательно имеет название
* Содержание файла
* Обязательно относится к какому-либо заданию

## Событие
* Обязательно имеет название и автора - преподавателя
* Описание необязательно
* Может быть назначено студентам
* Обязательно имеет время начала и конца

# Ограничение целостности для данных
* имя пользователя уникально, не более 30 символов
* email пользователя уникальный, не более 320 символов
* Пароль пользователя не более 16 символов
* Имя файла не более 256 символов

# Пользовательские роли
``` Преподаватель ```
* составляет расписание занятий
* создает упражнения и прикладывает необходимые файлы
* составляет домашние задания из созданных упражнений, отслеживает их выполнение, назначает дедлайн и прикладывает необходимые файлы
* отслеживает историю решений упражнения студента
* прикрепляет студентов к себе из уже существующих

``` Студент ```
* видит список преподавателей, домашних заданий и дедлайны
* создает решения к упражнениям из домашнего задания и прикладывает файлы к ним
* отслеживает историю решений упражнений

# API
* взаимодействие с базой данной данных может быть организовано посредством утилиты psql, поставляемой вместе с СУБД PostgreSQL (после инициализации предоставленной схемы)
* взаимодействие при помощи python-скриптов, используя библиотеку SQLAlchemy

# СУБД
PostgreSQL
# Cхема базы данных
![er](https://github.com/denis-verkholantsev/teacher-student-db/blob/main/er_diagram.png)
# Язык программирования
Python
# Технологии разработки
Docker, SQLAlchemy

# Как использовать
Предварительно убедитесь, что у вас установлены:
* [Python>=3.10](https://www.python.org/)
* [Docker](https://www.docker.com/)
* Склонируйте репозиторий \
```git clone https://github.com/denis-verkholantsev/teacher-student-db```
* Перейдя в директорию репозитория, создайте виртуальное окружение с Python3.10 любым
удобным способом (virtualenv, poetry, pyenv) и активируйте окружение
```
python3 -m venv .venv
source .venv/bin/activate
```
* Установите зависимости любым удобным способом(например, используя [pip](https://pip.pypa.io/en/stable/))
```
pip install -r requirements.txt
```
* Запустите локальный экземпляр Postgres в Docker
```
docker-compose up
```
* Инициализируйте базу данных
```
python3 main.py
```
# Тестирование
Запуск тестов на проверку создания сущностей и добавлению различных связей
```
python3 db/test.py
```

  
>>>>>>> 2b2c99398d0e81ab23b622628e5968c4eecf31ee
