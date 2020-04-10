from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.forms import CharField, ValidationError

from .models import Egg, LeaderboardEntry, Downtime, Answer
from ipware.ip import get_ip
from random import randrange
from datetime import datetime
import hashlib


# Create your views here.
def top_index(request):
    return HttpResponseRedirect('/egghunt/')


def index(request):
    try:
        n_levels = Egg.objects.latest('level').level
        leaders = [LeaderboardEntry.objects.filter(level__exact=i).order_by('publicationDate')[:25]
                   for i in range(1,n_levels+1)]
    except ObjectDoesNotExist:
        leaders = []
    return render(request, 'egghunt/index.html', {'leaders': leaders})


def leaderboard(request):
    try:
        n_levels = Egg.objects.latest('level').level
        leaders = [LeaderboardEntry.objects.filter(level__exact=i).order_by('publicationDate')[:25]
                   for i in range(1,n_levels+1)]
    except ObjectDoesNotExist:
        leaders = []
    return render(request, 'egghunt/leaderboard.html', {'leaders': leaders})


def resume(request):
    return render(request, 'egghunt/resume.html')


def checkDowntime(downtimes=None):
    cur_hour = datetime.time(datetime.now()).hour
    cur_min = datetime.time(datetime.now()).minute
    for downtime in downtimes:
        if (60*downtime.start_hour + downtime.start_min < 60*cur_hour + cur_min ) and \
                (60*downtime.end_hour + downtime.end_min > 60*cur_hour + cur_min ) and \
                downtime.in_use:
            return 1
    return 0


def checkIpAddressHash(ip, level):
    if ip is not None:
        # Check the has of the IP
        sha_1 = hashlib.sha1()
        sha_1.update(ip.encode('utf8'))
        if sha_1.hexdigest() not in [
            entry.ipAddress for entry in LeaderboardEntry.objects.filter(level__exact=level)
        ]:
            canEnter = True
        else:
            canEnter = False
    else:
        canEnter = True
    return canEnter


def makeIpAddressHash(ip):
    if ip is None:
        ip = str(randrange(0, 10000000))
    sha_1 = hashlib.sha1()
    sha_1.update(ip.encode('utf8'))
    return sha_1.hexdigest()


def visitEgg(request, egg):
    egg.visit()
    imgsBefore = egg.image_set.filter(placement__exact='before')
    imgsAfter = egg.image_set.filter(placement__exact='after')
    return render(request, 'egghunt/clues.html', {'egg': egg, 'imgsBefore': imgsBefore, 'imgsAfter': imgsAfter})


def clues(request, guess=None, noLeader=False, formSubmit=False):
    # The game is paused during any active downtime
    if checkDowntime(Downtime.objects.all()):
        return render(request, 'egghunt/nohunt.html', {})
    # The data is now sent as part of the GET data
    if guess is None:
        guess = request.GET['answer']
    field = CharField()
    try:
        guess = field.clean(guess).upper()
        matchedAnswers = Answer.objects.filter(answer__iexact=guess)
        # nearbyEggs = [egg for egg in Egg.objects.all() if egg.match(guess)]
    except ValidationError:
        return render(request, 'egghunt/noegg.html', {})
    if len(matchedAnswers) == 1:
        egg = matchedAnswers[0].egg
        if egg.levelJustEnded:
            # You've completed your level
            if noLeader:
                if egg.finalEnd:
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return visitEgg(request, egg)
            elif formSubmit:
                ip = get_ip(request)
                canEnter = checkIpAddressHash(ip, level=egg.levelJustEnded)
                if canEnter:
                    ipHash = makeIpAddressHash(ip)
                    newEntry = LeaderboardEntry(name=str(request.POST['name']),
                                                ipAddress=ipHash,
                                                publicationDate=timezone.now(),
                                                level=egg.levelJustEnded)
                    newEntry.save()
                return clues(request, guess=guess)
            else:
                # Test the IP address of the requester
                ip = get_ip(request)
                canEnter = checkIpAddressHash(ip, level=egg.levelJustEnded)
                return render(request, 'egghunt/leaderboardEntry.html',
                              {'egg': egg, 'canEnter': canEnter, 'answer': guess})
        else:
            # This is 'normal' behaviour
            return visitEgg(request, egg)
    elif len(matchedAnswers) == 0:
        return render(request, 'egghunt/noegg.html', {})
    else:
        # We should never get here!
        raise ValueError("Matched two or more answers")
