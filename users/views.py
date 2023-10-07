from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.core.mail import EmailMessage

name='Viswanath'
link = 'google.com'
message = f"""
Hi {name}, This mail is from VSTUD

To Reset Your Password Click On The Link
{link}
"""

# Create your views here.
def registration(request):
    
    if request.method=='POST':
        username = str(request.POST.get('register')).strip()
        email = str(request.POST.get('email')).strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = str(request.POST.get('name')).strip().capitalize()
        regulation = request.POST.get('regulation')
        batch = request.POST.get('batch')
        semester = request.POST.get('semester')
        department = request.POST.get('department')
        section = request.POST.get('section')
        year = request.POST.get('year')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        mobile = str(request.POST.get('mobile')).strip()

        print(username, email, password1, password2, name, regulation, batch, semester, section, dob, gender, mobile)
        if password1!=password2:
            print("Passwords Not Matched")
        elif not email.endswith('@velammalitech.edu.in'):
            print("You Are Not Authorized")
        elif len(mobile)!=10:
            print("Mobile length Issue")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )


            batch = Batch.objects.get(batch=batch)
            regulation = Regulation.objects.get(regulation=regulation)
            department = Department.objects.get(department=department)
            semester = Semester.objects.get(semester=semester)
            section = Section.objects.get(section=section)
            year = Year.objects.get(year=year)

            profile = StudentProfile.objects.create(
                user = user,
                name = name,
                batch = batch,
                regulation = regulation,
                department = department,
                section = section,
                semester = semester,
                year = year,
                date_of_birth = dob,
                gender = gender,
                mobile = mobile
            )

            if user and profile:
                user.save()
                profile.save()


    regulations = Regulation.objects.all()
    batches = Batch.objects.all()
    departments = Department.objects.all()
    semesters = Semester.objects.all()
    genders = StudentProfile.Gender.choices
    sections = Section.objects.all()
    years = Year.objects.all()

    context = {'regulations':regulations, 'batches':batches, 'departments':departments, 'semesters':semesters, 'genders':genders, 'sections':sections, 'years':years}
    return render(request, 'users/registration.html', context)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form = AuthenticationForm

def userLogout(request):
    logout(request)
    return redirect('login')



