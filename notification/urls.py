from django.urls import path


from notification import api


urlpatterns = [
    path('notification/create/', api.CreateNotification.as_view()),
    path('notification/list/<int:user_id>/', api.UserNotifications.as_view()),
]
