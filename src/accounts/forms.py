from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('User doesn\'t exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('User is not Active')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':'username'}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Account'}))
    email2 = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Email Account'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'password', 'id':'password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            raise forms.ValidationError("Email Must Match")

        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError("This Email has already been used.")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
