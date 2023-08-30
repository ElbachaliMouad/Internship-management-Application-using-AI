from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.db.models import Q
from django.core.validators import validate_email
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.http import HttpResponse
import hashlib
from .models import Stagiaire, Supervisor,Offre
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
    error=False
    message1=""
    message=""
    if request.method =="POST":
        username=request.POST.get('username', None)
        mail=request.POST.get('mail', None)
        password=request.POST.get('password', None)
        repassword=request.POST.get('repassword', None)
        try :
            validate_email(mail)==False
        except:
            error=True
            message="Enter a valid email !"

        if error==False :
           if  password != repassword :
               error=True
               message="The two passwords are not the same !"
                   
        user=User.objects.filter( email=mail ).first()
      

        if user:
            error=True
            message= f"A user with existing {mail}  mail  !"
           
       

                

        
            
                
                
        
        if error == False  :
            user=User(
                username=username,
                email=mail,
            )
            user.save()
            user.password=password
            user.set_password(user.password)
            user.save()
            


            stagiaire=Stagiaire(stagiaire_id=user)
            stagiaire.save()

            return redirect('signin')
            
        


    context= {
        'error':error,
        'message':message,
        'message1':message1,
    }
    return render (request,'stagiaire/signup.html',context)







def  signin(request):
    error=False
    valid=False
    message1=""
    message=""
    if request.method =="POST":
        mail=request.POST.get('mail', None)
        password=request.POST.get('password', None)
        try :
            validate_email(mail)==False
        except:
            error=True
            message="Enter a valid email !"


          
        print("=="*5, "NEW POST:", mail, "=="*5)
        print("=="*5, "NEW POST:", password, "=="*5)
  

        user=User.objects.filter(email=mail).first()
        if user:
            user_mail=authenticate(username=user.username, password=password)
            test=not(user.is_superuser)
            print(test)
            if user_mail :
                if test:
                    login(request, user_mail)
                    return redirect('search')
                else:
                    error=True
                    message="can't find  user"
            
            else:
                    error=True
                    message="wrong password"
               

        else:
            error=True
            message="The email is wrong"
        








    context= {
        'error':error,
        'message':message,
        'valid': valid
    }
    

    return render (request, 'stagiaire/signin.html',context)


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
     

    stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
    context={'stagiaire' : stagiaire}
    return render(request, 'stagiaire/search.html' , context)


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



