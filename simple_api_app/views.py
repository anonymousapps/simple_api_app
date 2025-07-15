# Django imports
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.views import generic
from django.db.models import Q
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

# Django REST framework imports
from .serializers import TaskSerializerWeb, StatusSerializerWeb, TaskSerializerAPI
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# internal imports
from .models import Task, Status
from .forms import TaskForm

#
# FRONT END VIEWS
# 

# Show Tasks
class IndexView(generic.ListView):
    template_name = 'simple_api_app/index.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(~Q(status__name='Done')).order_by("due_date")

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

#
# DJANGO REST FRAMEWORK VIEWS
# 

# Django Rest Framework Web views

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by('id')
    serializer_class = TaskSerializerWeb

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.order_by('id')
    serializer_class = StatusSerializerWeb

# Django Rest Framework API calls (tasks)

class TaskList(APIView):
    # List of tasks
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializerAPI(tasks, many=True)
        return Response(serializer.data)

    # Add task
    def post(self, request, format=None):
        serializer = TaskSerializerAPI(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    # helper method
    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    # get a task
    def get(self, request, pk, format=None):
        task = self.get_task(pk)
        serializer = TaskSerializerAPI(task)
        return Response(serializer.data)

    # update a task
    def put(self, request, pk, format=None):
        task = self.get_task(pk)
        serializer = TaskSerializerAPI(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a task
    def delete(self, request, pk, format=None):
        task = self.get_task(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)