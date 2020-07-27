from django.urls import path
from . import views 

urlpatterns = [
    # GET REQUEST
    path('', views.index), 
    path('books', views.books), 
    path('logout', views.logout), 
    path('book/<int:id>', views.show_book), 
    path('book/<int:id>/unlike', views.unlike), 
    path('book/<int:id>/like', views.like), 
    path('book/<int:id>/delete', views.delete_book), 
    # POST REQUEST   
    path('book/<int:id>/edit', views.edit_book), 
    path('login', views.login), 
    path('register', views.register), 
    path('add_book', views.add_book),
]
