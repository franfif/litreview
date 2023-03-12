from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div

from django import forms

from . import models


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Div(
                HTML("""{% if ticket.image %}<img class="col-auto" 
                     src="{{ ticket.image.url }}">{% endif %}"""),
                Field('image', wrapper_class='col'),
                css_class='row mb-3'
            )
        )

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
