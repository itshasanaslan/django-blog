
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theblog.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('vaultafed/', include('vaultafed.urls')),
   path('telegram_bot/', include('telegram_bot.urls')),
    path('cdm/', include('cdm.urls')),
    path('cypher/', include('cypher_enc_dec.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
