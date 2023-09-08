from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test


from django.db.models import Q
from django.core.validators import validate_email
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.http import HttpResponse
import hashlib
from .models import Stagiaire, Supervisor,Offre
from django.contrib.auth.models import User, Group
# Create your views here.




def is_special_user(user):
         return not(user.is_superuser)








############################
def about(request):
    return render(request,'stagiaire/about.html')

def contact(request):
    return render(request,'stagiaire/contact.html')


def index(request):
    domaines_dict=Offre.objects.values('domaine').distinct()
    missions_dict=Offre.objects.values('mission').distinct()
    dures_dict=Offre.objects.values('dure').distinct()
    niveaus_dict=Offre.objects.values('niveau_etude').distinct()

    domaines = [domaine['domaine'] for domaine in domaines_dict]
    missions=[mission['mission'] for mission in missions_dict]
    dures=[dure['dure'] for dure in dures_dict]
    niveaus=[niveau['niveau_etude'] for niveau in  niveaus_dict]
    print(niveaus)
    context={
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus
             }
    return render(request, 'stagiaire/index.html',context)

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
                    stagiaire = get_object_or_404(Stagiaire, stagiaire_id=user)
                    login(request, user_mail)
                    if stagiaire.status ==3:
                        return redirect('activitemain',args=[user.pk])
                    else:
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

        try:
            stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
            offre = get_object_or_404(Offre, id=id)
            context={'offre':offre,
                     'stagiaire':stagiaire}
            return render(request, 'stagiaire/offre.html',context)
        except Http404:
            return render(request, 'stagiaire/error.html',status=404)

            




############same work############################################

def postuler(request):
    return render(request,'stagiaire/postuler.html')



@login_required(login_url='signin', )
def search(request):

    try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        offres=Offre.objects.all() 
        domaines_dict=Offre.objects.values('domaine').distinct()
        missions_dict=Offre.objects.values('mission').distinct()
        dures_dict=Offre.objects.values('dure').distinct()
        niveaus_dict=Offre.objects.values('niveau_etude').distinct()

        number=offres.count()
        domaines = [domaine['domaine'] for domaine in domaines_dict]
        missions=[mission['mission'] for mission in missions_dict]
        dures=[dure['dure'] for dure in dures_dict]
        niveaus=[niveau['niveau_etude'] for niveau in  niveaus_dict]
        print(niveaus)
        context={'stagiaire' : stagiaire,
             'offres':offres,  
             'number':number,
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus
             }
        return render(request, 'stagiaire/search.html' , context)

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)

            



##########################same work###############################


@login_required(login_url='signin', )

def profile(request):
    
    try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status != 0 :
             offres=Offre.objects.all() 
             domaines_dict=Offre.objects.values('domaine').distinct()
             missions_dict=Offre.objects.values('mission').distinct()
             dures_dict=Offre.objects.values('dure').distinct()
             niveaus_dict=Offre.objects.values('niveau_etude').distinct()
             number=offres.count()
             domaines = [domaine['domaine'] for domaine in domaines_dict]
             missions=[mission['mission'] for mission in missions_dict]
             dures=[dure['dure'] for dure in dures_dict]
             niveaus=[niveau['niveau_etude'] for niveau in  niveaus_dict]
             print(niveaus)
             context={'stagiaire' : stagiaire,
             'offres':offres,  
             'number':number,
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus}
             return render(request, 'stagiaire/profile.html' , context)
        else:
            return render(request, 'stagiaire/error.html',status=404)


    except Http404:
            return render(request, 'stagiaire/error.html',status=404)


@login_required(login_url='signin', )
def profileinfo(request):
    try:
        # Retrieve stagiaire and offres data
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        offres = Offre.objects.all()

        # Query distinct values for various fields
        domaines_dict = Offre.objects.values('domaine').distinct()
        missions_dict = Offre.objects.values('mission').distinct()
        dures_dict = Offre.objects.values('dure').distinct()
        niveaus_dict = Offre.objects.values('niveau_etude').distinct()

        # Extract values from querysets
        domaines = [domaine['domaine'] for domaine in domaines_dict]
        missions = [mission['mission'] for mission in missions_dict]
        dures = [dure['dure'] for dure in dures_dict]
        niveaus = [niveau['niveau_etude'] for niveau in niveaus_dict]

        context = {
            'stagiaire': stagiaire,
            'offres': offres,
            'number': offres.count(),
            'domaines': domaines,
            'missions': missions,
            'dures': dures,
            'niveaus': niveaus,
            'error': False,
            'valid': False,
            'message1': "",
            'message': ""
        }

        if request.method == "POST":
            mail = request.POST.get('mail', None)
            username = request.POST.get('username', None)
            
            # Use Django's EmailValidator for email validation
            try:
                validate_email(mail)
            except:
                context['error'] = True
                context['message'] = "Enter a valid email !"
            
            user_by_email = User.objects.filter(email=mail).first()
            user_by_username = User.objects.filter(username=username).first()

            if user_by_email:
                context['error'] = True
                context['message'] = f"A user with existing {mail} mail !"

            if user_by_username:
                context['error'] = True
                context['message'] = f"A user with existing {username} username !"

            if not context['error']:
                user = request.user
                user.username = username
                user.email = mail
                user.save()
                return redirect('profileinfo')

        return render(request, 'stagiaire/profileinfo.html', context)

    except Http404:
        return render(request, 'stagiaire/error.html', status=404)
######



@login_required(login_url='signin', )
def profilepass(request):
    try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        offres=Offre.objects.all() 
        domaines_dict=Offre.objects.values('domaine').distinct()
        missions_dict=Offre.objects.values('mission').distinct()
        dures_dict=Offre.objects.values('dure').distinct()
        niveaus_dict=Offre.objects.values('niveau_etude').distinct()
        number=offres.count()
        domaines = [domaine['domaine'] for domaine in domaines_dict]
        missions=[mission['mission'] for mission in missions_dict]
        dures=[dure['dure'] for dure in dures_dict]
        niveaus=[niveau['niveau_etude'] for niveau in  niveaus_dict]
        print(niveaus)
        context={'stagiaire' : stagiaire,
        'offres':offres,  
             'number':number,
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus}
        return render(request, 'stagiaire/profilepass.html',context)

        

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)

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






