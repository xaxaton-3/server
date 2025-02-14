from django.urls import path


from activity_journal import api


urlpatterns = [
    path('logs/list/<int:user_id>/', api.UserLogs.as_view()),
    path('logs/create/', api.UserLogsCreate.as_view()),
]
