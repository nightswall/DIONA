from django.urls import path
from . import views

urlpatterns = [
    path("predict/temperature", views.predict_temperature, name="predict/temperature"),
]
