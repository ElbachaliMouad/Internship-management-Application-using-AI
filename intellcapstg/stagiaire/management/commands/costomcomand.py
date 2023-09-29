from django.core.management.base import BaseCommand, CommandError
import datetime
import json
from django.contrib.auth.models import User 
from django.shortcuts import render,redirect,get_object_or_404

from stagiaire.models  import Offre ,Supervisor
# from stagiaire.models import User
class Command(BaseCommand):
    #hhg
    def handle(self, *args, **options):
        json_file_path = r'C:\Users\hp\Desktop\estage\intellcapstg\stagiaire\management\commands\data.json'
        userr=get_object_or_404(User, username='mouad')
        supervis=get_object_or_404(Supervisor, supervisor_id=userr)
        print(supervis)
        with open(json_file_path, 'r' , encoding='utf-8') as json_file:
            data=json.load(json_file)
            for item in data:
                offre=Offre(owner=supervis,
                            domaine=item['domain'],
                            mission=item['mission'],
                            description=item['description'],
                            skills_needed=item['skills_needed'],
                            niveau_etude=item['education_level'],
                            dure=item['duration'])
                offre.save()



