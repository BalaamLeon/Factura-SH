# Django Library
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

# Thirdparty Library
# from apps.sale.models import *

# Localfolder Library


# ========================================================================== #
# class FatherTemplateView(TemplateView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['web_parameter'] = _web_parameter()
#         context['parameter'] = _parameter()
#         context['meta'] = _web_meta()
#         context['count_plugin'] = _count_plugin
#         context['company'] = Company.objects.filter(active=True)
#         return context
#
#     class Meta:
#         abstract = True


# ========================================================================== #
class FatherListView(ListView):
    template_name = 'base/list.html'
    # EXLUDE_FROM_FILTER = (
    #     'Company',
    #     'Country',
    #     'Courrency',
    #     'Plugin',
    #     'Sequence'
    # )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        verbose_name_plural = self.model._meta.verbose_name_plural
        context['page_title'] = '{}'.format(verbose_name_plural)
        # context['web_parameter'] = _web_parameter()
        # context['parameter'] = _parameter()
        # context['meta'] = _web_meta()
        # context['count_plugin'] = _count_plugin
        # context['company'] = Company.objects.filter(active=True)
        context['title'] = '{}'.format(verbose_name)
        context['add_url'] = reverse_lazy('{}:add'.format(object_name))
        context['detail_url'] = '{}:detail'.format(object_name)
        context['update_url'] = '{}:update'.format(object_name)
        context['delete_url'] = '{}:delete'.format(object_name)
        context['import_url'] = reverse_lazy('{}:import'.format(object_name))
        context['form_template'] = False
        context['breadcrumbs'] = [{
            'url': False,
            'name': '{}'.format(verbose_name)
        }]
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    class Meta:
        abstract = True


# ========================================================================== #
class FatherDetailView(DetailView):
    template_name = 'base/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        context['title'] = '{}'.format(verbose_name)
        context['back_url'] = reverse_lazy('{}:list'.format(object_name))
        context['breadcrumbs'] = [{
            'url': reverse_lazy('{}:list'.format(object_name)),
            'name': '{}'.format(verbose_name)
        }]
        context['list_url'] = '{}:list'.format(object_name)
        context['update_url'] = reverse_lazy(
            '{}:update'.format(object_name),
            kwargs={'pk': self.object.pk}
        )
        context['delete_url'] = '{}:delete'.format(object_name)
        context['detail_url'] = '{}:detail'.format(object_name)
        context['form_template'] = False
        forward = self.model.objects.filter(
            pk__gt=self.kwargs['pk'],
        ).first()
        backward = self.model.objects.filter(
            pk__lt=self.kwargs['pk'],
        ).order_by('-pk').first()
        if forward:
            context['forward'] = reverse_lazy(
                '{}:detail'.format(object_name),
                kwargs={'pk': forward.pk}
            )
        if backward:
            context['backward'] = reverse_lazy(
                '{}:detail'.format(object_name),
                kwargs={
                    'pk': backward.pk
                }
            )
        return context

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(
            pk=pk,
        )
        queryset = queryset.filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name}
            )
        return obj

    class Meta:
        abstract = True


# ========================================================================== #
class FatherCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        verbose_name_plural = self.model._meta.verbose_name_plural
        context['action'] = 'New'
        context['title'] = '{}'.format(verbose_name)
        context['page_title'] = 'New {}'.format(verbose_name)
        context['list_url'] = '{}:list'.format(object_name)
        context['update_url'] = '{}:update'.format(object_name)
        context['delete_url'] = '{}:delete'.format(object_name)
        context['detail_url'] = '{}:detail'.format(object_name)
        context['back_url'] = reverse_lazy('{}:list'.format(object_name))
        context['form_template'] = True
        context['breadcrumbs'] = [{
            'url': reverse_lazy('{}:list'.format(object_name)),
            'name': '{}'.format(verbose_name_plural)
        }]

        return context

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     form.save_m2m()
    #     return super().form_valid(form)

    class Meta:
        abstract = True


# ========================================================================== #
class FatherUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        context['action'] = 'Update'
        context['title'] = '{}'.format(verbose_name)
        context['page_title'] = 'Update {}'.format(verbose_name)
        context['list_url'] = '{}:list'.format(object_name)
        context['update_url'] = '{}:update'.format(object_name)
        context['delete_url'] = '{}:delete'.format(object_name)
        context['detail_url'] = '{}:detail'.format(object_name)
        context['form_template'] = True
        context['back_url'] = reverse_lazy(
            '{}:list'.format(object_name)
        )
        context['action_url'] = '{}:update'.format(object_name)
        if 'pk' in self.kwargs:
            forward = self.model.objects.filter(
                pk__gt=self.kwargs['pk'],
            ).first()
            backward = self.model.objects.filter(
                pk__lt=self.kwargs['pk'],
            ).order_by('-pk').first()
            if forward:
                context['forward'] = reverse_lazy(
                    '{}:update'.format(object_name),
                    kwargs={'pk': forward.pk}
                )
            if backward:
                context['backward'] = reverse_lazy(
                    '{}:update'.format(object_name),
                    kwargs={
                        'pk': backward.pk
                    }
                )
        context['breadcrumbs'] = [{
            'url': reverse_lazy('{}:list'.format(object_name)),
            'name': '{}'.format(verbose_name)
        }]
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            form.save_m2m()
            return super().form_valid(form)
        else:
            print(form.errors)

    class Meta:
        abstract = True


# ========================================================================== #
class FatherDeleteView(DeleteView):
    template_name = 'common/delete.html'
    success_message = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        name = self.get_object().name
        context['title'] = _("Delete %(obj_name)s") % {"obj_name": verbose_name}
        context['delete_message'] = _("Are you sure to delete <strong>%(obj_name)s</strong>?") % {"obj_name": name}
        context['action_url'] = '{}:delete'.format(object_name)
        return context

    def get_success_url(self):
        return '{}:list'.format(self.model._meta.object_name)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy(self.get_success_url())
        self.object.delete()
        return HttpResponseRedirect(success_url)

    class Meta:
        abstract = True


# ========================================================================== #
class FatherModalCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        context['title'] = '{}'.format(verbose_name)
        context['page_title'] = 'New {}'.format(verbose_name)
        context['list_url'] = '{}:list'.format(object_name)
        context['update_url'] = '{}:update'.format(object_name)
        context['delete_url'] = '{}:delete'.format(object_name)
        context['detail_url'] = '{}:detail'.format(object_name)
        context['back_url'] = reverse_lazy('{}:list'.format(object_name))
        context['form_template'] = True
        context['breadcrumbs'] = [{
            'url': reverse_lazy('{}:list'.format(object_name)),
            'name': '{}'.format(verbose_name)
        }]

        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.uc = self.request.user.pk
        self.object.company_id = self.request.user.active_company_id
        print(self.object.company_id)
        self.object.save()
        return super().form_valid(form)

    class Meta:
        abstract = True


# ========================================================================== #
class FatherTableListView(ListView):
    fields = None
    template_name = 'common/_table_list.html'

    def get(self, request, *args, **kwargs):
        object_name = self.model._meta.object_name
        data = dict()
        queryset = self.get_queryset()
        data['table'] = render_to_string(
            'common/_table_list.html',
            {'fields': self.fields,
             'object_list': queryset,
             'detail_url': '{}:detail'.format(object_name),
             'update_url': '{}:update'.format(object_name),
             'delete_url': '{}:delete'.format(object_name),
             'modal_add': True,
             },
            request=request
        )
        return JsonResponse(data, status=200, safe=False)

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    class Meta:
        abstract = True
