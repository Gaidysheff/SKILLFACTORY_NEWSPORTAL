
# импортируем функцию для перевода
from django.forms.models import model_to_dict
from requests import Response, delete
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.views import APIView
import pytz
from django.utils.translation import gettext as _
from django.views import View

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from urllib import request
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


from .forms import *
from .models import *
from .utils import *


class PostsHome(DataMixin, ListView):
    model = Post
    template_name = 'newsapp/index.html'
    context_object_name = 'posts'
    curent_time = timezone.now()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(status='p')
        # Отображаю только опубликованные (без черновиков и архива)


class PostCategory(DataMixin, ListView):
    model = Post
    template_name = 'newsapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(postCategory__slug=self.kwargs['postCategory_slug'], status='p')
        # Отображаю только опубликованные (без черновиков и архива)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Категория - ' + str(context['posts'][0].postCategory), cat_selected=context['posts'][0].postCategory_id)
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'newsapp/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'newsapp/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True
    # вывести '403 Forbidden' для неавторизованного пользователя (закоментить строку - тогда перенаправление на 'home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class SignUpUser(DataMixin, CreateView):
    form_class = SignUpUserForm
    template_name = 'newsapp/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginFormUser
    template_name = 'newsapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def set_timezone(request):
    context = {
        'current_time': timezone.localtime(timezone.now()),
        'timezones': pytz.common_timezones,
    }
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/posts/')
    else:
        return render(request, 'base.html', context)


# --------------Dgango REST Framework--------------------

class PostAPIView(APIView):

    def get(self, request):
        post_list = Post.objects.all()
        return Response({'posts': PostSerializer(post_list).data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = PostSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = PostSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.delete()

        return Response({"post": "delete post " + str(pk)})

# ---------------------------------------------------------------
#    _____ ПРЕДСТАВЛЕНИЕ ЧЕРЕЗ ФУНКЦИЮ ____Главная страница______


# def index(request):
#     posts = Post.objects.all()

#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'newsapp/index.html', context=context)

    # ---------------------------------------------------------------
#    _____ ПРЕДСТАВЛЕНИЕ ЧЕРЕЗ ФУНКЦИЮ ____Вывод Поста______


# def show_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.postCategory_id,
#     }
#     return render(request, 'newsapp/post.html', context=context)

    # ---------------------------------------------------------------
#    _____ ПРЕДСТАВЛЕНИЕ ЧЕРЕЗ ФУНКЦИЮ ____Категория через id - работает !!!______


# def show_category(request, cat_id):
#     posts = Post.objects.filter(postCategory=cat_id)
#     title_category = Category.objects.get(id=cat_id)

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': title_category,
#         'cat_selected': cat_id,
#     }
#     return render(request, 'newsapp/index.html', context=context)

    # ----------------------------------------------------------------
#    ______________ Категория через slug - НЕ РАБОТАЕТ________________

# def show_category(request, cat_slug):
#     posts = Post.objects.filter(postCategory=cat_slug)
#     # title_category = Category.objects.get(id=cat_slug)

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,
#         'menu': menu,
#         # 'title': title_category,
#         'cat_selected': cat_slug,
#     }
#     return render(request, 'newsapp/index.html', context=context)

    # ----------------------------------------------------------------
#    _________ ПРЕДСТАВЛЕНИЕ ЧЕРЕЗ ФУНКЦИЮ ____Добавить Пост___________


# @login_required
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'newsapp/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

    # ----------------------------------------------------------------
#    ____________________________ ЗАГЛУШКИ_____________________________


def about(request):
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'newsapp/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})
    # Просто пробник пагинации через функцию
   # ----------------------------------------------------------------


def contact(request):
    return HttpResponse(render(request, 'newsapp/contacts.html'))
    # return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация")

    # ----------------------------------------------------------------


def archive(request, year):
    if(int(year) > 2022):
        raise redirect('/', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    # ----------------------------------------------------------------


# class Index(View):
#     def get(self, request):
#         string = _('Hello world')

#         return HttpResponse(string)

class Index(View):
    def get(self, request):
        string = _('Hello world')

        context = {
            'string': string
        }
        return HttpResponse(render(request, 'newsapp/translation.html', context))
