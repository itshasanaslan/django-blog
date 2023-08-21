from django.urls import path
from django.conf.urls import include
from .views import *


urlpatterns = [
  path('', home, name="vaultafed_home"),
  path('hidden_database/',hidden_database, name='hidden_database' ),
  path('add_user', add_user, name = 'add_user'),
  path('get_user',get_user, name='get_user'),
  path('delete_user', delete_user, name='delete_user'),
  path('update_user', update_user, name = 'update_user'),
  path('send_mail', send_mail, name='send_mail'),
  path('verify_mail_code', verify_mail_code, name = 'verify_mail_code'),
  path('check_user_exists', check_user_exists, name = 'check_user_exists'),
  path('try_login', try_login, name = 'try_login'),
  path('get_user', get_user, name='get_user'),
  path('get_admin_message', get_admin_message, name="get_admin_message"),
]
