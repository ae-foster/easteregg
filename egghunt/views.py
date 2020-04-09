from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Egg, LeaderboardEntry, Downtime
from ipware.ip import get_ip
from random import randrange
from datetime import datetime


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


def mapresult(request):
    lat = request.GET['latitude']
    lng = request.GET['longitude']
    return HttpResponseRedirect(reverse('clues', args=(lat, lng)))


def start(request):
    return render(request, 'egghunt/start.html')


def resume(request):
    return render(request, 'egghunt/resume.html')


def check_downtime(downtimes=None):
    cur_hour = datetime.time(datetime.now()).hour
    cur_min = datetime.time(datetime.now()).minute
    for downtime in downtimes:
        if (60*downtime.start_hour + downtime.start_min < 60*cur_hour + cur_min ) and \
                (60*downtime.end_hour + downtime.end_min > 60*cur_hour + cur_min ) and \
                downtime.in_use:
            return 1
    return 0


def clues(request, observerLatitude, observerLongitude, noLeader=False, formSubmit=False):
    nearbyEggs = [egg for egg in Egg.objects.all() if egg.isClose(observerLatitude, observerLongitude)]
    if check_downtime(Downtime.objects.all()):
        return render(request, 'egghunt/nohunt.html', {})
    if len(nearbyEggs) == 1:
        egg = nearbyEggs[0]
        if egg.levelJustEnded:
            # You've completed your level
            if noLeader:
                if egg.finalEnd:
                    return HttpResponseRedirect(reverse('index'))
                else:
                    egg.visit()
                    return render(request, 'egghunt/clues.html', {'egg': egg})
            elif formSubmit:
                ip = get_ip(request)
                if ip is None:
                    ip = randrange(0, 10000000)
                newEntry = LeaderboardEntry(name=str(request.POST['name']),
                                            ipAddress=ip,
                                            publicationDate=timezone.now(),
                                            level=egg.levelJustEnded)
                newEntry.save()
                return HttpResponseRedirect(
                    reverse('clues', args=(observerLatitude, observerLongitude)))
            else:
                # Test the IP address of the requester
                ip = get_ip(request)
                if ip is not None:
                    # Check the IP
                    if ip not in [entry.ipAddress for entry in LeaderboardEntry.objects.filter(
                                  level__exact=egg.levelJustEnded)]:
                        canEnter=True
                    else:
                        canEnter=False
                else:
                    canEnter=True
                return render(request, 'egghunt/leaderboardEntry.html',
                              {'egg': egg, 'canEnter': canEnter, 'olat': observerLatitude,
                               'olong': observerLongitude})
        else:
            # This is 'normal' behaviour
            egg.visit()
            return render(request, 'egghunt/clues.html', {'egg': egg})
    elif len(nearbyEggs) == 0:
        return render(request, 'egghunt/noegg.html', {})
    else:
        # We should never get here!
        raise ValueError("Within range of two or more eggs")

