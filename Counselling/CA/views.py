
from django.shortcuts import render,redirect
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Marks,Student,Subject,Academic,Attendance,User,Counsellor
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from twilio.rest import Client


def ca_login(request):
    error=""
    if request.method == "POST":  
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)     
        if user: 
            login(request,user)
            error="Logged in successfully."
            if 's_login' in request.POST:
                return redirect('s_login')
            elif 'c_login' in request.POST:
                return redirect('c_login')
        else:
            error = "Invalid Login Credentials.Try again."

    return render(request, 'ca_login.html', {'error': error})
from django.shortcuts import get_object_or_404

@login_required
def c_login(request):
    error = ""
    
    if request.method == "POST":
        if 'logout' in request.POST:
            logout(request)
            error = "Log Out Success!!"
            return redirect('ca_login')

    counselor_user = request.user
    counselor = get_object_or_404(Counsellor, user=counselor_user)
    students = Student.objects.filter(c_id=counselor)

    context = {
        'students': students,
        'error': error
    }

    return render(request, 'c_login.html', context)
 


from django.http import JsonResponse
from twilio.rest import Client

def send_notification(request):
    if request.method == 'POST':
        print('Sending notification...')
        notification_message = request.POST.get('message')
        phone_number = request.POST.get('phone_number')
        print('Message:', notification_message)
        print('Phone number:', phone_number)

        # Your Twilio account SID and auth token
        account_sid = 'AC2d63fe9ec09467dd98b774e033fb78a6'
        auth_token = '8c6ca84a34a00a619749391d2429b7cc'

        # Create a Twilio client
        client = Client(account_sid, auth_token)

        try:
            # Send the SMS notification
            message = client.messages.create(
                body=notification_message,
                from_='+14068000727',
                to=phone_number
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

def s_login(request):
    error=""
    if request.method == "POST":
        if 'logout' in request.POST:
            logout(request)
            error="Log Out Success!!"
            return redirect('ca_login')   
    return render(request,'s_login.html', {'error': error})
 
def calculate_sgpa(student):
    marks = Marks.objects.filter(student=student)  # Retrieve marks for the student
    total_grade_points = 0
    total= 0
    total_credits=0

    for mark in marks:
        grade_points = mark.grade_points
        total_grade_points += grade_points
        credits=mark.subject.credits
        total_credits+=credits
        total += grade_points*credits

    if total_credits == 0:
        sgpa = Decimal(0)  
    else:
        sgpa = Decimal(total / total_credits).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)  # Calculate SGPA and round to 2 decimal places

    return sgpa


@login_required
def marks(request):  
    if request.user.groups.filter(name='Student').exists():
        student = request.user.student
    elif request.user.groups.filter(name='Counsellor').exists():
        student = request.user.username     
    else:
        student=None
    subjects = Subject.objects.all()
    marks = Marks.objects.filter(student=student)
    sgpa = 0 
   
    if marks:
        sgpa = calculate_sgpa(student)
    return render(request,'marks.html', {'subjects': subjects,'marks':marks, 'sgpa': sgpa})
     

def attendance(request):
    if request.user.groups.filter(name='Student').exists():
        student = request.user.student
        attendance_list = Attendance.objects.filter(s_id=student)
    elif request.user.groups.filter(name='Counsellor').exists():
        student = request.user.username
        attendance_list = Attendance.objects.filter(s_id=student)  
    else:
        student = None
        attendance_list = None
    
    context = {
        'attendance_list': attendance_list,
    }  
    return render(request, 'attendance.html', context)

def analysis(request):
    if request.user.groups.filter(name='Student').exists():
        student = request.user.student  
    elif request.user.groups.filter(name='Counsellor').exists():
         student = request.user.username
    marks_list = Marks.objects.filter(student=student)
    
    subject_names = []
    subject_marks = []
    
    for marks in marks_list:
        subject_names.append(marks.subject.subject_name)
        subject_marks.append(marks.consolidate_marks)
    
    context = {
        'subject_names': subject_names,
        'subject_marks': subject_marks
    }
    return render(request, 'analysis.html',context)


 