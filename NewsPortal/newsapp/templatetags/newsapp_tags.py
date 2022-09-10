from django import template
from newsapp.models import *
from newsapp.forms import SubscribeForm, CategorySubscribeForm, NewSubForm


register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('newsapp/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('newsapp/subscribe_form.html')
def subscribe_form():
    return{"subscribe_form": SubscribeForm()}


@register.inclusion_tag('newsapp/category_subscription.html')
def category_subscription():
    return{"category_subscription": CategorySubscribeForm()}


@register.inclusion_tag('newsapp/categorysubscribe_form.html')
def categorysubscribe_form():
    return{"categorysubscribe_form": NewSubForm()}
