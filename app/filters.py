import django_filters


def filter_sent(queryset, value):
    filtered = []
    for tour in queryset:
        if value and tour.sent:
            filtered.append(tour)
        elif not value and not tour.sent:
            filtered.append(tour)
    return filtered

def filter_accepted(queryset, value):
    filtered = []
    for tour in queryset:
        if value and tour.accepted:
            filtered.append(tour)
        elif not value and not tour.accepted:
            filtered.append(tour)
    return filtered

class TourFilter(django_filters.FilterSet):
    sent = django_filters.BooleanFilter(action=filter_sent)
    accepted = django_filters.BooleanFilter(action=filter_accepted)
