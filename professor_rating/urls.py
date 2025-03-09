from django.contrib import admin 
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Professor Rating System! Navigate to /rating/")

urlpatterns = [
    path('', home, name='home'), 
    path('admin/', admin.site.urls),
    path('rating/', include('rating_app.urls')),  
]

