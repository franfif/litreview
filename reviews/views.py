from django.shortcuts import render


def home_page(request):
    hello_world = "Hellow World!"
    return render(request,
                  'reviews/home_page.html',
                  context={'greetings': hello_world})
