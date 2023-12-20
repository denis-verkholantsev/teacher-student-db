from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Teacher, Student, Homework, FileStorage, Exercise, Homework, Solution, Event
from datetime import datetime, date, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models import Base
from sys import argv

URL="postgresql://postgres:1313@localhost:8765/postgres"

def test(Base=Base, URL=URL):
    Base.metadata.drop_all(bind=create_engine(URL))
    tests = [
            test_create_teacher_student, 
            test_create_homework_exercise,
            test_create_teacher_with_same_username,
            test_create_file_for_homework_exercise,
            test_create_solution_and_file,
            test_create_event
            ]
    for fun in tests:
        if not fun(Base, URL):
            print(f"Fall on {fun}")
            return
    print("All is passed")


def test_create_teacher_student(Base, URL):
    engine = create_engine(URL, echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    teacher =  Teacher(username="Alex", email="alex@gmail.com", password="alex999")
    teacher2 =  Teacher(username="George", first_name="Lucky", email="george@gmail.com", password="george999",
                       birthdate=date(1970, 2, 1))
    student = Student(username="Ivan", email="ivan@gmai.com", password="ivan999")
    teacher.students.add(student)
    session.add_all([teacher, teacher2, student])
    session.commit()

    teacher_alex = session.query(Teacher).where(Teacher.username=="Alex").one_or_none()
    if teacher_alex and len(teacher_alex.students):
        session.close()
        return student in teacher_alex.students

    session.close()
    raise NotImplementedError()


def test_create_teacher_with_same_username(Base, URL):
    engine = create_engine(URL, echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    teacher =  Teacher(username="Alex", email="alex@gmail.com", password="alex999")
    teacher_same_name =  Teacher(username="Alex", email="xx@gmail.com", password="xx999")
    try:
        session.add_all([teacher, teacher_same_name])
        session.commit()
    except IntegrityError:
        return True
    
    raise NotImplementedError()


def test_create_homework_exercise(Base, URL):
    engine = create_engine(URL, echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    
    teacher = session.query(Teacher).where(Teacher.username=="Alex").one_or_none()
    student = session.query(Student).where(Student.username=="Ivan").one_or_none()

    homework = Homework(title="my_homework", deadline=datetime.now()+timedelta(days=1))
    if teacher:
        teacher.homeworks.add(homework)
    if student:
        student.homeworks.add(homework)

    exercise1 = Exercise(title="ex1", description="First exercise", teacher_id=teacher.id)
    exercise2 = Exercise(title="ex2", description="Second exercise", teacher_id=teacher.id)

    homework.exercises.update([exercise1, exercise2])

    session.add_all([homework, exercise1, exercise2])
    session.commit()

    exs = session.query(Exercise).all()

    if len(exs) != 2:
        raise NotImplementedError()
    
    if exs[0] not in homework.exercises or exs[1] not in homework.exercises:
        raise NotImplementedError()
    
    if homework not in student.homeworks:
        raise NotImplementedError()

    session.close()

    return True


def test_create_file_for_homework_exercise(Base, URL):
    engine = create_engine(URL, echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    homeworks = session.query(Homework).where(Homework.title == "my_homework").all()
    exercises = session.query(Exercise).where(Exercise.title == "ex1").all()

    if len(homeworks) != 1 or len(exercises) != 1:
        raise NotImplementedError()
    
    homework = homeworks.pop()
    exercise = exercises.pop()

    file_h = FileStorage(filename="homework_file", file_data=b'filefilefile')
    file_e = FileStorage(filename="exercise_file", file_data=b'filefilefile')
    file_e.task = exercise
    file_h.task = homework

    session.add_all([file_h, file_e])
    session.commit()

    if len(homework.files) == 0 or len(exercise.files) == 0:
        raise NotImplementedError()
    
    session.close()

    return True


def test_create_solution_and_file(Base, URL):
    engine = create_engine(URL, echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    exercise = session.query(Exercise).where(Exercise.title == "ex1").one_or_none()
    student = session.query(Student).where(Student.username == "Ivan").one_or_none()
    file_s = FileStorage(filename="solution_file", file_data=b'filefilefile')
    solution = Solution()

    solution.files.add(file_s)
    if not exercise or not student:
        raise NotImplementedError()
    
    solution.exercise = exercise
    solution.student = student
    session.add(solution)
    session.commit()

    solution_copy = session.execute(select(Solution).where(Solution.exercise_id == exercise.id)).first()[0]

    if not len(solution_copy.files):
        raise NotImplementedError()
    
    if solution_copy.exercise.id != exercise.id:
        raise NotImplementedError()
    
    session.close()
    
    return True

def test_create_event(Base, URL):
    engine = create_engine(URL, echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    teacher = session.query(Teacher).where(Teacher.username=="Alex").one_or_none()
    student = session.query(Student).where(Student.username=="Ivan").one_or_none()

    event = Event(title="new_event", start=datetime.now(), end=datetime.now()+timedelta(hours=2))
    event.students.add(student)
    event.teacher = teacher

    session.add(event)
    session.commit()

    if len(teacher.events) != 1 or len(student.events) != 1:
        raise NotImplementedError()
    
    session.close()

    return True


if __name__== "__main__":
    test(Base=Base, URL=argv[1] if len(argv)>1 else URL)







    







