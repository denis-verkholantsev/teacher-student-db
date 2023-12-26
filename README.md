# Описание
## Наименование
**teacher-student-db** - система управления для взаимодействия преподавателя и студента в контексте образования.
## Предметная область
Образование. Сервис помогает выстравать коммуникацию между преподавателем и студентами, то есть: составлять расписание, создавать упражнения, создавать домашние задания и отправлять сразу множеству студентов, прикладывать к упражнениям и домашним заданиям файлы, решать студентам упражнения из домашних заданий, оценивать решения студентов преподавателем.
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
Пользователь может загружать файлы в систему и просмотривать файлы после загрузки.
Нельзя удалить файл, если с ним связано какое-либо упражнение, домашнее задание или решение.

## Упражнение
Преподаватель может создавать упражнения, которые содержат название, описание, прикладывать к ним ранее загруженные файлы. Имеет возможность просматривать созданные им упражнения, изменять, удалять. При удалении упражнения удаляются все связанные с ним решения студентов. Нельзя удалить, если связано с каким-либо домашним заданием.

Система хранит время создания и последнего обновления упражнения.

## Домашнее задание
Преподаватель может создавать домашние задания, которые хранят название, описание, время и дату дедлайна, прикладывать к ним загруженные файлы и ранее созданные упражнение, имеет возможность просмотра своих домашних заданий, изменения и удаления.

Система хранит время создания и последнего обновления домашнего задания.

Домашнее задание можно назначить студенту, который прежде был добавлен в ```друзья```(прикреплен к преподавателю), он также имеет возможность просматривать назначенные ему домашние задания.

## Решение
Студенты в качестве решения предлагают его описание и загруженные файлы.

Имеет статус, изначально - ```not approved```. При проверке преподаватель может сменить его на ```approved```, но обязательно оставить комменатрий.

Система хранит время создания и последнего обновления решения.

Удаляется при удалении упражнения, к которому было привязано данное решения.

## Событие
Преподаватель может запланировать событие, указав название, описание, время и дату начала и конца. А также отправить его выбранным студентам.
Таким образом формируется расписание.
Событие также можно удалить или изменить.

# Ограничение целостности для данных
* Имя пользователя уникально и валидно(может содержать буквы, цифры и символы ```_```, ```-```), не менее 3 и не более 30 символов
* email пользователя уникальный и валидный, не более 62 символов
* Пароль пользователя валидный (содержит как минимум одну букву, одну цифру и один из специальных символов ```@$!%*?&_```), не менее 8 символов
* Имя и фамилия пользователя не более 50 символов, могут содержать только буквы, ```-``` и ```'```
* Дата рождения не ранее 01.01.1900 и не в будущем
* Имя файла не более 256 символов
* Все названия не более 50 символов, описания не более 500 символов
# Пользовательские роли
``` Преподаватель ```
* ищет студентов по ```username``` и может добавлять их в ```друзья``` (прикреплять студентов к себе)
* составляет расписание занятий и может его просматривать (хранятся события +- 1 год от сегодняшней даты)
* создает упражнения и может их просматривать
* может узнать статус выполнения каждого упражнения из своих домашних заданий
  * не начато - не создано ни одного решения
  * не принято - нет решения со статусом ```approved```
  * принято - есть решение со статусом ``approved```
* составляет домашние задания из упражнений и назначает студентам, отслеживает их выполнение, назначает дедлайны, просматривает свои домашние задания
* может узнать статус домашнего задания для каждого студента, кому она была назначена
  * не начато - не создано ни одного решения к какому-либо упражнению
  * в работе - создано хотя бы одно решение к какому-либо упражнению
  * ожидает проверки - все последние решения каждого упражнения со статусом ``approved``` или без комментариев и со статусом ``not approved```
  * проверено - каждое упражнение имеет решение с комментарием, но не все решения имеют статус ```approved```
  * принято - каждое упражнение имеет решение с комментарием и статусом ```approved```
  * принято с опозданием - каждое упражнение имеет решение с комментарием и статусом ```approved``` и время создания не позже дедлайна
* проверяет решения каждого упражнения своих студентов, обязательно оставляет к ним комментарий и возможно меняет статус решения на ```approved```
* может просматривать историю решений упражнения из домашнего задания по каждому студенту

``` Студент ```
* видит список своих преподавателей, домашних заданий
* может просматривать расписание (хранятся события +- 1 год от сегодняшней даты)
* может узнать статус каждого домашнего задания
  * не начато - не создано ни одного решения к какому-либо упражнению
  * в работе - создано хотя бы одно решение к какому-либо упражнению
  * ожидает проверки - все последние решения каждого упражнения со статусом ``approved``` или без комментариев и со статусом ``not approved```
  * проверено - каждое упражнение имеет решение с комментарием, но не все решения имеют статус ```approved```
  * принято - каждое упражнение имеет решение с комментарием и статусом ```approved```
  * принято с опозданием - каждое упражнение имеет решение с комментарием и статусом ```approved``` и время создания позже дедлайна.
* видит упражнения своих домашних заданий
* может узнать статус выполнения каждого упражнения из своих домашних заданий - не начато, не принято, принято (определяется по статусу решения)
  * не начато - не создано ни одного решения
  * не принято - нет решения со статусом ```approved```
  * принято - есть решения со статусом ```approved```
* может решить упражнение, создав одно решение
* имеет право удалить это решение, если оно еще не было проверено преподавателем
* не может изменять решения
* после проверки преподавателем(если статус не ```approved``` и имеется комментарий), может создать новое решение
* может просматривть историю решений к упражнениям
* все решения упражнения удаляются при удалении этого упражнения

# API
Описание с помощью OpenAPI(Swagger).

# СУБД
PostgreSQL
# Cхема базы данных

![](https://github.com/denis-verkholantsev/teacher-student-db/blob/main/er_diagram.png)

# Язык программирования
Python (Flask+SQLAlchemy)
# Технологии разработки
Docker

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

## Тестирование
Ручное через Swagger по различным пользовательским сценариям
