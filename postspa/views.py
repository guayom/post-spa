from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Category, Task


@require_http_methods(["GET", "POST"])
def list_tasks(request):
    tasks = Task.objects.all().order_by("completed", "id")
    categories = Category.objects.all()
    query = request.GET.get("query", "")

    if query is not None:
        tasks = tasks.filter(title__icontains=query)

    if request.headers.get("Hx-Trigger-Name") == "query":
        return render(
            request,
            "tasks/list_tasks_rows.html",
            {"tasks": tasks, "categories": categories},
        )
    else:
        return render(
            request,
            "tasks/list_tasks.html",
            {"tasks": tasks, "categories": categories, "query": query},
        )


def add_task(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        Task.objects.create(title=title, category=category)
        tasks = Task.objects.all().order_by("completed", "id")
        categories = Category.objects.all()
        return render(
            request,
            "tasks/list_tasks_rows.html",
            {"tasks": tasks, "categories": categories},
        )
    return HttpResponse(status=405)


@require_http_methods(["DELETE"])
def delete_task(request, task_id):
    if request.method == "DELETE":
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            if request.headers.get("hx-request"):
                return HttpResponse(status=200)
            else:
                return HttpResponseRedirect(reverse("task_list"))
        except Task.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)


def toggle_task_completed(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
            if request.headers.get("hx-request"):
                tasks = Task.objects.all().order_by("completed", "id")
                categories = Category.objects.all()
                return render(
                    request,
                    "tasks/list_tasks_rows.html",
                    {"tasks": tasks, "categories": categories},
                )
            else:
                return HttpResponseRedirect(reverse("task_list"))
        except Task.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)
