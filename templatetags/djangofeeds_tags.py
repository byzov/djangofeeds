# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django import template

from djangofeeds.models import News

register = template.Library()

@register.simple_tag
def three_days_news():
    """
    Shows news for last three days
    """
    cols = []
    today = date.today()
    start_date = False
    days = (u'Сегодня', u'Вчера был', u'')
    party_days = (256,)
    for days_ago in range(3):
        end_date = today - timedelta(days=days_ago)
        if start_date:
            news = News.objects.filter(date__lt=start_date, date__gt=end_date)
        else:
            news = News.objects.filter(date__gt=end_date)
        title = []
        title.append(days[days_ago])
        title.append(end_date.strftime('%j'))
        title.append(u'день')
        is_party_day = False
        if int(end_date.strftime('%j')) in party_days:
            is_party_day = True
        cols.append({
            'date': ' '.join(title), 
            'news': news,
            'is_party_day': is_party_day,
        })
        start_date = end_date
    t = template.loader.get_template('djangofeeds/tags/three_days_news.html')
    c = template.Context({'cols': cols})
    return t.render(c)
