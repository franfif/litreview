from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

import authentication.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', LogoutView.as_view(
        template_name='authentication/logout.html',
    ), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path('following/', authentication.views.following_page, name='following'),

    path('feed/', reviews.views.feed, name='feed'),
    path('tickets/create_ticket/',
         reviews.views.create_ticket, name='create_ticket'),
    path('tickets/<int:ticket_id>/write_review/',
         reviews.views.write_review_from_ticket, name='write_review'),
    path('tickets/create_ticket_review/',
         reviews.views.create_ticket_and_review,
         name='create_ticket_review'),

    path('posts/', reviews.views.view_posts, name='posts'),

    path('tickets/<int:ticket_id>/edit_ticket/',
         reviews.views.edit_ticket, name='edit_ticket'),
    path('reviews/<int:review_id>/edit_review/',
         reviews.views.edit_review, name='edit_review'),

    path('tickets/<str:model_type>/<int:post_id>/delete/',
         reviews.views.delete_post, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
