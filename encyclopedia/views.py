from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from django.core.files.storage import default_storage
import re
from random import choice
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, TITLE):
        markdown = util.get_entry(TITLE)
        build_html(util.convert_html(markdown))
        return render(request, "encyclopedia/entry_page.html", {
        "Title": TITLE,
        "markdown": markdown,
    })
    
def build_html(html):
    with open("./encyclopedia/templates/encyclopedia/entry_page.html", 'w') as file:
        file.write('{% extends "encyclopedia/layout.html" %}{% block title %}{{Title}}{% endblock %}{% block body %}' + html +'<form action="{{Title}}/edit" method="get"><input type="submit" value="Edit"></form>{% endblock %}') 

def search_title(request):
    title = re.compile(request.GET['q'].strip(), re.IGNORECASE)
    matches = [entry for entry in util.list_entries() if re.search(title, entry)]
    if matches and len(matches) == 1:
        return render(request, "encyclopedia/entry_page.html", {
            "Title": matches[0]
            })
    elif matches:
        return render(request, "encyclopedia/search_results.html", {
            "Title": matches
            })
    else:
        return HttpResponse('Empty')

def create(request):
    if request.method == "POST":
        util.save_entry(request.POST["title"], request.POST["description"].strip())
        return HttpResponseRedirect('wiki/' + request.POST["title"])
    else:
        return render(request, 'encyclopedia/create.html')

def edit(request, TITLE):
    return render(request, "encyclopedia/edit.html", 
    {
        "Title": TITLE,
        "Markdown": util.get_entry(TITLE)
    })

def random(request):
    TITLE = choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=[TITLE]))

