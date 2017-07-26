# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse, resolve
from django.contrib import messages
from .models import Trip
from ..users.models import User
from ..users.decorators import user_login_required

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
@user_login_required
def index(request):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    my_trips =  Trip.objects.get_user_trips(user)
    available_trips = Trip.objects.get_available_trips(user)
    context = {'user': user,
                'my_trips': my_trips,
               'available_trips': available_trips}
    return render(request, 'trips/dashboard.html', context)


@user_login_required
def new(request):
    """Displays the New Form"""
    context = {'user': User.objects.logged_in(request.session)}
    return render(request, 'trips/add_trip.html', context)

@user_login_required(next_url='/trips/new/')
def create(request):
    """Creates the Object"""
    user = User.objects.logged_in(request.session)
    valid, data =Trip.objects.add_trip(user, request.POST)
    if valid:
        return redirect('trips:index')
    else:
        for i in data:
            messages.add_message(request, messages.ERROR, i.message)
        return redirect('trips:new')



@user_login_required
def show(request, trip_id):
    """Shows a specific Object"""
    user = User.objects.logged_in(request.session)
    trip = Trip.objects.get(id=trip_id)
    context = {'user': user,
                'trip': trip,
               }
    return render(request, 'trips/trip_details.html', context)

@user_login_required
def join(request, trip_id):
    """Shows a specific Object"""
    user = User.objects.logged_in(request.session)
    Trip.objects.add_traveler(trip_id, user)
    return redirect('trips:index')

# def edit(request, trip_id):
#     """Shows a specific Object for editing"""
#     return HttpResponse(logging.debug('%s.%s - %s' % (request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


# def update(request, trip_id):
#     """Updates a specific Object"""
#     return HttpResponse(logging.debug('%s.%s - %s' % (request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


# def destroy(request, trip_id):
#     """Deletes a specific Object"""
#     return HttpResponse(logging.debug('%s.%s - %s' % (request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))
