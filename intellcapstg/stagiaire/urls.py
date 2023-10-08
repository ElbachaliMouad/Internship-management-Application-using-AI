from django.urls import path ,include
from . import views 
from .views import download_file,download_filee,download_filerespond


urlpatterns=[
    path('',views.index,name='index'),


     path('about',views.about,name='about'),

    path('contact',views.contact,name='contact'),


    path('signin',views.signin,name='signin'),

    path('signup',views.signup,name='signup'),


    path('workspace/<int:id>/activitemain',views.activitemain,name='activitemain'),


    path('workspace/<int:id>/document',views.document, name='document'),


    path('workspace/<int:id>/forum',views.forum,name='forum'),


    path('postuler/',views.postuler,name='postuler'),
    


    path('offre/<int:id>',views.offre,name='offre'),


    path('profile/canditature',views.profile, name='profile'),


    path('profile/profileinfo',views.profileinfo, name='profileinfo'),


    path('profile/profilepass',views.profilepass, name='profilepass'),


    path('search',views.search, name='search'),
    
    
    
    
    ######################################################################
    
    path('supervisor/signin/', views.supersignin, name='supersignin'),


    path('supervisor/activiteadmin/', views.superoffre, name='superoffre'),


    path('supervisor/profile/', views.superprofile, name='superprofile'),

        path('supervisor/search_admin/', views.search_admin, name='search_admin'),



  ##################################################################################

    path('log_out_stagiaire',views.log_out_stagiaire, name='log_out_stagiaire'),
   
    path('delete_doc/<int:id>',views.delete_doc, name='delete_doc'),

    path('download/<int:pk>/', download_file, name='download_file'),

   
       path('download_filerespond/<int:pk>/', download_filerespond, name='download_filerespond'),

           path('download_filee/<int:pk>/', download_filee, name='download_filee'),

 
    path('delete_filee/<int:id>',views.delete_filee, name='delete_filee'),

    path('dash',views.dash, name='dash')

    ]







