from django.urls import path
from . import views
urlpatterns = [
  path('', views.index, name='index'),
  path('<slug:meetup_slug>/success/', views.success_register, name='success_register_tag'),
  path('<slug:meetup_slug>/', views.about, name='about'),
]