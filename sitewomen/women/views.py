from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template.loader import render_to_string

# Create your views here.
menu = [{'title': 'About site', 'url_name': 'about'},
        {'title': 'To add Article', 'url_name': 'add_page'},
        {'title': 'Feedback', 'url_name': 'contact'},
        {'title': 'log in', 'url_name': 'login'},
]


data_db = [
    {'id': 1, 'title': 'Angelina', 'content': 'Biography', 'is_published': True},
    {'id': 2, 'title': 'Margo', 'content': 'Biography', 'is_published': False}
]

def index(request):
    data = {
         'title': 'Main Page',
         'menu': menu,
         'posts': data_db
    }
    return render(request, 'women/index.html', context=data)

def about(request):
    return render(request, 'women/about.html', {'title': 'About site', 'menu': menu})

def show_post(request, post_id):
    return HttpResponse(f'Showing article with id = {post_id}')

def addpage(request):
    return HttpResponse('Adding article')

def contact(request):
    return HttpResponse('Feedback')

def login(request):
    return HttpResponse('Authorization')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page Not Found</h1>')
