from django.urls import path
from .views import TasksListView, TaskCreateView, AboutTemplateView, TaskEditView
from .services import delete_task
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # tasks/..
    path('about/', AboutTemplateView.as_view(), name='about_template'),
    path('', login_required(TasksListView.as_view()), name='tasks_list'),
    path('create-task/', login_required(TaskCreateView.as_view()), name='task_create'),
    path('<int:id>/delete/', login_required(delete_task), name='delete_task'),
    path('<int:pk>/edit/', login_required(TaskEditView.as_view()), name='edit_task'),
]