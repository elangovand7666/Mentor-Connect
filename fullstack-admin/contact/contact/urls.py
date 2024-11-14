"""
URL configuration for contact project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('crt/',views.crt,name='crt'),
    path('search/',views.search,name='search'),
    path('delete/<file_id>/<image_id>/', views.delete, name='delete'),
    path('update/<file_id>/<image_id>/', views.update, name='update'),
    path('update1/',views.update1,name='update1'),
    path('view_pdf/<file_id>/', views.view_pdf, name='view_pdf'),
    path('view_image/<str:file_id>/', views.view_image, name='view_image'),
]
