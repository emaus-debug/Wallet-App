from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="expenses"),
    path('create', views.create, name="create-expenses"),
]