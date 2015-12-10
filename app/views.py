import logging
from hashlib import md5

import account.views
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect

from django.template import Context

from django.template.loader import get_template

from django.utils.dateparse import parse_datetime

from django.core.mail import send_mail

from app.forms import TourForm, SignupForm
from AgentOrganizer.settings import DEFAULT_FROM_EMAIL
from app.models import Guide, GuideTour, Tour, Profile

logger = logging.getLogger(__name__)

sms_text_template = '%s offers a job: from %s to %s. Please answer: http://agentizer.com/respond?uid=[uid]'


def create_sms_text(company_name, tour):
    return sms_text_template % (company_name, tour.start_time.strftime('%Y-%m-%d %H:%M'), tour.end_time.strftime('%Y-%m-%d %H:%M'))


def md5_hash(s):
    return md5(s.encode('utf-8')).hexdigest()[:8]


def send_emails(context):
    tour_info = get_template('app/tour_content_email.html').render(Context(context))
    send_mail('Tour details', tour_info, DEFAULT_FROM_EMAIL, [context['guide'].email, context['user'].email], html_message=tour_info)


@login_required
def show_add_tour(request):
    tour = dict(
        ending_point='Town Hall Square',
        end_time='2015-11-20T13:00',
        description='Walking add_tour in Tallinn old town',
        group_size=110,
        language='English',
        start_time='2015-11-20T10:00',
        ref_number=15112015,
        meeting_point='Tervis SPA'
    )
    return render(request, 'app/add_tour.html', context=tour)


@login_required
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
            if request.POST['submit'] == 'Save':
                return redirect('edit_tour', tour.id)
            # redirect to add guides url with form id
            return redirect('add_guides', tour.id)
    elif tour_id:
        tour = get_object_or_404(Tour, id=tour_id, user=request.user)
        if tour.guidetour_set.all():
            return redirect('tour-detail', tour_id)
        form = TourForm(instance=tour)
    # if a GET (or any other method) we'll create a blank form
    else:
        initial = dict(
            ref_number='15112015',
            group_size='110',
            group_name='Some group',
            language='English',
            start_time=parse_datetime('2015-11-20T10:00'),
            end_time=parse_datetime('2015-11-20T13:00'),
            meeting_point='Tervis SPA',
            ending_point='Town Hall square',
            description='Walking tour in Tallinn old town',
        )
        form = TourForm(initial=initial)

    return render(request, 'app/add_tour.html', {'form': form})


@login_required
def add_guides(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    sms_text = create_sms_text(tour.user.profile.company_name, tour)

    guides_list = Guide.objects.order_by('name')

    context = dict(
        sms_text=sms_text,
        guides_list=guides_list,
        tour=tour,
        tour_id=tour.id,
        user=tour.user
    )
    return render(request, 'app/guides.html', context=context)


@login_required
def send_sms(request):
    tour_id = request.POST.get('tour_id')
    tour = Tour.objects.get(id=int(tour_id))

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
        # r = requests.post('http://api2.messente.com/send_sms/', data=post_body)
        # logger.warning('post response: %s', r.content)
    return render(request, 'app/sms_sent.html')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class TourListView(LoginRequiredMixin, ListView):
    model = Tour

    def get_queryset(self):
        return Tour.objects.filter(user=self.request.user)


class TourDetailView(LoginRequiredMixin, DetailView):
    model = Tour

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['guide_list'] = Guide.objects.all()
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

    for gt in guide_tour.tour.guidetour_set.all():
        if gt != guide_tour and gt.answer:
            return render(request, 'app/accepted.html')

    guide_answer = True if request.POST['answer'] == 'yes' else False

    context = dict(tour=guide_tour.tour, guide=guide_tour.guide, user=guide_tour.tour.user)

    # do not let the add_guides to change their answers
    if guide_tour.answer is not None:
        if guide_tour.answer:
            return render(request, 'app/accepted.html', context=context)
        else:
            return render(request, 'app/rejected.html')

    guide_tour.answer = guide_answer
    guide_tour.save()
    if not guide_tour.answer:
        return render(request, 'app/')

    send_emails(context)

    return render(request, 'app/accepted.html', context=context)
