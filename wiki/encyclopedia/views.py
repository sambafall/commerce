from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
from markdown2 import Markdown
from . import util





def index(request):
    request.session['TITLE'] = ''
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, TITLE):
    request.session['TITLE'] = TITLE
    page = util.get_entry(TITLE)
    markdowner = Markdown()
    page = markdowner.convert(page)
    if page is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return render(request, 'encyclopedia/entry_page.html', {
            'page': page
        })


def search(request):
    entries = util.list_entries()

    if request.method == 'GET':
        item = request.GET.get('q')
    
    result = [e for e in entries if item in e]

    if len(result) == 1 and result[0] == item:
        page = util.get_entry(result[0])
        markdowner = Markdown()
        page = markdowner.convert(page)
        return render(request, 'encyclopedia/entry_page.html', {
            'page': page
        })
        
    elif len(result) > 1 or (len(result) == 1 and result[0] != item):
        return render(request, "encyclopedia/index.html", {
        "entries": result
    })

    else:
        return HttpResponseNotFound(f'<h1>No results for {item} </h1>')

def add_page(request):
    return render(request, "encyclopedia/new_page.html")
    

def create_page(request):
    entries = util.list_entries()
    if request.method == 'POST':
        title = request.POST.get('title')
        infos = request.POST.get('info')
        if title in entries:
            return HttpResponseNotFound(f"<h1>A page for {title} already exist's </h1>")
        else:
            with open(f'entries/{title}.md', 'w') as mdFile:
                mdFile.write(infos)
                mdFile.close()
            return render(request, 'encyclopedia/entry_page.html', {
                'page': util.get_entry(title)
            })


def edit_page(request):
    TITLE = request.session['TITLE']
    page = util.get_entry(TITLE)
    if request.method == 'POST':
        infos = request.POST.get('info')
        with open(f'entries/{TITLE}.md', 'w') as mdFile:
                    mdFile.write(infos)
                    mdFile.close()
        return HttpResponseRedirect(reverse('wiki:entry_page', kwargs={'TITLE':TITLE}))
    
    else:
        return render(request, 'encyclopedia/edit_page.html', {
        'page': page
        })

    return render(request, 'encyclopedia/edit_page.html', {
        'page': page
        })
    

def random_page(request):
    entries = util.list_entries()
    TITLE = random.choice(entries)
    page = util.get_entry(TITLE)
    markdowner = Markdown()
    page = markdowner.convert(page)
    return render(request, 'encyclopedia/entry_page.html', {
            'page': page
        })
    