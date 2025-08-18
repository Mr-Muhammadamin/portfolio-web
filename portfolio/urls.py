from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('credentials/', views.CredentialsView.as_view(), name='credentials'),

    path('works/', views.WorksView.as_view(), name='works'),
    path('work/<slug:slug>/', views.WorkDetailView.as_view(), name='work_detail'),

    path('contact/', views.ContactView.as_view(), name='contact'),
    path('video/',views.YoutubeVideoListView.as_view(), name='video')
 

]