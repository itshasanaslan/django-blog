from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', telegram_main_page, name="telegram_mainpage" ),

]
