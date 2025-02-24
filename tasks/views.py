from django.http import Http404
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Task
from .forms import TaskForm
import logging


logger = logging.getLogger(__name__)

class TasksListView(ListView):
    """ Страница со всеми задачами (Главная) """
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        ordering = self.request.GET.get('order_by')
        if ordering in ('priority', '-priority', 'deadline', '-deadline'):
            return Task.objects.filter(user=self.request.user).order_by(ordering)
        else:
            return Task.objects.filter(user=self.request.user).order_by('-priority')


class TaskCreateView(CreateView):
    """ Страница с формой для создания задачи """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        logger.info(f"Task {self.object.id} created by user {self.request.user}")
        return response


class TaskEditView(UpdateView):
    """ Страница редактирования задачи """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_edit.html'
    success_url = reverse_lazy('tasks_list')

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.user != self.request.user:
            logger.warning(f"Unauthorized edit attempt: User {self.request.user} tried to edit Task {task.id}")
            raise Http404("Вы не можете редактировать эту задачу")
        logger.info(f"User {self.request.user} edited Task {task.id}")
        return task


class AboutTemplateView(TemplateView):
    template_name = 'tasks/about.html'


def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
