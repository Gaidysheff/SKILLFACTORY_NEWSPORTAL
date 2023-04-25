from urllib import request

from django.test import TestCase

# Create your tests here.
from django.contrib import auth

auth.get_user(request).username
