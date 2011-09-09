from django.http import HttpResponse
from djangofeeds.models import News, Feed

def parse(request):
    count = 0
    for feed in Feed.objects.all():
        count = feed.parse()
    return HttpResponse(count)
