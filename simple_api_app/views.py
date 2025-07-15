from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.views import generic

from rest_framework import viewsets
from .serializers import TaskSerializer, StatusSerializer

from .models import Task, Status
from .forms import TaskForm

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

# Show Tasks
class IndexView(generic.ListView):
    template_name = 'simple_api_app/index.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.order_by("due_date")

# Add/Edit a Task
def task(request, task_id=None):

    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('simple_api_app:index'))

    if task_id:
        task = get_object_or_404(Task, pk=task_id)
    else:
        task = Task()

    form = TaskForm(request.POST or None, instance=task)
    if request.POST:
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('simple_api_app:index'))

    return render(request, "simple_api_app/task.html", {"form": form})

# Delete a Task
class TaskDeleteView(DeleteView):

    model = Task
    success_url = reverse_lazy('simple_api_app:index')
    template_name = 'simple_api_app/delete_task.html'

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('simple_api_app:index'))
        else:
            return super(TaskDeleteView, self).post(request, *args, **kwargs)

# Django Rest Framweork view for tasks.
class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by('id')
    serializer_class = TaskSerializer

# Django Rest Framweork view for status.
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.order_by('id')
    serializer_class = StatusSerializer