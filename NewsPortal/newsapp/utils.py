from django.utils import timezone
from django.shortcuts import redirect
from .models import *
from django.db.models import Count
import pytz


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        # {'title': "Войти", 'url_name': 'login'},
        ]

#    _____ вариант исчезновения "Добавить статью" из меню для неавторизованного пользователя ___


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.order_by('name') # отображение всех категорий
        cats = Category.objects.annotate(Count('post')).order_by(
            'name')  # для исчезновения пустых категорий

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['current_time'] = timezone.now()
        # добавляем в контекст все доступные часовые пояса
        context['timezones'] = pytz.common_timezones
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('home')


#    _____ вариант без исчезновения "Добавить статью" из меню для неавторизованного пользователя ___

# class DataMixin:
#     paginate_by = 3
#
#     def get_user_context(self, **kwargs):
#         context = kwargs
#         cats = Category.objects.all()
#         context['menu'] = menu
#         context['cats'] = cats
#         if 'cat_selected' not in context:
#             context['cat_selected'] = 0
#         return context
