from django.views.generic import TemplateView


class DocsView(TemplateView):
    template_name = 'docs.html'


docs_view = DocsView.as_view()
