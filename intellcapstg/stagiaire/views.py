from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.core.validators import validate_email
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.http import HttpResponse
import hashlib
from .models import Stagiaire, Supervisor,Offre,Task, Document, Filesrespond, Fileresquest
from django.contrib.auth.models import User, Group
# Create your views here.
from datetime import datetime, timedelta

from django.utils import timezone
import re
from django.db.models import Q
import os
from django.http import FileResponse

from django.db.models import Count






def rechercher(query,results):

    for i, char in enumerate(query):
        # Combine queries using OR (|)
        or_query = Q(domaine__istartswith=query[:i+1]) | \
                   Q(mission__istartswith=query[:i+1]) | \
                   Q(skills_needed__istartswith=query[:i+1]) | \
                   Q(dure__istartswith=query[:i+1]) | \
                   Q(niveau_etude__istartswith=query[:i+1])

        # Apply the OR query
        results = results.filter(or_query)

    return results






        


def is_valid_phone_number(phone_number):
    # Define a regex pattern to match a typical phone number
    # This is a basic example and may need to be adapted to match your specific phone number format
    pattern = r'^\+?1?\d{9,15}$'

    return re.match(pattern, phone_number) is not None

def calculate_middle_date(date1, date2):
    # Calculate the average timestamp
    average_timestamp = (date1.timestamp() + date2.timestamp()) / 2

    # Convert the average timestamp back to a datetime object
    middle_date = datetime.fromtimestamp(average_timestamp)

    return middle_date.strftime('%Y-%m-%d')

def is_special_user(user):
         return not(user.is_superuser)








############################
def about(request):
    return render(request,'stagiaire/about.html')

def contact(request):
    return render(request,'stagiaire/contact.html')


def index(request):
    try:
        
            for offre in  Offre.objects.filter(valable=1):
                if offre.date_of_expiry:
                    if offre.date_of_expiry <= timezone.now():
                      offre.valable=0
                      offre.save()
                    else:
                        pass
                else:
                    pass

            offres= Offre.objects.filter(valable=1)
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
            
            context={
             'offres':offres,  
             'number':number,
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus,
             'exist':True
             }
            if  request.method== "POST":
                
                query=request.POST.get('query',None)
                dom=request.POST.get('dom',None)
                miss=request.POST.get('miss',None)
                periode=request.POST.get('periode',None)
                misssperiods = domsmisss = domsperiodes = domsperiodesmiss = periodes = misss = doms = None

                if  query:
                    a=rechercher(query,offres)

                else:
                    a=Offre.objects.none()
                if dom:
                    doms = offres.filter(domaine=dom)
                else:
                    doms=Offre.objects.none()
        
        # Filter based on mission if provided
                if miss:
                    misss = offres.filter(niveau_etude=miss)
                else:
                    miss=Offre.objects.none()
        # Filter based on periode if provided
                if periode:
                    periodes = offres.filter(dure=periode)
                else:
                    periodes=Offre.objects.none()
        # Perform intersection if multiple filters provided
                if dom and miss and periode:
                    domsperiodesmiss = offres.filter(domaine=dom, niveau_etude=miss, dure=periode)
                else:
                    domsperiodesmiss=domsperiodesmiss
                if dom and miss:
                    domsmisss = offres.filter(domaine=dom, niveau_etude=miss)
                else:
                    domsperiodesmiss=Offre.objects.none()
                if dom and periode:
                    domsperiodes = offres.filter(domaine=dom, dure=periode)
                else:
                    domsperiodes=Offre.objects.none()
                
                if miss and periode:
                    misssperiods = offres.filter(niveau_etude=miss, dure=periode)
                else:
                    misssperiods=Offre.objects.none()


                

                offres=a.union(domsperiodesmiss).union(domsmisss).union(domsperiodes).union(misssperiods).union(doms).union(misss).union(periodes)

               
            
                if len(offres)==0:
                    context['exist']=False
                else:
                    context['offres']=offres
                    context['number']=offres.count()


                    


                    


                redirect_url = 'postuler/?' + '&'.join([f'{k}={v}' for k, v in context.items()])

                return redirect(redirect_url)
            
            return render(request, 'stagiaire/index.html',context)


            

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)



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
                    try:
                        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=user)
                        login(request, user_mail)
                     
                    except Http404:
                        return render(request, 'stagiaire/error.html', status=404)

                    if stagiaire.status ==2:
                        return redirect('activitemain',id=stagiaire.offre_stage.pk)
                    
                    elif stagiaire.status ==1:
                        return redirect('profile')
                    
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
    try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.offre_stage.pk != id:
                return render(request, 'stagiaire/error.html', status=404)
        else:
            if stagiaire.status != 2:
                return render(request, 'stagiaire/error.html', status=404)
            else:
                pas=False
                tasks=Task.objects.filter(task_offre=stagiaire.offre_stage)
                documents=Document.objects.filter(owner=stagiaire)
                message = ''
                error = False
                if request.method == "POST":
                  error_messages = []
                  tas = request.POST.get('task', None)
                  tit = request.POST.get('title', None)
                  docu = request.FILES.get('document',None)
                  if not tas:

                     error_messages.append(" * Please chose task.")
                  if not tit:
                     error_messages.append(" * Please entre a  title.")
                  if not docu:
                     error_messages.append(" * Please upload a document.")


                  if not error_messages:
                    tas = get_object_or_404(Task, pk=tas)
                    existing_document = Document.objects.filter(owner=stagiaire, task_root=tas).first()
                    if existing_document:
                        existing_document.title=tit
                        existing_document.date_upload=timezone.now()
                        existing_document.content=docu
                        existing_document.save()
                    else:
                        new_document = Document.objects.create(owner=stagiaire, title=tit,date_upload=timezone.now(),content=docu,task_root=tas)

                  else:
                     error = True
                     message = "\n".join(error_messages)

                context={'stagiaire':stagiaire,
                         'tasks':tasks,
                         'error':error,
                         'message':message}
                return render(request, 'stagiaire/activitemain.html', context)



    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)






@login_required(login_url='signin', )
def document(request,id):
     try:
        owner = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if owner.offre_stage.pk != id:
                return render(request, 'stagiaire/error.html', status=404)
        else:
            if owner.status != 2:
                return render(request, 'stagiaire/error.html', status=404)
            else:
                message = ''
                error = False
                if request.method == "POST":
                  error_messages = []
                  title = request.POST.get('title', None)
                  file = request.FILES.get('file',None)
                  description=request.POST.get('description', None)
                  if not title:

                     error_messages.append(" * Please chose title.")
                  if not file:
                     error_messages.append(" * Please entre a  file.")
                  if not error_messages:
                      file= Fileresquest.objects.create(owner=owner, title=title,content=file,status=1,description=description)
                  else:
                     error = True
                     message = "\n".join(error_messages)
                context={'owner':owner,
                         
                         'error':error,
                         'message':message}      
                
                return render(request, 'stagiaire/document.html', context)



     except Http404 :
         return render(request, 'stagiaire/error.html', status=404)


@login_required(login_url='signin', )
def forum(request,id):
    try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.offre_stage.pk != id:
                return render(request, 'stagiaire/error.html', status=404)
        else:
            if stagiaire.status != 2:
                return render(request, 'stagiaire/error.html', status=404)
            else:
                context={'stagiaire':stagiaire}
                return render(request, 'stagiaire/forum.html', context)



    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)



#######################################
@login_required(login_url='signin', )
def offre(request, id):
    try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status==2:
            return render(request, 'stagiaire/error.html',status=404)


        else:
            offre = get_object_or_404(Offre, id=id)
            if offre.date_of_expiry:
                    if offre.date_of_expiry <= timezone.now():
                      offre.valable=0
                      offre.save()
                    else:
                        pass
            else:
                    pass
            if offre.valable==0:
                    return render(request, 'stagiaire/error.html', status=404)
            else:
                domaines_dict = Offre.objects.values('domaine').distinct()
                missions_dict = Offre.objects.values('mission').distinct()
                dures_dict = Offre.objects.values('dure').distinct()
                niveaus_dict = Offre.objects.values('niveau_etude').distinct()
                domaines = [domaine['domaine'] for domaine in domaines_dict]
                missions = [mission['mission'] for mission in missions_dict]
                dures = [dure['dure'] for dure in dures_dict]
                niveaus = [niveau['niveau_etude'] for niveau in niveaus_dict]
                message = ''
                error = False
                if request.method == "POST":
                  error_messages = []
                  last_name = request.POST.get('lastn', None)
                  first_name = request.POST.get('firstn', None)
                  phone = request.POST.get('phone', None)
                  school = request.POST.get('school', None)
                  motivation = request.POST.get('motiv', None)
                  niveau = request.POST.get('niveau', None)
                  cv = request.FILES.get('cv',None)

                  if not last_name:
                     error_messages.append(" * Please enter your last name.")
                  if not first_name:
                     error_messages.append(" * Please enter your first name.")
                  if not phone:
                     error_messages.append(" * Please enter your phone.")
                  if not school:
                     error_messages.append(" * Please enter your school.")
                  if not motivation:
                     
                     error_messages.append(" * Please  enter your motivation.")
                  if not niveau:
                     error_messages.append(" * Please  enter your niveau.")
                  if not cv :
                     error_messages.append(" * Please  enter your cv.")



            # Check for image file
                  if 'image' in request.FILES:
                     image = request.FILES['image']
                     if image.content_type.startswith('image'):
                        stagiaire.image = image
                
                     else:
                        error_messages.append(" * Invalid image file format. Please upload an image.")

          

            

              

                  if not error_messages:
                     
                     stagiaire.last_Name = last_name
                     stagiaire.fisrt_Name = first_name
                     stagiaire.phone = phone
                     stagiaire.school = school
                     stagiaire.motivation = motivation
                     stagiaire.niveau = niveau
                     stagiaire.status = 1
                     stagiaire.cv = cv
                     if stagiaire.offre_stage :
                          
                          if stagiaire.offre_stage != offre:
                              print(stagiaire.offre_stage)
                              print(offre)
                              stagiaire.offre_stage.demande -=1 
                              stagiaire.offre_stage.save()
                              offre.demande += 1
                              offre.save()
                              stagiaire.offre_stage=offre
                              
                          else:
                              pass

                     else:
                         offre.demande+=1
                         offre.save()

                         stagiaire.offre_stage=offre
                     stagiaire.save()
    # Link the user to the new offer

                  else:
                     error = True
                     message = "\n".join(error_messages)

                context = {
               'offre': offre,
               'stagiaire': stagiaire,
               'id': id,
               'domaines': domaines,
               'missions': missions,
                'dures': dures,
                'niveaus': niveaus,
                'message': message,
                 'error': error
                }

                return render(request, 'stagiaire/offre.html', context)

            
        
        

    except Http404:
        return render(request, 'stagiaire/error.html', status=404)


def postuler(request):
    
    try:
        
            for offre in  Offre.objects.filter(valable=1):
                if offre.date_of_expiry:
                    if offre.date_of_expiry <= timezone.now():
                      offre.valable=0
                      offre.save()
                    else:
                        pass
                else:
                    pass

            offres= Offre.objects.filter(valable=1)
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
            
            context={
             'offres':offres,  
             'number':number,
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus,
             'exist':True
             }
            if  request.method== "POST":
                
                query=request.POST.get('query',None)
                dom=request.POST.get('dom',None)
                miss=request.POST.get('miss',None)
                periode=request.POST.get('periode',None)
                print(query,dom,miss,periode)
                misssperiods = domsmisss = domsperiodes = domsperiodesmiss = periodes = misss = doms = None

                if  query:
                    a=rechercher(query,offres)

                else:
                    a=Offre.objects.none()
                if dom:
                    doms = offres.filter(domaine=dom)
                else:
                    doms=Offre.objects.none()
        
        # Filter based on mission if provided
                if miss:
                    misss = offres.filter(niveau_etude=miss)
                else:
                    miss=Offre.objects.none()
        # Filter based on periode if provided
                if periode:
                    periodes = offres.filter(dure=periode)
                else:
                    periodes=Offre.objects.none()
        # Perform intersection if multiple filters provided
                if dom and miss and periode:
                    domsperiodesmiss = offres.filter(domaine=dom, niveau_etude=miss, dure=periode)
                else:
                    domsperiodesmiss=domsperiodesmiss
                if dom and miss:
                    domsmisss = offres.filter(domaine=dom, niveau_etude=miss)
                else:
                    domsperiodesmiss=Offre.objects.none()
                if dom and periode:
                    domsperiodes = offres.filter(domaine=dom, dure=periode)
                else:
                    domsperiodes=Offre.objects.none()
                
                if miss and periode:
                    misssperiods = offres.filter(niveau_etude=miss, dure=periode)
                else:
                    misssperiods=Offre.objects.none()


                

                offres=a.union(domsperiodesmiss).union(domsmisss).union(domsperiodes).union(misssperiods).union(doms).union(misss).union(periodes)

               
            
                if len(offres)==0:
                    context['exist']=False
                else:
                    context['offres']=offres
                    context['number']=offres.count()


                    


                    


                
            return render(request, 'stagiaire/postuler.html' , context)

            

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)

   

############same work############################################

@login_required(login_url='signin', )
def search(request):
  
    try:
        
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status==2:
            return render(request, 'stagiaire/error.html',status=404)
        else:
            for offre in  Offre.objects.filter(valable=1):
                if offre.date_of_expiry:
                    if offre.date_of_expiry <= timezone.now():
                      offre.valable=0
                      offre.save()
                    else:
                        pass
                else:
                    pass

            offres= Offre.objects.filter(valable=1)
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
             'niveaus':niveaus,
             'exist':True
             }
            if  request.method== "POST":
                
                query=request.POST.get('query',None)
                dom=request.POST.get('dom',None)
                miss=request.POST.get('miss',None)
                periode=request.POST.get('periode',None)
                print(query,dom,miss,periode)
                misssperiods = domsmisss = domsperiodes = domsperiodesmiss = a= periodes = misss = doms = None

                if  query:
                    a=rechercher(query,offres)
                else:
                    a=Offre.objects.none()

                if dom:
                    doms = offres.filter(domaine=dom)
                else:
                    doms=Offre.objects.none()
        
        # Filter based on mission if provided
                if miss:
                    misss = offres.filter(niveau_etude=miss)
                else:
                    miss=Offre.objects.none()
        # Filter based on periode if provided
                if periode:
                    periodes = offres.filter(dure=periode)
                else:
                    periodes=Offre.objects.none()
        # Perform intersection if multiple filters provided
                if dom and miss and periode:
                    domsperiodesmiss = offres.filter(domaine=dom, niveau_etude=miss, dure=periode)
                else:
                    domsperiodesmiss=domsperiodesmiss
                if dom and miss:
                    domsmisss = offres.filter(domaine=dom, niveau_etude=miss)
                else:
                    domsperiodesmiss=Offre.objects.none()
                if dom and periode:
                    domsperiodes = offres.filter(domaine=dom, dure=periode)
                else:
                    domsperiodes=Offre.objects.none()
                
                if miss and periode:
                    misssperiods = offres.filter(niveau_etude=miss, dure=periode)
                else:
                    misssperiods=Offre.objects.none()


                

                offres=a.union(domsperiodesmiss).union(domsmisss).union(domsperiodes).union(misssperiods).union(doms).union(misss).union(periodes)

               
            
                if len(offres)==0:
                    context['exist']=False
                else:
                    context['offres']=offres
                    context['number']=offres.count()


                    


                    


                
            return render(request, 'stagiaire/search.html' , context)

            

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)

            



##########################same work###############################


@login_required(login_url='signin', )

def profile(request):
     
     
     try:
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status in [0,2]:
            return render(request, 'stagiaire/error.html',status=404)


        else:
            
            offre = get_object_or_404(Offre, id=stagiaire.offre_stage.pk)
            
            if offre.valable==0:
                    return render(request, 'stagiaire/error.html', status=404)
            else:
                domaines_dict = Offre.objects.values('domaine').distinct()
                missions_dict = Offre.objects.values('mission').distinct()
                dures_dict = Offre.objects.values('dure').distinct()
                niveaus_dict = Offre.objects.values('niveau_etude').distinct()
                domaines = [domaine['domaine'] for domaine in domaines_dict]
                missions = [mission['mission'] for mission in missions_dict]
                dures = [dure['dure'] for dure in dures_dict]
                niveaus = [niveau['niveau_etude'] for niveau in niveaus_dict]
                message = ''
                error = False
                if request.method == "POST":
                  error_messages = []
                  last_name = request.POST.get('lastn', None)
                  first_name = request.POST.get('firstn', None)
                  phone = request.POST.get('phone', None)
                  school = request.POST.get('school', None)
                  motivation = request.POST.get('motiv', None)
                  niveau = request.POST.get('niveau', None)
                  cv = request.FILES.get('cv',None)

                  if not last_name:
                     error_messages.append(" * Please enter your last name.")
                  if not first_name:
                     error_messages.append(" * Please enter your first name.")

                  if not phone:
                     error_messages.append(" * Please enter your phone.")
                  
                  if  not is_valid_phone_number(phone):
                     error_messages.append(" * Please enter a valide  phone: +212..")

                      
                      
                  if not school:
                     error_messages.append(" * Please enter your school.")
                  if not motivation:
                     
                     error_messages.append(" * Please  enter your motivation.")
                  if not niveau:
                     error_messages.append(" * Please  enter your niveau.")
                  if not cv :
                     error_messages.append(" * Please  enter your cv.")



            # Check for image file
                  if 'image' in request.FILES:
                     image = request.FILES['image']
                     if image.content_type.startswith('image'):
                        stagiaire.image = image
                
                     else:
                        error_messages.append(" * Invalid image file format. Please upload an image.")

          

            

              

                  if not error_messages:
                     
                     stagiaire.last_Name = last_name
                     stagiaire.fisrt_Name = first_name
                     stagiaire.phone = phone
                     stagiaire.school = school
                     stagiaire.motivation = motivation
                     stagiaire.niveau = niveau
                     stagiaire.status = 1
                     stagiaire.cv = cv
                     stagiaire.save()

                  else:
                     error = True
                     message = "\n".join(error_messages)

                context = {
               'offre': offre,
               'stagiaire': stagiaire,
               'id': id,
               'domaines': domaines,
               'missions': missions,
                'dures': dures,
                'niveaus': niveaus,
                'message': message,
                 'error': error
                }

                return render(request, 'stagiaire/profile.html', context)

            
        
        

     except Http404:
         return render(request, 'stagiaire/error.html', status=404)

    
    

    


@login_required(login_url='signin', )
def profileinfo(request):
    try:
        # Retrieve stagiaire and offres data
          stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
          offres =  Offre.objects.filter(valable=1)
          

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
              if mail != request.user.email:
                  try:
                     validate_email(mail)
                  except:
                     context['error'] = True
                     context['message'] = "Enter a valid email !"
            
                  user_by_email = User.objects.filter(email=mail).first()

                  if user_by_email:
                      context['error'] = True
                      context['message'] = f"A user with existing {mail} mail !"
              else:
                  pass

              if username != request.user.username:
                  user_by_username = User.objects.filter(username=username).first()
                  if user_by_username:                     
                     context['error'] = True
                     context['message'] = f"A user with existing {username} username !"
              else:
                  pass

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
            offres =  Offre.objects.filter(valable=1)
            domaines_dict = Offre.objects.values('domaine').distinct()
            missions_dict = Offre.objects.values('mission').distinct()
            dures_dict = Offre.objects.values('dure').distinct()
            niveaus_dict = Offre.objects.values('niveau_etude').distinct()
            number = offres.count()
            domaines = [domaine['domaine'] for domaine in domaines_dict]
            missions = [mission['mission'] for mission in missions_dict]
            dures = [dure['dure'] for dure in dures_dict]
            niveaus = [niveau['niveau_etude'] for niveau in niveaus_dict]

            context = {
            'stagiaire': stagiaire,
            'offres': offres,
            'number': number,
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
              error_messages = []

              current_pass = request.POST.get('password', None)
              new_pass = request.POST.get('neopassword', None)
              re_pass = request.POST.get('repassword', None)
              if not check_password(current_pass, request.user.password):
                error_messages.append("The current password is not correct.")

              elif new_pass != re_pass:
                error_messages.append("The new passwords do not match.")

              if not re_pass:
                error_messages.append("* Please enter your confirmation password")

              if not new_pass:
                error_messages.append("* Please enter your new password")

              if not current_pass:
                error_messages.append("* Please enter your password")

              if not error_messages:
                request.user.set_password(new_pass)
                request.user.save()
                return redirect('profilepass')
              else:
                error = True
                message = "\n".join(error_messages)
                context['error'] = error
                context['message'] = message
            return render(request, 'stagiaire/profilepass.html', context)

    except Http404:
        return render(request, 'stagiaire/error.html', status=404)
    

##########################supervisor##############################
 
def supersignin(request):
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
            test=user.is_superuser
            print(test)
            if user_mail :
                if test:
                    try:
                        supervisor = get_object_or_404(Supervisor, supervisor_id=user)
                        login(request, user_mail)
                        return redirect('search_admin')
                     
                    except Http404:
                        return render(request, 'stagiaire/error.html', status=404)

                    
                    
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
    


    return render(request,'supervisor/signin.html',context)



@login_required(login_url='supersignin', )
def superoffre(request):

    return render(request, 'supervisor/actviteadmin.html')




@login_required(login_url='supersignin', )
def  superprofile(request, id):

    
    return render(request, 'supervisor/profile.html')




@login_required(login_url='supersignin', )
def search_admin(request):
    
    try:
        
        supervisor = get_object_or_404(Supervisor, supervisor_id=request.user)
        
        for offre in  Offre.objects.filter(valable=1):
                if offre.date_of_expiry:
                    if offre.date_of_expiry <= timezone.now():
                      offre.valable=0
                      offre.save()
                    else:
                        pass
                else:
                    pass

        offres= Offre.objects.filter(owner=supervisor)
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
            
        context={'supervisor' : supervisor,
             'offres':offres,  
             'number':number,
             'domaines':domaines,
             'missions':missions,
             'dures':dures,
             'niveaus':niveaus,
             'exist':True
             }
        if  request.method== "POST":
                
                query=request.POST.get('query',None)
                dom=request.POST.get('dom',None)
                miss=request.POST.get('miss',None)
                periode=request.POST.get('periode',None)
                print(query,dom,miss,periode)
                misssperiods = domsmisss = domsperiodes = domsperiodesmiss = a= periodes = misss = doms = None

                if  query:
                    a=rechercher(query,offres)
                else:
                    a=Offre.objects.none()

                if dom:
                    doms = offres.filter(domaine=dom)
                else:
                    doms=Offre.objects.none()
        
        # Filter based on mission if provided
                if miss:
                    misss = offres.filter(niveau_etude=miss)
                else:
                    miss=Offre.objects.none()
        # Filter based on periode if provided
                if periode:
                    periodes = offres.filter(dure=periode)
                else:
                    periodes=Offre.objects.none()
        # Perform intersection if multiple filters provided
                if dom and miss and periode:
                    domsperiodesmiss = offres.filter(domaine=dom, niveau_etude=miss, dure=periode)
                else:
                    domsperiodesmiss=domsperiodesmiss
                if dom and miss:
                    domsmisss = offres.filter(domaine=dom, niveau_etude=miss)
                else:
                    domsperiodesmiss=Offre.objects.none()
                if dom and periode:
                    domsperiodes = offres.filter(domaine=dom, dure=periode)
                else:
                    domsperiodes=Offre.objects.none()
                
                if miss and periode:
                    misssperiods = offres.filter(niveau_etude=miss, dure=periode)
                else:
                    misssperiods=Offre.objects.none()


                

                offres=a.union(domsperiodesmiss).union(domsmisss).union(domsperiodes).union(misssperiods).union(doms).union(misss).union(periodes)

               
            
                if len(offres)==0:
                    context['exist']=False
                else:
                    context['offres']=offres
                    context['number']=offres.count()


                    


                    


                
        return render(request, 'supervisor/search_admin.html' , context)

            

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)


##########################logout#################################



@login_required(login_url='signin')
def log_out_stagiaire(request):
       
            logout(request)
            return redirect('index')



@login_required(login_url='signin')
def delete_doc(request,id):

    try:
        
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status != 2:
                return render(request, 'stagiaire/error.html', status=404)
        else:
            doc = get_object_or_404(Document, pk=id, owner=stagiaire)
            doc.delete()
            return redirect('activitemain' , id=stagiaire.offre_stage.pk )





    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)

import mimetypes

@login_required(login_url='signin')

def download_file(request,pk):
    try:
        stagiarire=get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiarire.status !=2:
            return render(request, 'stagiaire/error.html', status=404)
        else:
            obj = get_object_or_404(Document, pk=pk, owner=stagiarire)
            response =HttpResponse(obj.content, content_type='application/force-download')
            response['Content-Disposition']=f'attachment; filename={obj.content.name}"'
            return response
                


    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)



import mimetypes
@login_required(login_url='signin')
def download_filerespond(request,pk):

    try:
        stagiaire=get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status !=2:
            return render(request, 'stagiaire/error.html', status=404)
        else:
            obj = get_object_or_404(Filesrespond, pk=pk, file_request__owner=stagiaire)
            response =HttpResponse(obj.content, content_type='application/force-download')
            response['Content-Disposition']=f'attachment; filename={obj.content.name}"'
            return response
                


    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)



@login_required(login_url='signin')
def download_filee(request,pk):
    try:
        stagiarire=get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiarire.status !=2:
            return render(request, 'stagiaire/error.html', status=404)
        else:
            obj = get_object_or_404(Fileresquest, pk=pk , owner=stagiarire)
            response =HttpResponse(obj.content, content_type='application/force-download')
            response['Content-Disposition']=f'attachment; filename={obj.content.name}"'
            return response
                



    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)
    



@login_required(login_url='signin')
def delete_filee(request,id):
    try:
        
        stagiaire = get_object_or_404(Stagiaire, stagiaire_id=request.user)
        if stagiaire.status != 2:
                return render(request, 'stagiaire/error.html', status=404)
        else:
            doc = get_object_or_404(Fileresquest, pk=id, owner=stagiaire)
            doc.delete()
            return redirect('document' , id=stagiaire.offre_stage.pk )

    except Http404 :
        return render(request, 'stagiaire/error.html', status=404)
    


@login_required(login_url='supersignin')
def dashboard(request,id):
    try:
        

        
        for offre in  Offre.objects.filter(valable=1):
                if offre.date_of_expiry:
                    if offre.date_of_expiry <= timezone.now():
                      offre.valable=0
                      offre.save()
                    else:
                        pass
                else:
                    pass
        supervisor = get_object_or_404(Supervisor, supervisor_id=request.user)
        offre=get_object_or_404(Offre, pk=id, owner=supervisor, valable=0)
      
        tasks=Task.objects.filter(task_offre=offre)
        task_counts = tasks.annotate(document_count=Count('document'))
        a=tasks.count()
            
        colors = ['#1DC7EA', '#FB404B', '#FFA534', '#9368E9', '#87CB16', '#1F77D0', '#5e5e5e', '#dd4b39', '#35465c', '#e52d27', '#55acee', '#cc2127', '#1769ff', '#6188e2', '#a748ca', '#a748ca']
        task_colors = {task: colors[i % len(colors)] for i, task in enumerate(tasks)}
       
        import json
        p=0
        total_document_count = sum(task_count.document_count for task_count in task_counts)

            

        data = {
    'series':[f"{int((task_count.document_count / total_document_count) * 100)}" for task_count in task_counts]}

        json_data = json.dumps(data)

        context={'supervisor' : supervisor,
             'offre':offre,  
             'tasks':tasks,
             'task_counts':task_counts,
             'colors':colors,
             'task_colors':task_colors,
             'json_data':json_data
}

            
             
        return render(request, 'supervisor/dashboard.html' , context)

            

    except Http404:
            return render(request, 'stagiaire/error.html',status=404)
