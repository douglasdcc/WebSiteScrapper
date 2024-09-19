from django.contrib import admin
from django.urls import path
from home.views import home, scrape_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('scrape-urls/', scrape_urls, name='scrape_urls'),
]
