from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import datetime
from .models import User, Book
from django.http import Http404
import bcrypt


def index(request):
    return render(request, "index.html")

############## LOGIN & REGISTER AREA #################

def login(request):
    userEmail = User.objects.filter(email=request.POST['email'])
    print(request.POST)
    pass1 = False
    emai1 = False

    if userEmail:
        emai1 = True
        logged_user = userEmail[0]
        password_check = bcrypt.checkpw(
            request.POST['password'].encode(), logged_user.password.encode())
        if password_check:
            pass1 = True
            request.session['userid'] = logged_user.id
            request.session['login'] = True
            print(request.session['userid'])
            return redirect('/books')
    context = {
        'password': pass1,
        'email': emai1
    }
    errors = User.objects.login_validator(context)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)

    return redirect('/')

def register(request):
    errors = User.objects.register_validator(request.POST)
    print(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        registered_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash)
        request.session['userid'] = registered_user.id
        request.session['register'] = True
        print(request.POST['first_name']+" "+request.POST['last_name']+' just joined the party!')
        return redirect('/books')
    return redirect('/')

def logout(request):
    if request.session['userid']:
        request.session['userid'] = None
        request.session['register'] = False
        request.session['login'] = False
        return redirect('/')
    else:
        raise Http404("NOT ALLOWED")

############## BOOOOOOOKS AREA #################

def books(request):
    if request.session['userid']:
        id = request.session['userid']
        user = User.objects.get(id=id)
        all_books = Book.objects.all()
        fav_books = Book.objects.first().favorites.all()
        context = {
            'user': user,
            'book': all_books,
            'fav': fav_books,
        }
        print(fav_books)
        return render(request, "main.html", context)
    else:
        raise Http404("NOT ALLOWED")
    


def show_book(request, id):
    if request.session['userid']: 
        book_id = id
        user_id = request.session['userid']
        user = User.objects.get(id=user_id)
        view_book = Book.objects.get(id=book_id)
        fav_books = Book.objects.first().favorites.all()
        request.session['favored'] = False
        for favbook in fav_books:
            if favbook.id == user.id:
                request.session['favored'] = True
                print(fav_books)
        context = {
            'book': view_book,
            'user': user,
            'favorite': fav_books,   
        }
        return render(request, "view_book.html", context)
    else:
        raise Http404("NOT ALLOWED")

def edit_book(request, id):
    if request.session['userid']:
        book_id = int(id)
        errors = User.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
                return redirect(f'/book/{book_id}')
        else:  
            view_book = Book.objects.get(id=book_id)
            title = request.POST['title']
            desc = request.POST['desc']
            view_book.title = title
            view_book.desc = desc
            view_book.save()
            return redirect(f'/book/{book_id}')
    else:
        raise Http404("NOT ALLOWED")

def add_book(request):
    if request.session['userid']:
        errors = User.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/books')
        else:
            id = request.session['userid']
            user = User.objects.get(id=id)
            title = request.POST['title']
            desc = request.POST['desc']
            book = Book.objects.create(
                title=title,
                desc=desc,
                uploaded_by=user)
            book.favorites.add(user)
        return redirect('/books')
    else:
        raise Http404("NOT ALLOWED")

# BUTTON SECTION

def unlike(request, id):
    if request.session['userid']:
        book_id = int(id)
        user_id = request.session['userid']
        this_user = User.objects.get(id=user_id)
        this_book = Book.objects.get(id=book_id)
        this_book.favorites.remove(this_user)
        print(f" We Unliked =>>>> {this_book.title}")
        return redirect('/books')
    else:
        raise Http404("NOT ALLOWED")

def like(request, id):
    if request.session['userid']:
        book_id = int(id)
        user_id = request.session['userid']
        this_user = User.objects.get(id=user_id)
        this_book = Book.objects.get(id=book_id)
        this_book.favorites.add(this_user)
        print(f" We liked =>>>> {this_book.title}")
        return redirect('/books')
    else:
        raise Http404("NOT ALLOWED")

def delete_book(request, id):
    this_id = id
    Book.objects.get(id=this_id).delete()
    print(request.POST)
    return redirect('/books')

