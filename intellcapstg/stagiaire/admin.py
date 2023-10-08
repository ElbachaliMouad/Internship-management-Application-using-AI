from django.contrib import admin


from .models import  Stagiaire, Offre ,Supervisor,Document,Task,Fileresquest,Filesrespond
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class StagiaireAdmin(admin.ModelAdmin):
    list_display = ('stagiaire_id', 'last_Name','fisrt_Name','school','phone',
    'motivation','niveau','image','cv','status','offre_stage')


admin.site.register(Stagiaire, StagiaireAdmin)

class OffreAdmin(admin.ModelAdmin):
    list_display=('id', 'owner_id','domaine','mission','description',
    'skills_needed','dure','niveau_etude','count','valable','date_of_expiry','demande','accepted')


admin.site.register(Offre, OffreAdmin)


class SupervisorAdmin(admin.ModelAdmin):
    list_display=('supervisor_id', 'count_offre','count_demande')


admin.site.register(Supervisor, SupervisorAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display=('owner', 'title','date_upload','content','task_root')


admin.site.register(Document, DocumentAdmin)



class TaskAdmin(admin.ModelAdmin):
    list_display=('task_offre', 'task_Name','date_of_expiry','number_duc')


admin.site.register(Task, TaskAdmin)


class FileresquestAdmin(admin.ModelAdmin):
    list_display=('owner', 'title','content','status','description')
admin.site.register(Fileresquest, FileresquestAdmin)


class FilesrespondAdmin(admin.ModelAdmin):
    list_display=('file_request','title','content','description')

admin.site.register(Filesrespond, FilesrespondAdmin)

