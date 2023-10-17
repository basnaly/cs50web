from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

import random
from . import util

import markdown2


class NewWikiForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control mb-3'}), label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content', 'class': 'form-control'}), label='')
    
class EditWikiForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content', 'class': 'form-control'}), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_title": "All Pages",
    })

def title(request, name):
    title_md = util.get_entry(name)
    if not title_md:
        return render(request, "encyclopedia/error.html", {
            "error": "The entry does not exists"
        })
    return HttpResponse(markdown2.markdown(title_md))

def search(request):
    entries = util.list_entries()
    list_entries = []
    query = request.GET["q"]
    for entry in entries:
        if query == entry.lower():
            return HttpResponseRedirect(query)
        elif query in entry.lower():
            list_entries.append(entry)  
                 
    if len(list_entries) == 0:
        return render(request, "encyclopedia/error.html", {
            "error": f"For query '{query}' no results"
        })    
                 
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries,
        "search_title": f"Found Pages for query: '{query}'",
    })
    
def random_search(request):
    entries = util.list_entries()
    random_entrie = random.choice(entries)
    return HttpResponseRedirect(random_entrie)

def add(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            title_md = util.get_entry(title)
            if title_md:
                return render(request, "encyclopedia/error.html", {
                    "error": f"The entry '{ title }' already exists"
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
                "form": NewWikiForm
            })
        
def edit(request, name):
    if request.method == "GET":       
        title = name
        content = util.get_entry(title)
        form = EditWikiForm({"content": content})
        return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title,
                "url": f"/wiki/edit/{title}",
            })
    else:
        form = EditWikiForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
            return HttpResponseRedirect(f"/wiki/{name}")
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
        