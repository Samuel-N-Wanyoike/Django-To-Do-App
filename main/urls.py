from django.urls import path
from .views import TasksView, CreateTask, EditTask, DeleteTask, UserLogin, UserRegistration, CustomPasswordResetConfirm, CustomPasswordResetDone, CustomPasswordReset, CustomPasswordResetComplete
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    
    path("reset/", CustomPasswordReset.as_view(), name="password_reset"),
    path("reset-done/", CustomPasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset-complete/", CustomPasswordResetComplete.as_view(), name="password_reset_complete"),

    path("", TasksView.as_view(), name="tasks-view"),
    path("create-task/", CreateTask.as_view(), name="create-task"),
    path("edit-task/<int:pk>/", EditTask.as_view(), name="edit-task"),
    path("delete-task/<int:pk>/", DeleteTask.as_view(), name="delete-task")
]
