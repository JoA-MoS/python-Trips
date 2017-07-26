# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, Http404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from .models import User
from .decorators import user_login_required, anonymous_only
import base64
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create your views here.


@user_login_required
def index(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    user = User.objects.get_user(request.session['user_id'])
    context = {'user': user,
               'users': User.objects.all()}
    return render(request, 'users/list.html', context)


@user_login_required
def show_users_list(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    user = User.objects.get_user(request.session['user_id'])
    context = {'user': user,
               'users': User.objects.all()}
    return render(request, 'users/list.html', context)

# add user not logged in

@anonymous_only
def show_register(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    return render(request, 'users/register.html')

@anonymous_only
@require_http_methods(['POST'])
def create(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    valid, data = User.objects.add_user(request.POST, request.session)
    if valid:
        return redirect(settings.HOME_URL)
    else:
        for i in data:
            messages.add_message(request, messages.ERROR, i.message)
    # can we do this better
    return redirect(reverse('users:disp_reg'))


@anonymous_only
def show_register_login(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    return render(request, 'users/combined.html')


@anonymous_only
def show_login(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    context = {}
    if 'next' in request.GET:
        context['next_pg'] = request.GET['next']
    return render(request, 'users/login.html', context)


@anonymous_only
@require_http_methods(['POST'])
def login(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    """Validates user is username and password, sets session variables"""

    valid, data = User.objects.authenticate(request.POST, request.session)
    if valid:
        next_pg = settings.HOME_URL
        if 'next_pg' in request.POST and len(request.POST['next_pg']) > 0:
            enc = request.POST['next_pg']
            next_pg = base64.urlsafe_b64decode(enc.encode('ascii'))
        return redirect(next_pg)
    else:
        for i in data:
            messages.add_message(request, messages.ERROR, i.message)
        # TODO: looses next page if they type the password wrong
        return redirect('users:disp_login')


@user_login_required
def logout(request):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    request.session.flush()
    messages.add_message(request, messages.SUCCESS, 'You have been logged out')
    return redirect('users:disp_login')


@user_login_required
def show(request, user_id):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    user = User.objects.get_user(user_id)
    if user:
        context = {
            'user': user,
        }
        return render(request, 'users/show_user.html', context)
    else:
        raise Http404("No user does not exist.")

@user_login_required
def edit(request, user_id):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    """Shows a specific Object for editing"""
    user = User.objects.get_user(user_id)
    if user:
        context = {
            'user': user,
        }
        return render(request, 'users/edit_user.html', context)
    else:
        raise Http404("User does not exist.")


@user_login_required
def update(request, user_id):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    """Updates a specific Object"""
    pass


@user_login_required
def destroy(request, user_id):
    logging.debug(' %s. %s -  %s' % (request.resolver_match.namespaces,
                                     request.resolver_match.func.__name__, request.path))
    """Deletes a specific Object"""
    pass
