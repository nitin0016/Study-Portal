from django.urls import path
from .views import*
from django.contrib.auth import views as auth_views
urlpatterns = [path('',home,name='home'),
               path('notes',notes,name='notes'),
               path('delete_note/<int:pk>',delete_note,name='delete_note'),
               path('notes_detail/<int:pk>',notedetails,name='notes_detail'),
               path('homework',homework,name='homework'),
               path('update_homework/<int:pk>',update_homework,name='updatehomework'),
               path('delete_homework/<int:pk>',delete_homework,name='deletehomework'),
               path('youtube',youtube,name='youtube'),
               path('todo',todo,name='todo'),
               path('updatetodo/<int:pk>',updatetodo,name='updatetodo'),
               path('deletetodo/<int:pk>',deletetodo,name='deletetodo'),
               path('books',books,name='books'),
               path('dictionary',dictionary,name='dictionary'),
               path('WikiPedia',WikiPedia,name='WikiPedia'),


               path('register',register,name='register'),
               path('login',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
               path('profile',profile,name='profile'),
               path('logout',logout,name='logout'),
               
]
