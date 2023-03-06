from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def home_page(request):
    hello_world = "Hellow World!"
    return render(request,
                  'reviews/home_page.html',
                  context={'greetings': hello_world})
