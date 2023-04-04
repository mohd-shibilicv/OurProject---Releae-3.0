from django import forms
from App.models import Customer
from django.contrib.auth.models import User


class Customerform(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = Customer
        fields = "__all__"

# Reply mails
class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
    cc = forms.EmailField(required=False)
    subject = forms.CharField(max_length=100)
    attach = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    message = forms.CharField(required=True, widget=forms.Textarea)


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}), max_length=30, required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'}), max_length=100, required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }