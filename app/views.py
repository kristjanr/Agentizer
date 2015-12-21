import logging
from hashlib import md5

import account.views
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.template.loader import get_template
from django.utils.dateparse import parse_datetime
from django.core.mail import send_mail

from django_filters.views import FilterView

from django_tables2 import RequestConfig, SingleTableView

from django.utils.translation import ugettext as _
import requests

from app.filters import TourFilter
from app.forms import TourForm, SignupForm
from AgentOrganizer.settings import DEFAULT_FROM_EMAIL
from app.models import Guide, GuideTour, Tour, Profile
from app.tables import TourTable, GuideTourTable

logger = logging.getLogger(__name__)


def create_sms_text(company_name, tour):
    sms_text_template = '%s ' + _('offers a job') + ': ' + _('from') + ' %s ' + _('to') + ' %s. ' + _('Please respond') + ': http://agentizer.com/respond?uid=[uid]'
    return sms_text_template % (company_name, tour.start_time.strftime('%Y-%m-%d %H:%M'), tour.end_time.strftime('%Y-%m-%d %H:%M'))


def md5_hash(s):
    return md5(s.encode('utf-8')).hexdigest()[:8]


def send_emails(context):
    tour_info = get_template('app/tour_content_email.html').render(Context(context))
    send_mail(_('Tour details'), tour_info, DEFAULT_FROM_EMAIL, [context['guide'].email, context['user'].email], html_message=tour_info)


@login_required
def add_or_edit_tour(request, tour_id=None):
    if not request.user.is_staff:
        return redirect('/')
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
            if request.POST['submit'] == _('Save'):
                return redirect('edit_tour', tour.id)
            # redirect to add guides url with form id
            return redirect('add_guides', tour.id)
    elif tour_id:
        tour = get_object_or_404(Tour, id=tour_id, user=request.user)
        if tour.accepted:
            return redirect('tour-detail', tour_id)
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

    return render(request, 'app/add_tour.html', {'form': form})


@login_required
def add_guides(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id, user=request.user)

    sms_text = create_sms_text(tour.user.profile.company_name, tour)

    guides_list = Guide.objects.order_by('name')

    guides_sent = tour.guidetour_set.all()
    context = dict(
        sms_text=sms_text,
        guides_list=guides_list,
        tour=tour,
        tour_id=tour.id,
        user=tour.user,
    )
    if guides_sent:
        table = GuideTourTable(guides_sent)
        RequestConfig(request).configure(table)
        context['table'] = table
    return render(request, 'app/guides.html', context=context)


@login_required
def send_sms(request):
    tour_id = request.POST.get('tour_id')
    tour = get_object_or_404(Tour, id=tour_id, user=request.user)

    guide_ids = request.POST.getlist('guide_ids')
    if not guide_ids:
        return redirect('add_guides')

    for guide_id in guide_ids:
        guide = Guide.objects.get(id=int(guide_id))
        uid = md5_hash(str(tour.id) + '' + str(guide.id))
        if GuideTour.objects.filter(uid=uid):
            continue
        guide_tour = GuideTour.objects.create(uid=uid, guide=guide, tour=tour)
        sms_text = create_sms_text(request.user.profile.company_name, tour)
        sms_text = sms_text.replace('[uid]', guide_tour.uid)

        post_body = {
            'username': 'f35583f5f9fcd7a8a13f36a10afca6aa',
            'password': 'ea2254154190fab7a6a33c3ec79a21f0',
            'text': sms_text,
            'from': 'Agentizer',
            'to': guide.phone_number,
        }
        logger.warning('Sending SMS to: %s. Message: %s', post_body['to'], post_body['text'])
        r = requests.post('http://api2.messente.com/send_sms/', data=post_body)
        logger.warning('post response: %s', r.content)
    return redirect('tour-detail', tour_id)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class FilterTableView(FilterView, SingleTableView):
    def get_table_data(self):
        f = TourFilter(self.request.GET, queryset=super().get_queryset().filter(user=self.request.user))
        return f


class TourListView(LoginRequiredMixin, FilterTableView):
    model = Tour
    table_class = TourTable
    table_pagination = {"per_page": 20}
    filterset_class = TourFilter


class TourDetailView(LoginRequiredMixin, DetailView):
    model = Tour

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = GuideTourTable(self.object.guidetour_set.all())
        RequestConfig(self.request).configure(table)
        context['table'] = table
        return context


class SignupView(account.views.SignupView):
    form_class = SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = Profile.objects.create(user=self.created_user)
        profile.company_name = form.cleaned_data["company_name"]
        profile.save()


def respond(request):
    uid = request.GET['uid']
    guide_tour = GuideTour.objects.get(uid=uid)
    guide_tour.seen = True
    guide_tour.save()
    for gt in guide_tour.tour.guidetour_set.all():
        if gt != guide_tour and gt.answer:
            return render(request, 'app/accepted.html')

    context = dict(guide_tour=guide_tour)
    return render(request, 'app/respond.html', context=context)


def answer(request):
    uid = request.POST['uid']
    guide_tour = GuideTour.objects.get(uid=uid)

    # Check if someone else has already accepted the tour
    for gt in guide_tour.tour.guidetour_set.all():
        if gt != guide_tour and gt.answer:
            return render(request, 'app/accepted.html')

    guide_answer = True if request.POST['answer'] == _('yes') else False
    context = dict(tour=guide_tour.tour, guide=guide_tour.guide, user=guide_tour.tour.user)

    # Do not allow to change the answer from yes to no
    if guide_tour.answer:
        return render(request, 'app/accepted.html', context=context)

    guide_tour.answer = guide_answer
    guide_tour.save()

    # The guide answered no
    if not guide_tour.answer:
        return render(request, 'app/rejected.html')

    # The guide accepted the Tour
    send_emails(context)
    return render(request, 'app/accepted.html', context=context)
