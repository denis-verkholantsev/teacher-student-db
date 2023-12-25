# Описание
## Наименование
**teacher-student-db** - система управления для взаимодействия преподавателя и студента в контексте образования.
## Предметная область
Образование. Сервис помогает выстравать коммуникацию между преподавателем и студентами, то есть: составлять расписание, создавать упражнения, создавать домашние задания и отправлять сразу множеству студентов, прикладывать к упражнениям и домашним заданиям файлы, оценивать решения студентов.
# Данные
## Пользователь
При регистрации необходимо указать:
* email
* username
* пароль
#### Дополнительная информация
Имя, фамилия, дата рождения для удобства взаимодействия.

Логин производится по email и паролю
## Файл
Пользователь может загружать всеразличные файлы в систему.

## Упражнение
Преподаватель может создавать упражнения, которые содержат название, описание, прикладывать к ним ранее загруженные файлы.
Система хранит время создания и последнего обновления упражнения.

## Домашнее задание
Преподаватель может создавать домашние задание, которые хранят название, описание, время и дату дедлайна, прикладывать к ним загруженные файлы и ранее созданные упражнение.

Система хранит время создания и последнего обновления домашнего задания.

Домашнее задание можно назначить студенту, который прежде был доабвлен в ```друзья```.

## Решение
Студенты в качестве решения предлагают его описание и загруженные файлы.

Имеет статус, изначально - ```not approved```. Преподаватель может сменить его на ```approved```

Система хранит время создания и последнего обновления домашнего задания

## Событие
Преподаватель может запланировать событие, указав название, описание, время и дату начала и конца. А также отправить его выбранным студентам.
Таким образом формируется расписание.

# Ограничение целостности для данных
* Имя пользователя уникально и валидно, не менее 3 и не более 30 символов
* email пользователя уникальный и валидный, не более 62 символов
* Пароль пользователя валидный, не менее 8 символов
* Имя и фамилия пользователя не более 50 символов
* Дата рождения не ранее 1900 года и не в будущем
* Имя файла не более 256 символов
* Все названия не более 50 символов, описания не более 500 символов
# Пользовательские роли
``` Преподаватель ```
* составляет расписание занятий
* создает упражнения
* составляет домашние задания из упражнений и назначает студентам, отслеживает их выполнение, назначает дедлайны
* отслеживает историю решений студентов
* ищет студентов по ```username``` и добавляет в ```друзья``` (прикрепляет студентов к себе)

``` Студент ```
* видит список своих преподавателей, домашних заданий и дедлайны
* решает упражнения из домашних заданий
* отслеживает историю своих решений

# API
Описание с помощью OpenAPI(Swagger)

# СУБД
PostgreSQL
# Cхема базы данных

![](https://github.com/denis-verkholantsev/teacher-student-db/blob/main/er_diagram.png)

# Язык программирования
Python (Flask+SQLAlchemy)
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

В директории репозитория зайдите в оболочку
```
flask shell
```
Введите команду
```
db.create_all()
```
* Запустите приложение
```
flask run
```
* Посетите [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/) 
