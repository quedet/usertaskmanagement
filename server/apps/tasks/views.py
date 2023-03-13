import http
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required
from turbo_response import TurboFrame, TurboStream, TurboStreamResponse

from apps.tasks.models import Task
from apps.tasks.forms import TaskForm

# Create your views here.


def playground_view(request):
    messages.info(request, 'Info Message')
    messages.success(request, 'Success Message')
    messages.error(request, 'Error Message')
    messages.warning(request, 'Warning Message')
    return render(request, 'tasks/playground.html')


@login_required
@permission_required('tasks.add_task', raise_exception=True)
def create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "Task created successfully!")

            if request.turbo.frame:
                # response = TurboFrame(request.turbo.frame).template(
                #     'messages.html', {}).response(request)
                return TurboStreamResponse([
                    TurboStream('messages').append.template(
                        'components/messages_inner.html', {}).response(request).rendered_content,
                    TurboStream('task-create').update.template('tasks/form/create.html', {
                        'form': TaskForm(),
                        'request': request
                    }).response(request).rendered_content,
                ])
                # return redirect(reverse('tasks:task-detail', kwargs={'pk': instance.pk}))
            else:
                return redirect(reverse('tasks:task-detail', kwargs={'pk': instance.pk}))
        status = http.HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        status = http.HTTPStatus.OK
        form = TaskForm()

    return render(request, 'tasks/create_page.html', {
        'form': form
    }, status=status)


@login_required
@permission_required('tasks.change_task', raise_exception=True)
def update_view(request, pk):
    instance = get_object_or_404(Task, pk=pk)

    if request.user == instance.owner:
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Task updated successfully!")
                if request.turbo.frame:
                    # response = TurboFrame(request.turbo.frame).template(
                    #     'messages.html', {}).response(request)
                    # return response
                    return TurboStreamResponse([
                        TurboStream('messages').append.template(
                            'components/messages_inner.html', {}).response(request).rendered_content,
                        TurboStream(f'task-detail-{instance.pk}').update.template('tasks/task_detail.html', {
                            'task': instance
                        }).response(request).rendered_content
                    ])
                else:
                    return redirect(reverse('tasks:task-detail', kwargs={'pk': instance.pk}))
            status = http.HTTPStatus.UNPROCESSABLE_ENTITY
        else:
            status = http.HTTPStatus.OK
            form = TaskForm(instance=instance)
    else:
        return redirect('tasks:task-list')

    return render(request, 'tasks/update_page.html', {
        'form': form
    }, status=status)


@login_required
@permission_required('tasks.delete_task', raise_exception=True)
def delete_view(request, pk):
    instance = get_object_or_404(Task, pk=pk)

    if request.user == instance.owner:
        if request.method == 'POST':
            instance.delete()
            messages.success(request, "Task deleted successfully!")
            if request.turbo.frame:
                return TurboStreamResponse([
                    TurboStream('messages').append.template(
                        'components/messages_inner.html', {}).response(request).rendered_content,
                    TurboStream(
                        f'task-detail-li-{pk}').remove.render()
                ])
            return redirect('tasks:task-list')
    else:
        return redirect('tasks:task-list')

    return render(request, 'tasks/delete_page.html', {
        'instance': instance
    })


def detail_view(request, pk):
    instance = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/detail_page.html', {
        'instance': instance
    })


def list_view(request):
    return render(request, 'tasks/list_page.html', {
        'object_list': Task.objects.all()
    })
