from django.urls import path
from snclassifier_djangoapp import views

urlpatterns = [
    path("", views.home, name="home"),
]