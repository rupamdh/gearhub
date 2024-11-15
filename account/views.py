from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import Wallet, User
from shop.models import ServiceCenter
from .utils import generate_signup_coupon


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = generate_signup_coupon(user.first_name, user.last_name)
            user.username = username
            user.save()
            login(request, user)
            coupon = request.POST['coupon']
            root_user = User.objects.get(username=coupon)
            Wallet.objects.create(user=root_user, type='CR', amount=20, remark='Signup code used by someone')
            Wallet.objects.create(user=user, type='CR', amount=20, remark='Signup bonus')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    context = {
        'form' : form
    }
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    centers = ServiceCenter.objects.filter(user=request.user)
    total_center = centers.count()

    context = {
        'centers' : centers,
        'total_center' : total_center
    }
    return render(request, 'dashboard.html', context)