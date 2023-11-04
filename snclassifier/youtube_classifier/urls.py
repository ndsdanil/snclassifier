from django.urls import path
from . import views
app_name = "youtube_classifier"
urlpatterns = [
    path("", views.index, name="index"),
    path("process_data/", views.process_data, name="process_data"),
]