from django.urls import path


from users import api


urlpatterns = [
    path('users/list/', api.UserList.as_view()),
    path('users/detail/<int:user_id>', api.UserDetail.as_view()),
]
