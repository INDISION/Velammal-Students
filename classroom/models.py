from django.db import models

import sys
sys.path.append("..")
from users.models import *

# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=250)
    credit = models.CharField(max_length=25)

    def __str__(self):
        return self.code + " " + self.name

class Class(models.Model):
    regulation = models.ForeignKey(Regulation, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    subjects = models.ManyToManyField(Subject, null=True, blank=True)
    unique_field = models.CharField(max_length=250, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        
        unique_id = f"REG {self.regulation} | Batch {self.batch} | YEAR {self.year} | SEM {self.semester} | {self.department} {self.section}"
        self.unique_field = unique_id

        super(Class, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.unique_field)
    
class Attendance(models.Model):
    class Status(models.TextChoices):
        WORKING = 'Working Day', 'Working Day'
        NONWORKING = 'Non Working Day', 'Non Working Day'

    date = models.DateField(default=datetime.datetime.now())
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.WORKING)
    students = models.ManyToManyField(StudentProfile)

    def __str__(self):
        return str(self.date) + " | " + self.status
    
class Exam(models.Model):
    class Exams(models.TextChoices):
        IA1 = 'IA1', 'IA1'
        IA2 = 'IA2', 'IA2'
        IA3 = 'IA3', 'IA3'
        MODEL = 'MODEL', 'MODEL'
        SEMESTER = 'SEMESTER', 'SEMESTER'
    
    exam = models.CharField(max_length=250, choices=Exams.choices)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return "EXAM " + self.exam + " | " + self.class_id.unique_field
    
class Result(models.Model):
    class AttendStatus(models.TextChoices):
        ABSENT = 'ABSENT', 'ABSENT'
        PRESENT = 'PRESENT', 'PRESENT'
        OD = 'OD', 'OD'
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.CharField(max_length=25, null=True, blank=True)
    attend_status = models.CharField(choices=AttendStatus.choices, max_length=25, default=AttendStatus.PRESENT)

    def save(self, *args, **kwargs):
        if self.marks==None:
            self.attend_status = self.AttendStatus.ABSENT
        else:
            self.attend_status = self.AttendStatus.PRESENT
        super(Result, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.student.user.username + " | EXAM " + self.exam.exam + " | " + self.exam.class_id.unique_field