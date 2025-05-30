from datetime import date
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from backend.models import Loan, Fine, Reservation, Book
from frontend.forms import RegisterForm, LoginForm

# Create your views here.
def home(request):
    return render(request, "frontend/home.html")

def books_list(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, "frontend/books.html", context)

# Member Registration
def member_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('member_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'frontend/register.html', {'form': form})

# Member Login
def member_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('member_dashboard')
    else:
        form = LoginForm()
    return render(request, 'frontend/login.html', {'form': form})


# Logout
def member_logout(request):
    logout(request)
    return redirect('login')

# Dashboard (Optional)
@login_required
def member_dashboard(request):
    user = request.user
    total_book_loans = Loan.objects.filter(member_id=user).count()
    total_fine = Fine.objects.filter(member=user).aggregate(total=Sum('fine_amount'))['total'] or 0
    books_reserved = Reservation.objects.filter(member=user).count()
    context = {
        'total_book_loans': total_book_loans,
        'total_fine': total_fine,
        'books_reserved': books_reserved,
    }
    return render(request, 'frontend/dashboard.html', context)

# List of Loaned Books
@login_required
def loaned_books(request):
    loans = Loan.objects.filter(member=request.user)
    return render(request, 'frontend/loaned_books.html', {'loans': loans})

# List of Fines
@login_required
def fines_view(request):
    fines = Fine.objects.filter(member=request.user)
    return render(request, 'frontend/fines.html', {'fines': fines})


# View Reservations
@login_required
def reservations_view(request):
    reservations = Reservation.objects.filter(member=request.user)
    return render(request, 'frontend/reservations.html', {'reservations': reservations})


# Book Reservation
@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Reservation.objects.create(
        book=book,
        member=request.user,
        reservation_date=date.today(),
    )
    return redirect('reservations')