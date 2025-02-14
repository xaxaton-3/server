from django.urls import path


from ai_helper import api


urlpatterns = [
    path('unsafe/airefactor/text/', api.AiTextRefactoring.as_view()),
]
