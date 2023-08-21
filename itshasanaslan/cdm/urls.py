from django.urls import path
from django.conf.urls import include
from .views import *

urlpatterns = [
  path('', home, name="cdm_home"),
  path('attendance', attendance_page ,name = "cdm_attendance"),
  path('get_results', get_results, name="get_student_excuses"),
]
