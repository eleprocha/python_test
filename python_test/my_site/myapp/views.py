from django.shortcuts import render
from django.http import HttpResponse
from .models import Kataxoriseis

# Create your views here.

#def index(request,gm):
#    kataxoriseis= Kataxoriseis.objects.filter(gemh = gm).all()

 #   output ='<br>'.join(['name: ' + c.name + ' ' + 'registration date ' + c.date_website_registration + 
#    ' website: ' + c.website  + ' GEMH: ' + c.gemh  for c in kataxoriseis])
#    return HttpResponse(output)

def index(request):
    return render(request,'myapp/index.html')

def example(request):
    gm = request.GET['gm']
    kataxoriseis= Kataxoriseis.objects.filter(gemh = gm).all()
    my_var = {''.join(['name: ' + c.name + ' ' + 'registration date: ' + c.date_website_registration + ' website: ' + c.website  + ' GEMH: ' + c.gemh  for c in kataxoriseis])}
    return render(request,'myapp/example.html',{'my_var':my_var})
    

# Create your views here.
