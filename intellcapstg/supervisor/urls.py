from django.urls import path ,include
from . import views 

urlpatterns=[
    path('index',views.index,name='index'),

     path('about',views.about,name='about'),

    path('contact',views.contact,name='contact'),

    path('signin',views.signin,name='signin'),

    path('signup',views.signup,name='signup'),

    path('activitemain',views.activitemain,name='activitemain'),

    path('document',views.document, name='document'),

    path('forum',views.forum,name='forum'),

    path('postuler',views.postuler,name='postuler'),

    path('profile',views.profile, name='profile'),

    path('profileinfo',views.profileinfo, name='profileinfo'),

    path('profilepass',views.profilepass, name='profilepass'),


    path('search',views.search, name='search'),]







