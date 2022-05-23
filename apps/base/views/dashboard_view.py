from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from apps.base.models.customer import Customer
from apps.base.models.invoice import Invoice

User = get_user_model()


class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['page_title'] = _('Dashboard')
        context['customer'] = Customer.objects.all().filter()
        context['pending_invoice'] = Invoice.objects.all().filter(status='1')
        context['emitted_invoice'] = Invoice.objects.all().filter(status='2')
        return context
