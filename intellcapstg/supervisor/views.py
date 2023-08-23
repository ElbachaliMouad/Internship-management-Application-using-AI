
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def about(request):
    return render(request,'stagiaire/about.html')


def activitemain(request):
    return render(request, 'stagiaire/activitemain.html')


def contact(request):
    return render(request,'stagiaire/contact.html')





def document(request):
    return render(request, 'stagiaire/document')



def forum(request):
    return render(request, 'stagiaire/forum.html')


def index(request):
    return render(request, 'stagiaire/index.html')



def offre(request):

    return render(request, 'stagiaire/offre.html')


def postuler(request):
    return render(request,'stagiaire/postuler.html')





def profile(request):

    return render(request, 'stagiaire/profile.html')




def profileinfo(request):
    return render(request,'stagiaire/profileinfo.html')




def profilepass(request):

    return render(request, 'stagiaire/profilepass.html')



def search(request):
    return render(request, 'stagiaire/search.html')



def signup(request):
     return render (request,'stagiaire/signup.html')


def  signin(request):
    return render (request, '/stagiaire/signin.html')









