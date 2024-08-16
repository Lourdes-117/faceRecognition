from django.urls import path

from . import views

urlpatterns = [
    path("", views.face_recognition, name="index"),
]