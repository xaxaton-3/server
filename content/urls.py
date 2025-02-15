from django.urls import path


from content import api


urlpatterns = [
    path('content/forms/list/', api.PersonRequestsList.as_view()),
    path('content/forms/create/', api.PersonRequestCreate.as_view()),
    path('content/forms/delete/', api.PersonRequestDelete.as_view()),
]
