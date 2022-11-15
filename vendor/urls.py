from django.urls import path
from . import views

urlpatterns = [
    path('', views.vprofile),
    path('profile/', views.vprofile, name='vprofile'),

]
