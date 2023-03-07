from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models


@login_required
def home_page(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all().exclude(review__in=reviews)

    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda x: x.time_created,
                                 reverse=True)
    return render(request,
                  'reviews/home_page.html',
                  context={'tickets_and_reviews': tickets_and_reviews})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request,
                  'reviews/create_ticket.html',
                  context={'form': form})


@login_required
def write_review_from_ticket(request, ticket_id):
    form = forms.ReviewForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    return render(request,
                  'reviews/write_review.html',
                  context={'form': form,
                           'ticket': ticket})


@login_required
def create_ticket_and_review(request):
    pass


@login_required
def view_own_posts(request):
    pass
