from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from tasks.models import Task
import logging


logger = logging.getLogger(__name__)

@login_required
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)
        task.delete()
        logger.info(f"Task {id} was deleted by user {request.user}")
    except Exception as e:
        logger.info(f"Error deleting task {id}: {e}", exc_info=True)

    return redirect('tasks_list')
