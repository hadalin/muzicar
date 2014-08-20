from django.views.generic.list import ListView
from profile.models import User
from django.views.generic.edit import FormMixin
from frontpage.forms import SearchForm

class FrontpageView(FormMixin, ListView):
    model = User
    template_name = "frontpage.html"
    form_class = SearchForm

    def get_queryset(self):
        queryset = super(FrontpageView, self).get_queryset()
        self.form = SearchForm(self.request.GET)
        if self.form.is_valid():
            filters = User.get_queryset(self.form.cleaned_data)
            if len(filters):
                queryset = User.objects.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FrontpageView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
    