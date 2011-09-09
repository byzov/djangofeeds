# -*- coding: utf-8 -*-
from django import template
from datetime import date, timedelta
from djangofeeds.models import News

register = template.Library()

@register.simple_tag
def three_days_news():
    cols = []
    today = date.today()
    start_date = False
    days = (u'Сегодня', u'Вчера', u'Позавчера')
    for days_ago in range(3):
        end_date = today - timedelta(days=days_ago)
        if start_date:
            news = News.objects.filter(date__lt=start_date, date__gt=end_date)
        else:
            news = News.objects.filter(date__gt=end_date)
        cols.append({
            'date': days[days_ago], 
            'news': news,
        })
        start_date = end_date
    t = template.loader.get_template('three_days_news.html')
    c = template.Context({'cols': cols})
    return t.render(c)
