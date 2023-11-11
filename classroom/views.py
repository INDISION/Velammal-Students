from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users import models as user_models
from . import models as classroom_models
from django.utils import timezone
import calendar

@login_required
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

@login_required
def results(request):
    user = User.objects.get(pk=request.user.id)
    student_profile = user_models.StudentProfile.objects.get(user=user)
    exams = classroom_models.Result.objects.filter(student=student_profile)
    exams = {
        'IA' : {
            'IA1' : exams.filter(exam__exam='IA1'),
            'IA2' : exams.filter(exam__exam='IA2'),
            'IA3' : exams.filter(exam__exam='IA3'),
        },
        'MODEL' : exams.filter(exam__exam='MODEL'),
        'SEMESTER' : {
            'SEM 1' : exams.filter(exam__exam='SEM-1'),
            'SEM 2' : exams.filter(exam__exam='SEM-2'),
            'SEM 3' : exams.filter(exam__exam='SEM-3'),
            'SEM 4' : exams.filter(exam__exam='SEM-4'),
            'SEM 5' : exams.filter(exam__exam='SEM-5'),
            'SEM 6' : exams.filter(exam__exam='SEM-6'),
            'SEM 7' : exams.filter(exam__exam='SEM-7'),
            'SEM 8' : exams.filter(exam__exam='SEM-8'),
            }
    }
    return render(request, 'classroom/results.html', exams)
