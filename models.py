import feedparser
from datetime import datetime
from time import mktime
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    date = models.DateTimeField(blank=True)
    is_published = models.BooleanField()
    feed = models.ForeignKey('Feed', blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class Feed(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    last_parse_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    default_published_flag = models.BooleanField()

    def __unicode__(self):
        return self.name

    def parse(self):
        """
        Parse feed and save result
        """
        if not self.is_active:
            return False

        news_count = 0
        result = feedparser.parse( self.url )
        for item in result.entries:
            try:
                News.objects.get(url=item.link)
            except News.DoesNotExist:
                new = News()
                new.title = item.title
                new.url = item.link
                new.date = datetime.fromtimestamp(mktime(item.date_parsed))
                new.is_published = self.default_published_flag
                new.feed = self
                new.save()
                news_count += 1
        self.save()
        if news_count:
            return news_count
