# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User
from ..users.error import Error
import validate

# Create your models here.


class TripManager(models.Manager):
    def get_user_trips(self, user):
        return user.trips.all()|self.filter(travelers=user)

    def get_available_trips(self, user):
        return self.exclude(owner=user).exclude(travelers=user)

    def add_traveler(self, trip_id, user):
        trip = self.get(pk=trip_id)
        if trip.owner != user:
            trip.travelers.add(user)
            return True, self
        else: 
            errors = []
            errors.append(Error('add travelers', 'You can not be a traveler on your own trip'))
            return False, errors
        

    def add_trip(self, owner, data):
        # TODO: Add Valiation
        valid, errors = validate.trip_form(data)
        if valid:
            new_trip = self.create(owner=owner,
                        destination=data['destination'],
                        start_date=data['start_date'],
                        end_date=data['end_date'],
                        description=data['description'],)
            return (valid, new_trip)
        else:
            return (valid, errors)
      

class Trip(models.Model):
    objects = TripManager()

    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trips')
    travelers = models.ManyToManyField(User, related_name='joined_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s %s %s' % (self.id, self.destination, self.start_date, self.end_date)

    def __unicode__(self):
        return '%s: %s %s %s' % (self.id, self.destination, self.start_date, self.end_date)
