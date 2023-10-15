from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import random
from . import util

import markdown2


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
            
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries,
        "search_title": f"Found Pages for query: '{query}'",
    })
    
def random_search(request):
    entries = util.list_entries()
    random_entrie = random.choice(entries)
    print(random_entrie)
    random_title = util.get_entry(random_entrie)
    return HttpResponseRedirect(random_entrie)