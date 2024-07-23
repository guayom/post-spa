"""
URL configuration for postspa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from postspa.views import (
    add_task,
    delete_task,
    list_tasks,
    toggle_task_completed,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", list_tasks, name="home"),
    path("add-task/", add_task, name="add_task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete_task"),
    path(
        "toggle_task_completed/<int:task_id>/",
        toggle_task_completed,
        name="toggle_task_completed",
    ),
]
