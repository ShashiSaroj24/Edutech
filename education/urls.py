"""
URL configuration for education project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from EduApp import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Home/",views.Home,name="Home"), 
    path('Register/',views.Register,name="Register"),
    path('Login/',views.Login,name="Login"),
    path('Base/',views.Base),
    path('AboutUs/',views.AboutUs,name="AboutUs"),
    path('Contact/',views.Contact,name="Contact"),
    path('LatestNews/',views.LatestNews,name="LatestNews"),
    path('Coordinators/',views.Coordinators,name="Coordinators"),
    path('Coordinators_Details/<str:Name>/',views.Coordinators_Details,name="Coordinators_Details"),
    path('ForgetPassword/',views.ForgetPassword,name="Forget Password"),
    path('Check_OTP/',views.Check_OTP,name="Check_OTP"),
    path('Success/',views.Email,name="Success"),
    path('UserProfile/',views.UserProfile,name="User Profile"),
    path('Sidebar/',views.Sidebar,name="Sidebar"),
    path('Dashboard/',views.Dashboard,name="Dashboard"),
    path('ChangePassword/',views.ChangePassword,name="Change Password"),
    path('EditProfile/',views.EditProfile,name="Edit Profile"),
    path('HelpAndSupport/',views.HelpAndSupport,name="HelpAndSupport"),
    path('Logout/',views.Logout,name="Logout",),
    path('Articles/',views.Articles,name="Articles",),
    path('Laws/',views.Laws,name="Laws",),
    path('Laws_Details/<int:id>/',views.Laws_Details,name="Laws_Details",),
    path('Colleges/',views.Colleges,name="Colleges",),
    path('University/',views.University,name="University",),
    path('View Articles/<int:id>/',views.View_Articles, name='View Articles'),
    path('Courses/',views.Courses,name="Courses",),
    path('Exams/<str:name>',views.Exams, name='Exams'),
    path('Statistics/',views.Statistics,name="Statistics"),
    path('States/',views.States,name="States"),
    path('Analytics/',views.Analytics,name="Analytics"),
    path('Statewise_Universities/<str:name>',views.State_University_Details,name="Statewise Universities"),
    path("Student_Prediction/",views.Student_Prediction,name="Student_Prediction"),
    path("EduAnalysis1/",views.EduAnalysis1,name="EduAnalysis1"),
    path("EduAnalysis2/",views.EduAnalysis2,name="EduAnalysis2"),
    path("EduAnalysis3/",views.EduAnalysis3,name="EduAnalysis3"),
    path("EduAnalysis4/",views.EduAnalysis4,name="EduAnalysis4"),
    path("EduAnalysis5/",views.EduAnalysis5,name="EduAnalysis5"),
    path("EduAnalysis6/",views.EduAnalysis6,name="EduAnalysis6"),
    path("Eduexp1/",views.Eduexp1,name="Eduexp1"),
    path("Eduexp2/",views.Eduexp2,name="Eduexp2"),
    path("Eduexp3/",views.Eduexp3,name="Eduexp3"),
    path("Eduexp4/",views.Eduexp4,name="Eduexp4"),
    path("Eduexp5/",views.Eduexp5,name="Eduexp5"),
    path("Eduexp6/",views.Eduexp6,name="Eduexp6"),
    path("EduLit1/",views.EduLit1,name="EduLit1"),
    path("EduLit2/",views.EduLit2,name="EduLit2"),
    path("EduLit3/",views.EduLit3,name="EduLit3"),
    path("EduLit4/",views.EduLit4,name="EduLit4"),
    path("EduLit5/",views.EduLit5,name="EduLit5"),
    path("EduLit6/",views.EduLit6,name="EduLit6"),
    path("EduEnrollP1/",views.EduEnrollP1,name="EduEnrollP1"),
    path("EduEnrollP2/",views.EduEnrollP2,name="EduEnrollP2"),
    path("EduEnrollP3/",views.EduEnrollP3,name="EduEnrollP3"),
    path("EduEnrollP4/",views.EduEnrollP4,name="EduEnrollP4"),
    path("EduEnrollP5/",views.EduEnrollP5,name="EduEnrollP5"),
    path("EduEnrollP6/",views.EduEnrollP6,name="EduEnrollP6"),
    path("EduPop1/",views.EduPop1,name="EduPop1"),
    path("EduPop2/",views.EduPop2,name="EduPop2"),
    path("EduPop3/",views.EduPop3,name="EduPop3"),
    path("EduPop4/",views.EduPop4,name="EduPop4"),
    path("EduPop5/",views.EduPop5,name="EduPop5"),
    path("EduPop6/",views.EduPop6,name="EduPop6"),
    path("EduIllit1/",views.EduIllit1,name="EduIllit1"),
    path("EduIllit2/",views.EduIllit2,name="EduIllit2"),
    path("EduIllit3/",views.EduIllit3,name="EduIllit3"),
    path("EduIllit4/",views.EduIllit4,name="EduIllit4"),
    path("EduIllit5/",views.EduIllit5,name="EduIllit5"),
    path("EduIllit6/",views.EduIllit6,name="EduIllit6"),
    path("EduEnrollS1/",views.EduEnrollS1,name="EduEnrollS1"),
    path("EduEnrollS2/",views.EduEnrollS2,name="EduEnrollS2"),
    path("EduEnrollS3/",views.EduEnrollS3,name="EduEnrollS3"),
    path("EduEnrollS4/",views.EduEnrollS4,name="EduEnrollS4"),
    path("EduEnrollS5/",views.EduEnrollS5,name="EduEnrollS5"),
    path("EduEnrollS6/",views.EduEnrollS6,name="EduEnrollS6"),
    path("EduPrediction1/",views.EduPrediction1,name="EduPrediction1"),
    path("EduPrediction2/",views.EduPrediction2,name="EduPrediction2"),
    path("EduPrediction3/",views.EduPrediction3,name="EduPrediction3"),
    path("EduPredict4/",views.EduPredict4,name="EduPredict4"),
    path("EduPrediction4/",views.EduPrediction4,name="EduPrediction4"),
    path("EduPrediction4.1/",views.EduPrediction41,name="EduPrediction4.1"),
    path("EduPredict5/",views.EduPredict5,name="EduPredict5"),
    path("EduPrediction5/",views.EduPrediction5,name="EduPrediction5"),
    path("EduPrediction5.1/",views.EduPrediction51,name="EduPrediction5.1"),
    path("EduPrediction6/",views.EduPrediction6,name="EduPrediction6"),
    path("StudentAnalysis/",views.Student_Analysis,name="StudentAnalysis"),
    path("StudentEDA1/",views.Student_EDA1,name="StudentEDA1"),
    path("StudentEDA2/",views.Student_EDA2,name="StudentEDA2"),
    path("StudentEDA3/",views.Student_EDA3,name="StudentEDA3"),
    path("StudentEDA4/",views.Student_EDA4,name="StudentEDA4"),
    path("StudentEDA5/",views.Student_EDA5,name="StudentEDA5"),
    path("StudentEDA6/",views.Student_EDA6,name="StudentEDA6"),
    path("StudentEDA7/",views.Student_EDA7,name="StudentEDA7"),
    path("Chatbot/",views.Chatbot,name="Chatbot"),

]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
