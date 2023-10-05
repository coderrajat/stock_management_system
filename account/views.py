from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, logout, login
from . import Checklogin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models ,serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


def base(request):
    return render(request, 'Stock/index.html')

def signup(request):
    return render(request, 'Stock/Signup.html')

@login_required(login_url='/')
def dashboard(request):
    Total_stock=models.Stock.objects.filter(is_sold=False).count()
    Total_sale=models.Stock.objects.filter(is_sold=True).count()
    profit=0
    loss=0
    data=models.Order_placed.objects.all()
    list=serializers.new_order_serializer(data,many=True).data
    return render(request, 'Stock/dashboard/dashboard.html',{'total_stock':Total_stock,'total_sale':Total_sale,'profit':profit,'loss':loss,'order_list':list})


def dologin(request):
    if request.method =='POST':
        user=Checklogin.CheckUser.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            if user.active!=False:
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











class Addorder(APIView):
    def post(self,request):
        order=models.Stock.objects.get(id=request.POST['id'])
        if order.qnt!=0:
            order.qnt=order.qnt-int(request.POST['qut'])
            order.is_sold=True
            order.save()
            plcord=models.Order_placed()
            plcord.Product=order.Product
            plcord.amnt=order.amnt
            plcord.Order_by='test'
            plcord.save()

            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'Hurry! your order is placed'},

                                },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':'Order out of stock',
                            },status=status.HTTP_202_ACCEPTED) 
        
    def get(self,request):
        order=models.Stock.objects.all()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'data':serializers.stock_serializer(order,many=True).data},

                            },status=status.HTTP_202_ACCEPTED)