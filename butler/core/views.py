from django.core.urlresolvers import reverse
from django.views.generic import RedirectView


class Index(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard_list')
