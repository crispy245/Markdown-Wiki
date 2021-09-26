from django import forms
from django.db.models.base import Model
from django.forms import fields, widgets
from django.forms.models import ModelForm
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields='__all__'
        widgets = {
            'title' : widgets.TextInput(attrs={
            'autocomplete':'off','style': 'width: 500px;', 'class': 'form-control'}),
            'body' : widgets.Textarea(attrs={
            'autocomplete':'off','style': 'width: 900px;', 'class': 'form-control'})
        }
        def __str__(self):
            return self.title

    