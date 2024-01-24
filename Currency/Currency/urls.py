from django.contrib import admin
from django.urls import path

from currency_rate.views import current_usd

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-current-usd/', current_usd)
]
