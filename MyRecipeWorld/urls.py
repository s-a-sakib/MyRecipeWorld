from django.contrib import admin
from django.urls import path
from Recipe.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_recipe/', add_recipe , name= "add_recipe"),
    path('', home, name="home"),
    path('login/',login_page, name="login"),
    path('logout/', logout_page, name='logout_page'),
    path('register/',register_page, name="register"),
    path('update_recipe/<id>/', update_receipe, name="update_recipe"),
    path('delete_recipe/<id>/',delete_receipe, name="delete_recipe"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()