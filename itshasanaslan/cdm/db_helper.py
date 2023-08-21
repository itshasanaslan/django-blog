import os
import sqlite3
from datetime import datetime

class HandleDatabase:
    def __init__(self):
        self.location = os.path.join("/var/www/itshasanaslan/cdm", "attendance.db")
        #self.location = os.path.join("D:\\msihasan\\Format Yedek\\folders\\workspace\\py\\yoklama\\cdmtest\\cdm", "attendance.db")
        self.connection = sqlite3.connect(self.location, check_same_thread=False)
        self.passcode = "8448209aA"
        self.students = []
        self.lessons = []

    def add_excuse(self, user_id, lesson_id, excuse):
        cursor = self.connection.cursor()
        parameters = """Insert into Excuses (ExcuseUserId,Excuse, LessonId) values(?,?,?);"""
        parameter_values = (user_id, excuse, lesson_id)
        cursor.execute(parameters,parameter_values)
        self.connection.commit()

    def get_students(self):
        self.students = []
        cursor = self.connection.cursor()
        cursor.execute('SELECT * from Students')
        data = cursor.fetchall()
        for i in data:
            self.students.append(Student(i[0], i[1], i[2], i[3], i[4]))
        return self.students

    def get_lessons(self):
        self.lessons = []
        cursor = self.connection.cursor()
        cursor.execute('SELECT * from Lessons')
        data = cursor.fetchall()
        for i in data:
            # check  if the time  in past.
            current_date = datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
            if current_date > datetime.now():
                self.lessons.append(Lesson(i[0],i[1]))
        
        return self.lessons

    
    
    def get_excuses_list(self):
        parameters = "SELECT Excuses.ExcuseUserId, Excuses.LessonId,Students.Name, Students.LastName, Excuses.Excuse, Lessons.Date from Excuses left join Students on Excuses.ExcuseUserId = Students.Id inner join Lessons on Lessons.Id = Excuses.LessonId"
        cursor = self.connection.cursor()
        cursor.execute(parameters)
        return cursor.fetchall()

class Student:
    def __init__(self,name,last,mail,phone,id_):
        self.name = name
        self.last = last
        self.mail = mail
        self.phone = phone
        self.id = id_
        self.full = self.name + " " + self.last

class Lesson:
    def __init__(self,id_,date):
        self.id = id_
        self.date = date

