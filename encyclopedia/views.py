import re
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
from .forms import NewEntry
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def search(request):
    searched = request.GET.get('q',)
    if(util.get_entry(searched) is not None):
        return HttpResponseRedirect(reverse("entry",kwargs={'entry':searched}))
    elif (searched == ""):
        return HttpResponseRedirect(reverse("index"))
    else:
        return similar_entries(request,searched)



def entry(request,entry):
    if(util.get_entry(entry) is not None):
        return render(request, "encyclopedia/entry.html",
        {"entry":markdown2.markdown(util.get_entry(entry)),
         "found":True})
    else:
        return render(request,"encyclopedia/entry.html",
        {"found":False})


def similar_entries(request, searched):
    similar_entries_list = []
    for entry in util.list_entries():
        print(entry)
        if searched.upper() in entry.upper():
            similar_entries_list.append(entry)
    return render(request,"encyclopedia/similar_entries.html",
    {'entries':similar_entries_list,
     'searched':searched})

def new_entry(request):
    if request.method == 'POST':
        form = NewEntry(request.POST)
        if form.is_valid():
            print(form.cleaned_data['title'])
    return render(request,'encyclopedia/new_entry.html',
    {'form':NewEntry()})


def non_existant(request, any):
    return HttpResponseRedirect(reverse("index"))
