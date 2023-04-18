
# импортируем функцию для перевода
from urllib import request

import pytz
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseNotFound)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from requests import Response, delete
from rest_framework import generics
from rest_framework.views import APIView

from .forms import *
from .models import *
from .serializers import PostSerializer
from .utils import *


class PostsHome(DataMixin, ListView):
    model = Post
    template_name = 'newsapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(status='p')
        # Отображаю только опубликованные (без черновиков и архива)

        # по пост-запросу будем добавлять в сессию часовой пояс,
        # который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('home')


class PostCategory(DataMixin, ListView):
    model = Post
    template_name = 'newsapp/cat_index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Категория - ' + str(context['posts'][0].postCategory), cat_selected=context['posts'][0].postCategory_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(postCategory__slug=self.kwargs['postCategory_slug'], status='p')
        # Отображаю только опубликованные (без черновиков и архива)


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


class SubscribeView(LoginRequiredMixin, CreateView):
    model = Subscribe
    form_class = SubscribeForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    # raise_exception = True


def category_subscription(request):
    if request.method == 'POST':
        form = CategorySubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponse(f'<h2> Вы подписались на данную категорию</h2>')
            return redirect('home')
        else:
            return HttpResponse('Invalid data')
    else:
        form = CategorySubscribeForm()
        return render(request, 'newsapp/category_subscription.html', {'category_subscription': form})


# class CategorySubscribeView(LoginRequiredMixin, CreateView):
#     form_class = CategorySubscribeForm
#     model = CategorySubscribe
#     template_name = 'newsapp/subscribe_category.html'
#     success_url = 'home'
#     # context_object_name = 'sign/subscribe'

#     def form_valid(self, form):
#         form.instance.subscriber = User.objects.get(id=self.request.user_id)
#         if CategorySubscribe.objects.filter(categorySubscribed=form.instance.categorySubscribed, subscriber=form.instance.subscriber):
#             return super(CategorySubscribeView, self).form_invalid(form)
#         else:
#             return super(CategorySubscribeView, self).form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['mysubscribes'] = CategorySubscribe.objects.filter(
#             subscriber=User.objects.get(id=self.request.user.id))
#         print(CategorySubscribe.objects.filter(
#             subscriber=User.objects.get(id=self.request.user.id)))
#         return context


class UnSubscribeView(LoginRequiredMixin, DeleteView):
    model = CategorySubscribe
    template_name = 'unsubscribe.html'
    success_url = reverse_lazy('home')


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


""" 
>>> article = Article.objects.get(pk=1)
>>> article.headline
'My headline'
>>> form = ArticleForm(initial={'headline': 'Initial headline'}, instance=article)
>>> form['headline'].value()
'Initial headline'  
"""
# ------------------------------------------------------------------


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='p')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading " {}"'.format(
                cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'newsapp/share.html', {'post': post, 'form': form, 'sent': sent})


""" https://pythonru.com/primery """
