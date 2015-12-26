from django.core.mail import send_mail
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from AgentOrganizer.settings import DEFAULT_FROM_EMAIL
from app.models import GuideTour


def send_emails(context):
    tour_info = get_template('app/tour_content_email.html').render(Context(context))
    send_mail(_('Tour details'), tour_info, DEFAULT_FROM_EMAIL, [context['guide'].email, context['user'].email], html_message=tour_info)


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