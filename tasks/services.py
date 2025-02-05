from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Task


@login_required
def delete_task(request, id):
    """ Удаляет задачу """
    task = Task.objects.filter(id=id, user=request.user).first()
    if task:
        task.delete()
    return redirect('tasks_list')