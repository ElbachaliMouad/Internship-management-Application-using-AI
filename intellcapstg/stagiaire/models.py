from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete ,pre_delete
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 
import hashlib
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.exceptions import ValidationError

class Supervisor(models.Model):
    supervisor_id=models.ForeignKey(User, on_delete=models.CASCADE)
    count_offre=models.IntegerField(default=0)
    count_demande=models.IntegerField(default=0)

    class Meta:
        db_table = 'supervisor'

    def __str__(self):
         return (self.supervisor_id.username )



    

  
class Offre(models.Model):
    owner = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    domaine = models.CharField(max_length=255,blank=True,null=True)
    mission = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    skills_needed = models.CharField(max_length=255,blank=True,null=True)
    dure = models.CharField(max_length=255,blank=True,null=True)
    niveau_etude=models.CharField(max_length=255,blank=True,null=True)
    count=models.IntegerField(default=10)
    valable=models.IntegerField(default=1)
    date_of_expiry = models.DateTimeField(null=True, blank=True)
    demande=models.IntegerField(default=0)
    accepted=models.IntegerField(default=0)

    class Meta:
        db_table = 'offre'
    def __str__(self):
         return (f"{self.pk}" )
    
    

    
@receiver(pre_save, sender=Offre)
def validate_your_field(sender, instance, **kwargs):
    allowed_values = [0, 1]
    if instance.valable not in allowed_values:
        raise ValidationError('Invalid value. Only 0, 1, or 2 are allowed.')
    if instance.count==0:
        instance.valable=0
    if instance.date_of_expiry:
        if instance.date_of_expiry <= timezone.now():
            instance.valable=0
@receiver(pre_delete, sender=Offre)
def update_stagiaire_status(sender, instance, **kwargs):
    try:
        stagiaire = Stagiaire.objects.get(offre_stage=instance)
        stagiaire.status = 0
        stagiaire.save()
    except ObjectDoesNotExist:
        pass  


class Stagiaire(models.Model):
    stagiaire_id=models.ForeignKey(User, on_delete=models.CASCADE)
    last_Name=models.CharField(max_length=255,blank=True,default='')
    fisrt_Name=models.CharField(max_length=255,blank=True,default='')
    school=models.CharField(max_length=255,blank=True,default='')
    phone=models.CharField(max_length=20,blank=True,default='')
    motivation=models.TextField(null=True,blank=True,default='')
    niveau=models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='photos/', default='photos/default.jpg',)
    cv=models.FileField(upload_to='pdfs/',blank=True,null=True)
    status=models.IntegerField(default=0)
    offre_stage=models.ForeignKey(Offre, on_delete=models.SET_NULL,null=True)

   
    class Meta:
        db_table = 'stagiaire'

    def __str__(self):
         return (self.stagiaire_id.username )
    
@receiver(pre_save, sender=Stagiaire)
def validate_your_field(sender, instance, **kwargs):
    allowed_values = [0, 1, 2]
    if instance.status not in allowed_values:
        raise ValidationError('Invalid value. Only 0, 1, 2  are allowed.')
    
    if instance.stagiaire_id.is_superuser:
        raise ValidationError('only stagiaire can acces')
    if instance.status==0:
        instance.offre_stage=None
    if instance.offre_stage is None:
        instance.status==0





class Task(models.Model):
    task_offre=models.ForeignKey(Offre, on_delete=models.CASCADE,null=True)
    task_Name=models.CharField(max_length=255,blank=True,default='')
    date_of_expiry = models.DateTimeField(null=True, blank=True)
    number_duc=models.IntegerField(default=0)
    
    class Meta:
        db_table = 'task'

    def __str__(self):
         return (f"{self.pk}" )
    

    

class Document(models.Model):
    owner=models.ForeignKey(Stagiaire, on_delete=models.CASCADE,  limit_choices_to={'status': 2})
    title=models.CharField(max_length=255,blank=True,default='')
    date_upload = models.DateTimeField(null=True, blank=True )
    content=models.FileField(upload_to='documents/',blank=True,null=True)
    task_root=models.ForeignKey(Task, on_delete=models.CASCADE ,null=True)
    
    class Meta:
        db_table = 'document'

    def __str__(self):
         return (f"{self.pk}")
    
    
    
@receiver(pre_save, sender=Document)
def validate_your_field(sender, instance, **kwargs): 
   instance.task_root.number_duc+=1
   instance.date_upload=timezone.now()  
   if instance.task_root.date_of_expiry:
       if    instance.date_upload > instance.task_root.date_of_expiry:
        raise ValidationError('time out ')

       

class Fileresquest(models.Model):
    owner=models.ForeignKey(Stagiaire, on_delete=models.CASCADE,  limit_choices_to={'status': 2})
    title=models.CharField(max_length=255,blank=True,default='')
    description=models.TextField(null=True,blank=True)
    content=models.FileField(upload_to='filerequest/',blank=True,null=True)
    status=models.IntegerField(default=0)




    class Meta:
        db_table = 'Fileresquest'

    def __str__(self):
         return (f"{self.pk}")


class Filesrespond(models.Model):
    file_request=models.ForeignKey(Fileresquest, on_delete=models.SET_NULL,null=True  )
    content=models.FileField(upload_to='files/',blank=True,null=True)
    title=models.CharField(max_length=255,blank=True,default='')
    description=models.TextField(null=True,blank=True)


    class Meta:
        db_table = 'Filesrespond'

    def __str__(self):
         return (f"{self.pk}")


      
