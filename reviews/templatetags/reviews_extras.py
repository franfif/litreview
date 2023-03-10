from django import template

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if context['user'] == user:
        return 'You'
    return user.username


@register.filter
def stars(review):
    return review.get_rating_display()
