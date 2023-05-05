from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("bookstore.urls"))
]

handler404 = 'bookstore.views.handler404'
handler500 = 'bookstore.views.handler500'