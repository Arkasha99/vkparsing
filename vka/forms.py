from django import forms

class NewForm(forms.Form):
    name = forms.CharField(max_length=40)