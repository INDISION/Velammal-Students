from django.db import models
from django.contrib.auth.models import User
import datetime


class Batch(models.Model):
    batch = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.batch
    
class Regulation(models.Model):
    regulation = models.CharField(max_length=4, unique=True)
    def __str__(self):
        return self.regulation
    
class Department(models.Model):
    department = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.department

class Year(models.Model):
    year = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.year

class Semester(models.Model):
    semester = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.semester

class Section(models.Model):
    section = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.section
    

class StudentProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    regulation = models.ForeignKey(Regulation, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=Gender.choices)
    mobile = models.CharField(max_length=15)
    class_id = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.class_id = f"REG {self.regulation} | Batch {self.batch} | YEAR {self.year} | SEM {self.semester} | {self.department} {self.section}"
        super(StudentProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)