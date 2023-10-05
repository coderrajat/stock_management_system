
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('place_order', views.Addorder.as_view(), name='addorder'),

]
