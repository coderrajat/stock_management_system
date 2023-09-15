from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, logout, login
from . import Checklogin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
# Create your views here.


def base(request):
    return render(request, 'students/index.html')

def signup(request):
    return render(request, 'students/Signup.html')

@login_required(login_url='/')
def dashboard(request):
    return render(request, 'students/dashboard/dashboard.html')


def dologin(request):
    if request.method =='POST':
        user=Checklogin.CheckUser.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            if user.status!=False:
                return redirect('dashboard')
            else:
                messages.error(request,'User not verified!')  
                return redirect('/')
        else:
            messages.error(request,'Invalid username and password!')
            return redirect('/')

    else:         
        messages.error(request,'Invalid User!')  
        return redirect('/')

def registration(request):
    if request.method=='POST':
        try:
            user=models.User()
            user.image=request.POST.get('image')
            user.first_name=request.POST.get('first_name')
            user.last_name=request.POST.get('last_name')
            user.email=request.POST.get('email')
            user.phone_number=request.POST.get('phone_number')
            user.DOB=request.POST.get('DOB')
            user.cls_name=request.POST.get('cls_name')
            if request.POST.get('password')!=request.POST.get('confirm_password'):
                messages.error(request,'Confirm password is not matching')
                return redirect('signup')
            else:
                user.set_password(request.POST.get('password'))
                user.save()
                messages.success(request,'Hurry! you are successfully register. wait for admin review')  
                return redirect('/')
        except Exception as e:
            messages.error(request,str(e))  
            return redirect('signup')
    else:
        messages.error(request,'something went wrong!')  
        return redirect('signup')

def logoutuser(request):
    logout(request)
    return redirect('/')