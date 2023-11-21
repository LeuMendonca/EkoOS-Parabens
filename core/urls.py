from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include("ekoos_parabens.urls") , name="envia_email"),
]
