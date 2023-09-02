from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 
import hashlib
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver



class Supervisor(models.Model):
    supervisor_id=models.ForeignKey(User, on_delete=models.CASCADE)
    count_offre=models.IntegerField(default=0)
    count_demande=models.IntegerField(default=0)

    class Meta:
        db_table = 'supervisor'

    def __str__(self):
         return (self.supervisor_id.username )



class Stagiaire(models.Model):
    stagiaire_id=models.ForeignKey(User, on_delete=models.CASCADE)
    last_Name=models.CharField(max_length=255,blank=True,null=True)
    fisrt_Name=models.CharField(max_length=255,blank=True,null=True)
    school=models.CharField(max_length=255,blank=True,null=True)
    phone=models.CharField(max_length=20,blank=True,null=True)
    motivation=models.TextField(null=True,blank=True)
    niveau=models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='photos/', default='photos/default.jpg',blank=True,null=True)
    cv=models.FileField(upload_to='pdfs/',blank=True,null=True)
    status=models.IntegerField(default=0)

   
    class Meta:
        db_table = 'stagiaire'

    def __str__(self):
         return (self.stagiaire_id.username )
    
@receiver(pre_save, sender=Stagiaire)
def validate_your_field(sender, instance, **kwargs):
    allowed_values = [0, 1, 2]
    if instance.status not in allowed_values:
        raise ValidationError('Invalid value. Only 0, 1, or 2 are allowed.')
    if instance.stagiaire_id.is_superuser:
        raise ValidationError('only stagiaire can acces')



    

  
class Offre(models.Model):
    owner = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    domaine = models.CharField(max_length=255,blank=True,null=True)
    mission = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    skills_needed = models.CharField(max_length=255,blank=True,null=True)
    dure = models.CharField(max_length=255,blank=True,null=True)
    niveau_etude=models.CharField(max_length=255,blank=True,null=True)
    count=models.IntegerField(default=0)
    valable=models.IntegerField(default=0)

    class Meta:
        db_table = 'offre'
    def __str__(self):
         return (self.owner.supervisor_id.username )
    
    


    
@receiver(pre_save, sender=Offre)
def validate_your_field(sender, instance, **kwargs):
    allowed_values = [0, 1]
    if instance.valable not in allowed_values:
        raise ValidationError('Invalid value. Only 0, 1, or 2 are allowed.')
    if instance.count==0:
        instance.valable=0







