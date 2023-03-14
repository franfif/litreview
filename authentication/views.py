from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from authentication import forms, models


def login_page(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request,
                               "Login failed! Username or password incorrect.")

    form = forms.LoginForm()
    return render(request,
                  'authentication/login.html',
                  context={'form': form})


def signup_page(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.SignUpForm()
    return render(request,
                  'authentication/signup.html',
                  context={'form': form})


@login_required
def following_page(request):
    follow_form = forms.FollowUsersForm()
    unfollow_form = forms.UnfollowUsersForm()
    followed = request.user.follows.all()
    followers = models.User.objects.filter(follows__id=request.user.id)
    if request.method == 'POST':
        if 'follow_user' in request.POST:
            follow_form = forms.FollowUsersForm(request.POST)
            if follow_form.is_valid():
                username = follow_form.cleaned_data['follow_user']
                try:
                    user_to_follow = models.User.objects.get(username=username)
                    if user_to_follow and user_to_follow != request.user:
                        request.user.follows.add(user_to_follow)
                        return redirect('following')
                except models.User.DoesNotExist:
                    messages.error(
                        request,
                        f'There is no user with the username {username}.')

        if 'unfollow_user' in request.POST:
            unfollow_form = forms.UnfollowUsersForm(request.POST)
            if unfollow_form.is_valid():
                username = unfollow_form.cleaned_data['unfollow_user']
                try:
                    user_to_unfollow = models.User.objects.get(username=username)
                    if user_to_unfollow in followed:
                        request.user.follows.remove(user_to_unfollow)
                        return redirect('following')
                except models.User.DoesNotExist:
                    messages.error(
                        request,
                        f'There is no user with the username {username}.')

    context = {'follow_form': follow_form,
               'unfollow_form': unfollow_form,
               'followed': followed,
               'followers': followers}
    return render(request,
                  'authentication/following.html',
                  context=context)
