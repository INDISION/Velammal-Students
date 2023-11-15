from django.db import models
from django.utils import timezone
import os

import sys
sys.path.append("..")
from users import models as user_models

# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=250)
    credit = models.CharField(max_length=25)

    def __str__(self):
        return self.code + " " + self.name

class Class(models.Model):
    regulation = models.ForeignKey(user_models.Regulation, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(user_models.Batch, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(user_models.Year, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(user_models.Semester, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(user_models.Department, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(user_models.Section, on_delete=models.SET_NULL, null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    class_id = models.CharField(max_length=250, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        
        unique_id = f"REG {self.regulation} | Batch {self.batch} | YEAR {self.year} | SEM {self.semester} | {self.department} {self.section}"
        self.class_id = unique_id

        super(Class, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.class_id)
    
class Attendance(models.Model):
    class Status(models.TextChoices):
        WORKING = 'Working Day', 'Working Day'
        NONWORKING = 'Non Working Day', 'Non Working Day'

    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.WORKING)
    students = models.ManyToManyField(user_models.StudentProfile, blank=True)

    def __str__(self):
        return str(self.date) + " | " + self.status
    
class Exam(models.Model):
    class Exams(models.TextChoices):
        IA1 = 'IA1', 'IA1'
        IA2 = 'IA2', 'IA2'
        IA3 = 'IA3', 'IA3'
        MODEL = 'MODEL', 'MODEL'
        SEM1 = 'SEM-1', 'SEMESTER-1'
        SEM2 = 'SEM-2', 'SEMESTER-2'
        SEM3 = 'SEM-3', 'SEMESTER-3'
        SEM4 = 'SEM-4', 'SEMESTER-4'
        SEM5 = 'SEM-5', 'SEMESTER-5'
        SEM6 = 'SEM-6', 'SEMESTER-6'
        SEM7 = 'SEM-7', 'SEMESTER-7'
        SEM8 = 'SEM-8', 'SEMESTER-8'
    
    exam = models.CharField(max_length=250, choices=Exams.choices)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return "EXAM " + self.exam + " | " + self.class_id.class_id
    
class Result(models.Model):
    class AttendStatus(models.TextChoices):
        ABSENT = 'ABSENT', 'ABSENT'
        PRESENT = 'PRESENT', 'PRESENT'
        OD = 'OD', 'OD'
    class Grades(models.TextChoices):
        O = 10, 'O'
        APLUS = 9, 'A+'
        A = 8, 'A'
        BPLUS = 7, 'B+'
        B = 6, 'B'
        C = 5, 'C'
        NOGRADE = 0, 'NOGRADE'
    student = models.ForeignKey(user_models.StudentProfile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.CharField(max_length=25, null=True, blank=True)
    grade = models.CharField(choices=Grades.choices, max_length=25, default=Grades.NOGRADE)
    attend_status = models.CharField(choices=AttendStatus.choices, max_length=25, default=AttendStatus.PRESENT)

    def save(self, *args, **kwargs):
        if self.marks==None:
            self.attend_status = self.AttendStatus.ABSENT
        else:
            self.attend_status = self.AttendStatus.PRESENT
        
        self.marks = int(self.marks)*100//60

        if int(self.marks) in range(90, 101):
            self.grade = self.Grades.O
        elif int(self.marks) in range(80, 90):
            self.grade = self.Grades.APLUS
        elif int(self.marks) in range(70, 80):
            self.grade = self.Grades.A
        elif int(self.marks) in range(60,70):
            self.grade = self.Grades.BPLUS
        elif int(self.marks) in range(50,60):
            self.grade = self.Grades.B
        elif int(self.marks) in range(45,50):
            self.grade = self.Grades.C
        else:
            self.grade = self.Grades.NOGRADE
        
        print(self.grade)
        super(Result, self).save(*args, **kwargs)
        
    class Meta:
        unique_together = ('student', 'exam', 'subject')
        
    def __str__(self):
        return self.student.user.username + " | EXAM " + self.exam.exam + " | " + self.exam.class_id.class_id
    
class Notes(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notes/')

    def __str__(self):
        return self.title + " | " + str(self.subject) + " | " + self.class_id.class_id

class Assignments(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='assignments/')

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(Assignments, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title + " | " + str(self.subject) + " | " + self.class_id.class_id