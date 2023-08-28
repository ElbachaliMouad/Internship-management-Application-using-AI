from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.db.models import Q
from django.core.validators import validate_email
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.http import HttpResponse
import hashlib
from django.contrib.auth.models import User, Group
# Create your views here.



def about(request):
    return render(request,'stagiaire/about.html')

def contact(request):
    return render(request,'stagiaire/contact.html')


def index(request):
    return render(request, 'stagiaire/index.html')

#########################################




def signup(request):
     return render (request,'stagiaire/signup.html')


def  signin(request):
    return render (request, 'stagiaire/signin.html')


########same work################################################

@login_required(login_url='signin', )
###test
def activitemain(request,id):
    return render(request, 'stagiaire/activitemain.html')



@login_required(login_url='signin', )
def document(request,id):
    return render(request, 'stagiaire/document.html')


@login_required(login_url='signin', )
def forum(request,id):
    return render(request, 'stagiaire/forum.html')



#######################################
@login_required(login_url='signin', )
def offre(request,id):

    return render(request, 'stagiaire/offre.html')




############same work############################################

def postuler(request):
    return render(request,'stagiaire/postuler.html')



@login_required(login_url='signin', )
def search(request):
    return render(request, 'stagiaire/search.html')


########same work#################################################


@login_required(login_url='signin', )
def profile(request):

    return render(request, 'stagiaire/profile.html')



@login_required(login_url='signin', )
def profileinfo(request):
    return render(request,'stagiaire/profileinfo.html')





@login_required(login_url='signin', )
def profilepass(request):

    return render(request, 'stagiaire/profilepass.html')



##########################supervisor##############################

 
def supersignin(request):
    return render(request,'supervisor/signin.html')


def superoffre(request):
    return render(request, 'supervisor/actviteadmin.html')


def  superprofile(request, id):
    return render(request, 'supervisor/profile.html')



##########################logout#################################



@login_required(login_url='signin')
def log_out_stagiaire(request):
        logout(request)
        return redirect('index')



