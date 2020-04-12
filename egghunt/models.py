from django.db import models

from random import choice
from string import digits, ascii_uppercase
from os.path import splitext
from storages.backends.dropbox import DropBoxStorage

# from django.conf import settings
# print(settings.DROPBOX_OAUTH2_TOKEN)
STORAGE = DropBoxStorage()


class Egg(models.Model):
    sequenceNumber = models.IntegerField()
    locationName = models.CharField(max_length=255)
    textClue = models.TextField(blank=True)
    textClueAfter = models.TextField(blank=True)
    visits = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    levelJustEnded = models.IntegerField(default=None, blank=True, null=True)
    finalEnd = models.BooleanField(default=False)

    def __str__(self):
        return str(self.level) + " / " + str(self.sequenceNumber)+". "+str(self.locationName)

    def visit(self):
        self.visits += 1
        self.save()


class Downtime(models.Model):
    start_hour = models.IntegerField()
    start_min = models.IntegerField()
    end_hour = models.IntegerField()
    end_min = models.IntegerField()
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return str(self.start_hour) + " / " + str(self.end_hour)


def random_filename(instance, filename):
    _, extension = splitext(filename)
    return '/clueimage/' + ''.join(choice(ascii_uppercase + digits) for _ in range(12)) + extension


class Image(models.Model):
    egg = models.ForeignKey(Egg, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=random_filename, storage=STORAGE)
    placement = models.CharField(max_length=10, choices=[('before', 'Before'), ('after', 'After')])


class Answer(models.Model):
    egg = models.ForeignKey(Egg, on_delete=models.CASCADE)
    answer = models.CharField(max_length=511, primary_key=True)


class LeaderboardEntry(models.Model):
    name = models.CharField(max_length=255)
    ipAddress = models.CharField(max_length=100)
    publicationDate = models.DateTimeField('Entry time')
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.name

