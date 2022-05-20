from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path(r'kataxoriseis/',views.index, name = 'kataxoriseis'),
    path(r'kataxoriseis/gm',views.example)
]