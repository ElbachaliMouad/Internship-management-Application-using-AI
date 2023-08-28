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
    supervisor_id=models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    count_offre=models.IntegerField(default=0)
    count_demande=models.IntegerField(default=0)

    class Meta:
        db_table = 'supervisor'

    



class Stagiaire(models.Model):
    stagiaire_id=models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    last_Name=models.CharField(max_length=255)
    fisrt_Name=models.CharField(max_length=255)
    school=models.CharField(max_length=255)
    phone=models.CharField(max_length=20)
    motivation=models.TextField()
    niveau=models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/', default='photos/default.jpg')
    cv=models.FileField(upload_to='pdfs/')
    status=models.IntegerField(default=0)

   
    class Meta:
        db_table = 'stagiaire'

    def __str__(self):
         return (self.last_Name )
    
@receiver(pre_save, sender=Stagiaire)
def validate_your_field(sender, instance, **kwargs):
    allowed_values = [0, 1, 2]
    if instance.status not in allowed_values:
        raise ValidationError('Invalid value. Only 0, 1, or 2 are allowed.')
    

    

  
class Offre(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Supervisor, on_delete=models.CASCADE, to_field='id')
    domaine = models.CharField(max_length=255)
    mission = models.CharField(max_length=255)
    description = models.TextField()
    skills_needed = models.CharField(max_length=255)
    dure = models.CharField(max_length=255)
    niveau_etude=models.CharField(max_length=255)
    count=models.IntegerField()
    valable=models.IntegerField(default=1)

    class Meta:
        db_table = 'offre'
    def __str__(self):
         return (self.mission )
    
    


    
@receiver(pre_save, sender=Offre)
def validate_your_field(sender, instance, **kwargs):
    allowed_values = [0, 1]
    if instance.valable not in allowed_values:
        raise ValidationError('Invalid value. Only 0, 1, or 2 are allowed.')
    if instance.count==0:
        instance.valable=0







