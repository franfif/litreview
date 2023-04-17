from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value, BooleanField
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models


@login_required
def feed(request):
    # List all reviews if:
    #   the user wrote the review
    #   OR the user follows the review's author
    #   OR the user wrote the review's ticket
    # But only if the user already wrote a review for the same ticket
    reviews_reviewed = models.Review.objects.filter(
        (Q(user=request.user) |
         Q(user__in=request.user.follows.all()) |
         Q(ticket__user=request.user)) &
        Q(ticket__review__user=request.user)
    )
    # List all reviews if:
    #   the user follows the review's author
    #   OR the user wrote the review's ticket
    # But exclude all reviews when the user already wrote a review for the same ticket
    reviews_unreviewed = models.Review.objects.filter(
        (Q(user__in=request.user.follows.all()) |
         Q(ticket__user=request.user)) &
        ~Q(ticket__review__user=request.user)
    )
    # Merge the querySets
    reviews = chain(
        # Annotate the reviews as reviewed or unreviewed by the user
        reviews_reviewed.annotate(reviewed=Value(True, BooleanField())),
        reviews_unreviewed.annotate(reviewed=Value(False, BooleanField())))

    # List all tickets if:
    #   the user wrote the ticket
    #   OR the user follows the ticket's author
    # But only if the user already wrote a review for the tickets
    tickets_reviewed = models.Ticket.objects.filter(
        (Q(user=request.user) |
         Q(user__in=request.user.follows.all())) &
        Q(review__user=request.user)
    )
    # List all tickets if:
    #   the user wrote the ticket
    #   OR the user follows the ticket's author
    # But exclude all tickets when the user already wrote a review for them
    tickets_unreviewed = models.Ticket.objects.filter(
        (Q(user=request.user) |
         Q(user__in=request.user.follows.all())) &
        ~Q(review__user=request.user)
    )
    # Merge the querySets
    tickets = chain(
        # Annotate the tickets as reviewed or unreviewed by the user
        tickets_reviewed.annotate(reviewed=Value(True, BooleanField())),
        tickets_unreviewed.annotate(reviewed=Value(False, BooleanField())))

    # Order the tickets and reviews by time_created, most recent first
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
    reviews = ticket.review_set.all()
    for review in reviews:
        # The user already wrote a ticket
        if review.user == request.user:
            messages.warning(request,
                             "You already posted a review for this ticket. "
                             "You can edit your review here.")
            # Redirect the user to edit the ticket
            return redirect('edit_review', review.id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    # For any other request method than 'POST'
    return render(request,
                  'reviews/write_review.html',
                  context={'form': form,
                           'ticket': ticket})


@login_required
def create_ticket_and_review(request):
    # Use a form for each a ticket and a review
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            # Complete and save ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # Complete and save review
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
    reviews = reviews.annotate(editable=Value(True, BooleanField()))
    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(editable=Value(True, BooleanField()))

    # Merge and order the tickets and reviews by time_created, most recent first
    posts = sorted(chain(tickets, reviews),
                   key=lambda x: x.time_created,
                   reverse=True)

    return render(request,
                  'reviews/posts.html',
                  context={'posts': posts})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    # Only the author can edit a ticket
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
    # Only the author can edit a review
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
def delete_post(request, model_type, post_id):
    if model_type == 'Review':
        post_model = models.Review
    elif model_type == 'Ticket':
        post_model = models.Ticket
    else:
        # When the item to delete is neither a Review nor a Ticket
        messages.error(request,
                       'You are trying to delete something else than a '
                       'ticket or a review.')
        return redirect('posts')
    post = get_object_or_404(post_model, id=post_id)
    # The user is not allowed to delete a post they did not write
    if request.user != post.user:
        messages.error(request,
                       f"You don't have permission to delete this "
                       f"{model_type.lower()}.")
        return redirect('posts')
    if request.method == 'POST':
        post.delete()
        post_name = post.title if model_type == "Ticket" else post.headline
        messages.success(request,
                         f'The {model_type} {post_name} has been '
                         f'successfully deleted')
        return redirect('posts')
    return redirect('posts')
