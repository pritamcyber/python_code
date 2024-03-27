from django.urls import path
from .import views as v
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',v.TaskList.as_view(),name= 'tasks'),
    path('logout/',v.TaskLogout.as_view(),name= 'logout'),

    path('task-create',v.TaskCreate.as_view(),name= 'create'),
    path('task-update/<int:pk>',v.TaskUpdate.as_view(),name= 'update'),
    path('login/',v.CustomeLoigniew.as_view(),name ='login'),
    path('register/',v.RegisterPage.as_view(),name ='register'),
    
    path('task/<int:pk>',v.TaskDetail.as_view(),name= 'detail'),
    path('task-delete/<int:pk>',v.TaskDelete.as_view(),name= 'delete'),


    
]
