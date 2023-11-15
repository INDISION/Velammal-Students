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
    exam_results = classroom_models.Result.objects.filter(student=student_profile)
    exams = classroom_models.Exam.objects.filter(class_id__class_id = student_profile.class_id)
    exam_results = {
        'IA' : {
            'IA1' : [exam_results.filter(exam__exam='IA1')],
            'IA2' : [exam_results.filter(exam__exam='IA2')],
            'IA3' : [exam_results.filter(exam__exam='IA3')],
        },
        'MODEL' : [exam_results.filter(exam__exam='MODEL')],
        'SEMESTER' : {
            'SEM 1' : [exam_results.filter(exam__exam='SEM-1')],
            'SEM 2' : [exam_results.filter(exam__exam='SEM-2')],
            'SEM 3' : [exam_results.filter(exam__exam='SEM-3')],
            'SEM 4' : [exam_results.filter(exam__exam='SEM-4')],
            'SEM 5' : [exam_results.filter(exam__exam='SEM-5')],
            'SEM 6' : [exam_results.filter(exam__exam='SEM-6')],
            'SEM 7' : [exam_results.filter(exam__exam='SEM-7')],
            'SEM 8' : [exam_results.filter(exam__exam='SEM-8')],
            }
    }

    for i in ('IA', 'SEMESTER'):
        for exam, data in exam_results[i].items():
            scored_credits = 0
            total_credits = 0
            for paper in data[0]:
                scored_credits += int(paper.grade)*int(paper.subject.credit)
                total_credits += int(paper.subject.credit)*10
            if total_credits!=0:
                exam_results[i][exam].append(round(scored_credits/total_credits*10, 4))
    for subject in exam_results['MODEL'][0]:
        scored_credits += int(subject.grade)*int(subject.subject.credit)
        total_credits += int(subject.subject.credit)*10
        if total_credits!=0:
            exam_results['MODEL'].append(round(scored_credits/total_credits*10, 4))

    print(exam_results['SEMESTER']['SEM 4'][0][0].exam.class_id.year.year)
    return render(request, 'classroom/results.html', exam_results)

@login_required
def upload_results(request, year="I", sem="I"):
    user = User.objects.get(pk=request.user.id)
    student_profile = user_models.StudentProfile.objects.get(user=user)
    exam_results = classroom_models.Result.objects.filter(student=student_profile)
    student = f"REG {student_profile.regulation} | Batch {student_profile.batch} | YEAR {year} | SEM {sem} | {student_profile.department} {student_profile.section}"
    exams = classroom_models.Exam.objects.filter(class_id__class_id = student)
    print(student)
    student_class = classroom_models.Class.objects.get(class_id = student)
    if request.method=="POST":
        pass

    context = {
        'subjects' : student_class.subjects.all()
    }
    return render(request, "classroom/result_upload.html", context)