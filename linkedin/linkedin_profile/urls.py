from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="starting-page"),
    path('login',views.login,name="login"),
    path('linkedin',views.linkedin)
]