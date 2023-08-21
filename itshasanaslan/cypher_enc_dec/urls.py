from django.urls import path
from django.conf.urls import include
from .views import *

urlpatterns = [
  path('', main_page, name="cypher_home"),
  path('generate_key/', generate_key,name = "cypher_generate_key"),
  path('encrypt_message/', encrypt, name = "cypher_encrypt_message"),
  path('decrypt_message/', decrypt, name = "cypher_decrypt_message"),
  path('source_code/', source_code, name = "cypher_source_code"),
]
