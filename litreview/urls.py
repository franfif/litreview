from django.contrib import admin
from django.contrib.auth.views import LoginView, \
    LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

import authentication.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='authentication/logout.html',
    ), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path('home/', reviews.views.home_page, name='home'),
]
