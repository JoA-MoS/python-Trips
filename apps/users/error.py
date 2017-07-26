from django.utils import timezone


class Error(object):
    def __init__(self, field, msg):
        self.field = field
        self.message = msg
        self.created_at = timezone.now()

    def __str__(self):
        return '%s %s %s' % (self.created_at, self.field, self.message)

    def __unicode__(self):
        return '%s %s %s' % (self.created_at, self.field, self.message)
