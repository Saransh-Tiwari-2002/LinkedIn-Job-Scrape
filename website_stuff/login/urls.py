from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('state', views.state, name='state'),
    path('category', views.category, name='category'),
    path('subcategory', views.subcategory, name='subcategory'),
    path('job', views.job, name='job'),
]
