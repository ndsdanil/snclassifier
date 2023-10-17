from django.urls import path
from snclassifier_djangoapp import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("snclassifier_djangoapp/<name>", views.hello_there, name="hello_1there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]