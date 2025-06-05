from django.shortcuts import render, redirect
from django.contrib.auth import login  # 'django.contrib.auth.login' imported but unused
from .forms import RegistrationForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Local variable `user` is assigned to but never used
            # login(request, user) # Optional: Log the user in immediately after registration
            return redirect(
                "accounts:login"
            )  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})