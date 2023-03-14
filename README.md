<h1 align="center">
LITReview<br>Django Web Application<br>
<img alt="LITReview logo" src="./static/media/LITReview_Logo.png" width="224px"/><br/>
</h1>

## Introduction
LITReview is a (fictional - for education purposes) start-up that aims to release a product that enables a community of users to review books and literature on demand.

This application is a MVP (minimum viable product))

## Installation
To use this program:
- Clone this project to your local disk.
- Create and open a virtual environment:
```bash
$ python3 -m venv env
$ source env/bin/activate 
```
- Install all the packages required in [requirements.txt](requirements.txt).
```bash
$ pip install -r requirements.txt
```
- Run the server through the console.
```bash
$ python3 manage.py runserver
```
- Open localhost on your browser: http://127.0.0.1:8000/

## How to use the Web Application
### Sign up and Log in
First, a user needs to sign up and log in to the application.

Only a username and a password are required.
The password must contain at least 8 characters.
### Navigation
A navigation bar allows to navigate through the pages of the application:
- [Feed](#Feed)
- [Posts](#Posts)
- [Following](#Following)
- [Logout](#Logout)

The navigation bar is always visible when the user scrolls down.

For smaller screen, the options collapse into a dropdown menu with a burger button.
### Feed
The first page the user sees is their feed. 
The feed shows:
- all the users own tickets and reviews, 
- the ticket and reviews of the other user they follow, 
- and all the reviews of their own tickets, 
even if they don't follow the author.

From the feed, the user can:
- create a new ticket to request a review of a book or literature article,
- post a review of a book or article that does not have a ticket yet (the ticket will be created in the process),
- post a review from a ticket in their feed

Once a user has posted a review, they are not able to post another review on the same ticket.
### Posts
This page allows the user to edit or delete their own posts, tickets and reviews.

Deleting a ticket will delete all the associated reviews.

### Following
On this page, the user can enter other users' username to follow them.

They can see the list of users they follow, and are able to unfollow them.

They can also see the list of their own followers

For testing, a few users have been created with content. Feel free to follow them and respond to their tickets:
  - book_reviewer
  - super_review
  - litreviewer

### Logout
The Logout button is located in the dropdown menu with the user's username.

Once the user logs out, they are properly notified and invited to log again, if they want.

## Ideas for future developments

### Time zone
**Currently:** the date and time are displayed in the UTC time zone.
<br>
**Goal:** display date and time according to the user's timezone.

### Discover new users
**Currently:** a user can only follow another user if they know their username.
<br>
**Goal:** allow user to discover other users to initiate relationships.

### Respond to reviews
**Currently:** no comment is allowed on reviews.
<br>
**Goal:** allow user to respond to a review, to open interactions between users.

### See all reviews of a same ticket at once
**Currently:** tickets and reviews are only sorted by date/time of creation.
<br>
**Goal:** give the ability to aggregate all reviews of a same ticket to help reading through them.

### Look for tickets and reviews
**Currently:** a user can find a ticket or a review by scrolling their feed.
<br>
**Goal:** add a search engine to quickly find a ticket or a review.
