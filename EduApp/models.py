from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Contact_model(models.Model):
	Name=models.CharField(max_length=10000)
	Email=models.CharField(max_length=10000)
	Msg=RichTextField()

class Register_model(models.Model):
	Name=models.CharField(max_length=10000)
	Email=models.CharField(max_length=10000)
	Password=models.CharField(max_length=10000)
	Pincode=models.CharField(max_length=10000,blank=True,null=True)
	PhoneNo=models.CharField(max_length=10000,blank=True,null=True)
	DOB=models.CharField(max_length=10000,blank=True,null=True)
	City=models.CharField(max_length=10000,blank=True,null=True)
	Address=models.CharField(max_length=10000,blank=True,null=True)
	ProfileImg=models.ImageField(upload_to = 'profile',blank=True)


class Article(models.Model):
	Title=models.CharField(max_length=10000)
	Description=models.TextField(max_length=10000,blank=True,null=True)
	Article=models.TextField(max_length=5000)
	Upload=models.ImageField(upload_to = 'data',blank=True)
	def __str__(self):
		return self.Title

class College(models.Model):
	Name=models.CharField(max_length=10000)
	City=models.CharField(max_length=10000)
	Country=models.CharField(max_length=10000)
	Specialization=models.CharField(max_length=10000)
	PhoneNo=models.CharField(max_length=1000,blank=True,null=True)
	Email=models.EmailField()
	Website=models.URLField()
	Address=models.TextField(max_length=3100)
	Image=models.ImageField()
	def __str__(self):
		return self.Name+" "+self.City+" "+self.Specialization+" "+self.Country

class Universitie(models.Model):
	Name=models.CharField(max_length=10000)
	City=models.CharField(max_length=10000)
	State=models.CharField(max_length=10000)
	PhoneNo=models.CharField(max_length=10000,blank=True,null=True)
	Email=models.EmailField()
	Website=models.URLField()
	Address=models.TextField(max_length=3100)
	Image=models.ImageField()
	def __str__(self):
		return self.Name+" "+self.City+" "+self.State+" "+str(self.PhoneNo)+" "+self.Email

class law(models.Model):
	Name=models.CharField(max_length=10000)
	Description=models.TextField(max_length=10000)

class Course(models.Model):
	Name=models.CharField(max_length=1000,primary_key=True)
	Image=models.ImageField(upload_to = 'data',blank=True)
	def __str__(self):
		return self.Name

class EduInst(models.Model):
	Name=models.CharField(max_length=1000,primary_key=True)
	Image=models.ImageField(upload_to = 'data',blank=True)
	Description=models.TextField(max_length=10000)
	Logo=models.ImageField(upload_to = 'data',blank=True)
	Title=models.CharField(max_length=10000, blank=True, null=True)
	Description=models.CharField(max_length=10000, blank=True, null=True)
	Description1=models.TextField(max_length=10000, blank=True, null=True)
	PhoneNo=models.CharField(max_length=10000,blank=True,null=True)
	Email=models.EmailField(blank=True, null=True)
	Website=models.URLField(blank=True, null=True)
	Address=models.TextField(max_length=3100,blank=True, null=True)
	Website_Link=models.URLField(blank=True,null=True)
	Partnering_Institutes=models.CharField(max_length=10000, blank=True, null=True)
	Completed_Courses=models.CharField(max_length=10000, blank=True, null=True)
	Student_Enrollment=models.CharField(max_length=10000, blank=True, null=True)
	Exam_Registrations=models.CharField(max_length=10000, blank=True, null=True)
	Successful_Certification=models.CharField(max_length=10000, blank=True, null=True)
	def __str__(self):
		return self.Name
		
class Exam(models.Model):
	Name=models.ForeignKey(Course, on_delete=models.CASCADE)
	Exam_Name=models.CharField(max_length=1000, primary_key=True)
	Logo=models.ImageField(upload_to='data',blank=True)
	Link=models.URLField(blank=True,null=True)
	def __str__(self):
		return self.Exam_Name

class statistic(models.Model):
	Statistic=models.CharField(max_length=1000,primary_key=True)
	def __str__(self):
		return self.Statistic

class statistic_detail(models.Model):
	Statistic=models.ForeignKey(statistic, on_delete=models.CASCADE)
	Title=models.CharField(max_length=100)
	Year=models.CharField(max_length=100)
	pdf=models.FileField()
	def __str__(self):
		return self.Title

class State_and_Universitie(models.Model):
	State_name=models.CharField(max_length=1000,primary_key=True)
	map_image=models.ImageField()
	def __str__(self):
		return self.State_name

class Universities_detail(models.Model):
	State_Name=models.ForeignKey(State_and_Universitie, on_delete=models.CASCADE)
	Universities_Name=models.CharField(max_length=1000)
	Link=models.URLField(blank=True,null=True)

class Email(models.Model):
	Email=models.EmailField(blank=True,null=True)

class HelpandSupport(models.Model):
	Title=models.CharField(max_length=10000)
	Message=models.TextField()	