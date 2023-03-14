from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, Div

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


FORM_CLASS = 'form-signin mx-auto'


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = FORM_CLASS
        self.helper.add_input(Submit('submit', 'Log In'))

    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63,
                               widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = FORM_CLASS
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']


class FollowUsersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = FORM_CLASS
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('follow_user', wrapper_class='col mb-0',
                      placeholder="Enter a username"),
                Submit('submit', '🐵 Follow', css_class='col-auto'),
                css_class='row mb-3'
            )
        )
        # self.helper.add_input()

    class Meta:
        model = get_user_model()
        fields = []

    follow_user = forms.CharField(max_length=63)


class UnfollowUsersForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = []

    unfollow_user = forms.CharField(widget=forms.HiddenInput,
                                    initial="")
