from django.urls import path
from ekoos_parabens.views import envia_email , getAniversariantes

urlpatterns = [
    path('envia_email' , envia_email),
    path('get_aniversarios/' ,getAniversariantes)
]
