from django import forms

class NewEntry(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    