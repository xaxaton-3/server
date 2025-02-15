from django.urls import path


from docs.views import docs_view


urlpatterns = [path('', docs_view)]
