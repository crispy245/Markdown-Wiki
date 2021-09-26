import re
from django.forms.forms import Form
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import markdown2
from .forms import EntryForm
from . import util
import random



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
    if 'edit' in request.POST:
        return HttpResponseRedirect(reverse("edit",kwargs={'entry':entry}))
    if(util.get_entry(entry) is not None):
        return render(request, "encyclopedia/entry.html",
        {"entry":markdown2.markdown(util.get_entry(entry)),
         "title":entry,
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


def succes(request):
    return_message = ""
    found = False
    if request.POST:
        if request.htmx:
            form = EntryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']
            else:
                title = ""
                body = ""
            for entry in util.list_entries():
                if title == entry:
                    return_message = "Entry already exist"#TODO:Add link to entry
                    found = True
                    break
            if not found:
                util.save_entry(title,body)
                return_message = "Entry saved succesfully"#TODO:Add link also
    return render(request,'encyclopedia/succes.html',
    {'succes':return_message})


def save_edit(request):
    if request.POST:
        if request.htmx:
            form = EntryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']
            else:
                title = ""
                body = ""
            util.save_entry(title,body)
            headers = {
                "HX-Redirect": '../wiki/'+title
            }
            
            return HttpResponse("Succes",headers=headers)

def new_entry(request): 
    if request.POST:
            form = EntryForm(request.POST)
            title = form['title'].value()
            body = form['body'].value()
            if request.htmx:
                return render(request,'encyclopedia/entry_preview.html',
                {'title':title,'preview':markdown2.markdown(body)})

    return render(request,'encyclopedia/new_entry.html',
    {'form':EntryForm()})

def edit(request,entry):#TODO:Make save functional
    if request.POST:
        form = EntryForm(request.POST)
        title = form['title'].value()
        body = form['body'].value()
        if request.htmx:
            return render(request,'encyclopedia/entry_preview.html',
            {'title':title,'preview':markdown2.markdown(body)})

    form = EntryForm(initial={'title':entry,'body':util.get_entry(entry)})
    return render(request,'encyclopedia/edit_entry.html',
    {'form':form})
        
def non_existant(request, any):
    return HttpResponseRedirect(reverse("index"))

def random_entry(request):
    return HttpResponseRedirect(reverse("entry",kwargs={'entry':random.choice(util.list_entries())}))

