from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from .models import Women, Category, TagPost, UploadFiles
from .forms import AddPostForm, UploadFileForm
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

# Create your views here.
menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
]

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница', 'menu': menu, 'cat_selected': 0}

    def get_queryset(self):
        return Women.published.all().select_related('cat')

class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {'menu': menu, 'title': 'Добавление статьи',}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html', {'title': 'About site', 'menu': menu, 'form': form})

class ShowPost(DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

def contact(request):
    return HttpResponse('Feedback')

def login(request):
    return HttpResponse('Authorization')

#def show_category(request, cat_slug):
#    category = get_object_or_404(Category, slug=cat_slug)
#    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#    data = {
#        'title': f'Рубрика: {category.name}',
#        'menu': menu,
#        'posts': posts,
#        'cat_selected': category.pk
#    }
#    return render(request, 'women/index.html', context=data)

class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page Not Found</h1>')

class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
