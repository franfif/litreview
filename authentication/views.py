from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from authentication import forms


def signup_page(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.post)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.SignUpForm()
    return render(request,
                  'authentication/signup.html',
                  context={'form': form})
