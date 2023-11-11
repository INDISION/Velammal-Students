from django.contrib.auth.models import User
from django.shortcuts import render
from users import models as user_models
from . import models as classroom_models
from django.db.models import Count
from django.utils import timezone
import calendar

def attendence(request):
    user = User.objects.get(pk=request.user.id)
    student_profile = user_models.StudentProfile.objects.get(user=user)

    # attendence
    working_days = classroom_models.Attendance.objects.filter(status='Working Day')
    present_days = working_days.filter(students=student_profile)
    attendence = {}
    for i in range(timezone.now().month, timezone.now().month-5, -1):
        month = calendar.month_name[i]
        working_days_m = len(working_days.filter(date__month=i))
        present = len(present_days.filter(date__month=i))
        absent = len(working_days.filter(date__month=i)) - present
        present_percent = 0
        absent_percent = 0
        if working_days_m!=0:
            present_percent = round(present/working_days_m*100, 2)
            absent_percent = 100 - present_percent
        attendence[month] = {
            'present' : present,
            'presentPercent' : present_percent,
            'absent' : absent,
            'absentPercent' : absent_percent,
            'totalDays' : working_days_m}
    
    # Notes
    files = classroom_models.Notes.objects.filter(class_id__class_id = student_profile.class_id)
    
    # assignments
    assignemts = classroom_models.Assignments.objects.filter(class_id__class_id = student_profile.class_id)

    context = {
        'attendence' : attendence,
        'files' : files,
        'assignments':assignemts,
    }
    return render(request, "classroom/classroom.html", context)

def notes(request):
    user = User.objects.get(pk=request.user.id)
    student_profile = user_models.StudentProfile.objects.get(user=user)
    files = classroom_models.Notes.objects.filter(class_id = student_profile.class_id)
    print(files[0].file.url)

def results(request):
    user = User.objects.get(pk=request.user.id)
    student_profile = user_models.StudentProfile.objects.get(user=user)
    exams = classroom_models.Result.objects.filter(student=student_profile)
    ia1 = exams.filter(exam__exam='IA1')
    print(ia1[0].subject)
    exams = {
        'IA1' : exams.filter(exam__exam='IA1'),
        'IA2' : exams.filter(exam__exam='IA2'),
        'IA3' : exams.filter(exam__exam='IA3'),
        'MODEL' : exams.filter(exam__exam='MODEL'),
        'SEMESTER' : exams.filter(exam__exam='SEMESTER'),
    }
    return render(request, 'classroom/results.html', exams)
