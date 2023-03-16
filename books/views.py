from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.contrib.auth.models import User
from .models import Book , Downloads
from django.contrib.auth import authenticate, login
from django.db.models import Q

def home(request):
    return render(request, 'base.html')

def book_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        books = Book.objects.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books, 'search_query': search_query})


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmPassword")
        if pass1 != pass2:
            return HttpResponse("Your PASSWORD and CONFIRM PASSWORD are not same")
        else:
            try:
                my_user = User.objects.create_user(uname,email,pass1)
                my_user.save()
                messages.success(request, 'You have successfully signed up!')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Username already exists, please choose a different username')
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')



@login_required
def book_upload(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_upload.html', {'form': form})


@login_required
def book_download(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the user has already downloaded the book
    if Downloads.objects.filter(book=book, user=request.user).exists():
        messages.warning(request, 'You have already downloaded this book.')
    else:
        download = Downloads(book=book, user=request.user)
        download.save()
        messages.success(request, f'You have downloaded "{book.title}" successfully.')

    return render(request, 'book_download.html', {'book': book})



@login_required
def library(request):
    user_downloads = Downloads.objects.filter(user=request.user)
    user_books = [download.book for download in user_downloads]
    context = {
        'user_books': user_books,
    }
    return render(request, 'library.html', context)


