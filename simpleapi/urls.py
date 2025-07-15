"""
URL configuration for simpleapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from simple_api_app import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TasksViewSet)
router.register(r'status', views.StatusViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simpleapi/', include("simple_api_app.urls")),

    # web based API (with urls)
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # API calls
    path('api/task_list/', views.TaskList.as_view()),
    path('api/task_list/<int:pk>/', views.TaskDetail.as_view()),

    # User management
    path('accounts/', include('django.contrib.auth.urls')),
]
