from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from vendor.forms import VendorForm


def registerUser(request):
    if request.method == 'POST':
        form = UserForm()
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully!")
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)


    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                            password=password)
            user.role = User.RESTARAUNT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerVendor')
        else:
            print(form.errors, v_form.errors)

    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        "form": form,
        "v_form": v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)
