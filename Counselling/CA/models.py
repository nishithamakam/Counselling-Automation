from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib import admin
from django import forms
from django.contrib import admin

 
class Counsellor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    c_id=models.IntegerField(null=False,default=0)
    def __str__(self):
        return self.user.username

    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_id = models.ForeignKey(Counsellor, on_delete=models.CASCADE, related_name='students')
    batch = models.CharField(max_length=9, null=True)
    branch = models.CharField(max_length=5, choices=[('CSE', 'CSE'), ('CST', 'CST'), ('CSM', 'CSM'), ('CSD', 'CSD'), ('IT-A', 'IT-A'), ('IT-B', 'IT-B'), ('EEE', 'EEE'), ('ECE', 'ECE'), ('ETE', 'ETE')],default=0)
    dob = models.DateField(null=True)
    phno = models.CharField(max_length=20,null=True)
     

    def get_attendance_data(self):
        attendance_per_month = self.attendance.all()
        attendance_data = [(attendance.get_month_display(), attendance.percentage) for attendance in attendance_per_month]
        return attendance_data  
    def clean(self):
        super().clean()

        # Validate batch
        batch_parts = self.batch.split('-')
        if len(batch_parts) != 2 or int(batch_parts[1]) - int(batch_parts[0]) != 4:
            raise ValidationError('Incorrect Format')  
    
     
    def __str__(self):
        return self.user.username
    
 
    
class Attendance(models.Model):
    s_id= models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')    
    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
    month = models.IntegerField(choices=MONTH_CHOICES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ['s_id', 'month']

    def __str__(self):
        return f"{self.s_id.user} - {dict(self.MONTH_CHOICES)[self.month]}"
    

class Subject(models.Model):
    subject_code = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=100)
    credits = models.IntegerField(null=False,default=0)

    def __str__(self):
        return self.subject_name
       
class Marks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mid1_marks = models.IntegerField(default=0,null=True,validators=[MinValueValidator(0), MaxValueValidator(30)])
    mid2_marks = models.IntegerField(default=0,null=True,validators=[MinValueValidator(0), MaxValueValidator(30)])
    consolidate_marks = models.FloatField(default=0)
    external_marks = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(70)])
    grade_points = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def save(self, *args, **kwargs):
        self.consolidate_marks = (self.mid1_marks + self.mid2_marks) / 2.0
        if (self.consolidate_marks + self.external_marks) >= 90:
            self.grade_points = 10
        elif (self.consolidate_marks + self.external_marks) >= 80:
            self.grade_points = 9
        elif (self.consolidate_marks + self.external_marks) >= 70:
            self.grade_points = 8
        elif (self.consolidate_marks + self.external_marks) >= 60:
            self.grade_points = 7
        elif (self.consolidate_marks + self.external_marks) >= 50:
            self.grade_points = 6
        elif (self.consolidate_marks + self.external_marks) >= 60:
            self.grade_points = 5
        elif (self.consolidate_marks + self.external_marks) >= 50:
            self.grade_points = 4
        else:
           self.grade_points = 0
        super(Marks, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.subject.subject_name} - {self.student.user.username}" 
class Remarks(models.Model):
    s_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    c_id = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    date = models.DateField()
    student_opinion = models.TextField()
    counsellor_remarks = models.TextField()

    def __str__(self):
        return f'Date of Counselling {self.date}'

class Academic(models.Model):
    stu = models.ForeignKey(Student, on_delete=models.CASCADE,default=0)   
    academic_year = models.CharField(max_length=9)
    semester = models.PositiveSmallIntegerField(choices=[(1, '1st'), (2, '2nd')], default=0)
    subjects = models.ManyToManyField(Subject)
    marks = models.ManyToManyField(Marks)
    sgpa =  models.DecimalField(max_digits=5, decimal_places=2)

    
    def clean(self):
        super().clean()

        # Validate academic_year
        academic_year_parts = self.academic_year.split('-')
        if len(academic_year_parts) != 2 or int(academic_year_parts[1]) - int(academic_year_parts[0]) != 1:
            raise ValidationError('Incorrect Format')
        
     

    def __str__(self):
        return f"{self.academic_year} - Semester {self.semester}"
    
 
 
