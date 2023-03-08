from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models


@login_required
def feed(request):
    reviews = models.Review.objects.filter(
        Q(user=request.user) |
        Q(user__in=request.user.follows.all()) |
        Q(ticket__user=request.user)
    )
    tickets = models.Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__in=request.user.follows.all())
    )

    posts = sorted(chain(tickets, reviews),
                   key=lambda x: x.time_created,
                   reverse=True)
    return render(request,
                  'reviews/feed.html',
                  context={'posts': posts})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
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
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
                  'reviews/write_review.html',
                  context={'form': form,
                           'ticket': ticket})


@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
                  'reviews/create_ticket_review.html',
                  context={'ticket_form': ticket_form,
                           'review_form': review_form})


@login_required
def view_posts(request):
    reviews = models.Review.objects.filter(user=request.user)
    tickets = models.Ticket.objects.filter(user=request.user)

    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda x: x.time_created,
                                 reverse=True)
    return render(request,
                  'reviews/posts.html',
                  context={'tickets_and_reviews': tickets_and_reviews})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user != ticket.user:
        messages.error(request,
                       "You don't have permission to edit this ticket.")
        return redirect('posts')
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES,
                                instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request,
                  'reviews/edit_ticket.html',
                  context={'ticket': ticket,
                           'form': form})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.user != review.user:
        messages.error(request,
                       "You don't have permission to edit this review.")
        return redirect('posts')
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request,
                  'reviews/edit_review.html',
                  context={'review': review,
                           'form': form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user != ticket.user:
        messages.error(request,
                       "You don't have permission to delete this ticket.")
        return redirect('posts')
    if request.method == 'POST':
        ticket.delete()
        messages.success(request,
                         f'The ticket {ticket.title} has been successfully deleted')
        return redirect('posts')
    return render('posts')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.user != review.user:
        messages.error(request,
                       "You don't have permission to delete this review.")
        return redirect('posts')
    if request.method == 'POST':
        review.delete()
        messages.success(request,
                         f'The review {review.headline} has been successfully deleted')
        return redirect('posts')
    return render('posts')
