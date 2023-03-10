from django.urls import path
from apps.tasks.views import (
    create_view, update_view, delete_view, detail_view, list_view, playground_view
)

app_name = 'tasks'

urlpatterns = [
    path('create/', create_view, name='task-create'),
    path('edit/<int:pk>/', update_view, name='task-edit'),
    path('delete/<int:pk>/', delete_view, name='task-delete'),
    path('<int:pk>/', detail_view, name='task-detail'),
    path('', list_view, name='task-list'),
    path('playground/', playground_view, name='playground')
]
