from django.db import models


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Affair(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    title = models.CharField(max_length=255)
    involved = models.ManyToManyField(Person, through='PersonAffair')
    type = models.CharField(max_length=255)
    congress = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    submission_date = models.DateField()
    content = models.TextField(blank=True)

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.title)

    class Meta:
        get_latest_by = 'submission_date'


class PersonAffair(models.Model):

    AFFAIR_PERSON_TYPE = (
        (0, 'Submitter'),
        (1, 'Involved'),
    )
    person = models.ForeignKey(Person)
    affair = models.ForeignKey(Affair)
    type = models.IntegerField(choices=AFFAIR_PERSON_TYPE)
