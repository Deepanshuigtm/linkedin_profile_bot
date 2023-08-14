from django import forms

class ReviewForm(forms.Form):
    Username = forms.CharField(label="Your Linkedin Username",max_length=100,error_messages={
        "required": "Your name must not be empty",
        "max_length": "Please enter a shorter name",
    })
    Password = forms.CharField(widget=forms.PasswordInput())
    persons_username = forms.CharField(label="Target Username",max_length=100,error_messages={
        "required": "Your name must not be empty",
        "max_length": "Please enter a shorter name",
    })