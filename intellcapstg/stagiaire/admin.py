from django.contrib import admin


from .models import  Stagiaire, Offre ,Supervisor
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class StagiaireAdmin(admin.ModelAdmin):
    list_display = ('stagiaire_id', 'last_Name','fisrt_Name','school','phone',
    'motivation','niveau','image','cv','status')


admin.site.register(Stagiaire, StagiaireAdmin)

class OffreAdmin(admin.ModelAdmin):
    list_display=('id', 'owner_id','domaine','mission','description',
    'skills_needed','dure','niveau_etude','count','valable')


admin.site.register(Offre, OffreAdmin)


class SupervisorAdmin(admin.ModelAdmin):
    list_display=('supervisor_id', 'count_offre','count_demande')


admin.site.register(Supervisor, SupervisorAdmin)


