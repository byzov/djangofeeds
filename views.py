from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from djangofeeds.models import News, Feed

def news(request):
    """
    Shows news page paginated by date
    """
    news_per_page = 7
    paginator = Paginator(News.objects.filter(is_published=True), \
            news_per_page)
    page = request.GET.get('page')
    try:
        page_news = paginator.page(page)
    except TypeError, PageNotAnInteger:
        page_news = paginator.page(1)
    except EmptyPage:
        page_news = paginator.page(paginator.num_pages)

    days = {}
    for item in page_news.object_list:
        date = item.date.strftime('%j')
        if not date in days:
            days[date] = []
        days[date].append(item)

    days = [{"date": date, "news": day} for date, day in days.iteritems()]
    return render_to_response('djangofeeds/news.html', {
        "news": page_news, 
        "days": sorted(days, reverse=True),
    })

def parse(request):
    """
    Parse all feeds and save result
    """
    count = 0
    for feed in Feed.objects.all():
        count = feed.parse()
    return HttpResponse(count)
