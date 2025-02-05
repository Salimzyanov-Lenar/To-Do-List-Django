from django.http import Http404
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm


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
        return super().form_valid(form)


class TaskEditView(UpdateView):
    """ Страница редактирования задачи """
    model = Task
    fields = ("title", "description", "priority", "deadline")
    template_name = 'tasks/task_edit.html'
    success_url = reverse_lazy('tasks_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("Вы не можете редактировать эту задачу")
        return obj


class AboutTemplateView(TemplateView):
    template_name = 'tasks/about.html'