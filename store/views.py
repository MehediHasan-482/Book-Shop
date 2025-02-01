from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from account.models import Subscription
from .models import Category, Writer, Book, Review, Slider
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import RegistrationForm, ReviewForm


def index(request):
    # Fetch the most recently published books (new books)
    newpublished = Book.objects.order_by('-created')[:15]

    # Fetch the slides (slider items)
    slide = Slider.objects.order_by('-created')[:4]

    # Fetch the top selling books, ordered by the most reviews (totalreview)
    top_selling = Book.objects.order_by('-totalreview')[:7]  

    context = {
        "newbooks": newpublished,
        "slide": slide,
        "top_reviewed_books": top_selling  
    }

    return render(request, 'store/index.html', context)



def signin(request):
    # Redirect authenticated users to the index page
    if request.user.is_authenticated:
        return redirect('store:index')

    # Handle form submission
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')
        auth = authenticate(request, username=username, password=password)
        if auth is not None:
            login(request, auth)
            return redirect('store:index')
        else:
            messages.error(request, "Username and password don't match.")

    # Render the login page
    return render(request, 'store/login.html')	


def signout(request):
    logout(request)
    return redirect('store:index')	


def registration(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('store:signin')

	return render(request, 'store/signup.html', {"form": form})

def payment(request):
    return render(request, 'store/payment.html')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_preview.html', {'book': book})


def get_book(request, id):
    form = ReviewForm(request.POST or None)
    book = get_object_or_404(Book, id=id)
    rbooks = Book.objects.filter(category_id=book.category.id)
    r_review = Review.objects.filter(book_id=id).order_by('-created')

    paginator = Paginator(r_review, 4)
    page = request.GET.get('page')
    rreview = paginator.get_page(page)

    # Check if the user has an active subscription
    has_active_subscription = False
    if request.user.is_authenticated:
        has_active_subscription = Subscription.objects.filter(
            user=request.user,
            end_date__gte=date.today()  
        ).exists()

    # Handle the form submission for a review
    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                temp = form.save(commit=False)
                temp.customer = User.objects.get(id=request.user.id)
                temp.book = book
                # Increase total review count and rating
                book.totalreview += 1
                book.totalrating += int(request.POST.get('review_star'))
                form.save()  
                book.save()

                messages.success(request, "Review Added Successfully")
                form = ReviewForm()  # Reset the form
        else:
            messages.error(request, "You need to log in first.")

    context = {
        "book": book,
        "rbooks": rbooks,
        "form": form,
        "rreview": rreview,
        "has_active_subscription": has_active_subscription  
    }
    
    return render(request, "store/book.html", context)


def get_books(request):
    books_ = Book.objects.all().order_by('-created')
    paginator = Paginator(books_, 10)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, "store/category.html", {"book":books})

def get_book_category(request, id):
    book_ = Book.objects.filter(category_id=id)
    paginator = Paginator(book_, 10)
    page = request.GET.get('page')
    book = paginator.get_page(page)
    return render(request, "store/category.html", {"book":book})

def get_writer(request, id):
    wrt = get_object_or_404(Writer, id=id)
    book = Book.objects.filter(writer_id=wrt.id)
    context = {
        "wrt": wrt,
        "book": book
    }
    return render(request, "store/writer.html", context)

