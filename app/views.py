import logging
from hashlib import md5

import account.views
import requests
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView

from AgentOrganizer.settings import LOGIN_URL, MESSENTE_PASSWORD, MESSENTE_USER
from app.filters import TourFilter
from app.forms import TourForm, SignupForm, GuideForm
from app.models import Guide, GuideTour, Tour, Profile
from app.tables import TourTable, GuideTourTable, GuideTable

logger = logging.getLogger(__name__)


def create_sms_text(company_name, tour):
    sms_text_template = '%s ' + _('offers a job') + ': ' + _('from') + ' %s ' + _('to') + ' %s. ' + _(
        'Please respond') + ': http://%s/respond?uid=[uid]' % Site.objects.get_current()
    return sms_text_template % (
        company_name, tour.start_time.strftime('%Y-%m-%d %H:%M'), tour.end_time.strftime('%Y-%m-%d %H:%M'))


def md5_hash(s):
    return md5(s.encode('utf-8')).hexdigest()[:8]


def protected_area(view_func):
    return user_passes_test(
        lambda u: u.is_active,
        login_url=LOGIN_URL,
        redirect_field_name=REDIRECT_FIELD_NAME
    )(view_func)


@protected_area
def add_or_edit_tour(request, tour_id=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TourForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            tour_dict = form.cleaned_data
            tour_dict['user'] = request.user
            tour_dict['id'] = get_object_or_404(Tour, id=tour_id).id if tour_id else None
            tour = Tour(**tour_dict)
            tour.save()
            if request.POST['submit'] == _('Save & Close'):
                return redirect('tours')
            # redirect to add guides url with form id
            return redirect('add_guides', tour.id)
    elif tour_id:
        tour = get_object_or_404(Tour, id=tour_id, user=request.user)
        if tour.accepted:
            return redirect('view_tour', tour_id)
        if tour.sent:
            return redirect('add_guides', tour_id)
        form = TourForm(instance=tour)
    # if a GET (or any other method) we'll create a blank form
    else:
        initial = dict(
            ref_number='15112015',
            group_size='110',
            group_name=_('Some group'),
            language=_('English'),
            start_time=parse_datetime('2015-11-20T10:00'),
            end_time=parse_datetime('2015-11-20T13:00'),
            meeting_point=_('Tervis spa'),
            ending_point=_('Town Hall square'),
            description=_('Walking tour in Tallinn old town'),
        )
        form = TourForm(initial=initial)

    return render(request, 'app/add_tour.html', {'form': form, 'tour_id': tour_id})


@protected_area
def add_guides(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id, user=request.user)
    if tour.accepted:
        return redirect('view_tour', tour_id)

    sms_text = create_sms_text(tour.user.profile.company_name, tour)

    guidetours_sent = tour.guidetour_set.all()

    guides_list = Guide.objects.exclude(id__in=[o.guide_id for o in guidetours_sent]).order_by('name')

    context = dict(
        sms_text=sms_text,
        guides_list=guides_list,
        tour=tour,
        tour_id=tour.id,
        user=tour.user,
    )
    update_sms_status(guidetours_sent)

    if guidetours_sent:
        table = GuideTourTable(guidetours_sent)
        RequestConfig(request).configure(table)
        context['table'] = table

    return render(request, 'app/tour_detail.html', context=context)


def update_sms_status(guidetours):
    for guide_tour in guidetours:
        if guide_tour.delivered or guide_tour.failed:
            continue

        params = {
            'username': MESSENTE_USER,
            'password': MESSENTE_PASSWORD,
            'sms_unique_id': guide_tour.sms_unique_id,
        }
        r = requests.get('http://api2.messente.com/get_dlr_response/', params=params)
        if r.status_code != 200 or 'OK ' not in r.text:
            logger.warning('Could not get proper response when checking SMS delivery: HTTP STATUS CODE: %d, %s',
                           r.status_code, r.text)
            continue

        sms_status = r.text.lstrip('OK ')
        if sms_status == 'DELIVERED':
            guide_tour.delivered = True
            guide_tour.sent = True
            guide_tour.failed = False
        elif sms_status == 'SENT':
            guide_tour.delivered = False
            guide_tour.sent = True
            guide_tour.failed = False
        elif sms_status == 'FAILED':
            guide_tour.delivered = False
            guide_tour.sent = False
            guide_tour.failed = True

        guide_tour.save()


@protected_area
def send_sms(request):
    tour_id = request.POST.get('tour_id')
    tour = get_object_or_404(Tour, id=tour_id, user=request.user)
    if tour.accepted:
        return redirect('view_tour', tour_id)

    guide_ids = request.POST.getlist('guide_ids')
    if not guide_ids:
        return redirect('add_guides')

    for guide_id in guide_ids:
        guide = Guide.objects.get(id=int(guide_id))
        uid = md5_hash(str(tour.id) + '' + str(guide.id))
        if GuideTour.objects.filter(uid=uid):
            continue
        sms_text = create_sms_text(request.user.profile.company_name, tour)
        sms_text = sms_text.replace('[uid]', uid)

        post_body = {
            'username': MESSENTE_USER,
            'password': MESSENTE_PASSWORD,
            'text': sms_text,
            'from': 'Agentizer',
            'to': guide.phone_number,
        }
        logger.warning('Sending SMS to: %s. Message: %s', post_body['to'], post_body['text'])
        r = requests.post('http://api2.messente.com/send_sms/', data=post_body)
        if r.status_code == 200 and 'OK ' in r.text:
            GuideTour.objects.create(uid=uid, guide=guide, tour=tour, sms_unique_id=r.text.lstrip('OK '))
            logger.info('post response: %s', r.content)
        else:
            logger.warning('post response: %s', r.text)
    return redirect('add_guides', tour_id)


class SignupView(account.views.SignupView):
    form_class = SignupForm

    def after_signup(self, form):
        super(SignupView, self).after_signup(form)
        self.create_profile(form)

    def create_profile(self, form):
        profile = Profile.objects.create(user=self.created_user)
        profile.company_name = form.cleaned_data["company_name"]
        profile.save()


class StaffMemberRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StaffMemberRequiredMixin, cls).as_view(**initkwargs)
        return protected_area(view)


class FilterTableView(FilterView, SingleTableView):
    def get_table_data(self):
        f = TourFilter(self.request.GET, queryset=super().get_queryset().filter(user=self.request.user))
        return f


class TourListView(StaffMemberRequiredMixin, FilterTableView):
    model = Tour
    table_class = TourTable
    table_pagination = {"per_page": 20}
    filterset_class = TourFilter


class TourDetailView(StaffMemberRequiredMixin, DetailView):
    model = Tour

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = GuideTourTable(self.object.guidetour_set.all())
        RequestConfig(self.request).configure(table)
        context['table'] = table
        return context

    def get(self, request, *args, **kwargs):
        # update GuideTours with messente API if needed
        foo = ''
        return super().get(request, *args, **kwargs)


class GuideListView(StaffMemberRequiredMixin, SingleTableView):
    model = Guide
    table_class = GuideTable


class GuideCreateView(StaffMemberRequiredMixin, CreateView):
    model = Guide
    success_url = reverse_lazy('guides')
    form_class = GuideForm


class GuideUpdate(StaffMemberRequiredMixin, UpdateView):
    model = Guide
    form_class = GuideForm


class GuideDelete(StaffMemberRequiredMixin, DeleteView):
    model = Guide
    success_url = reverse_lazy('guides')
