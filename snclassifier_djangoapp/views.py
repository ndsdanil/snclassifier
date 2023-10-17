from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from django.utils.timezone import datetime

def home(request):
    return render(request, "snclassifier_djangoapp/home.html")

def about(request):
    return render(request, "snclassifier_djangoapp/about.html")

def contact(request):
    return render(request, "snclassifier_djangoapp/contact.html")


# def hello_there(request, name):
#     print(request.build_absolute_uri()) #optional
#     return render(
#         request,
#         'snclassifier_djangoapp/init_page.html',
#         {
#             'name': name,
#             'date': datetime.now()
#         }
#     )