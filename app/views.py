from copy import copy
# import the logging library
import logging
import account.views
import app.forms
# Get an instance of a logger
import requests

logger = logging.getLogger(__name__)
from hashlib import md5

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.dateparse import parse_datetime
from AgentOrganizer.settings import DEFAULT_FROM_EMAIL

from app.models import Guide, GuideTour, Tour, Profile, UserTour
from django.core.mail import send_mail

sms_text_template = '%s offers a job: from %s to %s. Please answer: http://agentizer.com/respond?uid=[uid]'


def create_sms_text(company_name, tour):
    return sms_text_template % (company_name, tour.start_time.strftime('%Y-%m-%d %H:%M'), tour.end_time.strftime('%Y-%m-%d %H:%M'))


def md5_hash(s):
    return md5(s.encode('utf-8')).hexdigest()[:8]


def index(request):
    return render(request, 'app/index.html')


def send_emails(context):
    tour_info = get_template('app/tour_details_email.html').render(Context(context))
    send_mail('Tour details', tour_info, DEFAULT_FROM_EMAIL, [context['guide'].email, context['user'].email], html_message=tour_info)


@login_required
def create_tour(request):
    tour = dict(
        ending_point='Town Hall Square',
        end_time='2015-11-20T13:00',
        description='Walking tour in Tallinn old town',
        group_size=110,
        language='English',
        start_time='2015-11-20T10:00',
        ref_number=15112015,
        meeting_point='Tervis SPA'
    )

    return render(request, 'app/tour.html', context=tour)


@login_required
def guides(request):
    tour_dict = copy(request.POST)
    del tour_dict['csrfmiddlewaretoken']
    tour_dict = {k: v for k, v in tour_dict.items()}
    tour_dict['start_time'] = parse_datetime(tour_dict['start_time'])
    tour_dict['end_time'] = parse_datetime(tour_dict['end_time'])
    tour = Tour.objects.create(**tour_dict)
    user_tour = UserTour.objects.create(user=request.user, tour=tour)
    user_tour.save()

    sms_text = create_sms_text(request.user.profile.company_name, tour)

    guides_list = Guide.objects.order_by('name')

    user_who_created_tour = tour.usertour_set.all()[0].user
    context = dict(sms_text=sms_text, guides_list=guides_list, tour=tour, tour_id=tour.id, user=user_who_created_tour
                   )
    return render(request, 'app/guides.html', context=context)


@login_required
def send_sms(request):
    tour_id = request.POST.get('tour_id')
    tour = Tour.objects.get(id=int(tour_id))

    for guide_id in request.POST.getlist('guide_ids'):
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
    return render(request, 'app/sms_sent.html')


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

    user_who_created_tour = guide_tour.tour.usertour_set.all()[0].user
    context = dict(tour=guide_tour.tour, guide=guide_tour.guide, user=user_who_created_tour)

    # do not let the guides to change their answers
    if guide_tour.answer is not None:
        if guide_tour.answer:
            return render(request, 'app/accepted.html', context=context)
        else:
            return render(request, 'app/rejected.html')

    guide_tour.answer = guide_answer
    guide_tour.save()
    if not guide_tour.answer:
        return render(request, 'app/rejected.html')

    send_emails(context)

    return render(request, 'app/accepted.html', context=context)


def tour_details(request):
    uid = request.GET['uid']
    guide_tour = get_object_or_404(GuideTour, uid=uid)

    context = dict(tour=guide_tour.tour)

    return render(request, 'app/tour_details.html', context=context)


class SignupView(account.views.SignupView):
    form_class = app.forms.SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = Profile.objects.create(user=self.created_user)
        profile.company_name = form.cleaned_data["company_name"]
        profile.save()
