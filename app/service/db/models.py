from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import Column, ForeignKey, String, Table, LargeBinary
from sqlalchemy.sql import func
from uuid import UUID, uuid4
from datetime import date, datetime
from typing import Set
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


teacher_student_association = Table(
    "teacher_student",
    db.metadata,
    Column("teacher_id", ForeignKey("teacher.id"),
           primary_key=True, onupdate="cascade"),
    Column("student_id", ForeignKey("student.id"),
              primary_key=True, onupdate="cascade")
)


homework_exercise_association = Table(
    "homework_exercise",
    db.metadata,
    Column("homework_id", ForeignKey("homework.id"),
           primary_key=True, onupdate="cascade"),
    Column("exercise_id", ForeignKey("exercise.id"),
              primary_key=True, onupdate="cascade")
)


homework_student_association = Table(
    "homework_student",
    db.metadata,
    Column("homework_id", ForeignKey("homework.id"),
           primary_key=True, onupdate="cascade"),
    Column("student_id", ForeignKey("student.id"),
              primary_key=True, onupdate="cascade")
)


student_event_association = Table(
    "student_event",
    db.metadata,
    Column("student_id", ForeignKey("student.id"),
           primary_key=True, onupdate="cascade"),
    Column("event_id", ForeignKey("event.id"),
              primary_key=True, onupdate="cascade")
)

file_task_association = Table(
    "file_task",
    db.metadata,
    Column("file_id", ForeignKey("file.id"),
           primary_key=True, onupdate="cascade"),
    Column("task_id", ForeignKey("task.id"),
              primary_key=True, onupdate="cascade")
)

class User(UserMixin, db.Model):
    __tablename__ = "user_"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(30),unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(62), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    birthdate: Mapped[date] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column()

    files: Mapped[Set["FileStorage"]] = relationship(back_populates="user", cascade="all, delete",)

    __mapper_args__={
        "polymorphic_identity" : "user_",
        "polymorphic_on" : type,
    }


class Teacher(User):
    __tablename__ = "teacher"
    
    id: Mapped[UUID] = mapped_column(ForeignKey("user_.id"), primary_key=True)

    # one to many teacher -> student
    students: Mapped[Set["Student"]] = relationship(
        secondary=teacher_student_association, 
        back_populates="teachers",
        )
    
    # one to many teacher -> homework
    homeworks: Mapped[Set["Homework"]] = relationship(back_populates="teacher")

    # one to many teacher -> exercises
    exercises: Mapped[Set["Exercise"]] = relationship(back_populates="teacher")

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }

    events: Mapped[Set["Event"]] = relationship(back_populates="teacher", cascade="all, delete")


class Student(User):
    __tablename__ = "student"

    id: Mapped[UUID] = mapped_column(ForeignKey("user_.id"), primary_key=True)

    # many to many teachers <-> student
    teachers: Mapped[Set["Teacher"]] = relationship(
        secondary=teacher_student_association, 
        back_populates="students",
        )
    
    # many to many student <-> homework
    homeworks: Mapped[Set["Homework"]] = relationship(
        secondary=homework_student_association, 
        back_populates="students",
        )
    
    # one to many student -> solution
    solutions: Mapped[Set["Solution"]] = relationship(back_populates="student", cascade="all,delete")

    # many to many student <-> event
    events: Mapped[Set["Event"]] = relationship(
        secondary=student_event_association, 
        back_populates="students",
        )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }



class FileStorage(db.Model):
    __tablename__ = "file"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    filedata = Column(LargeBinary)

    # many to many task <-> file
    tasks: Mapped[Set["Task"]] = relationship(
        secondary=file_task_association, 
        back_populates="files",
        )

    # one to many user -> file
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="files")

    @compiles(DropTable, "postgresql")
    def _compile_drop_table(element, compiler, **kwargs):
        return compiler.visit_drop_table(element) + " CASCADE"


class Task(db.Model):
    __tablename__ = "task"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    type: Mapped[str] = mapped_column()

    # many to many task <-> file
    files: Mapped[Set["FileStorage"]] = relationship(
        secondary=file_task_association, 
        back_populates="tasks",
        )

    __mapper_args__={
        "polymorphic_identity" : "task",
        "polymorphic_on" : type,
    }


class Solution(Task):
    __tablename__ = "solution"
    id: Mapped[UUID] = mapped_column(ForeignKey("task.id"), primary_key=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)

    ''' Not approved -> approved  '''
    status: Mapped[str] = mapped_column(default="not approved", nullable=False)

    # one - to - many student -> solution
    student_id: Mapped[UUID] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    student: Mapped["Student"] = relationship(back_populates="solutions")
    
    # one - to - many exercise -> solution
    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercise.id", ondelete="CASCADE"))
    exercise: Mapped["Exercise"] = relationship(back_populates="solutions", foreign_keys=[exercise_id])

    __mapper_args__ = {
        "polymorphic_identity": "solution",
    }

    @compiles(DropTable, "postgresql")
    def _compile_drop_table(element, compiler, **kwargs):
        return compiler.visit_drop_table(element) + " CASCADE"


class Exercise(Task):
    __tablename__ = "exercise"
    id: Mapped[UUID] = mapped_column(ForeignKey("task.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)

    # one to many teacher -> exercise
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey("teacher.id", ondelete="SET NULL"), nullable=True)
    teacher: Mapped["Teacher"] = relationship(back_populates="exercises")

    # many - to - many exs - homeworks
    homeworks: Mapped[Set["Homework"]] = relationship(
        secondary=homework_exercise_association, 
        back_populates="exercises",
        )

    # one - to many exercise -> solution
    solutions: Mapped[Set["Solution"]] = relationship(back_populates="exercise", foreign_keys=[Solution.id], cascade="all, delete")

    __mapper_args__ = {
        "polymorphic_identity": "exercise",
    }

    @compiles(DropTable, "postgresql")
    def _compile_drop_table(element, compiler, **kwargs):
        return compiler.visit_drop_table(element) + " CASCADE"


class Homework(Task):
    __tablename__ = "homework"
    id: Mapped[UUID] = mapped_column(ForeignKey("task.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    deadline: Mapped[datetime] = mapped_column(nullable=True)

    # one to many homework -> teacher
    teacher: Mapped["Teacher"] = relationship(back_populates="homeworks")
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey("teacher.id", ondelete="SET NULL"), nullable=True)

    # many to many student <-> homework
    students: Mapped[Set["Student"]] = relationship(
        secondary=homework_student_association, 
        back_populates="homeworks",
        )

    # many to many exercise <-> homework
    exercises: Mapped[Set["Exercise"]] = relationship(
        secondary=homework_exercise_association, 
        back_populates="homeworks",
        )
    
    __mapper_args__ = {
        "polymorphic_identity": "homework",
    }
    
    @compiles(DropTable, "postgresql")
    def _compile_drop_table(element, compiler, **kwargs):
        return compiler.visit_drop_table(element) + " CASCADE"


class Event(db.Model):
    __tablename__ = "event"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    start: Mapped[datetime] = mapped_column(nullable=False)
    end: Mapped[datetime] = mapped_column(nullable=False)
    
    # one to many teacher -> event
    teacher: Mapped["Teacher"] = relationship(back_populates="events")
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey("teacher.id"))
    # many to many student <-> event
    students: Mapped[Set["Student"]] = relationship(
        secondary=student_event_association, 
        back_populates="events",
        )
    
    @compiles(DropTable, "postgresql")
    def _compile_drop_table(element, compiler, **kwargs):
        return compiler.visit_drop_table(element) + " CASCADE"

    




